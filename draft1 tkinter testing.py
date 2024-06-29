#MorseMaster
#Draft 1

import math, random, winsound, threading
import tkinter as tk
import numpy as np
import pynput as pn
import socket as sk
import wavio as wv
import pyaudio as au

class MorseMaster(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = Title(container, self)

        self.frames[Title] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Title)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        
class Title(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="MorseMaster", font=("Verdana", 36))
        label.pack(pady=10,padx=10)


app = MorseMaster()
app.mainloop()