from tkinter import *
from tkinter import messagebox
from wforms import Form, NewChat, BrowseChat
from sapi import get_chats, delete_chat


class Channels(Form):
    def __getattr__(self, item):
        if item in ('password', 'username', 'check_connection', 'site'):
            return getattr(self.index_form, item)
        raise KeyError

    def refresh(self):
        if not self.check_connection():
            return
        channels = get_chats(self.site, self.username, self.password)
        self.lb.delete(0, END)
        self.li = []
        for n, chn in channels:
            self.lb.insert(END, chn)
            self.li.append(n)

    def delete_chat(self, num):
        if not self.check_connection():
            return False
        if delete_chat(self.site, self.username, self.password, num):
            messagebox.showinfo('delete chat', 'You are delete chat!')
            return True
        messagebox.showerror('delete chat', "i can't delete this chat")
        return False

    def click_back(self):
        self.switch(self.index_form)

    def click_new_chat(self):
        self.switch(self.new_chat_form)

    def click_browse_chat(self):
        chat = self.lb.curselection()
        if not chat:
            messagebox.showerror('browse chat', 'Please select one of chats from ListBox')
            return
        self.browse_chat_form.chat_id = self.li[chat[0]]
        self.switch(self.browse_chat_form)

    def click_delete_chat(self):
        chat = self.lb.curselection()
        if not chat:
            messagebox.showerror('delete chat', 'Please select one of chats from ListBox')
            return
        if self.delete_chat(self.li[chat[0]]):
            self.refresh()

    def __init__(self, master, index_form):
        self.index_form = index_form
        self.new_chat_form = NewChat.NewChat(master, self)
        self.browse_chat_form = BrowseChat.BrowseChat(master, self)
        self.li = []

        self.f1 = Frame(master)
        self.b1 = Button(self.f1, text='back', command=lambda: self.click_back())
        self.lb = Listbox(self.f1)
        self.sb = Scrollbar(self.f1, command=self.lb.yview)
        self.lb.config(yscrollcommand=self.sb.set)

        self.f2 = Frame(master)
        self.b2 = Button(self.f2, text='refresh', command=lambda: self.refresh())
        self.b3 = Button(self.f2, text='new chat', command=lambda: self.click_new_chat())
        self.b4 = Button(self.f2, text='browse chat', command=lambda: self.click_browse_chat())
        self.b5 = Button(self.f2, text='delete chat', command=lambda: self.click_delete_chat())

        self.obj = [self.f1, self.f2]

    def activate(self):
        self.f1.pack(side=LEFT)
        self.b1.pack(side=TOP)
        self.lb.pack(side=LEFT)
        self.sb.pack(side=LEFT, fill=Y)

        self.f2.pack()
        self.b2.pack(side=TOP)
        self.b3.pack(side=TOP)
        self.b4.pack(side=TOP)
        self.b5.pack(side=TOP)

        self.refresh()
