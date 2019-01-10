from requests import get
from bs4 import BeautifulSoup
import re

from playx.playlist.playlistbase import (
    PlaylistBase, SongMetadataBase
)

from playx.logger import (
    Logger
)

# Setup logger
logger = Logger("Spotify")


class SpotifySong(SongMetadataBase):
    """Spotify songs container."""

    def __init__(self, title='', artist='', album=''):
        super().__init__()
        self.title = title
        self.artist = artist
        self.album = album
        self._create_search_querry()
        self._remove_duplicates()

    def _create_search_querry(self):
        """
        Create a search querry.
        """
        self.search_querry = self.title + ' ' + self.artist


class SpotifyIE(PlaylistBase):
    """Spotify playlist data extractor."""

    def __init__(self, URL, is_shuffle, pl_start=None, pl_end=None):
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.list_content_tuple = []
        self.playlist_name = ''
        self.is_shuffle = is_shuffle

    def get_data(self):
        r = get(self.URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        s = soup.findAll(attrs={'class': 'track-name-wrapper'})
        name = soup.findAll(attrs={'class': 'media-bd'})
        name = re.sub(
                    r'<span.*?>|</span>',
                    '',
                    re.findall(
                            r'<span dir="auto">.*?</span>',
                            str(name))[0]
                    )
        self.playlist_name = name

        for i in s:
            title = re.sub(r'class="track-name".*?>|</span>',
                            '',
                            re.findall(r'class="track-name".*?</span>', str(i))[0])
            artist = re.sub(r'a href="/artist.*?<span dir=".*?>|</span>|</a>',
                            '',
                            re.findall(r'a href="/artist.*?</a>', str(i))[0])
            album = re.sub(r'a href="/album.*?<span dir=".*?>|</span>|</a>',
                            '',
                            re.findall(r'a href="/album.*?</a>', str(i))[0])
            self.list_content_tuple.append(SpotifySong(title, artist, album))

        self.strip_to_start_end()

        if self.is_shuffle:
            self.shufflelist()


def get_data(URL, pl_start, pl_end, shuffle):
    """Generic function. Should be called only when
    it is checked if the URL is a spotify playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """
    logger.info("Extracting Playlist Contents")
    spotify_playlist = SpotifyIE(URL, shuffle, pl_start, pl_end)
    spotify_playlist.get_data()
    return spotify_playlist.list_content_tuple, spotify_playlist.playlist_name
