"""Functions to handle the caching of playlists."""

from pathlib import Path
from os import makedirs
import os
import json
import glob

from playx.playlist.playlistbase import (
    PlaylistBase, SongMetadataBase
)

from playx.logger import Logger

# Get the logger
logger = Logger('PlaylistCache')


class PlaylistCache:
    """
    All functions related to playlist caching are
    defined here.

    The structure of the cached playlist is following
    -----------------------------------------
    |[Name]:[<name of the playlist>]        |
    |[URL]:[<URL of the playlist>]          |
    |[Type]:[<PlaylistType>]                |
    |[Song]:[Song name, URL of song, query]|
    |........                               |
    |........                               |
    -----------------------------------------

    The playlist is saved by <NameOfPlaylist-Type>.playlist
    """

    def __init__(self, entity):
        self.entity = entity  # Entity can be either a name or an URL
        self.dir_path = Path('~/.playx/playlist').expanduser()
        self.file_path = None
        self._check_dir()

    def _check_dir(self):
        """
        Check if the dir_path is available or not.
        If not, create the dir.
        """
        if not self.dir_path.exists():
            makedirs(self.dir_path, exist_ok=True)

    def extract_playlist_type(self):
        """
        Extract the type of the playlist.
        """
        READSTREAM = open(self.file_path)
        FILE_CONTENTS = READSTREAM.read().split('\n')
        TYPE = FILE_CONTENTS[2][FILE_CONTENTS[2].index(':')+2:-1]
        return TYPE

    def _get_data(self, path_to_file):
        """
        Extract the name and URL from the passed file.
        """
        READSTREAM = open(self.dir_path.joinpath(path_to_file), 'r')
        FILE_CONTENTS = READSTREAM.read().split('\n')
        NAME = FILE_CONTENTS[0][FILE_CONTENTS[0].index(':')+2:-1]
        URL = FILE_CONTENTS[1][FILE_CONTENTS[1].index(':')+2:-1]
        return (NAME, URL)

    def is_cached(self):
        """
        Check if the passed playlist name or URL
        is saved in the playlist dir.
        """
        files = [file for file in self.dir_path.glob("*.playlist")]

        for file in files:
            name, url = self._get_data(file)
            if (self.entity.lower() == name.lower()) or (self.entity == url):
                self.file_path = self.dir_path.joinpath(file)
                return True

        return False

    def cache(self, name, url, pltype, data):
        """
        Save the data locally.
        """
        file_name = name + '-' + pltype + '.playlist'
        WSTREAM = open(self.dir_path.joinpath(file_name), 'w')
        WSTREAM.write('[Name]:[{}]\n'.format(name))
        WSTREAM.write('[URL]:[{}]\n'.format(url))
        WSTREAM.write('[TYPE]:[{}]\n'.format(pltype))

        for song in data:
            song_details = '[SONG]:[{},{},{}]'.format(
                                                    song.title,
                                                    song.URL,
                                                    song.search_query
                                                )
            WSTREAM.write(song_details + '\n')

        WSTREAM.close()


class PlaylistCache2:
    """
        This is a new and improved (structured) version for the playlist cache.
        Each playlistcache corresponds to a json file for a playlist which is
        structured as:

        some-playlist.json
        ```json
            {
                "name": <playlist name> (string)
                "type": <playlist type> (string)
                "url": <playlist url> (string)
                "data": <list of the song metadata> (list)
            }
        ```

        Each song metadata is actually another dict/json
        The "data" part is a list of song metadata which is structured as:
            [
                { "title": <title>, "url": <url>, "search_query": <search_query> }
                { "title": <title>, "url": <url>, "search_query": <search_query> }
                ...
            ]
    """
    def __init__(self, entity):
        self.entity = entity  # Entity can be either a name or an URL
        self.dir_path = Path('~/.playx/playlist').expanduser()
        self.file_path = None
        self._check_dir()

    def _check_dir(self):
        """
        Check if the dir_path is available or not.
        If not, create the dir.
        """
        if not self.dir_path.exists():
            makedirs(self.dir_path, exist_ok=True)

    def cache(self, name, url, pltype, data):
        """
            Save the data locally.
        """
        res = {
            'name': name,
            'type': pltype,
            'url': url,
            'data': []
        }
        for song in data:
            s = {
                'title': song.title,
                'url': song.URL,
                'search_query': song.search_query
            }
            res['data'].append(s)
        file_name = name + '-' + pltype + '.json'
        with open(self.dir_path.joinpath(file_name), 'w') as f:
            json.dump(res, f, indent=4)

    def extract_playlist_type(self):
        """
        Extract the type of the playlist.
        """
        with open(self.file_path) as f:
            playlist = json.load(f)
            return playlist['type']

    def _get_data(self, path_to_file):
        """
        Extract the name and URL from the passed file.
        """
        with open(self.dir_path.joinpath(path_to_file), 'r') as f:
            playlist = json.load(f)
            return (playlist['name'], playlist['url'])

    def is_cached(self):
        """
        Check if the passed playlist name or URL
        is saved in the playlist dir.
        """
        for fname in self.dir_path.glob("*.json"):
            name, url = self._get_data(fname)
            if (self.entity.lower() == name.lower()) or (self.entity == url):
                self.file_path = self.dir_path.joinpath(fname)
                return True
        return False


