#!/bin/bash

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

    if [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
       printf "\nPlease install the font in the directory\n"
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
Exec=${dir}/cuteplayer.py
Icon=${dir}/pics/cato.ico
Path=${dir}
Terminal=false
Type=Application" > cuteplayer.desktop

        # Move entry 
        sudo mv cuteplayer.desktop ~/.local/share/applications/
        printf "\n\n[::Entry Created::]\n"

    else
        cp cuteplayer.py cuteplayer.command
        chmod +x cuteplayer.command
    fi
}

function installRequirements {

    if [ -f "/etc/arch-release" ]; then
        ver=$(python -V 2>$1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
        if [ "$ver" -gt "38" ]; then
            printf "\nInstalling python3.6 on the system\n"
            mkdir tmp
            cd tmp
            git clone https://aur.archlinux.org/python36.git
            cd python36
            makepkg -si
            curl -O https://bootstrap.pypa.io/get-pip.py
            python3.6 get-pip.py
            python3.6 -m pip install tk pygame==1.9.6 mutagen youtube-dl 

        else
            pip3 install tk pygame==1.9.6 mutagen youtube-dl 
        fi
    else
        pip3 install tk pygame==1.9.6 mutagen youtube-dl 
    fi
}

# Do stuff
u=`uname`
dir=`pwd`

installRequirements
installFont
installEntry
