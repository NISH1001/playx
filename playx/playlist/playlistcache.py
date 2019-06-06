"""Functions to handle the caching of playlists."""

from pathlib import Path
from os import makedirs

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
    |[Song]:[Song name, URL of song, querry]|
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
        files = [file for file in self.dir_path.iterdir()]

        for file in files:
            name, url = self._get_data(file)
            logger.debug("{}:{}".format(name, url))
            logger.debug(self.entity)
            if (self.entity == name) or (self.entity == url):
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

        for song in data:
            song_details = '[SONG]:[{},{},{}]'.format(
                                                    song.title,
                                                    song.URL,
                                                    song.search_querry
                                                )
            WSTREAM.write(song_details + '\n')

        WSTREAM.close()


class CachedSongs(SongMetadataBase):
    """
    Class to contain songs extracted from the cached
    playlist.
    """
    def __init__(self, title, URL, querry):
        super().__init__()
        self.title = title
        self.URL = URL
        self.search_querry = querry


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
        logger.debug(self.playlist_name)

        for line in FILECONTENTS[2:-1]:
            logger.debug(line)
            song_details = line[line.index(':')+2:-1].split(',')
            logger.debug(str(song_details))
            logger.hold()
            logger.debug("{}:{}:{}".format(song_details[0], song_details[1], song_details[2]))
            self.list_content_tuple.append(CachedSongs(
                                                        song_details[0],
                                                        song_details[1],
                                                        song_details[2],
                                                    ))
        self.strip_to_start_end()


def save_data(PlaylistName, URL, pltype, data):
    """
    Cache the playlist data to a local file.
    """
    playlist_cache = PlaylistCache(None)
    playlist_cache.cache(PlaylistName, URL, pltype, data)


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a cached playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """
    logger.info("Extracting Playlist Contents")
    cached_playlist = CachedIE(URL, pl_start, pl_end)
    cached_playlist.get_data()

    return cached_playlist.list_content_tuple, cached_playlist.playlist_name
