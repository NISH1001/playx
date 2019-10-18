#!/usr/bin/env python3
"""It is an abstract module for searching songs"""

from playx.youtube import search_youtube


def search(song,no_kw_in_search):
    """Search the song in youtube."""
    videos = search_youtube(song,no_kw_in_search)
    try:
        video = videos[0]
    except IndexError:
        return None
    return video
