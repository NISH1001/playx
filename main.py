#!/usr/bin/env python3

"""Main function for playx."""

from songfinder import search
from utility import run_mpd
from youtube import grab_link
import playlist
import argparse
from search import search_locally


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', '-n',
                        help="Name of the song to download.\
                         Words separated by space",
                        default=None, nargs='+', type=str)
    parser.add_argument('--url', '-u',
                        help="Youtube song link.")
    parser.add_argument('--playlist', '-p',
                        help="Path to playlist")
    args = parser.parse_args()
    return args


def stream(search_type, value=None):
    """Start streaming the song."""
    is_local = False
    # No matter if a link or name we need to search
    result = search(value)

    if search_type == 'url':
        value = result.title

    local_res = search_locally(value)

    if len(local_res) != 0:
        value = local_res
        is_local = True
    else:
        value = grab_link(result.url)

    if not is_local:
        result.display()

    run_mpd(value, 'local' if is_local else None)


def main():
    """Search the song in youtube and stream through mpd."""
    args = parse()

    if args.url is not None:
        stream('url', args.url)
    elif args.playlist is not None:
        playlist.read_playlist(args.playlist)
    else:
        stream('name', ' '.join(args.name))


if __name__ == "__main__":
    main()
