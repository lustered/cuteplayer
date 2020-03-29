#!/usr/bin/env python3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview
import os
from subprocess import call,Popen
import fnmatch
from time import sleep
import pygame
from pygame import mixer
import mutagen.mp3
import random


class Downloader(Frame):
    delay = 2000
    path = ""+os.path.expanduser("~")+"/Music/cuteplayer/"
    mp3_songs = []
    currentSong = None
    sample_rate = 48000
    current_song_length = 0
    playlist = []
    play_counter = 0
    print("default settings", 
            "\nsample rate: ",sample_rate,
            "\nsong dir:    ",path)

    def __init__(self,master=None):
        super().__init__(master)
        self.master = master 
        self.windowSettings(master)
        self.mainMenu()
        self.music_settings()
        self.songsTable()
        self.updateTable()
        self.pack() 

        self.playlist = random.sample(self.mp3_songs,len(self.mp3_songs))
        self.playlist = [''+self.path+song for song in self.playlist]


    def windowSettings(self,master):
        self.master.geometry("400x400")
        self.master.title(" 김성경")
        self.master.configure(bg='pink')


    def mainMenu(self):
        # basic buttons
        self.entry = Entry(self,fg='lavender',background='teal',font=('ArcadeClassic',15),width = 30)

        self.quit = Button(self, text="quit", bg="pink",
                                font=('ArcadeClassic',20),
                                command=self.master.destroy)

        self.enter = Button(self, text="download",bg="pink",
                                font=('ArcadeClassic',20),
                                command=self.download)

        self.play = Button(self, text='play',bg='lavender',
                                font=('ArcadeClassic',15),
                                command=lambda: mixer.music.unpause())
                
        self.pause = Button(self, text='pause',bg='lavender',
                                font=('ArcadeClassic',15),
                                command=lambda: mixer.music.pause())

        self.shuffleSongList = Button(self, text='shuffle',bg='lavender',
                                font=('ArcadeClassic',15),
                                command=self.shuffle_songs)
       
        # packing/grid
        self.entry.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.enter.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        self.quit.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.play.pack(side=BOTTOM,fill=X)
        self.pause.pack(side=BOTTOM,fill=X)
        self.shuffleSongList.pack(side=BOTTOM,fill=BOTH)


    def selectedItem(self,x):#idk what the 2nd arg is for
        self.play_counter = 0
        try:
            curItem = self.table.focus()
            # print(self.table.item(curItem)['text'])
            self.currentSong = self.path+self.table.item(curItem)['text'] + ".mp3"
            self.update_sample_rate()
            # play song selected in treeview table
            print(self.currentSong)
            mixer.music.load(self.currentSong)
            mixer.music.play()
        except (FileNotFoundError):
            pass
    

    def update_sample_rate(self):
        try:
            # override sample rate for song
            self.defined_sample_rate = mutagen.mp3.MP3(self.currentSong).info.sample_rate # sample rate of selected song
        except(mutagen.MutagenError):
            print("Mutagen being bad")
        # set appropiate sample rate if the song selected has a different one
        if self.defined_sample_rate != self.sample_rate:
            print("new sample rate: ", self.defined_sample_rate)
            self.sample_rate = self.defined_sample_rate
            self.music_settings() # init with new sample rate


    def music_settings(self):
        mixer.quit() # in case we change sample rate
        mixer.init(self.sample_rate)
        mixer.music.set_volume(.1)


    def shuffle_songs(self):
        self.play_counter -= 1
        if abs(self.play_counter) <= len(self.playlist): 
            self.currentSong = self.playlist[self.play_counter]
            print(self.currentSong)
        try: 
            # get current song's length
            self.current_song_length = mutagen.mp3.MP3(self.currentSong).info.length
        except(mutagen.MutagenError):
            print("Mutagen is retarded")

        self.update_sample_rate()
        mixer.music.load(self.currentSong)
        mixer.music.play()
        
        # length of the song to call function again to play the next song
        wait_time = int(self.current_song_length * 1000) + 1
        # repeat when song is over
        self.after(wait_time,self.shuffle_songs)


    # displaying and updating table
    def songsTable(self):
        # list of songs in dir
        # styling for Treeview
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="pink",font=("ArcadeClassic",10))

        # table itself
        self.table = Treeview(self,columns=("Format","songNumber"))
        # column labels
        self.table.column("Format",width=29)
        self.table.column("songNumber",width=1)
        # font style
        self.table.configure(style="BW.TLabel")
        self.table.heading("Format", text="Format")
        self.table.heading("songNumber", text="#") 
        self.table.pack(side=BOTTOM,fill=BOTH,expand=True)

        # selecting songs from table interaction 
        self.table.bind('<ButtonRelease-1>', self.selectedItem)


    def updateTable(self):
        self.table.delete(*self.table.get_children())
        pattern = "*.mp3"
        ls = os.listdir(self.path)

        # list of mp3 songs in dir
        for entry in ls:
            if fnmatch.fnmatch(entry,pattern) and entry not in self.mp3_songs:
                self.mp3_songs.append(entry)
         
        self.mp3_songs.sort()
        # print(self.mp3_songs)
        # add new song to table list
        for i,song in enumerate(self.mp3_songs):
            self.table.insert("",i,text="%s" % (song.strip(".mp3")),values=("mp3",i+1))

        self.after(self.delay,self.updateTable)

    
    def download(self):
        try: 
            os.mkdir(self.path)
            print("download directory created")
        except FileExistsError:
            print("download directory already exists")

        if len(self.entry.get()) > 0:
            try:
                print('[[**** Video Downloading ****]]')
                Popen(["'youtube-dl' '-o' '%s' '--extract-audio' '--audio-format' 'mp3'\
                         '%s'"  % (self.path+"%(title)s.%(ext)s",self.entry.get())],shell = True)
            except:
                print("Error Downloading")
            print("[Song Downloaded]") 
            self.entry.delete(0,'end')
            

if __name__ == '__main__':
    root = Tk()
    app = Downloader(master = root)
    app.mainloop()

