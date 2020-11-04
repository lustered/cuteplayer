#!/usr/bin/env python3
from utils.interface import *
from utils.update import update
import sys

if __name__ == "__main__":

    update = os.system(" bash update.sh")
    if update is not 0:
        os.execv(__file__, sys.argv)

    # print(os.system(" bash update.sh"))
    #     os.execv(__file__, sys.argv)

    ROOT = Tk()
    ROOT.attributes('-topmost', True)
    APP = Cuteplayer(master=ROOT)
    APP.mainloop()
