#!/bin/bash
u=`uname`
dir=`pwd`
if [[ "$u" == 'Linux' ]];  then
    echo  "[Desktop Entry]
Version=1.0
Name=simple-mp3-GUI
Comment=cute simple GUI to download mp3 from YouTube
Exec=python3 ${dir}/simple.py
Icon=${dir}/cat.jpg
Path=${dir}
Terminal=false
Type=Application" > simple-mp3.desktop
fi

