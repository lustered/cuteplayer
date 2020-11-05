#!/usr/bin/env python3
from utils.interface import *
import sys

if __name__ == "__main__":

    ROOT = Tk()
    ROOT.attributes('-topmost', True)
    APP = Cuteplayer(master=ROOT)
    APP.mainloop()
