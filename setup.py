import sys 
import os
import cx_Freeze

base = None

# TODO: Fix youtube-dl stdout
# By hiding the console on Windows, youtube-dl won't run the process.
#if sys.platform == 'win32':
#    base = 'Win32GUI'

options = {'build_exe':{"packages":['tkinter','ffmpeg', 'ffprobe'],
            'include_files':['mpv-1.dll', 'ffprobe.exe', 'ffmpeg.exe', 'DLLs', 'pics','utils', 'themes'], 
            }}

executables = [cx_Freeze.Executable('cuteplayer.py', base=base, icon='pics/cato.ico')]

cx_Freeze.setup(name = 'cuteplayer',
        options=options,
        version='1.0',
        author='https://github.com/lustered',
        description='An aesthetic retro arcade music player',
        executables=executables
        )
