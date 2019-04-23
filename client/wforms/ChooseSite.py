from tkinter import *
from tkinter import messagebox
from sapi import check_connection
from wforms import Login, Form


class ChooseSite(Form):
    def click(self):
        site = self.e.get().rstrip('/')
        if check_connection(site):
            self.login_form.site = site
            self.switch(self.login_form)
        else:
            messagebox.showerror('Error', 'failed connect')

    def activate(self):
        self.f1.pack()
        self.l.pack(side=LEFT)
        self.e.pack(side=LEFT)

        self.f2.pack()
        self.b.pack()

        self.clear()

    def __init__(self, master):
        self.login_form = Login.Login(master)

        self.f1 = Frame(master)
        self.l = Label(self.f1, text='Input URL of chat:')
        self.e = Entry(self.f1, width=50)

        self.f2 = Frame(master)
        self.b = Button(self.f2, text='Connect', command=lambda: self.click())

        self.obj = [self.f1, self.f2]

    def clear(self):
        self.e.delete(0, END)
        self.e.insert(0, 'http://localhost:50000/')
