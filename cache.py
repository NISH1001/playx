#!/usr/bin/env python3
"""
    Module for caching songs.
"""

import glob
import os

from youtube import YoutubeMetadata
from stringutils import get_closest_match, get_closest_match_ignorecase

class Cache:
    """
        The main caching component
    """
    def __init__(self, directory="~/.playx/"):
        self.directory = directory
        self.create_cache(directory)

    def create_cache(self, directory):
        """
            Create the cache directory if it doesn't exist
        """
        directory = directory.strip()
        directory = os.path.abspath(os.path.expanduser(directory))

        # Create the directory if doesn't exist.
        if not os.path.exists(directory):
            print("Creating the cache directory : {}".format(directory))
            os.makedirs(directory)
        else:
            print("Old cache found at : {}".format(directory))

        self.directory = directory

    def list_mp3(self):
        """
            Get the list of all the mp3 files in the cache
        """
        os.chdir(self.directory)
        return glob.glob("*.mp3")

    def search_exactly(self, song_name):
        """
            Search the song in the cache.
            Tries to match the song name exactly.
        """
        print("Searching the song : {} in the cache...".format(song_name))
        song_name = song_name.lower()
        cached_songs = self.list_mp3()
        for song in cached_songs:
            if song.lower() == song_name:
                return song
        return None

    def get_full_location(self, song_name):
        return self.directory + "/" + song_name

    def search_fuzzy(self, song_name):
        """
            Fuzzy search the song in the cache
        """
        print("Fuzzy searching the song : '{}' in the cache...".format(song_name))
        cached_songs = self.list_mp3()
        return get_closest_match_ignorecase(cached_songs, song_name)

    def __str__(self):
        string = "Cache directory : {}".format(self.directory)
        return string

def main():
    cache = Cache("~/.playx")
    song_name = "Eagles#-#Hotel#California#with#English#lyrics#&#Persian#translation#by#Ehsan#Najafi.mp3"
    song = "hotel California"
    match = cache.search_fuzzy(song)
    print(match)

if __name__ == "__main__":
    main()

