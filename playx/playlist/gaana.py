"""
Functions related to gaana playlist.
"""

import requests
import re

from playx.playlist.playlistbase import (
    PlaylistBase, SongMetadataBase
)

from playx.logger import (
    Logger
)

# Setup logger
logger = Logger("Gaana")


class SongMetadata(SongMetadataBase):
    """
    title: Title of the song
    track_seokey: Seokey of the track
    album_seokey: Seokey of the album
    artist_seokey: Seokey of the artist(s).
    In case more than one artist then they will be added
    seperated by a ' ' to the artist_seokey
    """

    def __init__(
                self,
                artist_tuple=[],
                title='',
                track_seokey='',
                album_seokey='',
                ):
        super().__init__()
        self.title = title
        self.album_seokey = album_seokey
        self.track_seokey = track_seokey
        self.artist_seokey = ''
        self.artist_tuple = artist_tuple
        self._update_artist()
        self._create_search_querry()
        self._remove_duplicates()
        self._remove_stopletters()

    def _remove_stopletters(self):
        """
        Remove letters like - and numbers from the searchquery
        """
        self.search_querry = re.sub(r'-|[0-9]|&amp', ' ', self.search_querry)

    def _update_artist(self):
        """
        In case the passed artist argument is a list
        then split it into a string.
        """
        for artist in self.artist_tuple:
            self.artist_seokey += ' ' + artist['seokey']

    def _create_search_querry(self):
        """
        Update the search querry of the base class.
        """
        self.search_querry = self.track_seokey + ' ' + self.album_seokey + '' + self.artist_seokey
        self._remove_stopletters()


class GaanaIE(PlaylistBase):

    def __init__(self, URL, pl_start, pl_end):
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.API_URL = 'http://api.gaana.com/?type=playlist&subtype=playlist_detail&seokey={}&format=JSON'
        self.playlist_seokey = ''
        self.list_content_tuple = []
        self.playlist_name = ''
        self._extract_playlist_seokey()

    def _extract_playlist_seokey(self):
        """
        The playlist seokey is the basename present in the URL.
        """
        self.playlist_seokey = self.URL.split('/')[-1]

    def extract_data(self):
        """
        Extract playlist data by using the API.
        """
        r = requests.get(self.API_URL.format(self.playlist_seokey)).json()
        tracks = r['tracks']
        logger.debug(type(tracks))
        # For the time being keep playlist seokey as playlist name
        self.playlist_name = self.playlist_seokey

        for track in tracks:
            track_title = track['track_title']
            track_seokey = track['seokey']
            album_seokey = track['albumseokey']
            artist = track['artist']
            self.list_content_tuple.append(SongMetadata(
                                                        artist,
                                                        track_title,
                                                        track_seokey,
                                                        album_seokey
                                                       ))

        self.strip_to_start_end()


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a youtube playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """

    logger.info("Extracting Playlist Content")
    gaana_IE = GaanaIE(URL, pl_start, pl_end)
    gaana_IE.extract_data()

    return gaana_IE.list_content_tuple, gaana_IE.playlist_name
