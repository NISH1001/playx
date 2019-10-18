#!/usr/bin/env python3
"""It is an abstract module for searching songs"""

from playx.youtube import search_youtube
from difflib import SequenceMatcher


def search(song):
    """Search the song in youtube."""
    videos = search_youtube(song)
    try:
        video = videos[0]
    except IndexError:
        return None
    return video


def search_with_exclude(song, exclude_songs, no_kw_in_search):
    """Search the song in youtube but removes result pass in exclude"""
    print("no_kw_in_search {}".format(no_kw_in_search))
    videos = search_youtube(song, no_kw_in_search)
    # print("Excluding {} and choosing one from {} option".format(exclude_songs, len(videos)))
    try:
        video = videos[0]
        for i in range(len(videos)):
            video = videos[i]
            # if video.title == exclude_songs:
            #     break
            similar_ratio = SequenceMatcher(None, video.title, exclude_songs[0]).ratio()
            # print("Matching {} <----> {} Result: {}".format(video.title, exclude_songs[0], similar_ratio))
            if similar_ratio < 0.5:
                break

    except IndexError:
        return None

    return video
