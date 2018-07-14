#!/usr/bin/env python3

from songfinder import search_song
from utility import run_mpd
from youtube import get_youtube_streams
import argparse

import sys


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('SONG_NAME', help="Name of the song to download.",
                        default=None, nargs='?', type=str)
    parser.add_argument('--url',
                        help="Youtube song link.")

    args = parser.parse_args()
    return args


def main():
    """Search the song in youtube and stream through mpd."""
    args = parse()

    if args.url is not None:
        stream = get_youtube_streams(args.url)
    else:
        song = args.SONG_NAME
        result = search_song(song)
        print("Song found in youtube...")
        result.display()

    # input(stream['audio'])
    run_mpd(stream['audio'])


if __name__ == "__main__":
    main()
