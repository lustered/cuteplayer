#!/usr/bin/python3
from tkinter import *
import sys
from subprocess import call
import os
from os import path
from pytube import YouTube as yt
import validators as valid

testing_url = "https://www.youtube.com/watch?v=-wv3ZUCy1Rg"
download_video = "youtube-dl "
download_mp3 = "--extract-audio --audio-format mp3 "
# both_download = download + ' ' + mp3 + ' -k'

# TODO:
#     add support to choose either download video or mp3
#     add soundcloud support as well

    

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
            # Downloading the video
            warningMessage.grid_forget()
            print('[[**** Video Downloading ****]]')
            if both_check.get():
                call(["%s %s" % (download_video, url_inserted)], shell = True)
                call(["%s %s %s" % (download_video, download_mp3,url_inserted)], shell = True)
            elif mp3_check.get():
                call(["%s %s %s" % (download_video, download_mp3, url_inserted)], shell = True)
            else:
                call(["%s %s" % (download_video, url_inserted)], shell = True)
            print("[Song: %s] \t[DOWNLOADED]" % (video.title))
    else: 
        print('** Please enter a valid URL **')
        warningMessage.grid(column = 3, row = 5)


    entry.delete(0,'end')
    entry.focus()


# main driver
window = Tk()

# creating frame
window.title('download youtube mp3')
window.geometry('400x200')                        
window.configure(background = 'lavender')
mainlbl = Label(window,text = 'insert link', bg = 'lavender',fg = '#deafba',font = ('Courier',17))

# buttons and entry setup
download = Button(window, text ="download", bg="pink", fg = 'purple', command = download_url)
quit = Button(window, text ="exit", bg = "pink", fg = 'purple', command = window.destroy)
warningMessage = Label(window, bg = 'red',fg = 'black')
warningMessage.configure(text = "Enter a valid URL")
entry = Entry(window, bg = '#f0eafe',width = 30)


# check buttons
video_check = IntVar()
mp3_check = IntVar()
both_check = IntVar() 

video = Checkbutton(window, text="video", bg = 'pink', fg = 'purple', \
        onvalue = 1, offvalue = 0, variable = video_check).grid(row = 5, column = 2)
mp3 = Checkbutton(window, text="MP3", bg = 'pink', fg = 'purple', \
        onvalue = 1, offvalue = 0, variable = mp3_check).grid(row=6, column = 2)
both = Checkbutton(window, text="both", bg = 'pink', fg = 'purple', \
        onvalue = 1, offvalue = 0, variable = both_check).grid(row=7, column = 2)

# buttons,label and entry box  label placement
mainlbl.grid(column = 3, row = 0)
download.grid(column = 2, row = 1)
quit.grid(column = 4, row = 1)
entry.grid(column = 3,row = 4,sticky = W + E)

window.mainloop()
