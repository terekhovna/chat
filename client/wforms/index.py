from tkinter import *
from tkinter import messagebox
from wforms import Form, friends, chat_rooms
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
        self.login_form.clear()
        self.switch(self.login_form)

    def click_chat_rooms(self):
        if not self.check_connection():
            return
        self.switch(self.channels_form)

    def click_view_friends(self):
        if not self.check_connection():
            return
        self.switch(self.friends_form)

    def __init__(self, master, login_form):
        self.login_form = login_form
        self.friends_form = friends.Friends(master, self)
        self.channels_form = chat_rooms.ChatRooms(master, self)

        self.frame1 = Frame(master)
        self.logout_button = Button(self.frame1, text='logout', command=lambda: self.click_logout())

        self.frame2 = Frame(master)
        self.view_chat_rooms_button = Button(self.frame2, text='chat rooms', command=lambda: self.click_chat_rooms())
        self.view_friends_button = Button(self.frame2, text='friends', command=lambda: self.click_view_friends())

        self.obj = [self.frame1, self.frame2]

    def activate(self):
        self.frame1.pack()
        self.logout_button.pack(side=LEFT)

        self.frame2.pack()
        self.view_chat_rooms_button.pack(side=LEFT)
        self.view_friends_button.pack(side=LEFT)
