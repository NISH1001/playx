from requests import get
from bs4 import BeautifulSoup
import re

from playx.playlist.playlistbase import (
    PlaylistBase
)

# url = "https://open.spotify.com/playlist/3YSjAfvq8CVG2mqrzJcv31?si=U72PoitqQiyRmAJ1HZzDeA"
url = "https://open.spotify.com/playlist/37i9dQZF1DX5Ozry5U6G0d"


class SpotifySong:
    """Spotify songs container."""

    def __init__(self, title='', artist='', album=''):
        self.title = title
        self.artist = artist
        self.album = album


class SpotifyIE():
    """Spotify playlist data extractor."""

    def __init__(self, URL):
        self.URL = URL
        self.playlist_content = []
        self.playlist_name = ''

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
            self.playlist_content.append(SpotifySong(title, artist, album))

        return self.playlist_content


class SpotifyPlaylist(PlaylistBase):
    """Container that uses the SpotifyIE to properly align
    all the data and return a proper tuple.
    """

    def __init__(self, URL, pl_start=None, pl_end=None):
        super().__init__(pl_start, pl_end)
        self.URL = URL
        self.list_content_tuple = []
        self.playlist_name = ''

    def extract_data(self):
        """Extract the playlist data."""
        spotify = SpotifyIE(self.URL)
        self.list_content_tuple = spotify.get_data()
        self.playlist_name = spotify.playlist_name
        self.strip_to_start_end()


def get_data(URL, pl_start, pl_end):
    """Generic function. Should be called only when
    it is checked if the URL is a spotify playlist.

    Returns a tuple containing the songs and name of
    the playlist.
    """
    spotify_playlist = SpotifyPlaylist(URL, pl_start, pl_end)
    spotify_playlist.extract_data()
    return spotify_playlist.list_content_tuple, spotify_playlist.playlist_name
