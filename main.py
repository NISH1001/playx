#!/usr/bin/env python3

from songfinder import search_song
from utility import run_mpd
from youtube import get_youtube_streams
import vlc

import sys


def main():
    """Search the song in youtube and stream through mpd."""
    args = sys.argv[1:]
    if len(args) > 0:
        song = ' '.join(args)
        result = search_song(song)
        print("Song found in youtube...")
        result.display()
        stream = get_youtube_streams(result.url)
        # input(stream['audio'])
        run_mpd(stream['audio'])
    else:
        print("Lol! That is a retarded command just like me...")


if __name__ == "__main__":
    main()
