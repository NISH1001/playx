from requests import get
from bs4 import BeautifulSoup
import re

# url = "https://open.spotify.com/playlist/3YSjAfvq8CVG2mqrzJcv31?si=U72PoitqQiyRmAJ1HZzDeA"
url = "https://open.spotify.com/playlist/37i9dQZF1DX5Ozry5U6G0d"


class SpotifySong:

    def __init__(self):
        self.title = ''
        self.artist = ''
        self.album = ''


class Spotify:

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

    def get_playlist_name(self):
        """Get the name of the playlist."""

