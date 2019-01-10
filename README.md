<h1 align=center>
<img src="logo/1024 bg.svg" width=100%>
</h1>

## Search and play any song from terminal.

# playx in action

![GIF](https://i.imgur.com/7P3dSWT.gif)

# playx  

1. [Philosophy](#philosophy)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Features](#features)
5. [Usage](#usage)
6. [Example](#example)
7. [Contribution](#contributions)
8. [TO-DO](#to-do)
9. [Acknowledgements](#acknowledgements)

# Philosophy
Play any songs that come in your mind.
> Hoping to make it an awesome music assistant
---------

## Requirements/Dependencies

1. Python3.x

2. pip3

3. MPV

 * Get <a href = https://mpv.io/>MPV (website)</a> from here.

 * Get <a href = https://github.com/mpv-player/mpv>MPV (github)</a> from here.

> **Note**: These dependencies in linux can be installed in other variants.  
> For *arch linux*, you can use **pacman** package manager accordingly.


------------

## Installation

 * Run the following command in the root directory to install playx.

```
pip install -e .
```

* Or install using setup.py as:

```bash
python setup.py install
```

------------

## Features

- play by query
- play by youtube url
- play a youtube playlist
- play a billboard chart
- play a spotify playlist
- play from soundcloud playlist
- play from JioSaavn playlist
- play from gaana playlist.
- play from local playlist
- cache support
- CLI using `mpv`
- auto generate playlist
------------

## Usage
For now, the application is in development phase.  

```bash
usage: playx [-h] [-p] [-n] [-auto] [-d] [-l] [--pl-start PL_START]
             [--pl-end PL_END]
             [song [song ...]]

playx - Search and play any song that comes to your mind. If you have any
issues, raise an issue in the github (https://github.com/NISH1001/playx) page

positional arguments:
  song                  Name or youtube link of song to download

optional arguments:
  -h, --help            show this help message and exit
  -p, --play-cache      Play all songs from the cache. The cache is located at
                        ~/.playx/songs/ by default
  -n, --no-cache        Don\'t download the song for later use.
  -auto, --auto         Auto generate playlist on the basis of previously
                        played songs.
  -s, --shuffle         Shuffle the playlist. Not applicbble if playlist not
                        passed.

  -d, --dont-cache-search
                        Don't search the song in the cache.
  -l, --lyrics          Show lyircs of the song.
  --pl-start PL_START   Start position in case a playlist is passed. If passed
                        without a playlist it has no effect.
  --pl-end PL_END       End position in case a playlist is passed. If passed
                        without a playlist it has no effect.
```

------------

### Example
**Play by song name**
```bash
playx man sold world nirvana
```
This plays the song titled "The man who sold the world by Nirvana"  
  
**Play by youtube link**  
```bash
playx https://www.youtube.com/watch?v=4zLfCnGVeL4
```
This plays the song *The Sound of Silence*.   

**Play by soundcloud links**
```sh
playx https://api.soundcloud.com/tracks/232673157
```
This plays soundcloud [track](https://api.soundcloud.com/tracks/232673157)
  
**Play from youtube playlist**  
```bash
playx https://www.youtube.com/playlist?list=PLwg22VSCR0W6cwuCKUJSkX72xEvYXS0Zx
```
This plays the songs from my personal (and public) playlist named *Chilld and Wisdom*.

**Play from a Billboard Chart**
```sh
playx hot-100
```
This plays the songs from Billboards [hot-100](https://www.billboard.com/charts/hot-100) chart. The billboard charts can be found [here](https://www.billboard.com/charts)  

**Play from spotify playlist**
```sh
playx https://open.spotify.com/playlist/37i9dQZF1DX5Ozry5U6G0d
```
This plays the songs from Spotify [Summer Party](https://open.spotify.com/playlist/37i9dQZF1DX5Ozry5U6G0d) playlist.

**Play from soundcloud playlist**
```sh
playx https://soundcloud.com/devintracy/sets/goodafternoon
```
This plays the songs from SoundCloud [playlist](https://soundcloud.com/devintracy/sets/goodafternoon)

**Play from JioSaavn playlist**
```sh
playx https://www.jiosaavn.com/featured/magical-amit-trivedi/IGYxX3V4T7w_
```
This plays songs from the JioSaavn [playlist](https://www.jiosaavn.com/featured/magical-amit-trivedi/IGYxX3V4T7w_)

**Play from local playlist**

The local playlist should have an extension ```.playx``` in order for us to recognize it as a playlist.
```sh
playx example.playx
```
This plays a playlist named example.playx

For a playlist every line is considered an entry. Refer to [example.playx](https://github.com/NISH1001/playx/blob/develop/example.playx).  
  
**Auto-Generate Playlist**
```bash
playx --auto
```
This will automatically generate a playlist by using the frequency of songs played that has been logged in the log file.  
*Note: This will improve in future releases using more robust method (like Markov Chains)*  
  
------------

## Cache Directory Structure
By default, `playx` creates a directory in the home as `~/.playx` (which is a hidden folder). 
Structure is like:  
```bash
.playx
    |- songs/
    |- logs/
```

*songs*: This stores all the songs downloaded by `playx`  
*logs*: This stores the log for user activities of songs that are searched and played with creation date. This will be used for recommendation of songs in future version

------------

## Contributions
Contributions are warmly welcome. Please do go through [CONTRIBUTING](https://github.com/NISH1001/playx/blob/develop/CONTRIBUTING.md).

------------

## TO-DO
- ~~caching of downloaded songs (if the song exists locally, play it right away else play from youtube)~~
- ~~speed up the whole **search->download->convert->play** process~~
- ~~stream/play while downloading the song~~
- ~~play all the songs from the cache~~
- ~~search lyrics~~
- ~~play from youtube playlist~~
- ~~play from local playlist (may be a list of song names)~~
- ~~play from other playlist (spotify, billboard, etc.)~~
- ~~log activity~~
- ~~auto generate playlist~~
- use Markov Chains to improve auto-playlist
- use Factorization Machines to improve auto-playlist
- use logs to create simple recommendations


## Acknowledgements
- Thanks to [Deepjyoti Barman](https://github.com/deepjyoti30) for doing all the major contributions (parallelizing streaming + downloads
, playlist, logger)
- Thanks to [Mirza Zulfan](https://github.com/mirzazulfan) for logo for `playx`. It's neat (and cool)
- Thanks to [Mattwmaster58](https://github.com/Mattwmaster58) for creating packaging structure with setup file
