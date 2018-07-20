#!/usr/bin/env python3
"""It is a module that wraps cache and youtube."""

from youtube import search_youtube


def search(song):
    """Search the song in youtube."""
    videos = search_youtube(song)
    video = videos[0]
    return video
