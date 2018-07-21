#!/usr/bin/env python3
"""It is an abstract module for searching songs"""

from youtube import search_youtube


def search(song):
    """Search the song in youtube."""
    videos = search_youtube(song)
    video = videos[0]
    return video
