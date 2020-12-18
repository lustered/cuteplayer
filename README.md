# Cuteplayer - simple GUI mp3 downloader/player

Simple tkinter GUI to download and play youtube files in mp3 format using youtube-dl

[![cuteplayer](https://github.com/lustered/cuteplayer/blob/master/pics/wTimeline.jpeg)]

## Timeline slider branch can:

    .Control position of the song
    .Update slider as the song plays

# Install

    ./install.sh

### MacOs

    - Make sure you have python > 3.7 < 3.9 from python.org
    - Tk is a pain
    - Pygame==1.9.6 is a pain 
    - youtube-dl env setup can be a pain
    - ./install

### For Ubuntu-based systems[optional]

    sudo apt-get install ffmpeg:i386
    or
    sudo apt-get install libav-tools

## I do not own the font

    https://www.dafont.com/arcade-classic-2.font

# Branch known issues

    .Slider continues if the timeline is manually changed while the song is paused.
    .If the slider is set all the way to the end the frame locks up
