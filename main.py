#!/usr/bin/env python3

"""Main function for playx."""

from songfinder import search
from utility import direct_to_play
from youtube import grab_link
import argparse
from cache import search_locally


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', '-n',
                        help="Name of the song to download.\
                         Words separated by space",
                        default=None, nargs='+', type=str)
    parser.add_argument('--url', '-u',
                        help="Youtube song link.")
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
    is_local = False
    local_res = search_locally(value)
    if local_res:
        value = local_res
        is_local = True
    else:
        result = search(value)
        value = grab_link(result.url)

    direct_to_play(value, 'local' if is_local else None)


def main():
    """Search the song in youtube and stream through mpd."""
    args = parse()

    if args.url is not None:
        stream('url', args.url)
    else:
        stream('name', ' '.join(args.name))


if __name__ == "__main__":
    main()
