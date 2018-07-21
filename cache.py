"""Definitions related to caching the song."""

import youtube_dl
import os
import threading
import glob
from fuzzywuzzy import fuzz, process
import sys
from stringutils import (
    remove_multiple_spaces, remove_punct, compute_jaccard
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

    def _search_fuzzy(self, song_name):
        song_name = remove_multiple_spaces(song_name)
        """Fuzzy search the song in the cache."""
        cached_songs = self.list_mp3()
        # matches = process.extract(song_name, cached_songs, limit=5)
        matches = []
        for song in cached_songs:
            name = os.path.splitext(song)[0]
            name = remove_multiple_spaces(name)
            dist = fuzz.token_sort_ratio(song_name, name)
            matches.append((song, dist))
        matches = sorted(matches, key = lambda x : x[1], reverse=True)
        if matches:
            song = matches[0][0]
            return self.get_full_location(song)
        else:
            return []

    def search(self, song_name):
        return self._search_tokens(song_name)

    def _search_tokens(self, song_name):
        """Search song in the cache based on each word matching"""
        print("Searching in the cache at :: {}".format(self.dir))
        song_name = remove_multiple_spaces(song_name).lower()
        tokens1 = song_name.split()
        cached_songs = self.list_mp3()

        res = []
        for song in cached_songs:
            name = os.path.splitext(song)[0].lower()
            name = remove_punct(name)
            name = remove_multiple_spaces(name)
            tokens2 = name.split()
            dist = compute_jaccard(tokens1, tokens2)
            res.append((song_name, song, dist))
        res = sorted(res, key = lambda x : x[2], reverse = True)
        if res and res[0][2]>0:
            return self.get_full_location(res[0][1])
        else:
            return None

    @staticmethod
    def dw(link):
        """Download the song."""
        dw = Cache()
        print("Downloading from {}".format(link))
        dw_thread = threading.Thread(target=dw.GRAB_SONG, args=(link,))
        dw_thread.start()

    def GRAB_SONG(self, link):
        """Return true if the song is downloaded else false."""
        ydl_opts = {
            'format': 'bestaudio',
            'quiet': True,
            'outtmpl': os.path.join(self.dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec':  'mp3',
                'preferredquality': '320'
            }]
        }

        # Download the song with youtube-dl
        try:
            ydl = youtube_dl.YoutubeDL(ydl_opts)
            ydl.download([link])
            return True
        except TimeoutError:
            print('Timed Out! Are you connected to internet?\a')
            return False
        else:
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
