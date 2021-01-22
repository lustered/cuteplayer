from utils.interface import *
import sys

if __name__ == "__main__":
    ROOT = Tk()
    # Stay on top
    ROOT.attributes('-topmost', True)
    ROOT.iconbitmap(default=r'pics/cato.ico')
    APP = Cuteplayer(master=ROOT, _theme="bliss")
    APP.mainloop()
