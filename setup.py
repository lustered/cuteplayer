import pip
import os

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ["TCL_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, "tcl8.6")
os.environ["TK_LIBRARY"] = os.path.join(PYTHON_INSTALL_DIR, "tk8.6")

pip_packages = ["mutagen", "tk", "youtube-dl", "cx_freeze"]
pip.main(["install", *pip_packages])

import cx_Freeze

options = {
    "packages": ["tkinter"],
    "includes": ["pip"],
    "excludes": [],
    "include_files": ["utils", "themes"],
}

executables = [
    cx_Freeze.Executable(
        "cuteplayer.py", base=None, icon=r"pics/cato.ico", target_name="cuteplayer"
    )
]

cx_Freeze.setup(
    name="cuteplayer",
    options={"build_exe": options},
    version="1.0",
    author="https://github.com/lustered",
    description="An aesthetic retro arcade music player",
    executables=executables,
)

# Standard commands:
#   build             build everything needed to install
#   build_py          "build" pure Python modules (copy to build directory)
#   build_ext         build C/C++ extensions (compile/link to build directory)
#   build_clib        build C/C++ libraries used by Python extensions
#   build_scripts     "build" scripts (copy and fixup #! line)
#   clean             clean up temporary files from 'build' command
#   install           install everything from build directory
#   install_lib       install all Python modules (extensions and pure Python)
#   install_headers   install C/C++ header files
#   install_scripts   install scripts (Python or otherwise)
#   install_data      install data files
#   sdist             create a source distribution (tarball, zip file, etc.)
#   register          register the distribution with the Python package index
#   bdist             create a built (binary) distribution
#   bdist_dumb        create a "dumb" built distribution
#   bdist_rpm         create an RPM distribution
#   bdist_wininst     create an executable installer for MS Windows
#   check             perform some checks on the package
#   upload            upload binary package to PyPI

# Extra commands:
#   build_exe         build executables from Python scripts
#   install_exe       install executables built from Python scripts
#   bdist_wheel       create a wheel distribution
#   alias             define a shortcut to invoke one or more commands
#   bdist_egg         create an "egg" distribution
#   develop           install package in 'development mode'
#   dist_info         create a .dist-info directory
#   easy_install      Find/get/install Python packages
#   egg_info          create a distribution's .egg-info directory
#   install_egg_info  Install an .egg-info directory for the package
#   rotate            delete older distributions, keeping N newest files
#   saveopts          save supplied options to setup.cfg or other config file
#   setopt            set an option in setup.cfg or another config file
#   test              run unit tests after in-place build (deprecated)
#   upload_docs       Upload documentation to PyPI
