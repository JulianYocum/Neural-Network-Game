#!/usr/bin/env python

from preprocessor import process
from collector import capture
from interface import Interface
from PIL import Image, ImageTk
import Tkinter
from subprocess import check_output, call
import glob
import os


def main():

    # open interface
    gui_interface()

    # remove images in img_stream
    for im in glob.glob("../data/img_stream/*.jpg"):
        os.remove(im)

    # poweroff screen
    call(['adb','shell','input','keyevent = POWER'])


def gui_interface():

    image_size = 275
    num_of_tries = 0

    root = Tkinter.Tk()
    my_gui = Interface(root)

    root.mainloop()


if __name__ == "__main__":
    main()
