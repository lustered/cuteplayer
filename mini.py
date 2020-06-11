from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
from subprocess import Popen
import fnmatch
from time import sleep
import pygame
from pygame import mixer
import mutagen.mp3
import random
import os


class Cuteplayer(Frame):
    path = "" + os.path.expanduser("~") + "/Music/cuteplayer/"
    try:
        os.mkdir(path)
        print("download directory created")
    except FileExistsError:
        print("download directory already exists")

    mp3_songs = []
    currentSong = None
    sample_rate = 48000
    current_song_length = 0
    playlist = []
    play_counter = 0

    print("default settings", "\nsample rate: ", sample_rate, "\nsong dir:    ", path)

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
        self.master.geometry("300x400")
        self.master.title(" 김성경")
        self.master.configure(bg="#333333")

    def mainMenu(self):
        # basic buttons
        self.entry = Entry(
            self,
            fg="#333333",
            background="#333333",
            font=("ArcadeClassic", 15),
            width=20,
            highlightbackground="#333333",
        )

        self.quit = Button(
            self,
            text="quit",
            bg="#333333",
            font=("ArcadeClassic", 20),
            command=self.master.destroy,
        )

        self.enter = Button(
            self,
            text="download",
            bg="#333333",
            font=("ArcadeClassic", 20),
            command=self.Download,
        )

        self.play = Button(
            self,
            text="play",
            bg="#333333",
            font=("ArcadeClassic", 15),
            command=lambda: mixer.music.unpause(),
        )

        self.pause = Button(
            self,
            text="pause",
            bg="#333333",
            font=("ArcadeClassic", 15),
            command=lambda: mixer.music.pause(),
        )

        self.shuffleSongList = Button(
            self,
            text="shuffle",
            bg="#333333",
            font=("ArcadeClassic", 15),
            command=self.shuffle_songs,
        )

        self.skip = Button(
            self,
            text="skip",
            bg="#333333",
            font=("ArcadeClassic", 15),
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
        if not self.currentSong:
            return
        self.playlist = [song for song in self.mp3_songs]
        self.playlist = ["" + self.path + song for song in self.playlist]

        new_song = self.playlist.index(self.currentSong)
        self.currentSong = self.playlist[new_song + 1]

        self.update_sample_rate()
        mixer.music.load(self.currentSong)
        mixer.music.play()
        print("new song: ", self.currentSong.strip(self.path))

    def selectedItem(self, x):  # idk what the 2nd arg is for
        self.after_cancel(self.que_song)
        self.play_counter = 0
        try:
            curItem = self.table.focus()
            # print(self.table.item(curItem)['text'])
            self.currentSong = self.path + self.table.item(curItem)["text"] + ".mp3"
            self.update_sample_rate()
            # play song selected in treeview table
            mixer.music.load(self.currentSong)
            mixer.music.play()
            print(self.currentSong.strip(self.path))
        except (FileNotFoundError, pygame.error):
            mixer.music.load(self.currentSong)
            mixer.music.play()
            # pass

    def update_sample_rate(self):
        try:
            # override sample rate for song
            self.defined_sample_rate = mutagen.mp3.MP3(
                self.currentSong
            ).info.sample_rate  # sample rate of selected song
        except (mutagen.MutagenError):
            print("Mutagen being bad")
        # set appropiate sample rate if the song selected has a different one
        if self.defined_sample_rate != self.sample_rate:
            print("new sample rate: ", self.defined_sample_rate)
            self.sample_rate = self.defined_sample_rate
        self.music_settings()  # init with new sample rate

    def music_settings(self):
        mixer.quit()  # in case we change sample rate
        mixer.init(self.sample_rate)
        mixer.music.set_volume(0.5)

    def shuffle_songs(self):
        self.playlist = random.sample(self.mp3_songs, len(self.mp3_songs))
        self.playlist = ["" + self.path + song for song in self.playlist]
        for index, song in enumerate(self.playlist):
            print("%s - Current Playlist: %s" % (index, song.strip(self.path)))

        if len(self.playlist) > 0:
            self.currentSong = self.playlist.pop()
            self.update_sample_rate()
            mixer.music.load(self.currentSong)
            mixer.music.play(0)
        if len(self.playlist) > 0:
            self.que_song()

    def que_song(self):
        pos = mixer.music.get_pos()
        if int(pos) == -1:
            print(self.currentSong.strip(self.path))
            self.update_sample_rate()
            self.currentSong = self.playlist.pop()
            mixer.music.load(self.currentSong)
            mixer.music.play(0)

        if len(self.playlist) > 0:
            self.after(1000, self.que_song)

    # creating object Treeview/table

    def songsTable(self):
        # list of songs in dir
        # styling for Treeview
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            foreground="black",
            background="#333333",
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
        pass

    def updateTable(self):
        self.table.delete(*self.table.get_children())
        pattern = "*.mp3"
        ls = os.listdir(self.path)

        # list of mp3 songs in dir
        for entry in ls:
            if fnmatch.fnmatch(entry, pattern) and entry not in self.mp3_songs:
                self.mp3_songs.append(entry)

        self.mp3_songs.sort()
        # add new song to table list
        for i, song in enumerate(self.mp3_songs):
            self.table.insert("", i, text="%s" % (song.strip(".mp3")), values=(i + 1))

        self.after(2000, self.updateTable)

    def Download(self):
        if len(self.entry.get()) > 0:
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
            except e:
                print("Error Downloading")
            print("[Song Downloaded]")
            self.entry.delete(0, "end")


if __name__ == "__main__":
    root = Tk()
    root = Tk()
    app = Cuteplayer(master=root)
    app.mainloop()
