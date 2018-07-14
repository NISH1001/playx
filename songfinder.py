#!/usr/bin/env python3
"""It is a module that wraps cache and youtube."""

from youtube import search_youtube


def search_song(song):
    """Search the song locally at first.

    If not found, search in youtube
    """
    videos = search_youtube(song)
    video = videos[0]
    return video
