#!/usr/bin/env python3
from tkinter import *
import tkinter as tk
from tkinter.ttk import Treeview
from tkinter import ttk
import os
from subprocess import call
import fnmatch
from time import sleep
from pygame import mixer
import mutagen.mp3


class Downloader(Frame):
    path = ""+os.path.expanduser("~")+"/Music/cuteplayer/"
    def __init__(self,master=None):
        super().__init__(master)
        self.master = master 
        self.windowSettings(master)
        self.mainMenu()
        self.songsTable()
        self.pack()

    def windowSettings(self,master):
        self.master.geometry("600x400")
        self.master.title(" 김성경")
        self.master.configure(bg='pink')


    def mainMenu(self):
        # basic buttons
        self.entry = Entry(self,fg='lavender',background='teal',font=('Cascadia Code',15),width = 30)

        self.quit = Button(self, text="quit", bg="pink",
                                font=('Cascadia Code',14),
                                command=self.master.destroy)
        self.enter = Button(self, text="download",bg="pink",
                                font=('Cascadia Code',14),
                                command=self.download)
                
       
        # packing/grid
        self.entry.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)
        self.enter.pack(side=TOP, fill=BOTH, expand=True, padx=0, pady=0)
        self.quit.pack(side=TOP, fill=BOTH, expand=True, padx=1, pady=1)


    def selectedItem(self,z):#idk what the 2nd arg is for
        curItem = self.table.focus()
        # print(self.table.item(curItem)['text'])
        self.currentSong = self.path+self.table.item(curItem)['text'] + ".mp3"
        print(self.currentSong)

        # play song selected in treeview table
        mp3 = mutagen.mp3.MP3(self.currentSong)
        mixer.init(frequency=mp3.info.sample_rate)
        mixer.music.load(self.currentSong)
        mixer.music.play()
    

    # TODO:
    #     update table when song is downloaded
    # displaying and updating table
    def songsTable(self):
        # list of songs in dir
        # styling for Treeview
        style = ttk.Style()
        style.configure("BW.TLabel", foreground="black", background="pink",font=("Cascadia Code",10))

        # table itself
        self.table = Treeview(self,columns=("Format","songNumber"))
        # column labels
        self.table.column("Format",width=29)
        self.table.column("songNumber",width=1)
        # font style
        self.table.configure(style="BW.TLabel")
        self.table.heading("Format", text="Format")
        self.table.heading("songNumber", text="#")
        self.table.pack(side=BOTTOM,fill=BOTH,expand=True,padx=10,pady=10,ipady=10)

        self.table.bind('<ButtonRelease-1>', self.selectedItem)

        # songs in the downloads directory
        mp3_songs=[]
        pattern = "*.mp3"
        ls = os.listdir(self.path)

        for entry in ls:
            if fnmatch.fnmatch(entry,pattern):
                mp3_songs.append(entry)
         
        # print(mp3_songs)
        for i,song in enumerate(mp3_songs):
            self.table.insert("",i,text="%s" % (song.strip(".mp3")),values=("mp3",i+1))


    
    def download(self):
        # print(self.path)
        try: 
            os.mkdir(self.path)
            print("download directory created")
        except FileExistsError:
            print("download directory already exists")

        if len(self.entry.get()) > 0:
            try:
                print('[[**** Video Downloading ****]]')
                call(["youtube-dl -o '%s' --extract-audio --audio-format mp3 \
                         %s"  % (self.path+"%(title)s.%(ext)s",self.entry.get())], shell = True)
            except:
                print("Error Downloading")
            print("[Song Downloaded]") 
            self.entry.delete(0,'end')
            self.table.destroy()
            # self.table.delete(*self.table.get_children())
            self.songsTable()


if __name__ == '__main__':
    root = Tk()
    app = Downloader(master = root)
    app.mainloop()

