import sys 
import cx_Freeze
import pip

pip_packages= ['mutagen', 'tk', 'pygame==1.9.6', 'youtube-dl', 'cx_freeze']
pip.main(['install', *pip_packages])

base = None

# TODO: Fix youtube-dl stdout
# By hiding the console on Windows, youtube-dl won't run the process.
#if sys.platform == 'win32':
#    base = 'Win32GUI'


shortcut_table = [
    ("DesktopShortcut",                                             # Shortcut
     "DesktopFolder",                                               # Directory_
     "cuteplayer",                                                  # Name
     "TARGETDIR",                                                   # Component_
     "[TARGETDIR]cuteplayer.exe",                                   # Target
     None,                                                          # Arguments
     None,                                                          # Description
     None,                                                          # Hotkey
     None,                                                          # Icon
     None,                                                          # IconIndex
     None,                                                          # ShowCmd
     "TARGETDIR",                                                   # WkDir
     )
]

msi_data = {"Shortcut": shortcut_table}

bdist_msi_options = {
        'data': msi_data,
        'add_to_path': True,
        'dist_dir': 'cuteplayer-installer',
        'initial_target_dir': r'[DesktopFolder]\Cuteplayer',
        }

options = {"packages":['tkinter'],
            'include_files':['mpv-1.dll', 'DLLs', 'pics','utils', 'themes'], 
            }

executables = [cx_Freeze.Executable('cuteplayer.py', base=base, icon='pics/cato.ico')]


cx_Freeze.setup(
        options={'build_exe' : options, 'bdist_msi': bdist_msi_options},
        version='1.0',
        author='https://github.com/lustered',
        name = 'cuteplayer',
        description='An aesthetic retro arcade music player',
        executables=executables,
        )
