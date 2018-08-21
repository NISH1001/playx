#!/usr/bin/env python3
"""It is an abstract module for searching songs"""

from .youtube import search_youtube

def search(song):
    """Search the song in youtube."""
    videos = search_youtube(song)
    try:
        video = videos[0]
    except IndexError:
        return None
    return video
