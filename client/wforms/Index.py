from tkinter import *
from tkinter import messagebox
from wforms import Form, Friends, Chats
from sapi import check_login


class Index(Form):
    username = None
    password = None
    site = None

    def check_connection(self):
        if check_login(self.site, self.username, self.password):
            return True
        else:
            messagebox.showerror('Connection Failed', "Can't get info from site!")
            return False

    def click_logout(self):
        #messagebox.showinfo('Logout', 'You are logout')
        self.login_form.clear()
        self.switch(self.login_form)

    def click_channels(self):
        if not self.check_connection():
            return
        self.switch(self.channels_form)

    def click_friends(self):
        if not self.check_connection():
            return
        self.switch(self.friends_form)

    def activate(self):
        self.f1.pack()
        self.b1.pack(side=LEFT)

        self.f2.pack()
        self.b2.pack(side=LEFT)
        self.b3.pack(side=LEFT)

    def __init__(self, master, login_form):
        self.login_form = login_form
        self.friends_form = Friends.Friends(master, self)
        self.channels_form = Chats.Channels(master, self)

        self.f1 = Frame(master)
        self.b1 = Button(self.f1, text='logout', command=lambda: self.click_logout())

        self.f2 = Frame(master)
        self.b2 = Button(self.f2, text='channels', command=lambda: self.click_channels())
        self.b3 = Button(self.f2, text='friends', command=lambda: self.click_friends())

        self.obj = [self.f1, self.f2]

