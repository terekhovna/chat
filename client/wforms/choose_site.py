from tkinter import *
from tkinter import messagebox
from sapi import check_connection
from wforms import login, Form


class ChooseSite(Form):
    def connect(self):
        site = self.url_entry.get().rstrip('/')
        if check_connection(site):
            self.login_form.site = site
            self.switch(self.login_form)
        else:
            messagebox.showerror('Error', 'failed connect')

    def __init__(self, master):
        self.login_form = login.Login(master)

        self.frame1 = Frame(master)
        self.url_label = Label(self.frame1, text='Input URL of chat:')
        self.url_entry = Entry(self.frame1, width=50)

        self.frame2 = Frame(master)
        self.connect_button = Button(self.frame2, text='Connect', command=lambda: self.connect())

        self.obj = [self.frame1, self.frame2]

    def activate(self):
        self.frame1.pack()
        self.url_label.pack(side=LEFT)
        self.url_entry.pack(side=LEFT)

        self.frame2.pack()
        self.connect_button.pack()

        self.clear()

    def clear(self):
        self.url_entry.delete(0, END)
        self.url_entry.insert(0, 'http://localhost:50000/')
