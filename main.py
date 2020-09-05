from pypresence import Presence
import tkinter as tk
import diskcache
import asyncio
import time

cache = diskcache.Cache('tmp')


class Application(tk.Frame):
    def __init__(self, master=tk.Tk()):
        super().__init__(master)
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.rpc = Presence(CLIENT_ID, pipe=0)

        self.rpc.connect()
        self.detail, self.state = "Custom Presence", "Launching!"

        self.initial()
        self.pack()
        self.loop_rpc()

    def initial(self):
        tk.Label(self, text="State: ").grid(row=1)
        self.states = tk.Entry(self)
        tk.Label(self, text="Details: ").grid(row=2)
        self.details = tk.Entry(self)

        self.update_ = tk.Button(self, text="Update Presence", command=self.update_)

        self.states.grid(row=1, column=1)
        self.details.grid(row=2, column=1)
        self.update_.grid(row=3, column=2)

    def loop_rpc(self):
        self.rpc.update(details=self.detail, state=self.state, large_image="futabalargeimagekey")
        self.master.after(10, self.loop_rpc)

    def update_(self):
        try:
            self.error.pack_forget()
            self.correct.pack_forget()
        except: pass

        if not self.details.get() or not self.states.get():
            self.error = tk.Label(text="Details and States cannot be empty!")
            return

        self.detail, self.state = self.details.get(), self.states.get()

    def on_exit(self):
        self.rpc.close()
        self.master.destroy()


app = Application()
app.mainloop()