import pathlib
from sys import platform
import os
import random
import mutagen.mp3
from pygame import mixer
import pygame
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from subprocess import Popen
import fnmatch
from time import sleep


class Cuteplayer(Frame):
    """The app itself"""

    # update youtube-dl on start
    os.system("pip3 install --upgrade youtube-dl")

    # Path stuff
    LINUX_PATH = "" + os.path.expanduser("~/Music") + "/cuteplayer/"
    WIN_PATH = "" + os.path.expanduser("~/Music") + "\\cuteplayer\\"
    path = WIN_PATH if "win32" in platform else LINUX_PATH

    print("*"*90)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print('Download directory exists')

    mp3_songs = []
    currentSong = None
    sample_rate = 48000
    current_song_length = 0
    playlist = []
    bg_color = "#e6d5ed"

    print("default settings", "\nsample rate: ",
          sample_rate, "\nsong dir:    ", path)
    print("*"*90)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.windowSettings(master)
        self.mainMenu()
        self.music_settings()
        self.songsTable()
        self.updateTable()
        self.pack()

    def windowSettings(self, master):
        """Set the main window settings"""
        self.master.geometry("300x400")
        self.master.title("김성경")
        self.master.configure(bg="#e6d5ed")
        self.master.resizable(False, False)

    def mainMenu(self):
        # basic buttons
        self.entry = Entry(
            self,
            fg="#333333",
            # background="#e6d5ed",
            background="#c6aadf",
            font=("ArcadeClassic", 15),
            width=20,
            highlightbackground="#e6d5ed",
        )

        self.quit = Button(
            self,
            text="quit",
            bg="pink",
            font=("ArcadeClassic", 20),
            command=self.master.destroy,
        )

        self.enter = Button(
            self,
            text="download",
            bg="pink",
            font=("ArcadeClassic", 20),
            command=self.download,
        )

        self.play = Button(
            self,
            text="play",
            bg="pink",
            font=("ArcadeClassic", 20),
            command=lambda: mixer.music.unpause(),
        )

        self.pause = Button(
            self,
            text="pause",
            bg="pink",
            font=("ArcadeClassic", 20),
            command=lambda: mixer.music.pause(),
        )

        self.shuffleSongList = Button(
            self,
            text="shuffle",
            bg="pink",
            font=("ArcadeClassic", 20),
            command=self.shuffle_songs,
        )

        self.skip = Button(
            self,
            text="skip",
            bg="pink",
            font=("ArcadeClassic", 20),
            command=self.skip_song,
        )

        # packing/grid
        self.enter.grid(row=1, column=0, sticky=NSEW)
        self.quit.grid(row=1, column=1, sticky=NSEW)
        self.entry.grid(
            row=0, column=0, columnspan=3, sticky=W + E + N + S, padx=3, pady=3
        )

        self.play.grid(row=2, column=0, sticky=NSEW)
        self.pause.grid(row=2, column=1, sticky=NSEW)

        self.skip.grid(row=5, column=0, sticky=NSEW)
        self.shuffleSongList.grid(row=5, column=1, sticky=NSEW)

    def skip_song(self):
        """Play the next song in the playlist"""
        if not self.currentSong:
            return

        self.currentSong = self.playlist[self.playlist.index(
            self.currentSong) + 1]

        self.update_sample_rate()
        mixer.music.load(self.currentSong)
        mixer.music.play()
        print("new song: ", self.currentSong.strip(self.path))

    def selectedItem(self, __x):  # idk what the 2nd arg is for
        """Play a song when clicking on the table"""
        self.after_cancel(self.que_song)
        try:
            curItem = self.table.focus()
            # print(self.table.item(curItem)['text'])
            self.currentSong = self.path + \
                self.table.item(curItem)["text"] + ".mp3"
            self.playlist = ["" + self.path + song for song in self.mp3_songs]
            self.update_sample_rate()
            # play song selected in treeview table
            mixer.music.load(self.currentSong)
            mixer.music.play()
            print(self.currentSong.strip(self.path))
            # print(self.currentSong[len(self.path):])
        except (FileNotFoundError, pygame.error):
            sleep(0.05)
            mixer.music.load(self.currentSong)
            mixer.music.play()

    def update_sample_rate(self):
        try:
            # override sample rate for song
            self.sample_rate = mutagen.mp3.MP3(
                self.currentSong
            ).info.sample_rate  # sample rate of selected song
        except mutagen.MutagenError:
            print("Mutagen being bad")
        # set appropiate sample rate if the song selected has a different one
        if self.sample_rate != self.sample_rate:
            print("new sample rate: ", self.sample_rate)
            self.sample_rate = self.sample_rate
        self.music_settings()  # init with new sample rate

    def music_settings(self):
        """reset sample rate since it may vary from each song"""
        mixer.quit()  # in case we change sample rate
        mixer.init(self.sample_rate)
        mixer.music.set_volume(.5)

    def shuffle_songs(self):
        """Shuffle all current songs in the download directory and play them"""
        self.playlist = random.sample(self.mp3_songs, len(self.mp3_songs))
        self.playlist = ["" + self.path + song for song in self.playlist]
        print("********** Current Playlist ********** ")
        for index, song in enumerate(self.playlist):
            print("%s - : %s" % (index, song.strip(self.path)))

        if self.playlist:
            # self.currentSong = self.playlist.pop()
            self.currentSong = self.playlist[0]
            self.update_sample_rate()
            mixer.music.load(self.currentSong)
            mixer.music.play(0)
            # if self.playlist:
            self.que_song()

    def que_song(self):
        """Used by the shuffle_songs function to queu the next song in the list"""
        pos = mixer.music.get_pos()
        if int(pos) is -1:
            self.skip_song()

        self.after(1000, self.que_song)

    def songsTable(self):
        """Object Treeview/table"""
        # list of songs in dir
        # styling for Treeview
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            foreground="black",
            background="#e6d5ed",
            font=("ArcadeClassic", 10),
        )

        # table itself
        # self.table = Treeview(self,columns=("Format","songNumber"))
        self.table = Treeview(self, columns=("songNumber"))
        # column labels
        # self.table.column("Format")#width=20)
        self.table.column("songNumber", width=10)
        # font style
        self.table.configure(style="BW.TLabel")
        # self.table.heading("Format", text="Format")
        self.table.heading("songNumber", text="#")

        self.table.grid(
            row=3,
            column=0,
            rowspan=2,
            columnspan=3,
            sticky=W + E + N + S,
            padx=3,
            pady=3,
        )

        # selecting songs from table interaction
        self.table.bind("<ButtonRelease-1>", self.selectedItem)

    # update table every 2 seconds
    def updateTable(self):
        """Refresh the song table list"""
        self.table.delete(*self.table.get_children())
        pattern = "*.mp3"
        _ls = os.listdir(self.path)

        # list of mp3 songs in dir
        for entry in _ls:
            if fnmatch.fnmatch(entry, pattern) and entry not in self.mp3_songs:
                self.mp3_songs.append(entry)

        self.mp3_songs.sort()
        # add new song to table list
        for i, song in enumerate(self.mp3_songs):
            self.table.insert("", i, text="%s" %
                              (song.strip(".mp3")), values=(i + 1))

        self.after(2000, self.updateTable)

    def download(self):
        """Downloads the song/video to the home/user/music/cuteplayer directory"""
        if self.entry.get():
            try:
                print("[[**** Video Downloading ****]]")
                Popen(
                    [
                        "'youtube-dl' '-o' '%s' '--extract-audio' '--audio-format' 'mp3'\
                         '%s'"
                        % (self.path + "%(title)s.%(ext)s", self.entry.get())
                    ],
                    shell=True,
                )
            except Exception:
                print("Error Downloading")

            print("[Song Downloaded]")
            self.entry.delete(0, "end")
