#!/usr/bin/env python3.6
from utils.interface import *
import sys

if __name__ == "__main__":

    ROOT = Tk()
    # ROOT.attributes('-topmost', True)
    APP = Cuteplayer(master=ROOT, _theme="bliss")
    APP.mainloop()