class CachedSong(SongMetadataBase):
    """
    Class to contain songs extracted from the cached
    playlist.
    """
    def __init__(self, title, URL, query):
        super().__init__(title, URL, query)

class CachedIE(PlaylistBase):
    """
    Class to extract data in cached playlists.
    """
    def __init__(self, URL, pl_start=None, pl_end=None):
        super().__init__(pl_start, pl_end)
        self.URL = URL  # Here the URL is actually a local dir path
        self.playlist_name = ''

    def get_data(self):
        """
        Extract the data from the cached playlist.
        """
        READSTREAM = open(self.URL, 'r')
        FILECONTENTS = READSTREAM.read().split('\n')

        self.playlist_name = FILECONTENTS[0][FILECONTENTS[0].index(':')+2: -1]
        self.actual_URL = FILECONTENTS[1][FILECONTENTS[1].index(':')+2: -1]
        self.type = FILECONTENTS[2][FILECONTENTS[2].index(':')+2: -1]

        for line in FILECONTENTS[3:-1]:
            logger.debug(line)
            logger.hold()
            song_details = line[line.index(':')+2:-1].split(',')
            logger.debug(str(song_details))
            logger.debug("{}:{}:{}".format(song_details[0], song_details[1], song_details[2]))
            self.list_content_tuple.append(CachedSong(
                                                        song_details[0],
                                                        song_details[1],
                                                        song_details[2],
                                                    ))
        self.strip_to_start_end()

class CachedIE2(PlaylistBase):
    """
    Class to extract data in cached playlists.
    """
    def __init__(self, URL, pl_start=None, pl_end=None):
        super().__init__(pl_start, pl_end)
        self.URL = URL  # Here the URL is actually a local dir path
        self.playlist_name = ''

    def get_data(self):
        """
        Extract the data from the cached playlist.
        """
        playlist = {}
        with open(self.URL, 'r') as f:
            playlist = json.load(f)
        if not playlist:
            return []
        self.playlist_name = playlist['name']
        for song in playlist['data']:
            self.list_content_tuple.append(CachedSong(
                song['title'],
                song['url'],
                song['search_query']
            ))
        self.strip_to_start_end()


def save_data(PlaylistName, URL, pltype, data):
    """
    Cache the playlist data to a local file.
    """
    playlist_cache = PlaylistCache2(None)
    playlist_cache.cache(PlaylistName, URL, pltype, data)

def list_all():
    """
    Return all the playlist names with playlist URL's
    """
    dir_path = Path('~/.playx/playlist').expanduser()
    files = glob.glob(os.path.join(dir_path, '*.json'))
    # files = [file for file in dir_path.iterdir()]
    list_playlist = []

    for fname in files:
        with open(fname) as f:
            pl = json.load(f)
            name = pl['name']
            url = pl['url']
            pl_type = pl['type']
            list_playlist.append((name, url, pl_type))
    return list_playlist


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a cached playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """
    logger.debug("Extracting Playlist Contents")
    cached_playlist = CachedIE2(URL, pl_start, pl_end)
    cached_playlist.get_data()
    return cached_playlist.list_content_tuple, cached_playlist.playlist_name


def migrate2(src):
    """Migrate to the new playlist structure."""
    # Open the src file using the older extractor class
    # Open the des using the new extractor
    old_playlist = CachedIE(src)
    old_playlist.get_data()
    new_one = PlaylistCache2(None)
    new_one.cache(
                    old_playlist.playlist_name,
                    old_playlist.actual_URL,
                    old_playlist.type,
                    old_playlist.list_content_tuple
                )


if __name__ == "__main__":
    old_file = "/home/deepjyoti30/.playx/playlist/Secret Stash-spotify.playlist"
    migrate2(old_file)
