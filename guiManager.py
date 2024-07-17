import tkinter as tk
import textValidator, textParser

class MorseMaster(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = Title(container, self)
        self.frames[Title] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Title)

        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar.menubar)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MenuBar:
    def __init__(self,app):
        self.menubar = tk.Menu(app)

        file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=file)
        file.add_command(label='Exit', command=app.destroy)

        options = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Options', menu=options)

        help_ = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=help_)
        help_.add_command(label='MorseMaster Help', command=None)
        help_.add_command(label='About MorseMaster', command=None)

class Title(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="MorseMaster", font=("Verdana", 36))
        label.pack(pady=10,padx=10)

app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.mainloop()