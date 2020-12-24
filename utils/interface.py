import os
import random
import mutagen.mp3
import fnmatch
from pygame import mixer
import pygame
from tkinter import *
from tkinter import ttk
from subprocess import Popen
from time import sleep
from threading import Thread
from .utils import theme

class Cuteplayer(Frame):
    # update youtube-dl on start
    uthread = Thread(target=lambda: os.system("pip3 install --upgrade youtube-dl")).start()

    # Path stuff
    path = "" + os.path.expanduser("~/Music") + "/cuteplayer/"

    print("*"*90)
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        print('Download directory exists at: ', path)


    mp3_songs   = []
    playlist    = []
    currentSong = None
    timelineid  = None
    queid       = None
    vol         = 5
    sample_rate = 48000
    crtime      = 0

    def __init__(self, master=None, _theme='default'):
        super().__init__(master)
        # Theme selection
        self.palette = theme(_theme)

        self.bgcolor             = self.palette['bgcolor']
        self.entrybg             = self.palette['entrybg']
        self.textcolor           = self.palette['textcolor']
        self.buttonbg            = self.palette['buttonbg']
        self.volumetroughcolor   = self.palette['volumetroughcolor']
        self.timelinetroughcolor = self.palette['timelinetroughcolor']
        self.highlightedsongfg   = self.palette['highlightedsongfg']
        self.highlightedsongbg   = self.palette['highlightedsongbg']
        self.buttontext          = self.palette['buttontext']
        self.currentsongtext     = self.palette['currentsongtext']
        self.volumetext          = self.palette['volumetext']
        self.timelinetext        = self.palette['timelinetext']
        self.headerbg            = self.palette['headerbg']
        self.headertext          = self.palette['headertext']

        self.master = master
        self.windowSettings(master)
        self.mainMenu()
        self.music_settings()
        mixer.pre_init(self.sample_rate,-16,0)
        self.songsTable()
        self.updateTable()
        self.updateTimeline()
        self.pack()


    def windowSettings(self, master):
        """Set the main window settings"""
        self.master.geometry("330x560")
        self.master.title("cuteplayer")
        self.master.configure(bg=self.bgcolor)
        self.master.resizable(False, False)
        self.master.grid_propagate(False)

    def mainMenu(self):
       ############################## Buttons Setup ########################### 
        self.entry = Entry(self, fg=self.textcolor, background=self.entrybg,
            font=("ARCADECLASSIC", 15), width=20, highlightbackground=self.bgcolor)

        self.quit = Button(self, text="quit", bg=self.buttonbg, fg=self.buttontext, font=("ARCADECLASSIC", 20),
                command=lambda: [mixer.music.pause(), self.master.destroy()])

        self.dl = Button(self, text="download", bg=self.buttonbg,fg=self.buttontext, font=("ARCADECLASSIC", 20),
                command=lambda: Thread(target=self.download).start()) # Run a new thread

        self.play = Button(self, text="play", bg=self.buttonbg,fg=self.buttontext, font=("ARCADECLASSIC", 20),
                           command=lambda: [mixer.music.unpause(), self.updateTimeline()])

        self.pause = Button(self, text="pause", bg=self.buttonbg, fg=self.buttontext, font=("ARCADECLASSIC", 20),
                        command=lambda: [mixer.music.pause(), self.after_cancel(self.timelineid)])

        self.shuffleSongList = Button(self, text="shuffle", bg=self.buttonbg, fg=self.buttontext,
                                font=("ARCADECLASSIC", 20), command=self._shuffle)

        self.skipButton = Button(self, text="skip", bg=self.buttonbg,fg=self.buttontext, font=("ARCADECLASSIC", 20),
                                 command=self.skip)

        self.CurSong = Label(self, bg=self.bgcolor, text="Now\tPlaying", fg=self.currentsongtext,
                             font=('ARCADECLASSIC', 10), wraplength=250)

        self.VolumeSlider = Scale(self, length=5, font="ARCADECLASSIC", orient='horizontal',
                                  bg=self.bgcolor, fg=self.volumetext, showvalue=0, command=self.VolAdjust,
                                  highlightthickness=10, highlightbackground=self.bgcolor,
                                  troughcolor=self.volumetroughcolor)

        # Set the default value to 50% volume
        self.VolumeSlider.set(self.vol)

        self.VolumeSlider.configure(label="%60s"%("volume"))

        self.timeline = Scale( self, length=100, font="ARCADECLASSIC",
                               orient='horizontal', bg=self.bgcolor, fg=self.timelinetext, showvalue=0,
                               highlightthickness=10, highlightbackground=self.bgcolor,
                               troughcolor=self.timelinetroughcolor, label=' ')

        self.timeline.bind("<Button-1>", lambda event: self.after_cancel(self.timelineid))
        self.timeline.bind("<ButtonRelease-1>", self.setTimeline)
        ############################## End ############################## 

        ############################# Packing ############################## 
        self.entry.grid( row=0, column=0, columnspan=3, sticky=W + E + N + S, padx=3, pady=3)

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


    def VolAdjust(self, vol):
        self.vol = int(vol) / 100
        mixer.music.set_volume(self.vol)


    def skip(self):
        """Play the next song in the playlist"""
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
            self.currentSong = self.path + \
                self.table.item(curItem)["text"] + ".mp3"

            self.playlist = ["" + self.path + song for song in self.mp3_songs]
            self.updatenplay()
        except (FileNotFoundError, Exception):
            sleep(1)
            self.updatenplay()

        self.que_song()

    def updatenplay(self, _shuffcall=None):
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
        self.CurSong.configure(text=str(self.currentSong[len(self.path):-4])[:30])
        self.crtime = 0

        # Getting the correct child_id for the currently playing song. We need this so
        # we can focus the item on the songs table, then it'll be highlighted
        if self.currentSong:
            if _shuffcall is None:
                child_id = self.table.get_children()[(self.playlist.index(self.currentSong))]
            else:
                child_id = self.table.get_children()[_shuffcall]
            self.table.focus(child_id)
            self.table.selection_set(child_id)

        print(":: %s" % self.currentSong[len(self.path):-4])

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

        print('playlist\n' , self.playlist)
        print('mp3_songs\n' , self.mp3_songs)

        print("********** Current Playlist ********** ")
        for index, song in enumerate(self.playlist):
            print("%s - : %s" % (index, song.strip(self.path)))

        if self.playlist:
            self.currentSong = self.playlist[0]
            self.updatenplay(_shuffcall=self.mp3_songs.index(self.currentSong[len(self.path):]))
            # if self.playlist:
            self.que_song()

    def que_song(self):
        """ Used by the _shuffle function to queu the next song in the list """
        if int(mixer.music.get_pos()) == -1:
            self.skip()

        self.queid = self.after(1000, self.que_song)

    def songsTable(self):
        """ Widget Treeview/table with songs """
        ####################### STYLE ####################### 
        self.style = ttk.Style()

        ######## Treeview Styling
        self.style.configure("Treeview", foreground=self.textcolor, background=self.bgcolor, 
                borderwidth=0, fieldbackground=self.bgcolor, font=("ARCADECLASSIC", 10))

        # Selected song highlight colors
        self.style.map('Treeview', background=[('selected', self.highlightedsongbg)])
        self.style.map('Treeview', foreground=[('selected', self.highlightedsongfg)])

        ######## Treeview Header Styling
        self.style.configure("Treeview.Heading", background= self.headerbg,
                              foreground=self.headertext, borderwidth=0)

        # Hover highlight color
        self.style.map('Treeview.Heading', background=[('selected', self.bgcolor)])
        self.style.map('Treeview.Heading', foreground=[('selected', self.textcolor)])

        ####################### STYLE ####################### 

        self.table = ttk.Treeview(self, columns=("songNumber"), style="Treeview")
        # Column config
        self.table.column("songNumber", width=-50)
        self.table.heading("songNumber", text="☪ ")

        self.table.grid(row=3, column=0, rowspan=2, columnspan=3, sticky=W + E + N + S, ipady=3,)

        # Selecting songs from table event
        self.table.bind("<ButtonRelease-1>", self.selectedItem)

    def setTimeline(self, _time_event):
        """ Set the position of the song in a timeline slider """
        if mixer.music.get_busy():
            self.after_cancel(self.timelineid)
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
        if self.timelineid is not None:
            self.after_cancel(self.timelineid)
        try:
            song = mutagen.mp3.MP3(self.currentSong)
            self.timeline.configure(to=song.info.length)
            self.timeline.set(self.crtime)
            self.crtime += 1

            m,s = divmod(self.crtime, 60)
            self.timeline.configure(label="%60s %1s: %2s"%(" ",int(m),int(s)))
        except Exception:
            pass
            
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
            self.table.insert("", i, text="%s" % song[:len(song)-4], values=(i + 1))

    def download(self):
        """ Downloads the song/video to the home/user/music/cuteplayer directory """
        if self.entry.get():
            try:
                print(":"*30+"[ Video Downloading ]"+(":"*30))
                Popen(["'youtube-dl' '-o' '%s' '--extract-audio' '--audio-format' 'mp3'\
                        '%s'" % (self.path + "%(title)s.%(ext)s", self.entry.get())],
                        shell=True).wait()

                self.entry.delete(0, "end")
                self.updateTable()
            except (RuntimeError, Exception) as e:
                print(e)
                pass
