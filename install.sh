#!/bin/bash

# Build app executable
function build_executable {
printf "\n\n[::Do you want to build the executable?::]\n"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) echo "[::Building executable::]" ; pyinstaller --onefile --icon=pics/cato.ico app.py; break;;
        No ) exit;;
    esac
done
}

function installFont {
# Download font, remove unnecessary files
echo "[::Downloading & Installing font::]"
curl "https://dl.dafont.com/dl/?f=arcade_classic_2" -o font.zip; unzip font.zip; rm font.zip pizzadudedotdk.txt

if [ "$isLinux" == true ]; then
    # Move font to local fonts
    mv ARCADECLASSIC.TTF ~/.local/share/fonts/
fi
}

# Create desktop entry 
function installLinuxEntry {
    echo  "[Desktop Entry]
    Version=1.0
    Name=cuteplayer
    Comment=Cute music player to download music 
    Exec=python3 ${dir}/app.py
    Icon=${dir}/pics/cat.jpeg
    Path=${dir}
    Terminal=false
    Type=Application" > cuteplayer.desktop

    # Move entry 
    mv cuteplayer.desktop ~/.local/share/applications/
    echo "[::Entry Created::]"
}

function installRequirements {
    pip3 install tk pygame mutagen youtube-dl pyinstaller
}

# Do stuff

u=`uname`
dir=`pwd`
isLinux=false

installRequirements

# For Linux systems
if [[ "$u" == 'Linux' ]]; then
    isLinux=true
    installLinuxEntry
    install_font
    build_executable
fi

# For MacOs
if [[ "$u" == 'Darwin' ]]; then
    build_executable
    installFont
fi

