from tkinter import *
from tkinter import messagebox
from sapi import register
from wforms import Form


class Register(Form):
    def click_register(self):
        username = self.e1.get()
        password = self.e2.get()
        password2 = self.e3.get()
        if password != password2:
            messagebox.showerror('Error', "Passwords don't match!")
            self.e3.delete(0, END)
        elif register(self.login_from.site, username, password):
            messagebox.showinfo('Register', 'register success')
            self.login_from.set_user(username, password)
            self.switch(self.login_from)
        else:
            messagebox.showerror('Error', "Can't register on server")

    def click_back(self):
        self.switch(self.login_from)

    def activate(self):
        self.f1.pack()
        self.l1.pack(side=LEFT)
        self.e1.pack(side=LEFT)

        self.f2.pack()
        self.l2.pack(side=LEFT)
        self.e2.pack(side=LEFT)

        self.f3.pack()
        self.l3.pack(side=LEFT)
        self.e3.pack(side=LEFT)

        self.f4.pack()
        self.bb.pack(side=LEFT)
        self.br.pack(side=LEFT)

        self.clear()

    def __init__(self, master, login_from):
        self.login_from = login_from

        self.f1 = Frame(master)
        self.l1 = Label(self.f1, text='Login:')
        self.e1 = Entry(self.f1)

        self.f2 = Frame(master)
        self.l2 = Label(self.f2, text='Password:')
        self.e2 = Entry(self.f2)

        self.f3 = Frame(master)
        self.l3 = Label(self.f3, text='Repeat Password:')
        self.e3 = Entry(self.f3)

        self.f4 = Frame(master)
        self.bb = Button(self.f4, text='Back', command=lambda: self.click_back())
        self.br = Button(self.f4, text='Register', command=lambda: self.click_register())

        self.obj = [self.f1, self.f2, self.f3, self.f4]

    def clear(self):
        self.e1.delete(0, END)
        self.e2.delete(0, END)
        self.e3.delete(0, END)
