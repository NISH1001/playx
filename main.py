#!/usr/bin/env python3

from songfinder import search_song
from utility import run_mpd
from youtube import get_youtube_streams
import playlist
import argparse


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('SONG_NAME', help="Name of the song to download.",
                        default=None, nargs='?', type=str)
    parser.add_argument('--url',
                        help="Youtube song link.")
    parser.add_argument('-p', '--playlist',
                        help="Path to playlist")
    args = parser.parse_args()
    return args


def stream(type, value=None):
    """Start streaming the song."""
    if type == 'name':
        song = value
        result = search_song(song)
        print("Song found in youtube...")
        result.display()
        stream = get_youtube_streams(result.url)
    elif type == 'url':
        stream = get_youtube_streams(value)

    run_mpd(stream['audio'])


def main():
    """Search the song in youtube and stream through mpd."""
    args = parse()

    if args.url is not None:
        stream('url', args.url)
    elif args.playlist is not None:
        playlist.read_playlist(args.playlist)
    else:
        stream('name', args.SONG_NAME)


if __name__ == "__main__":
    main()
