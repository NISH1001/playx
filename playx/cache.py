"""Definitions related to caching the song."""

import os
import threading
import glob
import sys
import requests
from shutil import copyfileobj
from .stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard, remove_stopwords,
    check_keywords
)


class Cache:
    """Class to cache the song to a dir for quick acces."""

    def __init__(self, directory='~/.playx'):
        """Init the stuff."""
        self.dir = os.path.expanduser(directory)
        self.create_cache_dir()

    def create_cache_dir(self):
        """If cache dir is not already present make it."""
        if not os.path.isdir(self.dir):
            # Make the dir
            os.mkdir(self.dir)

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
        return self._search_tokens(song_name)

    def _search_tokens(self, song_name):
        """Search song in the cache based on simple each word matching."""
        print("Searching in the cache at :: {}".format(self.dir))
        song_name = remove_stopwords(remove_multiple_spaces(song_name).lower())
        tokens1 = song_name.split()
        cached_songs = self.list_mp3()

        res = []
        for song in cached_songs:
            name = os.path.splitext(song)[0].lower()
            title = name
            name = remove_punct(name)
            name = remove_multiple_spaces(name)
            tokens2 = name.split()
            match = check_keywords(tokens1, tokens2)
            if match:
                dist = compute_jaccard(tokens1, tokens2)
                res.append((song_name, song, title, dist))
        res = sorted(res, key=lambda x: x[-1], reverse=True)
        if res and res[0][-1] > 0:
            return res[0][2], self.get_full_location(res[0][1])
        else:
            return None

    @staticmethod
    def dw(link, name):
        """Download the song."""
        dw = Cache()
        # check if song is already downloaded...
        songs = dw.list_mp3()
        if name in songs:
            return
        print("Downloading {}".format(name))
        dw_thread = threading.Thread(target=dw.dw_song, args=(link, name))
        dw_thread.start()

    def dw_song(self, link, name):
        """Download the song."""
        try:
            path = os.path.join(self.dir, name)
            # Start downloading the song
            response = requests.get(link, stream=True)
            with open(path, 'wb') as out_file:
                copyfileobj(response.raw, out_file)

            del response

            return name
        except Exception:
            return False


def search_locally(song=None):
    """To be used by other files."""
    cache = Cache("~/.playx")
    if song:
        match = cache.search(song)
    else:
        match = []
    return match


if __name__ == "__main__":
    name = ' '.join(sys.argv[1:])
    cache = Cache()
    res = search_locally(name)
    print(res)
