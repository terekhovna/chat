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
        self.e1.delete(0, END)
        self.lb.delete(0, END)
        for fr in friends:
            self.lb.insert(END, fr)

    def add_friend(self, friend_name: str):
        if not self.check_connection():
            return False
        if add_friend(self.site, self.username, self.password, friend_name):
            #messagebox.showinfo('add Friend', 'You are add Friend!')
            return True
        messagebox.showerror('add Friend', "i can't add this friend")
        return False

    def delete_friend(self, friend_name: str):
        if not self.check_connection():
            return False
        if delete_friend(self.site, self.username, self.password, friend_name):
            #messagebox.showinfo('delete Friend', 'You are delete Friend!')
            return True
        messagebox.showerror('delete Friend', "i can't delete this friend")
        return False

    def click_add_friend(self):
        friend_name = self.e1.get()
        if friend_name == '':
            messagebox.showerror('add Friend', 'Please type friend name')
            return
        if self.add_friend(friend_name):
            self.refresh()

    def click_delete_friend(self):
        friend_name = self.e1.get()
        if friend_name == '':
            messagebox.showerror('delete Friend', 'Please type friend name')
            return
        if self.delete_friend(friend_name):
            self.refresh()

    def click_back(self):
        self.switch(self.index_form)

    def __init__(self, master, index_form):
        self.index_form = index_form

        self.f1 = Frame(master)
        self.b1 = Button(self.f1, text='back', command=lambda: self.click_back())
        self.lb = Listbox(self.f1, selectmode=EXTENDED)
        self.sb = Scrollbar(self.f1, command=self.lb.yview)
        self.lb.config(yscrollcommand=self.sb.set)

        self.f2 = Frame(master)
        self.b2 = Button(self.f2, text='refresh', command=lambda: self.refresh())
        self.e1 = Entry(self.f2, width=20)
        self.b3 = Button(self.f2, text='add friend', command=lambda: self.click_add_friend())
        self.b4 = Button(self.f2, text='delete friend', command=lambda: self.click_delete_friend())

        self.obj = [self.f1, self.f2]

    def activate(self):
        self.f1.pack(side=LEFT)
        self.b1.pack(side=TOP)
        self.lb.pack(side=LEFT)
        self.sb.pack(side=LEFT, fill=Y)

        self.f2.pack()
        self.b2.pack(side=TOP)
        self.e1.pack(side=TOP)
        self.b3.pack(side=TOP)
        self.b4.pack(side=TOP)

        self.refresh()
