import tkinter as tk

class MorseMaster(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        textFrame = Text(container, text='HELLO!')
        textFrame.grid(row = 0, column = 0, sticky = "nw")
        textFrame.tkraise()

        textFrame2 = Text(container, text='GOODBYE!')
        textFrame2.grid(row = 1, column = 0, sticky = "nw")
        textFrame2.tkraise()

        self.menu_bar = MenuBar(self)
        self.config(menu = self.menu_bar.menubar)


class MenuBar:
    def __init__(self,app):
        self.menubar = tk.Menu(app)

        file = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = 'File', menu = file)
        file.add_command(label = 'Exit', command = app.destroy)

        options = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label='Options', menu = options)

        help_ = tk.Menu(self.menubar, tearoff = 0)
        self.menubar.add_cascade(label = 'Help', menu = help_)
        help_.add_command(label = 'MorseMaster Help', command = None)
        help_.add_command(label = 'About MorseMaster', command = None)


class NavigationBar:
    pass


class TextTranslator:
    pass


class SoundTranslator:
    pass


class Keyer:
    pass


class ChallengeMode:
    pass


class Networking:
    pass


class Text(tk.Frame):
    def __init__(self, parent, text = 'MorseMaster', fontSize = 12, fontType = 'Verdana', anchor = 'w'):
        self.fontSize = fontSize
        self.fontType = fontType
        self.text = text
        self.anchor = anchor
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = self.text, font = (self.fontType, self.fontSize), anchor = self.anchor)
        label.pack(pady = 10, padx = 10)


class Button():
    pass


class TextEntry():
    pass


class LightBox:
    pass


app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,300)
app.mainloop()