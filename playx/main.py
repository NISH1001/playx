#!/usr/bin/env python3

"""
    Main function for playx.
"""

import argparse

from .cache import (
    Cache, search_locally
)

from .utility import (
    direct_to_play, run_mpv_dir, move_songs
)

from .youtube import (
    grab_link
)

from .playlist import (
    YoutubePlaylist, Playxlist,
    BillboardPlaylist, is_playlist
)

from .import billboard


from .songfinder import search
from .stringutils import is_song_url


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="playx - Search and play\
                                     any song that comes to your mind.\n\
                                     If you have any issues, raise an issue in\
                                     the github\
                                     (https://github.com/NISH1001/playx) page")
    parser.add_argument('song',
                        help="Name or youtube link of song to download",
                        default=None, type=str, nargs="*")
    parser.add_argument('-p', '--play-cache',
                        action='store_true',
                        help="Play all songs from the cache.\
                        The cache is located at ~/.playx/songs/ by default")
    parser.add_argument('-n', '--no-cache',
                        action='store_true',
                        help="Don't download the song for later use.")
    parser.add_argument('-d', '--dont-cache-search',
                        action='store_true',
                        help="Don't search the song in the cache.")
    parser.add_argument('-l', '--lyrics',
                        action='store_true',
                        help="Show lyircs of the song.")
    parser.add_argument('--pl-start', help="Start position in case a\
                         playlist is passed. If passed without a playlist\
                         it has no effect.", default=None, type=int)
    parser.add_argument('--pl-end', help="End position in case a \
                        playlist is passed. If passed without a playlist\
                        it has no effect.", default=None, type=int)
    args = parser.parse_args()
    return parser, args


def online_search(value, no_cache):
    """Search the song online."""
    result = search(value)
    if result is None:
        return print("No results found")
    result.display()
    title = result.title
    value = grab_link(result.url, title, no_cache)
    return value, title


def get_value(value, no_cache):
    """Get the value of the song."""
    value = online_search(value, no_cache)
    if value is None:
        print("No audio attached to video")
        exit(-1)
    else:
        return value[0], value[1]


def stream_from_name(value=None, show_lyrics=False, no_cache=False,
                     dont_cache_search=False):
    """Start streaming the song.

    First search in the local cache.
    If no song is found in the cache, search in the youtube.
    """
    # Need to check if searching locally is forbidden
    if not dont_cache_search:
        match = search_locally(value)
        if match:
            value = match[1]
            title = match[0]
        else:
            value, title = get_value(value, no_cache)
    else:
        value, title = get_value(value, no_cache)

    direct_to_play(value, show_lyrics, title)


def stream_from_url(url, show_lyrics=False, no_cache=False,
                    dont_cache_search=False, ytObj=None):
    """Stream the song using the url.

    Before searching the stream, get the title of the song
    If local search is not forbidden, search it locally
    """
    if ytObj is None:
        result = search(url)
        if result is None:
            return print("No results found")
    else:
        result = ytObj
    result.display()
    title = result.title

    # Now search the song locally
    if not dont_cache_search:
        match = search_locally(title)
        if match:
            # Change the value to local path
            value = match[1]
        else:
            value = grab_link(result.url, title, no_cache)
    else:
        value = grab_link(result.url, title, no_cache)

    direct_to_play(value, show_lyrics, title)


def stream_cache_all(cache):
    run_mpv_dir(cache.dir)


def playx(parser, args, song):
    """Search the song in youtube and stream through mpd."""
    if not song and args.play_cache:
        cache = Cache("~/.playx/songs")
        return stream_cache_all(cache)
    if is_song_url(song):
        # In case the song is a url
        stream_from_url(
                        song,
                        args.lyrics,
                        args.no_cache,
                        args.dont_cache_search
                        )
    elif is_playlist(song, 'billboard'):
        print("Billboard chart name passed.")
        # Initiate a billboard object
        billboard_playlist = BillboardPlaylist(
                                        song,
                                        args.pl_start,
                                        args.pl_end
                                        )
        billboard_playlist.extract_list_contents()
        print("{}: {} {}".format(
                                billboard_playlist.playlist_name,
                                len(billboard_playlist.list_content_tuple),
                                'song' if len(billboard_playlist.list_content_tuple) < 2 else 'songs'
                                )
              )
        for i in billboard_playlist.list_content_tuple:
            stream_from_name(
                            i.title,
                            args.lyrics,
                            args.no_cache,
                            args.dont_cache_search
                            )
    elif is_playlist(song, 'youtube'):
        print("Youtube playlist passed.")
        youtube_playlist = YoutubePlaylist(song, args.pl_start, args.pl_end)
        name, data = youtube_playlist.extract_playlistdata()
        print("{}: {} {}".format(name, len(data),
                                'song' if len(data) < 2 else 'songs'))
        # Play all the songs from the data one by one
        for i in data:
            stream_from_url(song, args.lyrics, args.no_cache,
                            args.dont_cache_search, i)
    elif not song:
        parser.print_help()
    else:
        stream_from_name(song, args.lyrics, args.no_cache,
                         args.dont_cache_search)


def main():
    # Before doing anything, make sure all songs are in the new song dir
    move_songs()
    parser, args = parse()
    song = ' '.join(args.song)
    # Put a check to see if the passed arg is a list
    playx_list = Playxlist(song, args.pl_start, args.pl_end)
    if not playx_list.is_playx_list():
        playx(parser, args, song)
    else:
        for i in playx_list.get_list_contents():
            playx(parser, args, i)


if __name__ == "__main__":
    main()
