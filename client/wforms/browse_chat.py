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
        self.message_history.config(state=NORMAL)
        self.message_history.delete(1.0, END)
        for aut, mes in messages:
            if aut == self.username:
                self.message_history.insert(END, aut + ':\n', 'me')
                self.message_history.insert(END, mes + '\n', 'me_text')
            else:
                self.message_history.insert(END, aut + ':\n', 'author')
                self.message_history.insert(END, mes + '\n', 'author_text')
        self.message_history.config(state=DISABLED)

    def send_message(self, text: str):
        if not self.check_connection():
            return False
        if post_message(self.site, self.username, self.password, self.chat_id, text):
            return True
        return False

    def click_back(self):
        self.switch(self.channels_form)

    def click_send(self):
        text = self.message_text.get(1.0, END)
        if text.isspace():
            messagebox.showerror('send message', 'Please type message')
            return
        if self.send_message(text):
            self.clear()
            self.refresh()

    def __init__(self, master, channels_form):
        self.channels_form = channels_form

        self.frame1 = Frame(master)
        self.back_button = Button(self.frame1, text='back', command=lambda: self.click_back())
        self.refresh_button = Button(self.frame1, text='refresh', command=lambda: self.refresh())

        self.frame2 = Frame(master)
        self.message_text = ScrolledText(self.frame2, height=5, width=25, wrap=WORD)
        self.b3 = Button(self.frame2, width=5, text='send', command=lambda: self.click_send())

        self.frame3 = Frame(master)
        self.message_history = ScrolledText(self.frame3, height=14, width=30, wrap=WORD, state=DISABLED)
        self.message_history.tag_config('author', foreground="blue", justify=LEFT)
        self.message_history.tag_config('author_text', justify=LEFT)
        self.message_history.tag_config('me', foreground="red", justify=RIGHT)
        self.message_history.tag_config('me_text', justify=RIGHT)

        self.obj = [self.frame1, self.frame2, self.frame3]

    def activate(self):
        self.frame1.pack()
        self.back_button.pack(side=LEFT)
        self.refresh_button.pack(side=LEFT)

        self.frame2.pack()
        self.message_text.pack(side=LEFT)
        self.b3.pack(side=LEFT)

        self.frame3.pack()
        self.message_history.pack(side=LEFT)

        self.clear()
        self.refresh()

    def clear(self):
        self.message_text.delete(1.0, END)
