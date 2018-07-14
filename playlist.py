#!/usr/bin/env python3

"""Definitions to interact with playlists."""

from main import stream
from utility import is_on
from time import sleep


def check_type(line):
    """Check if the line has a url or song name."""
    if 'http' in line:
        return 'url'
    else:
        return 'name'


def read_playlist(file):
    """Read the playlist and play songs accordingly."""
    song_stream = open(file, 'r')
    while True:
        # Remove \n if present
        song = song_stream.readline()
        if not song:
            break
        song = song.replace('\n', '')
        type = check_type(song)
        stream(type, song)
        # show_menu()
        while is_on():
            sleep(0.5)
