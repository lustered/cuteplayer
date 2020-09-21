from utils.interface import *

if __name__ == "__main__":
    ROOT = Tk()
    ROOT.attributes('-topmost', True)
    APP = Cuteplayer(master=ROOT)
    APP.mainloop()
