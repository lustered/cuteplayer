# Cuteplayer - simple GUI mp3 downloader/player

Simple tkinter GUI to download and play youtube files in mp3 format using youtube-dl

![GUI interface](https://github.com/lustered/cuteplayer/blob/master/pics/master.jpeg)

## Timeline slider branch can:

    .Control position of the song
    .Update slider as the song plays

# Install

    ./install.sh

### MacOs

    - Make sure you have python > 3.7 < 3.9 from python.org
    otherwise an older version of tkinter will be used
    - Tk is a pain in the butt
    - Pygame==1.9.6 can be a pain ^
    - youtube-dl env setup can be a pain

    - ./install

### For Ubuntu-based systems[optional]

    sudo apt-get install ffmpeg:i386
    or
    sudo apt-get install libav-tools

## I do not own the font used, found here

    https://www.dafont.com/arcade-classic-2.font

# Branch known issues

    .Slider continues if the timeline is manually changed while the song is paused.
