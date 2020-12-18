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
import threading


class Cuteplayer(Frame):
    # update youtube-dl on start
    os.system("pip3 install --upgrade youtube-dl")

    # Path stuff
    path = "" + os.path.expanduser("~/Music") + "/cuteplayer/"

    print("*"*90)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print('Download directory exists')

    mp3_songs = []
    currentSong = None
    vol = 5
    sample_rate = 48000
    current_song_length = 0
    playlist = []
    bg_color = "#e6d5ed"
    id = None
    crtime = 0

    print("default settings", "\nsample rate: ", sample_rate, "\nsong dir: ", path)
    print("*"*90)

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.windowSettings(master)
        self.mainMenu()
        self.music_settings()
        self.songsTable()
        self.updateTable()
        self.updateTimeline()
        self.pack()
        self.dthread = threading.Thread(target=self.download) # threaded dl

    def windowSettings(self, master):
        """Set the main window settings"""
        self.master.geometry("330x560")
        self.master.title("cuteplayer")
        self.master.configure(bg="#e6d5ed")
        self.master.resizable(False, False)
        self.master.grid_propagate(False)

    def mainMenu(self):
        # basic buttons
        self.entry = Entry(
            self,
            fg="#333333",
            # background="#e6d5ed",
            background="#c6aadf",
            font=("ARCADECLASSIC", 15),
            width=20,
            highlightbackground="#e6d5ed",
        )

        self.quit = Button(
            self,
            text="quit",
            bg="pink",
            font=("ARCADECLASSIC", 20),
            command=self.master.destroy,
        )

        self.enter = Button(
            self,
            text="download",
            bg="pink",
            font=("ARCADECLASSIC", 20),
            command=lambda: self.dthread.start(),
        )

        self.play = Button(
            self,
            text="play",
            bg="pink",
            font=("ARCADECLASSIC", 20),
            command=lambda: [mixer.music.unpause(), self.updateTimeline()]
        )

        self.pause = Button(
            self,
            text="pause",
            bg="pink",
            font=("ARCADECLASSIC", 20),
            command=lambda: [mixer.music.pause(), self.after_cancel(self.id)],
        )

        self.shuffleSongList = Button(
            self,
            text="shuffle",
            bg="pink",
            font=("ARCADECLASSIC", 20),
            command=self.shuffle_songs
        )

        self.skip = Button(
            self,
            text="skip",
            bg="pink",
            font=("ARCADECLASSIC", 20),
            command=self.skip_song
        )

        self.VolumeSlider = Scale(
            self, length=5, font="ARCADECLASSIC",
            orient='horizontal', bg=self.bg_color, showvalue=0,
            command=self.VolAdjust, highlightthickness=10,
            highlightbackground=self.bg_color, troughcolor='#c6aadf')
        self.VolumeSlider.configure(label="%60s"%("volume"))

        self.timeline = Scale(
            self, length=100, font="ARCADECLASSIC",
            orient='horizontal', bg=self.bg_color, showvalue=0,
            highlightthickness=10, highlightbackground=self.bg_color, troughcolor='pink',
            label=' ')

        self.timeline.bind("<Button-1>", lambda event: self.after_cancel(self.id))
        self.timeline.bind("<ButtonRelease-1>", self.setTimeline)

        # Set the default value to 50% volume
        self.VolumeSlider.set(self.vol)

        self.CurSong = Label(self, bg=self.bg_color, text="Now\tPlaying",
                             font=('ARCADECLASSIC', 10), wraplength=250)

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

        self.VolumeSlider.grid(
            row=8, column=0, columnspan=3, sticky=NSEW)

        self.CurSong.grid(row=6, column=0, columnspan=2, sticky=NSEW)#, ipady=5)


        self.timeline.grid(row=7, column=0, columnspan=3, sticky=NSEW)

    def VolAdjust(self, vol):
        self.vol = int(vol) / 100
        mixer.music.set_volume(self.vol)


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
        self.CurSong.configure(text=str(self.currentSong[len(self.path):-4])[:30])
        self.crtime = 0

    def selectedItem(self, event):
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
        except (FileNotFoundError, Exception):
            sleep(1)
            mixer.music.load(self.currentSong)
            mixer.music.play()

        # Only show up to 30 characters to avoid line wrap
        self.CurSong.configure(text=str(self.currentSong[len(self.path):-4])[:30])

        self.crtime = 0
        self.que_song()

    def update_sample_rate(self):
        try:
            # override sample rate for song
            sample_rate = mutagen.mp3.MP3(self.currentSong).info.sample_rate
        except mutagen.MutagenError:
            pass
            # print("Mutagen being bad")
            # sleep(1)
            # sample_rate = mutagen.mp3.MP3(self.currentSong).info.sample_rate  # retry

        # set appropiate sample rate if the song selected has a different one
        if self.sample_rate != sample_rate:
            print("new sample rate: ", sample_rate)
            self.sample_rate = sample_rate

        self.music_settings()  # init with new sample rate

    def music_settings(self):
        """ Reset sample rate since it may vary from each song """
        # In case we change sample rate
        mixer.quit()  
        mixer.init(self.sample_rate)
        mixer.music.set_volume(self.vol)

    def shuffle_songs(self):
        """ Shuffle all current songs in the download directory and play them """
        self.crtime = 0
        self.playlist = random.sample(self.mp3_songs, len(self.mp3_songs))
        self.playlist = ["" + self.path + song for song in self.playlist]

        print("********** Current Playlist ********** ")
        for index, song in enumerate(self.playlist):
            print("%s - : %s" % (index, song.strip(self.path)))

        if self.playlist:
            self.currentSong = self.playlist[0]
            self.update_sample_rate()
            mixer.music.load(self.currentSong)
            mixer.music.play(0)
            self.CurSong.configure(text=str(self.currentSong[len(self.path):-4])[:30])
            # if self.playlist:
            self.que_song()

    def que_song(self):
        """ Used by the shuffle_songs function to queu the next song in the list """
        if int(mixer.music.get_pos()) == -1:
            self.skip_song()

        self.after(1000, self.que_song)

    def songsTable(self):
        """ Object Treeview/table """
        # List of songs in dir
        # styling for Treeview
        style = ttk.Style()
        style.configure(
            "BW.TLabel",
            foreground="black",
            background="#e6d5ed",
            font=("ARCADECLASSIC", 10),
        )
        style.map('BW.TLabel', background=[('selected',"#c5a7d1")])

        self.table = Treeview(self, columns=("songNumber"))

        # column labels
        self.table.column("songNumber", width=-50)
        # font style
        self.table.configure(style="BW.TLabel")
        self.table.heading("songNumber", text="#")

        self.table.grid(
            row=3,
            column=0,
            rowspan=2,
            columnspan=3,
            sticky=W + E + N + S,
            ipady=3,
        )

        # selecting songs from table
        self.table.bind("<ButtonRelease-1>", self.selectedItem)

    def setTimeline(self, _time_event):
        """ Set the position of the song in a timeline slider """
        if mixer.music.get_busy():
            self.after_cancel(self.id)
            self.crtime += (mixer.music.get_pos() / 1000)

            # Check boundry since actual play time might be off and lock the frame.
            # Usually happens when setting the slider to the end.
            if self.timeline.get() <= mutagen.mp3.MP3(self.currentSong).info.length:
                mixer.music.set_pos(self.timeline.get())
            else:
                mixer.music.set_pos(mutagen.mp3.MP3(self.currentSong).info.length - 1)

            self.crtime += self.timeline.get() - self.crtime
            self.updateTimeline()
        return

    def updateTimeline(self):
        """ Update the song slider """
        try:
            song = mutagen.mp3.MP3(self.currentSong)
            val = song.info.length
            self.timeline.configure(to=val)
            self.timeline.set(self.crtime)
            self.crtime += 1

            m,s = divmod(self.crtime, 60)
            self.timeline.configure(label="%60s %1s: %2s"%(" ",int(m),int(s)))
        except Exception:
            pass
            
        self.id = self.after(1000, self.updateTimeline)


    # update table every 2 seconds
    def updateTable(self):
        """ Refresh the song table list """
        self.table.delete(*self.table.get_children())
        pattern = "*.mp3"
        _ls = os.listdir(self.path)

        # list of mp3 songs in dir
        for entry in _ls:
            if fnmatch.fnmatch(entry, pattern) and entry not in self.mp3_songs:
                self.mp3_songs.append(entry)

        # add new song to table list
        self.mp3_songs.sort()
        for i, song in enumerate(self.mp3_songs):
            self.table.insert("", i, text="%s" % song[:len(song)-4], values=(i + 1))

    def download(self):
        """ Downloads the song/video to the home/user/music/cuteplayer directory """
        if self.entry.get():
            try:
                print("\n\t\t\t[ Video Downloading ]")
                Popen(
                    [ "'youtube-dl' '-o' '%s' '--extract-audio' '--audio-format' 'mp3'\
                         '%s'" % (self.path + "%(title)s.%(ext)s", self.entry.get())
                    ], shell=True).wait()

                self.entry.delete(0, "end")
                self.updateTable()

            except Exception as e:
                print("Error Downloading", e)
