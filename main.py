#!/usr/bin/env python3

"""Main function for playx."""

from songfinder import search
from utility import direct_to_play, run_mpv_dir
from youtube import grab_link
from lyrics import search_lyricswikia
import argparse
from cache import (
    Cache, search_locally
)


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', '-n',
                        help="Name of the song to download.\
                         Words separated by space",
                        default=None, nargs='+', type=str)
    parser.add_argument('--url', '-u',
                        help="Youtube song link.")
    parser.add_argument('--play-cache',
                        action='store_true',
                        help="Play all songs from the cache.")
    parser.add_argument('--lyrics', '-l',
                        action='store_true',
                        help="Show lyircs of the song.")
    args = parser.parse_args()
    return args

def stream(search_type, value=None, show_lyrics=False):
    """
        Start streaming the song.
        First search in the local cache.
        If no song is found in the cache, search in the youtube.

        Fow now, the search in the cache happens based on individual words.
        This will be later improved
    """
    # if query by name -> search locally
    if search_type == 'name':
        match = search_locally(value)
        if match:
            value = match[1]
            title = match[0]
        else:
            result = search(value)
            result.display()
            title = result.title
            value = grab_link(result.url, title)

        if show_lyrics:
            lyric = search_lyricswikia(title)
            print("----\n{}\n----".format(lyric))
    else:
        # if url just grab the stream url (no caching is done)
        value = grab_link(value)

    direct_to_play(value)


def stream_cache_all(cache):
    run_mpv_dir(cache.dir)


def main():
    """Search the song in youtube and stream through mpd."""
    args = parse()

    if args.url is not None:
        stream('url', args.url, args.lyrics)
    elif args.name:
        stream('name', ' '.join(args.name), args.lyrics)
    elif args.play_cache:
        cache = Cache("~/.playx/")
        stream_cache_all(cache)


if __name__ == "__main__":
    main()
