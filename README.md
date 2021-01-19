# Cuteplayer - A retro arcade music player

### Simple and lightweight tk GUI to download and play youtube files in mp3 format or video

### Themes

##### Pre-tabs pictures

![bliss](https://github.com/lustered/cuteplayer/blob/master/pics/BlissVid.png) ![rainy](https://github.com/lustered/cuteplayer/blob/master/pics/RainyVid.png)

![pastel](https://github.com/lustered/cuteplayer/blob/master/pics/PastelVid.png) ![flame](https://github.com/lustered/cuteplayer/blob/master/pics/FlameVid.png)

## Install | Quite crappy install script

It will install python3.6 for arch systems since most likely 3.9+ will be installed.
If you don't want it to, just make sure you have a python3 < 3.9 version and install the requirements

Ubuntu-based: mpv version can be a hassle. Make sure you install the latest mpv(repo)/libmpv and python-mpv=0.3.9

    ./install

## Mac

- 3.6 < Python3 < 3.8 from python.org. The brew package has issues with tcl-tk
- Pygame==1.9.6
- youtube-dl env setup can be a pain

  ./install

## Windows

### Notes before installing

For the videos implementation feature you will need python-mpv. This can be quite tricky to install properly.
Please read through this [issue](https://github.com/jaseg/python-mpv/issues/60#issuecomment-352719773) before installing the
pip requirements

If you do not want to deal with this and simply want a functional version without the videos integration,
feel free to use this [discotinued version](https://github.com/lustered/cuteplayer/tree/d5c8ed79a82d9102e0cb4ed105045a0696953f3f)

     pip3 install tk pygame==1.9.6 mutagen youtube-dl python-mpv

- Download ffmpeg/ffprobe/ffplay package from [here](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.7z)
- Extract with 7z
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
