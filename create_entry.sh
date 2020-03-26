#!/bin/bash
u=`uname`
dir=`pwd`
if [[ "$u" == 'Linux' ]];  then
    echo  "[Desktop Entry]
Version=1.0
Name=cuteplayer
Comment=cute simple GUI to download and play mp3
Exec=python3 ${dir}/cuteplayer.py
Icon=${dir}/cat.jpg
Path=${dir}
Terminal=false
Type=Application" > cuteplayer.desktop
fi

