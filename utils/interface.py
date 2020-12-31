from __future__ import unicode_literals
import os
import random
from time import sleep
import mutagen.mp3
import fnmatch
import pygame
from pygame import mixer
from tkinter import *
from tkinter import ttk
from subprocess import Popen
from threading import Thread
from subprocess import *
import youtube_dl
from .utils import theme
from .utils import tStyle


class Cuteplayer(Frame):

    # Path stuff
    path = "" + os.path.expanduser("~/Music") + "/cuteplayer/"
    print("*" * 90)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print("Download directory exists at: ", path)

    # List with songs being displayed in the table
    mp3_songs   = []
    # Current actual playlist Eg. Shuffle/Normal orders
    playlist    = []
    currentSong = None
    timelineid  = None
    queid       = None
    vol         = 50
    sample_rate = 48000
    crtime      = 0
    busy        = None

    def __init__(self, master, _theme="pastel"):
        super().__init__(master)
        # update youtube-dl on start
        uthread = Thread(target=lambda: os.system("pip3 install --upgrade youtube-dl"))
        uthread.start()

        self.palette = theme(_theme)
        self.master = master
        self.windowSettings(master)
        self.mainMenu()
        mixer.pre_init(self.sample_rate, -16, 0)
        self.music_settings()
        self.songsTable()
        self.updateTable()
        self.updateTimeline()
        self.pack()

    def windowSettings(self, master):
        """Set the main window settings"""
        self.master.geometry("330x560")
        self.master.title("cuteplayer")
        self.master.configure(bg=self.palette["bgcolor"])
        self.master.resizable(False, False)
        self.master.grid_propagate(False)

    def mainMenu(self):
        ############################## Buttons Setup ###########################
        self.entry = Entry(
            self,
            fg=self.palette["entrytext"],
            background=self.palette["entrybg"],
            font=("ARCADECLASSIC", 15),
            highlightbackground=self.palette["bgcolor"], bd=3,
        )

        self.quit = Button(
            self,
            text="quit",
            bg=self.palette["buttonbg"],
            fg=self.palette["buttontext"],
            font=("ARCADECLASSIC", 20),
            highlightbackground=self.palette['bgcolor'],
            highlightthickness=3,
            activebackground=self.palette['activebuttonbg'],
            command=lambda: [mixer.music.pause(), self.master.destroy()]
        )

        self.dl = Button(
            self,
            text="download",
            bg=self.palette["buttonbg"],
            fg=self.palette["buttontext"],
            font=("ARCADECLASSIC", 20),
            highlightbackground=self.palette['bgcolor'],
            highlightthickness=3,
            activebackground=self.palette['activebuttonbg'],
            command=lambda: Thread(target=self.download).start() # Run a new thread
        )  

        self.play = Button(
            self,
            text="play",
            bg=self.palette["buttonbg"],
            fg=self.palette["buttontext"],
            font=("ARCADECLASSIC", 20),
            highlightbackground=self.palette['bgcolor'],
            highlightthickness=3,
            activebackground=self.palette['activebuttonbg'],
            command=lambda: [mixer.music.unpause(), self.setbusy(False), self.updateTimeline()] 
        )

        self.pause = Button(
            self,
            text="pause",
            bg=self.palette["buttonbg"],
            fg=self.palette["buttontext"],
            font=("ARCADECLASSIC", 20),
            highlightbackground=self.palette['bgcolor'],
            highlightthickness=3,
            activebackground=self.palette['activebuttonbg'],
            command=lambda: [mixer.music.pause(), self.setbusy(True), self.after_cancel(self.timelineid)]
        )

        self.shuffleSongList = Button(
            self,
            text="shuffle",
            bg=self.palette["buttonbg"],
            fg=self.palette["buttontext"],
            font=("ARCADECLASSIC", 20),
            highlightthickness=3,
            highlightbackground=self.palette['bgcolor'],
            activebackground=self.palette['activebuttonbg'],
            command=self._shuffle,
        )

        self.skipButton = Button(
            self,
            text="skip",
            bg=self.palette["buttonbg"],
            fg=self.palette["buttontext"],
            font=("ARCADECLASSIC", 20),
            highlightbackground=self.palette['bgcolor'],
            highlightthickness=3,
            activebackground=self.palette['activebuttonbg'],
            command=self.skip,
        )

        self.CurSong = Label(
            self,
            bg=self.palette["bgcolor"],
            text="Now\tPlaying",
            fg=self.palette["currentsongtext"],
            font=("ARCADECLASSIC", 10),
            wraplength=250,
        )

        self.VolumeSlider = Scale(
            self,
            length=5,
            font="ARCADECLASSIC",
            orient="horizontal",
            bg=self.palette["bgcolor"],
            fg=self.palette["volumetext"],
            showvalue=0,
            command=self.VolAdjust,
            highlightthickness=10,
            highlightbackground=self.palette["bgcolor"],
            troughcolor=self.palette["volumetroughcolor"],
            activebackground=self.palette['bgcolor'],
            borderwidth=0
        )

        # Set the default value to 50% volume
        self.VolumeSlider.set(self.vol)

        self.VolumeSlider.configure(label="%60s" % ("volume"))

        self.timeline = Scale(
            self,
            length=100,
            font="ARCADECLASSIC",
            orient="horizontal",
            bg=self.palette["bgcolor"],
            fg=self.palette["timelinetext"],
            showvalue=0,
            highlightthickness=10,
            highlightbackground=self.palette["bgcolor"],
            troughcolor=self.palette["timelinetroughcolor"],
            label="  ",
            activebackground=self.palette['bgcolor'],
            borderwidth=0,
        )

        self.timeline.bind("<Button-1>", lambda event: self.after_cancel(self.timelineid))
        self.timeline.bind("<ButtonRelease-1>", self.setTimeline)
        ############################## End ##############################

        ############################# Packing ##############################
        self.entry.grid(row=0, column=0, columnspan=3, sticky=W + E + N + S)#, padx=3, pady=3)

        self.dl.grid(row=1, column=0, sticky=NSEW)
        self.quit.grid(row=1, column=1, sticky=NSEW)

        self.play.grid(row=2, column=0, sticky=NSEW)
        self.pause.grid(row=2, column=1, sticky=NSEW)

        self.skipButton.grid(row=5, column=0, sticky=NSEW)
        self.shuffleSongList.grid(row=5, column=1, sticky=NSEW)

        self.CurSong.grid(row=6, column=0, columnspan=2, sticky=NSEW)
        self.timeline.grid(row=7, column=0, columnspan=3, sticky=NSEW)
        self.VolumeSlider.grid(row=8, column=0, columnspan=3, sticky=NSEW)
    ############################## END ##############################

    def setbusy(self, state):
        """ Set current state """
        self.busy = state

    def VolAdjust(self, vol):
        self.vol = int(vol) / 100
        mixer.music.set_volume(self.vol)

    def skip(self):
        """ Play the next song in the playlist """
        if not self.currentSong:
            return

        try:
            self.currentSong = self.playlist[self.playlist.index(self.currentSong) + 1]
        except IndexError:
            print("Reached the end of the list...\nStarting over.")
            self.currentSong = self.playlist[0]

        self.updatenplay()

    def selectedItem(self, event):
        """Play a song when clicking on the table"""
        if self.queid is not None:
            self.after_cancel(self.queid)

        try:
            curItem = self.table.focus()
            # Remove the selection dashed lines after the focus redraws
            # self.master.focus_set()

            self.currentSong = self.path + self.table.item(curItem)["text"] + ".mp3"

            # Override playlist if the user manually selects a song from the table
            # This is needed as the _shuffle function rearranges the order
            self.playlist = ["" + self.path + song for song in self.mp3_songs]
            self.updatenplay()
        except (FileNotFoundError, Exception):
            sleep(1)
            self.updatenplay()

        self.que_song()

    def updatenplay(self):
        try:
            # override sample rate for song
            sample_rate = mutagen.mp3.MP3(self.currentSong).info.sample_rate
        except mutagen.MutagenError:
            pass

        # set appropiate sample rate if the song selected has a different one
        if self.sample_rate != sample_rate:
            print("new sample rate: ", sample_rate)
            self.sample_rate = sample_rate

        # Re-init settings
        self.music_settings()
        mixer.music.load(self.currentSong)
        mixer.music.play()

        # Only show up to 30 characters to avoid line wrap
        self.CurSong.configure(text=str(self.currentSong[len(self.path) : -4])[:30])
        self.setbusy(False)
        self.crtime = 0
        self.updateTimeline()

        # Getting the correct child_id for the currently playing song. We need this so
        # we can focus the item on the songs table, then it'll be highlighted
        if self.currentSong:
            child_index = self.mp3_songs.index(self.currentSong[len(self.path) :])
            child_id = self.table.get_children()[child_index]

            self.table.selection_set(child_id)

        print(":: %s" % self.currentSong[len(self.path) : -4])

    def music_settings(self):
        """ Reset sample rate since it may vary from each song """
        # In case we change sample rate
        mixer.quit()
        mixer.init(self.sample_rate)
        mixer.music.set_volume(self.vol)

    def _shuffle(self):
        """ Shuffle all current songs in the download directory and play them """
        if self.queid is not None:
            self.after_cancel(self.queid)

        self.playlist = random.sample(self.mp3_songs, len(self.mp3_songs))
        self.playlist = ["" + self.path + song for song in self.playlist]

        print("********** Current Playlist ********** ")
        for index, song in enumerate(self.playlist):
            print("%s - : %s" % (index, song.strip(self.path)))

        if self.playlist:
            self.currentSong = self.playlist[0]
            # self.updatenplay(_shuffcall=self.mp3_songs.index(self.currentSong[len(self.path) :]))
            self._shuffcall = True
            self.updatenplay()
            # if self.playlist:
            self.que_song()

    def que_song(self):
        """ Used to queu the next song """
        if int(mixer.music.get_pos()) == -1:
            self.skip()

        self.queid = self.after(1000, self.que_song)

    def songsTable(self):
        """ Widget Treeview/table with songs """
        # Get customized style
        style = tStyle()
        self.table = ttk.Treeview(self, columns=("songNumber"), style="Treeview")
        # Column config
        self.table.column("songNumber", width=-50)
        self.table.heading("songNumber", text="☪ ")

        self.table.grid(
            row=3,
            column=0,
            rowspan=2,
            columnspan=3,
            sticky=W + E + N + S,
        )

        # Selecting songs from table event
        self.table.bind("<Return>", self.selectedItem)
        self.table.bind("<ButtonRelease-1>", self.selectedItem)

    def setTimeline(self, _time_event):
        """ Set the position of the song in a timeline slider """
        if mixer.music.get_busy():
            self.after_cancel(self.timelineid)
            self.crtime += mixer.music.get_pos() / 1000

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
        # Close other instances -> Otherwise the play button will spawn multiple instances
        if self.timelineid is not None:
            self.after_cancel(self.timelineid)

        try:
            song = mutagen.mp3.MP3(self.currentSong)
            self.timeline.configure(to=song.info.length)
            self.timeline.set(self.crtime)
            self.crtime += 1

            m, s = divmod(self.crtime, 60)
            self.timeline.configure(label="%60s %1s: %2s" % (" ", int(m), int(s)))
        except Exception:
            pass

        if self.busy is False:
            self.timelineid = self.after(1000, self.updateTimeline)

    def updateTable(self):
        """ Refresh the song table list """
        self.table.delete(*self.table.get_children())

        # list of mp3 songs in dir
        for entry in os.listdir(self.path):
            if fnmatch.fnmatch(entry, "*.mp3") and entry not in self.mp3_songs:
                self.mp3_songs.append(entry)

        # add new song to table list
        self.mp3_songs.sort()
        for i, song in enumerate(self.mp3_songs):
            self.table.insert("", i, text="%s" % song[: len(song) - 4], values=(i + 1))

    def download(self):
        """ Download the song to the path and covert to mp3 if necessary """
        dpath = self.path + "%(title)s.%(ext)s"
        ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': dpath,
                'postprocessors':[{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }],
                }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(":" * 30 + "[ Video Downloading ]" + (":" * 30))
            ydl.download([self.entry.get()])
            print(":" * 30 + "[ Song Downloaded ]" + (":" * 30))

        self.entry.delete(0, "end")
        self.updateTable()
