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

# TODO:
    # fix stupid stuff and exception handling 
    # add pre-processing to youtube_video title

def platform():
    url_inserted = entry.get()
    isvalid = False
    plat = {'youtube': 1,'soundcloud' : 2}

    if valid.url(url_inserted):
        isvalid = True
    else:
        warningMessage.grid(column = 3, row = 5)
        print('[Please enter a valid URL]')
        return [0,0,False]  

    if True:
        platform_used = [k for k,v in plat.items() if k in url_inserted]
        print('[Valid URL from %s]' % (platform_used[0]))
        # check if file already exists [for YouTube only]
        file_exists = False
        youtube_file = None
        if 'youtube' in platform_used:
            youtube_file = yt(url_inserted)
            print(youtube_file.title)
            # terminal commands 
            pwd = os.getcwd()
            ls = os.listdir(pwd)
            file_exists = False

            if any(youtube_file.title in s for s in ls):
                file_exists = True
                print("File exists and video won't be downloaded")
                warningMessage.configure(text = 'File already exists')
                warningMessage.grid(column = 3, row = 3)
            else: file_exists = False

        return [platform_used[0],youtube_file,file_exists]


def download_url():
    url_inserted = entry.get()
    platform_validation = platform()

    if platform_validation[2] == False:
        # Downloading the video
        warningMessage.grid_forget()
        if platform_validation[0] == 'soundcloud':
            call(["%s %s" % (download_video, url_inserted)], shell = True)
        elif platform_validation[0] == 'youtube':
            if both_check.get():
                call(["%s %s %s" % (download_video, download_mp3,url_inserted)], shell = True)
                # download video
                call(["%s %s" % (download_video, url_inserted)], shell = True)
            elif mp3_check.get():
                call(["%s %s %s" % (download_video, download_mp3,url_inserted)], shell = True)
            elif video_check.get():
                call(["%s %s" % (download_video, url_inserted)], shell = True)
            print("[Song: %s] \t[Downloaded from %s]" % (platform_validation[1].title,platform_validation[0].strip()))
        else:
            print('select an option')
    else:
        pass

    entry.delete(0,'end')
    entry.focus()


# GUI Interface
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
