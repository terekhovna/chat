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
            #messagebox.showinfo('create chat, 'You are create chat')
            return True
        messagebox.showerror('create chat', "i can't create chat")
        return False

    def click_back(self):
        self.switch(self.channels_form)

    def click_create_chat(self):
        title = self.e1.get()
        if title == '':
            messagebox.showerror('create chat', 'Please type title')
            return
        friends = list(map(lambda x: self.lb2.get(x), range(self.lb2.size())))
        if self.create_chat(title, friends):
            self.switch(self.channels_form)

    def click_add(self):
        friends = list(map(lambda x: self.lb1.get(x), self.lb1.curselection()))
        for f in friends:
            self.s.add(f)
        self.refresh()

    def click_remove(self):
        friends = list(map(lambda x: self.lb2.get(x), self.lb2.curselection()))
        for f in friends:
            self.s.remove(f)
        self.refresh()

    def __init__(self, master, channels_form):
        self.channels_form = channels_form

        self.f1 = Frame(master)
        self.b1 = Button(self.f1, text='back', command=lambda: self.click_back())

        self.f2 = Frame(master)
        self.l1 = Label(self.f2, text='title')
        self.e1 = Entry(self.f2)
        self.b2 = Button(self.f2, text='create chat', command=lambda: self.click_create_chat())

        self.f3 = Frame(master)

        self.f3_1 = Frame(self.f3)
        self.l2 = Label(self.f3_1, text='your friends')
        self.lb1 = Listbox(self.f3_1, selectmode=EXTENDED)
        self.sb1 = Scrollbar(self.f3_1, command=self.lb1.yview)
        self.lb1.config(yscrollcommand=self.sb1.set)

        self.f3_2 = Frame(self.f3)
        self.b3 = Button(self.f3_2, text='>>', command=lambda: self.click_add())
        self.b4 = Button(self.f3_2, text='<<', command=lambda: self.click_remove())

        self.f3_3 = Frame(self.f3)
        self.s = set()
        self.l3 = Label(self.f3_3, text='friends to chat')
        self.lb2 = Listbox(self.f3_3, selectmode=EXTENDED)
        self.sb2 = Scrollbar(self.f3_3, command=self.lb2.yview)
        self.lb2.config(yscrollcommand=self.sb2.set)

        self.obj = [self.f1, self.f2, self.f3]

    def activate(self):
        self.f1.pack()
        self.b1.pack(side=LEFT)

        self.f2.pack()
        self.l1.pack(side=LEFT)
        self.e1.pack(side=LEFT)
        self.b2.pack(side=LEFT)

        self.f3.pack()

        self.f3_1.pack(side=LEFT)
        self.l2.pack(side=TOP)
        self.sb1.pack(side=LEFT)
        self.lb1.pack(side=LEFT)

        self.f3_2.pack(side=LEFT)
        self.b3.pack()
        self.b4.pack()

        self.f3_3.pack(side=LEFT)
        self.l3.pack(side=TOP)
        self.lb2.pack(side=LEFT)
        self.sb2.pack(side=LEFT)

        self.clear()
        self.refresh()

    def clear(self):
        self.e1.delete(0, END)
        self.s.clear()

    def refresh(self):
        if not self.check_connection():
            return
        friends = get_friends(self.site, self.username, self.password)
        self.lb1.delete(0, END)
        for fr in friends:
            self.lb1.insert(END, fr)

        self.lb2.delete(0, END)
        for fr in self.s:
            self.lb2.insert(END, fr)
