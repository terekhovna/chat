from tkinter import *
from tkinter import messagebox
from sapi import check_login
from wforms import Form, Register, Index


class Login(Form):
    site = None

    def click_login(self):
        username = self.e1.get()
        password = self.e2.get()
        if check_login(self.site, username, password):
            self.index_form.username = username
            self.index_form.password = password
            self.index_form.site = self.site
            #messagebox.showinfo('Login', 'login success')
            self.switch(self.index_form)
        else:
            messagebox.showerror('Error', 'failed login')

    def click_register(self):
        self.switch(self.register_form)

    def activate(self):
        self.f1.pack()
        self.l1.pack(side=LEFT)
        self.e1.pack(side=LEFT)

        self.f2.pack()
        self.l2.pack(side=LEFT)
        self.e2.pack(side=LEFT)

        self.f3.pack()
        self.bl.pack(side=LEFT)
        self.br.pack(side=LEFT)

    def __init__(self, master):
        self.register_form = Register.Register(master, self)
        self.index_form = Index.Index(master, self)

        self.f1 = Frame(master)
        self.l1 = Label(self.f1, text='Login:')
        self.e1 = Entry(self.f1)

        self.f2 = Frame(master)
        self.l2 = Label(self.f2, text='Password:')
        self.e2 = Entry(self.f2)

        self.f3 = Frame(master)
        self.bl = Button(self.f3, text='Login', command=lambda: self.click_login())
        self.br = Button(self.f3, text='Or Register', command=lambda: self.click_register())

        self.obj = [self.f1, self.f2, self.f3]
        self.set_user('admin', 'secret')

    def clear(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)

    def set_user(self, username, password):
        self.clear()
        self.e1.insert(0, username)
        self.e2.insert(0, password)
