from tkinter import *
from tkinter import messagebox
from sapi import check_login
from wforms import Form, register, index


class Login(Form):
    site = None

    def clear(self):
        self.login_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def set_user(self, username, password):
        self.clear()
        self.login_entry.insert(0, username)
        self.password_entry.insert(0, password)

    def click_login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()
        if check_login(self.site, username, password):
            self.index_form.username = username
            self.index_form.password = password
            self.index_form.site = self.site
            self.switch(self.index_form)
        else:
            messagebox.showerror('Error', 'failed login')

    def click_register(self):
        self.switch(self.register_form)

    def __init__(self, master):
        self.register_form = register.Register(master, self)
        self.index_form = index.Index(master, self)

        self.frame1 = Frame(master)
        self.login_label = Label(self.frame1, text='Login:')
        self.login_entry = Entry(self.frame1)

        self.frame2 = Frame(master)
        self.password_label = Label(self.frame2, text='Password:')
        self.password_entry = Entry(self.frame2)

        self.frame3 = Frame(master)
        self.login_button = Button(self.frame3, text='Login', command=lambda: self.click_login())
        self.register_button = Button(self.frame3, text='Or Register', command=lambda: self.click_register())

        self.set_user('admin', 'secret')

        self.obj = [self.frame1, self.frame2, self.frame3]

    def activate(self):
        self.frame1.pack()
        self.login_label.pack(side=LEFT)
        self.login_entry.pack(side=LEFT)

        self.frame2.pack()
        self.password_label.pack(side=LEFT)
        self.password_entry.pack(side=LEFT)

        self.frame3.pack()
        self.login_button.pack(side=LEFT)
        self.register_button.pack(side=LEFT)
