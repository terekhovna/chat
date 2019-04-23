class Form:
    obj = []

    def activate(self):
        for b in self.obj:
            b.pack()

    def deactivate(self):
        for b in self.obj:
            b.pack_forget()

    def switch(self, form):
        self.deactivate()
        form.activate()
