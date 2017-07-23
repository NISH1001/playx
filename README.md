# playx  

Search and play any song from terminal.  
Hopefully, it will be something that you can play anything from terminal.

---------

## Dependencies
It uses `python3` with libraries : `requests`, `beautifulsoup`. These can be installed using **pip** for python3.  
The OS level dependencies are: `ffmpeg`, `mplayer`, `youtube-dl`

```bash
pip install requests beautifulsoup4
```

```bash
sudo apt install ffmpeg libav-tools x264 x265
```

```bash
sudo apt-get install mplayer 
```

```bash
sudo add-apt-repository ppa:nilarimogard/webupd8
sudo apt-get update
sudo apt-get install youtube-dl
```

> **Note**: These dependencies in linux can be installed in other variants.  
> For *arch linux*, you can use **pacman** package manager accordingly.

------------

## Usage
For now, the application is in development phase. Just run `main.py` with song name as arguments. You can tinker with it if you like.  

Example: 
Play hotel california 

```bash
python3 main.py hotel california acousitc live
```

First, it tries to search locally. If not found, the song will be downloaded from youtube.

------------

## TO-DO
- ~~caching of downloaded songs (if the song exists locally, play it right away else play from youtube)~~
- speed up the whole **search->download->convert->play** process
- stream/play while downloading the song
