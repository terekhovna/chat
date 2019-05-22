from tkinter import *
from tkinter import messagebox
from wforms import Form, new_chat, browse_chat
from sapi import get_chats, delete_chat


class ChatRooms(Form):
    def __getattr__(self, item):
        if item in ('password', 'username', 'check_connection', 'site'):
            return getattr(self.index_form, item)
        raise KeyError

    def refresh(self):
        if not self.check_connection():
            return
        channels = get_chats(self.site, self.username, self.password)
        self.chat_listbox.delete(0, END)
        self.chat_list = []
        for n, chn in channels:
            self.chat_listbox.insert(END, chn)
            self.chat_list.append(n)

    def delete_chat(self, num):
        if not self.check_connection():
            return False
        if delete_chat(self.site, self.username, self.password, num):
            return True
        messagebox.showerror('delete chat', "i can't delete this chat")
        return False

    def click_back(self):
        self.switch(self.index_form)

    def click_new_chat(self):
        self.switch(self.new_chat_form)

    def click_browse_chat(self):
        chat = self.chat_listbox.curselection()
        if not chat:
            messagebox.showerror('browse chat', 'Please select one of chats from ListBox')
            return
        self.browse_chat_form.chat_id = self.chat_list[chat[0]]
        self.switch(self.browse_chat_form)

    def click_delete_chat(self):
        chat = self.chat_listbox.curselection()
        if not chat:
            messagebox.showerror('delete chat', 'Please select one of chats from ListBox')
            return
        if self.delete_chat(self.chat_list[chat[0]]):
            self.refresh()

    def __init__(self, master, index_form):
        self.index_form = index_form
        self.new_chat_form = new_chat.NewChat(master, self)
        self.browse_chat_form = browse_chat.BrowseChat(master, self)
        self.chat_list = []

        self.frame1 = Frame(master)
        self.back_button = Button(self.frame1, text='back', command=lambda: self.click_back())
        self.chat_listbox = Listbox(self.frame1)
        self.chat_list_scrollbar = Scrollbar(self.frame1, command=self.chat_listbox.yview)
        self.chat_listbox.config(yscrollcommand=self.chat_list_scrollbar.set)

        self.frame2 = Frame(master)
        self.refresh_button = Button(self.frame2, text='refresh', command=lambda: self.refresh())
        self.new_chat_button = Button(self.frame2, text='new chat', command=lambda: self.click_new_chat())
        self.browse_chat_button = Button(self.frame2, text='browse chat', command=lambda: self.click_browse_chat())
        self.delete_chat_button = Button(self.frame2, text='delete chat', command=lambda: self.click_delete_chat())

        self.obj = [self.frame1, self.frame2]

    def activate(self):
        self.frame1.pack(side=LEFT)
        self.back_button.pack(side=TOP)
        self.chat_listbox.pack(side=LEFT)
        self.chat_list_scrollbar.pack(side=LEFT, fill=Y)

        self.frame2.pack()
        self.refresh_button.pack(side=TOP)
        self.new_chat_button.pack(side=TOP)
        self.browse_chat_button.pack(side=TOP)
        self.delete_chat_button.pack(side=TOP)

        self.refresh()
