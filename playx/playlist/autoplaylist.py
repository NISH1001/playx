#!/usr/bin/env python3

"""
    This module is intended to use Markov Chains for generating playlist automatically.
    For now, simple counter is used to create a "naive" baseline auto-playlist.
"""

import pathlib
import re

from collections import Counter

def remove_multiple_spaces(string):
    return re.sub(r'\s+', ' ', string).strip()

def remove_punct(string):
    string = re.sub(r"[']+", '', string)
    return re.sub(r"[-:_!,/.()#?;&]+", ' ', string)

def get_timeseries_data(log_path):
    data = []
    with open(log_path) as f:
        for line in f:
            line = line.strip().lower()
            if 'playing' not in line:
                continue
            matches = re.findall(r"\[.*?\]", line)
            module, timestamp = matches[0], matches[1]
            try:
                song = matches[2]
                ts = re.sub(r"[\[\]]+", '', timestamp)
                song = re.sub(r"[\[\]]+", '', song)
                song = remove_punct(song)
                song = remove_multiple_spaces(song)
                data.append((ts, song))
            except IndexError:
                continue
    return data

def main():
    path = pathlib.Path("~/.playx/logs/log.cat").expanduser()
    data = get_timeseries_data(path)
    ts, songs = zip(*data)
    counter = Counter(songs)
    songs_frequent, c = zip(*counter.most_common())
    with open(pathlib.Path("~/.playx/playxlist/auto.playx").expanduser(), 'w') as f:
        for s in songs_frequent:
            f.write("{}\n".format(s))

if __name__ == "__main__":
    main()

