"""Functions related to getting soundcloud data."""

import requests


def get_track_info(url):
    """
    Get the track info of the passed URL.
    """
    _client_ID = 'LvWovRaJZlWCHql0bISuum8Bd2KX79mb'
    api = "http://api.soundcloud.com/resolve.json?url={}&client_id={}"
    URL = api.format(url, _client_ID)
    r = requests.get(URL).json()
    title = r['title']
    stream_url = r['stream_url'] + '?client_id=' + _client_ID
    return title, stream_url
