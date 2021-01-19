#!/usr/bin/env python3.6
import cx_Freeze
import sys 
import matplotlib

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

options = {'build_exe':{"packages":['tkinter'],
            'include_files':['pics','utils', 'themes']}}

executables = [cx_Freeze.Executable('cuteplayer.py', base=base, icon='pics/cato.ico')]

cx_Freeze.setup(name = 'cuteplayer',
        options=options,
        version='1.0',
        author='Cluis',
        description='An aesthetic retro punk music player',
        executables=executables

        )
