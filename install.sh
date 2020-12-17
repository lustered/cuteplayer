#!/bin/bash

# Build app executable
function buildExecutable {

    printf "\n\n[::Do you want to build the executable?::]\n"
    select yn in "Yes" "No"; do
        case $yn in
            [Yy]* ) printf "\n\n[::Building executable::]\n" ; pyinstaller --onefile --icon=pics/cato.ico cuteplayer.py; break;;
            [Nn]* ) exit;;
        esac
    done
}

function installFont {
    # Download font, remove unnecessary files
    printf "\n[::Downloading & Installing font::]\n"
    curl "https://dl.dafont.com/dl/?f=arcade_classic_2" -o font.zip; unzip font.zip; rm font.zip pizzadudedotdk.txt

    if [[ "$u" == "Linux" ]] 
    then
        # Move font to local fonts
        mv ARCADECLASSIC.TTF ~/.local/share/fonts/
    fi

    if [[ "$u" == "Darwin" ]]
    then
        # System wide fonts
        mv ARCADECLASSIC.TFF /Library/Fonts
    fi
}

# Create desktop entry 
function installEntry {

    if [[ "$u" == "Linux" ]]
    then
        echo  "[Desktop Entry]
Version=1.0
Name=cuteplayer
Comment=Cute music player to download music 
Exec=python3 ${dir}/cuteplayer.py
Icon=${dir}/pics/cat.jpeg
Path=${dir}
Terminal=false
Type=Application" > cuteplayer.desktop

        # Move entry 
        sudo mv cuteplayer.desktop ~/.local/share/applications/
        printf "\n\n[::Entry Created::]\n"

    else
        cp cuteplayer.py cuteplayer.command
    fi
}

function installRequirements {

    pip3 install tk pygame==1.9.6 mutagen youtube-dl pyinstaller

    if [[ "$u" == "Linux" ]] 
    then
        sudo apt-get install python3-dev python-dev
    else
        brew install python3-dev python-dev
    fi
}

# Do stuff
u=`uname`
dir=`pwd`

installRequirements
installFont
installEntry
buildExecutable
