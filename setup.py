import cx_Freeze
import pip

pip_packages = ["mutagen", "tk", "pygame==1.9.6", "youtube-dl", "cx_freeze"]
pip.main(["install", *pip_packages])

options = {
    "packages": ["tkinter"],
    "includes": [],
    "excludes": [],
    "include_files": ["utils", "themes"],
}

executables = [cx_Freeze.Executable("cuteplayer.py", base=None, icon=r"pics/cato.ico")]

cx_Freeze.setup(
    name="cuteplayer",
    options={"build_exe": options},
    version="1.0",
    author="https://github.com/lustered",
    description="An aesthetic retro arcade music player",
    executables=executables,
)
