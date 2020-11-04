#!/bin/bash

# Build app executable
function buildExecutable {
printf "\n\n[::Do you want to build the executable?::]\n"
select yn in "Yes" "No"; do
    case $yn in
        [Yy]* ) printf "\n\n[::Building executable::]\n" ; pyinstaller --onefile --icon=pics/cato.ico app.py; break;;
        [Nn]* ) exit;;
    esac
done
}

function installFont {
# Download font, remove unnecessary files
printf "\n[::Downloading & Installing font::]\n"
curl "https://dl.dafont.com/dl/?f=arcade_classic_2" -o font.zip; unzip font.zip; rm font.zip pizzadudedotdk.txt

if [[ "$u" == 'Linux' ]]; then
    # Move font to local fonts
    mv ARCADECLASSIC.TTF ~/.local/share/fonts/
fi


if [[ "$u" == "Darwin" ]]; then
    # System wide fonts
    mv ARCADECLASSIC.TFF /Library/Fonts
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
    printf "\n\n[::Entry Created::]\n"
}

function installRequirements {
    sudo apt-get install python3-dev python-dev
    pip3 install tk pygame mutagen youtube-dl pyinstaller
}

# Do stuff
u=`uname`
dir=`pwd`

installRequirements
installFont
buildExecutable

# For Linux systems
if [[ "$u" == 'Linux' ]]; then
    installLinuxEntry
fi
