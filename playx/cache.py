"""Definitions related to caching the song."""

import os
import threading
import glob
import sys
import json
import urllib.request

from json.decoder import JSONDecodeError

from playx.stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard, remove_stopwords,
    check_keywords, fix_title
)
from playx.logger import Logger

# Setup logger
logger = Logger('cache')


class Cache:
    """Class to cache the song to a dir for quick acces."""

    def __init__(self, directory='~/.playx/songs'):
        """
            Init the stuff.
            directory: the directory where songs lie

            Note:
                The reason for choosing `playx/songs` is that I have allocated
                other tree structure for misc activities like `playx/logs` and
                `playx/playxlist`
        """
        self.dir = os.path.expanduser(directory)
        self.create_cache_dir()
        self.partial_log_file = os.path.expanduser('~/.playx/logs/partial_log')

    def create_cache_dir(self):
        """If cache dir is not already present make it."""
        if not os.path.isdir(self.dir):
            # Make the dir
            os.makedirs(self.dir)

    def list_mp3(self):
        """Get the list of all the mp3 files in the cache."""
        os.chdir(self.dir)
        return glob.glob("*.mp3")

    def search_exactly(self, song_name):
        """Search the song in the cache.

        Tries to match the song name exactly.
        """
        song_name = song_name.lower()
        cached_songs = self.list_mp3()
        for song in cached_songs:
            if song.lower() == song_name:
                return song
        return None

    def get_full_location(self, song_name):
        """Get the full location of the song."""
        return os.path.join(self.dir, song_name)

    def search(self, song_name):
        """Return results of search_tokens."""
        ret = self.search_single(song_name)
        if ret is None:
            return ret

        if self.in_partial_dw(ret[1]):
            logger.debug("Found in partial downloads.")
            return []
        else:
            return ret

    def search_terms(self, *terms):
        logger.debug("Searching terms [{}] in the cache at [{}]".format(terms, self.dir))
        if type(terms) in [list, tuple, set]:
            song_name = " ".join(*terms)
        if type(terms) is str:
            song_name = terms
        return self._search_tokens(song_name)

    def _search_tokens(self, song_name):
        """Search song in the cache based on simple each word matching."""
        logger.debug("Searching [{}] in the cache at [{}]".format(song_name, self.dir))
        song_name = remove_stopwords(remove_multiple_spaces(song_name).lower())
        song_name = remove_punct(song_name)
        tokens1 = song_name.split()
        cached_songs = self.list_mp3()

        res = []
        for song in cached_songs:
            name = os.path.splitext(song)[0].lower()
            title = name
            name = remove_stopwords(name)
            name = remove_punct(name)
            name = remove_multiple_spaces(name)
            tokens2 = name.split()
            match = check_keywords(tokens1, tokens2)
            if match:
                dist = compute_jaccard(tokens1, tokens2)
                res.append((song_name, song, title, dist))
        return sorted(res, key=lambda x: x[-1], reverse=True)

    def search_single(self, song_name):
        res = self._search_tokens(song_name)
        if res and res[0][-1] > 0:
            return res[0][2], self.get_full_location(res[0][1])
        else:
            return None

    def in_partial_dw(self, song_name):
        """Check if the file is present in partial dw file."""
        if not os.path.exists(self.partial_log_file):
            return False

        data = open(self.partial_log_file, 'r').read()
        if song_name in data:
            return True

    def log_partial_dw(self, song_name):
        """Log the name of the song that is being downloaded."""
        # Write the song_name and the size to the log_file
        if not os.path.exists(self.partial_log_file):
            open(self.partial_log_file, 'w').close()

        with open(self.partial_log_file, 'a') as WSTREAM:
            WSTREAM.write(song_name + '\n')

    def unlog_partial_dw(self, song_name):
        """Remove the song_name from the file."""
        if not os.path.exists(self.partial_log_file):
            return

        data = open(self.partial_log_file, 'r').read()
        data = data.replace(song_name + '\n', '')
        open(self.partial_log_file, 'w').write(data)

    @staticmethod
    def dw(link, name, URL=None):
        """Download the song."""
        dw = Cache()
        # check if song is already downloaded...
        songs = dw.list_mp3()
        if name in songs and not dw.in_partial_dw(name):
            logger.debug("{} already downloaded.".format(name))
            return
        logger.debug("Downloading {}".format(name))
        dw_thread = threading.Thread(target=dw.dw_song, args=(link, name, URL))
        dw_thread.start()

    def dw_song(self, link, name, URL):
        """Download the song."""
        try:
            path = os.path.join(self.dir, name)
            headers = {}

            # Put a check to see if the file already exists.
            if os.path.exists(path):
                remain_size = os.path.getsize(path)
                headers = {"Range": "bytes={}-".format(remain_size)}
                logger.debug("Resuming download at {} byte".format(remain_size))

            req = urllib.request.Request(url=link, headers=headers)
            u = urllib.request.urlopen(req)
            block_sz = 8192

            f = open(path, 'wb')

            # Log the file in the partial_log_file.
            self.log_partial_dw(path)
            # Start downloading the song
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                f.write(buffer)

            self.unlog_partial_dw(path)
            logger.debug("Download complete.")
            if URL is not None and not search_URL(URL):
                update_URL_cache(name, URL)
            return name
        except Exception:
            return False


def search_locally(song=None):
    """To be used by other files."""
    cache = Cache("~/.playx/songs")
    if song:
        match = cache.search(song)
    else:
        match = []
    return match


def search_URL(URL):
    """
    Check if the URL is cached.
    """
    file_path = os.path.expanduser('~/.playx/logs/urls.json')
    logger.debug(URL)

    # check if file exists
    if not os.path.exists(file_path):
        temp = open(file_path, 'w')
        temp.close()
        data = {}

    try:
        with open(file_path, 'r') as RSTREAM:
            data = json.load(RSTREAM)
            logger.debug("Searching {} in the cached file".format(URL))
    except JSONDecodeError:
        data = {}
    return data.get(URL, None)


def update_URL_cache(title, URL):
    """
    Update the URL cache saved in the mapURL.json file.
    """
    log_dir = os.path.expanduser('~/.playx/logs')
    songs_dir = os.path.expanduser('~/.playx/songs')
    file_path = os.path.join(log_dir, 'urls.json')
    song_path = os.path.join(songs_dir, fix_title(title))

    if not os.path.exists(file_path):
        temp = open(file_path, 'w')
        temp.close()
        data = {}
    else:
        with open(file_path, 'r') as RSTREAM:
            try:
                data = json.load(RSTREAM)
            except JSONDecodeError: data = {}

    data.update({URL: song_path})

    with open(file_path, 'w') as WSTREAM:
        json.dump(data, WSTREAM)

def clean_url_cache():
    """
        Remove URLs for which file paths do not exist.
        (Most probably the file has been manually deleted by the user)
    """
    log_dir = os.path.expanduser('~/.playx/logs')
    file_path = os.path.join(log_dir, 'urls.json')
    logger.debug(f"Cleaning URL Cache at {file_path}")
    if not os.path.exists(file_path):
        return False
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except JSONDecodeError:
            data = {}
    processed = {}
    for url, fname in data.items():
        if not os.path.exists(fname):
            logger.info(f"File [{fname}] does not exist.")
            continue
        processed[url] = fname
    with open(file_path, 'w') as f:
        json.dump(processed, f)
    return True




if __name__ == "__main__":
    name = ' '.join(sys.argv[1:])
    cache = Cache()
    res = search_locally(name)
    print(res)
