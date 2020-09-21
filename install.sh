#!/bin/bash
pip3 install tk pygame mutagen youtube-dl

u=`uname`
dir=`pwd`
if [[ "$u" == 'Linux' ]];  then
    echo  "[Desktop Entry]
Version=1.0
Name=cuteplayer
Comment=Cute music player to download music 
Exec=python3 ${dir}/app.py
Icon=${dir}/pics/cat.jpeg
Path=${dir}
Terminal=false
Type=Application" > cuteplayer.desktop

mv cuteplayer.desktop ~/.local/share/applications/
pyinstaller --onefile --icon=pics/cato.ico app.py
fi

