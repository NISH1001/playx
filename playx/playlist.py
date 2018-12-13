"""Youtube Playlist related functions."""

from requests import get
from bs4 import BeautifulSoup
import re
from .youtube import YoutubeMetadata


class YoutubePlaylist():
    """Class to store YouTube playlist data."""

    def __init__(self, URL):
        self.URL = URL
        self.data = []

    def extractName(self, name):
        """Extract the name of the playlist."""
        name = str(name).replace('\n', '')
        name = ''.join(re.findall(r'>.*?<', name)).replace('>', '').replace('<', '')
        name = ' '.join(re.findall(r'[^ ]+', name))
        return name

    def extractPlaylistData(self):
        """Extract all the videos into YoutubeMetadata objects."""

        url_prepend = 'https://www.youtube.com/watch?v='
        r = get(self.URL)
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.findAll('h1', attrs={'class': 'pl-header-title'})
        name = self.extractName(name)
        soup = soup.findAll('tr', attrs={'class': 'pl-video',
                                        'class': 'yt-uix-tile'})

        for i in soup:
            a = re.findall(r'class="pl-video yt-uix-tile ".*?data-title=.*?data-video-id=.*?>', str(i))
            video_title = re.findall(r'data-title=".*?"', a[0])
            video_id = re.findall(r'data-video-id=".*?"', a[0])
            if len(video_title) != 0 and len(video_id) != 0:
                video_title = video_title[0].replace("data-title=", '').replace('"', '')
                video_id = video_id[0].replace("data-video-id=", '').replace('"', '')
                youtube_metadata = YoutubeMetadata()
                youtube_metadata.url = url_prepend + video_id
                youtube_metadata.title = video_title
                youtube_metadata.duration = '0'
                self.data.append(youtube_metadata)

        if len(self.data) == 0:
            print("Are you sure you have videos in your playlist? Try changing privacy\
                    to public.")

        return (name, self.data)


def isPlaylist(url):
    """Check if the passed URL is a playlist."""
    playlistPart = 'https://www.youtube.com/playlist?list'
    if playlistPart in url:
        return True
    else:
        return False
