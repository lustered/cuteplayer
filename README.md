# Cuteplayer - A retro arcade music player

### Simple and lightweight tk GUI to download and play youtube files in mp3 format or video

### Themes

##### Pre-tabs pictures

![bliss](https://github.com/lustered/cuteplayer/blob/master/pics/blissTheme.png) ![rainy](https://github.com/lustered/cuteplayer/blob/master/pics/rainyTheme.png)

![pastel](https://github.com/lustered/cuteplayer/blob/master/pics/pastelTheme.png) ![flame](https://github.com/lustered/cuteplayer/blob/master/pics/flameTheme.png)

## Install | Quite crappy install script

##### It will install python3.6 for arch systems since most likely 3.9+ will be installed.

##### If you don't want it to, just make sure you have a python3 < 3.9 version and install the requirements

    ./install

## Mac

    - 3.6 < Python3 < 3.8 from python.org. The brew package has issues with tcl-tk
    - Pygame==1.9.6
    - youtube-dl env setup can be a pain
    - ./install

## Windows

    - pip3 install tk pygame==1.9.6 mutagen youtube-dl pyinstaller
    - Download ffmpeg/ffprobe/ffplay package from https://www.gyan.dev/ffmpeg/builds/
    - You will need to add it to your Path env

## Alternatively

    pip3 install -r requirements.txt

## Known issues

    Hitting the play button will add 1 second every time

## Font:

    https://www.dafont.com/arcade-classic-2.font

# Disclaimer

    Please use this application responsibly. I do not condone the distribution nor profiting
    of copyrighted content by using this application.
