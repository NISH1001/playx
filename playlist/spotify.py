from requests import get
from bs4 import BeautifulSoup
import re

# url = "https://open.spotify.com/playlist/3YSjAfvq8CVG2mqrzJcv31?si=U72PoitqQiyRmAJ1HZzDeA"
url = "https://open.spotify.com/playlist/37i9dQZF1DX5Ozry5U6G0d"


class SpotifySong:
    """Spotify songs container."""

    def __init__(self):
        self.title = ''
        self.artist = ''
        self.album = ''


class SpotifyIE:
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
            songObj = SpotifySong()
            songObj.title = re.sub(r'class="track-name".*?>|</span>',
                            '',
                            re.findall(r'class="track-name".*?</span>', str(i))[0])
            songObj.artist = re.sub(r'a href="/artist.*?<span dir=".*?>|</span>|</a>',
                            '',
                            re.findall(r'a href="/artist.*?</a>', str(i))[0])
            songObj.album = re.sub(r'a href="/album.*?<span dir=".*?>|</span>|</a>',
                            '',
                            re.findall(r'a href="/album.*?</a>', str(i))[0])
            self.playlist_content.append(songObj)

        return self.playlist_content


class SpotifyPlaylist:
    """Container that uses the SpotifyIE to properly align
    all the data and return a proper tuple.
    """

    def __init__(self, URL, pl_start=None, pl_end=None):
        self.URL = URL
        self.list_content_tuple = []
        self.pl_end = pl_end
        self.pl_start = pl_start
        self.default_end = 0
        self.default_start = 1
        self.is_valid_start = False
        self.is_valid_end = False
        self.playlist_name = ''

    def is_valid(self):
        """Check if pl_start and pl_end are valid."""
        self.is_valid_start = True if self.pl_start in range(
                                            self.default_start,
                                            self.default_end + 1) else False
        self.is_valid_end = True if self.pl_end in range(
                                            self.default_start,
                                            self.default_end + 1) else False

    def strip_to_start_end(self):
        """Strip the tuple to positions passed by the user."""
        # Before doing anything check if the passed numbers are valid
        self.is_valid()
        if self.pl_start is not None and self.is_valid_start:
            self.default_start = self.pl_start
        if self.pl_end is not None and self.is_valid_end:
            self.default_end = self.pl_end
        self.list_content_tuple = self.list_content_tuple[self.default_start - 1: self.default_end]

    def extract_data(self):
        """Extract the playlist data."""
        spotify = SpotifyIE(self.URL)
        self.list_content_tuple = spotify.get_data()
        self.playlist_name = spotify.playlist_name
        self.default_end = len(self.list_content_tuple)
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
