#!/usr/bin/env python3

"""Main function for playx."""

from songfinder import search
from utility import direct_to_play, run_mpv_dir
from youtube import grab_link
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
    args = parser.parse_args()
    return args

def stream(search_type, value=None):
    """
        Start streaming the song.
        First search in the local cache.
        If no song is found in the cache, search in the youtube.

        Fow now, the search in the cache happens based on individual words.
        This will be later improved
    """
    # if query by name -> search locally
    if search_type == 'name':
        local_res = search_locally(value)
        if local_res:
            value = local_res
        else:
            result = search(value)
            value = grab_link(result.url)
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
        stream('url',args.url)
    elif args.name:
        stream('name', ' '.join(args.name))
    elif args.play_cache:
        cache = Cache("~/.playx/")
        stream_cache_all(cache)


if __name__ == "__main__":
    main()
