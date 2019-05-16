from tkinter import *
from tkinter import messagebox
from wforms import Form
from sapi import create_chat, get_friends


class NewChat(Form):
    def __getattr__(self, item):
        if item in ('password', 'username', 'check_connection', 'site'):
            return getattr(self.channels_form, item)
        raise KeyError

    def create_chat(self, title, friends):
        if not self.check_connection():
            return False
        if create_chat(self.site, self.username, self.password, title, friends):
            return True
        messagebox.showerror('create chat', "i can't create chat")
        return False

    def click_back(self):
        self.switch(self.channels_form)

    def click_create_chat(self):
        title = self.title_entry.get()
        if title == '':
            messagebox.showerror('create chat', 'Please type title')
            return
        friends = list(map(lambda x: self.friends_in_chat_listbox.get(x), range(self.friends_in_chat_listbox.size())))
        if self.create_chat(title, friends):
            self.switch(self.channels_form)

    def click_add(self):
        friends = list(map(lambda x: self.friends_listbox.get(x), self.friends_listbox.curselection()))
        for f in friends:
            self.chosen_friends.add(f)
        self.refresh()

    def click_remove(self):
        friends = list(map(lambda x: self.friends_in_chat_listbox.get(x), self.friends_in_chat_listbox.curselection()))
        for f in friends:
            self.chosen_friends.remove(f)
        self.refresh()

    def __init__(self, master, channels_form):
        self.channels_form = channels_form

        self.top_frame = Frame(master)
        self.back_button = Button(self.top_frame, text='back', command=lambda: self.click_back())

        self.mid_frame = Frame(master)
        self.title_label = Label(self.mid_frame, text='title')
        self.title_entry = Entry(self.mid_frame)
        self.create_chat_button = Button(self.mid_frame, text='create chat', command=lambda: self.click_create_chat())

        self.bottom_frame = Frame(master)

        self.left_frame = Frame(self.bottom_frame)
        self.friends_listbox = Listbox(self.left_frame, selectmode=EXTENDED)
        self.friends_listbox_label = Label(self.left_frame, text='your friends')
        self.friends_list_scrollbar = Scrollbar(self.left_frame, command=self.friends_listbox.yview)
        self.friends_listbox.config(yscrollcommand=self.friends_list_scrollbar.set)

        self.frame_add = Frame(self.bottom_frame)
        self.add_to_chat_button = Button(self.frame_add, text='>>', command=lambda: self.click_add())
        self.remove_from_chat_button = Button(self.frame_add, text='<<', command=lambda: self.click_remove())

        self.right_frame = Frame(self.bottom_frame)
        self.friends_in_chat_listbox = Listbox(self.right_frame, selectmode=EXTENDED)
        self.friends_in_chat_listbox_label = Label(self.right_frame, text='friends to chat')
        self.friends_in_chat_list_scrollbar = Scrollbar(self.right_frame, command=self.friends_in_chat_listbox.yview)
        self.friends_in_chat_listbox.config(yscrollcommand=self.friends_in_chat_list_scrollbar.set)
        self.chosen_friends = set()

        self.obj = [self.top_frame, self.mid_frame, self.bottom_frame]

    def activate(self):
        self.top_frame.pack()
        self.back_button.pack(side=LEFT)

        self.mid_frame.pack()
        self.title_label.pack(side=LEFT)
        self.title_entry.pack(side=LEFT)
        self.create_chat_button.pack(side=LEFT)

        self.bottom_frame.pack()

        self.left_frame.pack(side=LEFT)
        self.friends_listbox_label.pack(side=TOP)
        self.friends_list_scrollbar.pack(side=LEFT)
        self.friends_listbox.pack(side=LEFT)

        self.frame_add.pack(side=LEFT)
        self.add_to_chat_button.pack()
        self.remove_from_chat_button.pack()

        self.right_frame.pack(side=LEFT)
        self.friends_in_chat_listbox_label.pack(side=TOP)
        self.friends_in_chat_listbox.pack(side=LEFT)
        self.friends_in_chat_list_scrollbar.pack(side=LEFT)

        self.clear()
        self.refresh()

    def clear(self):
        self.title_entry.delete(0, END)
        self.chosen_friends.clear()

    def refresh(self):
        if not self.check_connection():
            return
        friends = get_friends(self.site, self.username, self.password)
        self.friends_listbox.delete(0, END)
        for fr in friends:
            self.friends_listbox.insert(END, fr)

        self.friends_in_chat_listbox.delete(0, END)
        for fr in self.chosen_friends:
            self.friends_in_chat_listbox.insert(END, fr)
