from tkinter import *
from tkinter import messagebox
from wforms import Form
from sapi import get_friends, delete_friend, add_friend


class Friends(Form):
    def __getattr__(self, item):
        if item in ('password', 'username', 'check_connection', 'site'):
            return getattr(self.index_form, item)
        raise KeyError

    def refresh(self):
        if not self.check_connection():
            return
        friends = get_friends(self.site, self.username, self.password)
        self.name_entry.delete(0, END)
        self.friend_listbox.delete(0, END)
        for fr in friends:
            self.friend_listbox.insert(END, fr)

    def add_friend(self, friend_name: str):
        if not self.check_connection():
            return False
        if add_friend(self.site, self.username, self.password, friend_name):
            return True
        messagebox.showerror('add Friend', "i can't add this friend")
        return False

    def delete_friend(self, friend_name: str):
        if not self.check_connection():
            return False
        if delete_friend(self.site, self.username, self.password, friend_name):
            return True
        messagebox.showerror('delete Friend', "i can't delete this friend")
        return False

    def click_add_friend(self):
        name = self.name_entry.get()
        if name == '':
            messagebox.showerror('add Friend', 'Please type friend name')
            return
        if self.add_friend(name):
            self.refresh()

    def click_delete_friend(self):
        name = self.name_entry.get()
        if name == '':
            messagebox.showerror('delete Friend', 'Please type friend name')
            return
        if self.delete_friend(name):
            self.refresh()

    def click_back(self):
        self.switch(self.index_form)

    def __init__(self, master, index_form):
        self.index_form = index_form

        self.frame1 = Frame(master)
        self.back_button = Button(self.frame1, text='back', command=lambda: self.click_back())
        self.friend_listbox = Listbox(self.frame1, selectmode=EXTENDED)
        self.friend_list_scrollbar = Scrollbar(self.frame1, command=self.friend_listbox.yview)
        self.friend_listbox.config(yscrollcommand=self.friend_list_scrollbar.set)

        self.frame2 = Frame(master)
        self.refresh_button = Button(self.frame2, text='refresh', command=lambda: self.refresh())
        self.name_entry = Entry(self.frame2, width=20)
        self.add_friend_button = Button(self.frame2, text='add friend', command=lambda: self.click_add_friend())
        self.delete_friend_button = Button(self.frame2, text='delete friend', command=lambda: self.click_delete_friend())

        self.obj = [self.frame1, self.frame2]

    def activate(self):
        self.frame1.pack(side=LEFT)
        self.back_button.pack(side=TOP)
        self.friend_listbox.pack(side=LEFT)
        self.friend_list_scrollbar.pack(side=LEFT, fill=Y)

        self.frame2.pack()
        self.refresh_button.pack(side=TOP)
        self.name_entry.pack(side=TOP)
        self.add_friend_button.pack(side=TOP)
        self.delete_friend_button.pack(side=TOP)

        self.refresh()
