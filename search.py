#!/usr/bin/env python3
"""Use it to search for the song in cached dir."""

import glob
import os

from stringutils import get_closest_match_ignorecase


class Cache:
    """The main caching component."""

    def __init__(self, directory="~/.playx/"):
        """Init the stuff."""
        directory = os.path.expanduser(directory)
        self.directory = directory

    def list_mp3(self):
        """Get the list of all the mp3 files in the cache."""
        os.chdir(self.directory)
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
        return os.path.join(self.directory, song_name)

    def search_fuzzy(self, song_name):
        """Fuzzy search the song in the cache."""
        cached_songs = self.list_mp3()
        song = get_closest_match_ignorecase(cached_songs, song_name)
        if song is not None:
            return self.get_full_location(song)
        else:
            return []


def search_locally(song=None):
    """To be used by other files."""
    cache = Cache("~/.playx")
    if song is not None:
        match = cache.search_fuzzy(song)
    else:
        match = []
    return match


if __name__ == "__main__":
    search_locally()
