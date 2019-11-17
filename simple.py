#!/usr/bin/python3
from tkinter import *
import sys
from subprocess import call
import os
from os import path
from pytube import YouTube as yt
import validators as valid

testing_url = "https://www.youtube.com/watch?v=-wv3ZUCy1Rg"

def download_url():
    url_inserted = entry.get()
    isvalid_domain = False
    if valid.url(url_inserted) and 'youtube' in url_inserted:
        isvalid_domain = True
        print('[Valid URL]')

    if url_inserted and isvalid_domain:
        video = yt(url_inserted)
        cwd = os.getcwd()
        ls = os.listdir(cwd)
        exists = False

        for x in range(len(ls)):
            if video.title in ls[x]:
                exists = True

        if exists:
            print("file exists and video won't be downloaded")
        else: 
            warningMessage.grid_forget()
            print('[[**** Video Downloading ****]]')
            call(["youtube-dl --extract-audio --audio-format mp3 \
                 %s" % (url_inserted)], shell = True)
            print("[Song: %s \tDownloaded" % (video.title))
    else:
        print('** Please enter a valid URL **')
        warningMessage.grid(column = 3, row = 5)


    entry.delete(0,'end')
    entry.focus()


# main driver
window = Tk()

# creating frame
window.title('download youtube mp3')
window.geometry('400x120')                        
window.configure(background = 'lavender')
mainlbl = Label(window,text = 'insert link', bg = 'lavender',fg = 'purple',font = ('Courier',20))

# buttons and entry setup
download = Button(window, text ="download", bg="pink", fg = 'purple', command = download_url)
quit = Button(window, text ="exit", bg = "pink", fg = 'purple', command = window.destroy)
warningMessage = Label(window, bg = 'red',fg = 'black')
warningMessage.configure(text = "Enter a valid URL")
entry = Entry(window)

# buttons,label and entry box  label placement
mainlbl.grid(column = 3, row = 0)
download.grid(column = 2, row = 1)
quit.grid(column = 4, row = 1)
entry.grid(column = 3,row = 4,sticky = W + E)

window.mainloop()
