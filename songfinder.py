#!/usr/bin/env python3
"""
    It is a module that wraps cache and youtube
"""

from cache import Cache
from youtube import search_youtube

class SongSource:
    CACHE = "local"
    NETWORK = "youtube"
    def __init__(self):
        pass

def search_song(song):
    """
        Search the song locally at first.
        If not found, search in youtube
    """
    cache = Cache("~/.playx/")
    cached_song = cache.search_fuzzy(song)
    if cached_song:
        return SongSource.CACHE, cache.get_full_location(cached_song)
    else:
        videos = search_youtube(song)
        video = videos[0]
        return SongSource.NETWORK, video

def main():
    pass

if __name__ == "__main__":
    main()

