from wforms.ChooseSite import ChooseSite
from tkinter import Tk, Frame, LEFT, RIGHT, TOP, BOTTOM

twosides = False

width = 500
if twosides:
    width *= 2
height = 500
root = Tk()
root.title('Chat client')
w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w // 2 - width // 2
h = h // 2 - height // 2
root.geometry(f'{width}x{height}+{w}+{h}')


if twosides:
    f = Frame(root)
    f2 = Frame(root)
    f.pack(side=LEFT, expand=True)
    f2.pack(side=RIGHT, expand=True)

    c = ChooseSite(f)
    c2 = ChooseSite(f2)
    c.activate()
    c2.activate()
else:
    f = Frame(root)
    f.pack(expand=True)
    c = ChooseSite(f)
    c.activate()

root.mainloop()
