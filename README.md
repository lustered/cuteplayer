## cuteplayer - simple GUI mp3 downloader/player
###### Simple tkinter GUI to download and play youtube/soundcloud files in mp3 format using youtube-dl

![GUI interface](https://github.com/lustered/youtube-mp3-GUI/blob/master/pics/gui.jpeg)

# Install requirements:
    * linux desktop entry
        pip3 install -r requirements.txt
        ./create_entry.sh
        sudo cp cuteplayer.desktop /usr/share/applications
    * or  executable in /dist

# Adding to terminal path [might need root permission]
    cp cuteplayer.py /usr/local/bin
    mv cuteplayer.py cuteplayer

# for ubuntu-based systems[optional]
    sudo apt-get install ffmpeg:i386
    or
    sudo apt-get install libav-tools

# known issues:
    * sometimes pygame.mixer.music will fail to load a song, but works if you click it again
    * won't open if a song has emojis, simlpy rename
    * ignore pulseaudio/ALSA verbose: [ALSA lib pcm.c:8306:(snd_pcm_recover) underrun occurred]

    * [mutagen has some issues: https://github.com/ritiek/spotify-downloader/issues/149
    * although this won't affect the functionality much, aside from sometimes 
    * crashing the shuffle option]

