#! /usr/bin/python3
from wforms.choose_site import ChooseSite
from tkinter import Tk, Frame, LEFT, RIGHT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--two_sides', dest='t', action="store_true")
args = parser.parse_args()

two_sides = args.t

width = 500
if two_sides:
    width *= 2
height = 500

root = Tk()
root.title('Chat client')
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - width // 2
h = h // 2 - height // 2
root.geometry(f'{width}x{height}+{w}+{h}')

if two_sides:
    frame = Frame(root)
    frame2 = Frame(root)
    frame.pack(side=LEFT, expand=True)
    frame2.pack(side=RIGHT, expand=True)

    c = ChooseSite(frame)
    c2 = ChooseSite(frame2)
    c.activate()
    c2.activate()
else:
    frame = Frame(root)
    frame.pack(expand=True)
    c = ChooseSite(frame)
    c.activate()

root.mainloop()
