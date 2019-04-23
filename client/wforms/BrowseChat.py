from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from wforms import Form
from sapi import get_messages, post_message


class BrowseChat(Form):
    chat_id = None

    def __getattr__(self, item):
        if item in ('password', 'username', 'check_connection', 'site'):
            return getattr(self.channels_form, item)
        raise KeyError

    def refresh(self):
        if not self.check_connection():
            return
        messages = get_messages(self.site, self.username, self.password, self.chat_id)
        self.tt.config(state=NORMAL)
        self.tt.delete(1.0, END)
        for aut, mes in messages:
            if aut == self.username:
                self.tt.insert(END, aut + ':\n', 'me')
                self.tt.insert(END, mes + '\n', 'me_text')
            else:
                self.tt.insert(END, aut + ':\n', 'author')
                self.tt.insert(END, mes + '\n', 'author_text')
        self.tt.config(state=DISABLED)

    def send_message(self, text: str):
        if not self.check_connection():
            return False
        if post_message(self.site, self.username, self.password, self.chat_id, text):
            return True
        return False

    def click_back(self):
        self.switch(self.channels_form)

    def click_send(self):
        text = self.tm.get(1.0, END)
        if text.isspace():
            messagebox.showerror('send message', 'Please type message')
            return
        if self.send_message(text):
            self.clear()
            self.refresh()

    def __init__(self, master, channels_form):
        self.channels_form = channels_form

        self.f1 = Frame(master)
        self.b1 = Button(self.f1, text='back', command=lambda: self.click_back())
        self.b2 = Button(self.f1, text='refresh', command=lambda: self.refresh())

        self.f2 = Frame(master)
        self.tm = ScrolledText(self.f2, height=5, width=25, wrap=WORD)
        self.b3 = Button(self.f2, width=5, text='send', command=lambda: self.click_send())

        self.f3 = Frame(master)
        self.tt = ScrolledText(self.f3, height=14, width=30, wrap=WORD, state=DISABLED)
        self.tt.tag_config('author', foreground="blue", justify=LEFT)
        self.tt.tag_config('author_text', justify=LEFT)
        self.tt.tag_config('me', foreground="red", justify=RIGHT)
        self.tt.tag_config('me_text', justify=RIGHT)

        self.obj = [self.f1, self.f2, self.f3]

    def activate(self):
        self.f1.pack()
        self.b1.pack(side=LEFT)
        self.b2.pack(side=LEFT)

        self.f2.pack()
        self.tm.pack(side=LEFT)
        self.b3.pack(side=LEFT)

        self.f3.pack()
        self.tt.pack(side=LEFT)

        self.clear()
        self.refresh()

    def clear(self):
        self.tm.delete(1.0, END)

