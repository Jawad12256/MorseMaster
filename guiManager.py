import tkinter as tk
from tkinter import ttk

class MorseMaster(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        s = ttk.Style()
        s.configure('TNotebook.Tab', font = ('Verdana',10), padding = [10, 2])

        self.tabBar = TabBar(self)
        self.tabBar.pack(side='top', fill='both', expand=True)

        self.menuBar = MenuBar(self)
        self.config(menu = self.menuBar.menubar)


class MenuBar:
    def __init__(self, app):
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


class TabBar(ttk.Notebook):
    def __init__(self, app):
        super().__init__(app)
        
        self.textTranslatorTab = tk.ttk.Frame(self)
        self.soundTranslatorTab = tk.ttk.Frame(self)
        self.keyerTab = tk.ttk.Frame(self)
        self.challengeModeTab = tk.ttk.Frame(self)
        self.networkingTab = tk.ttk.Frame(self)
        
        self.add(self.textTranslatorTab, text='Text Translator')
        self.add(self.soundTranslatorTab, text='Sound Translator')
        self.add(self.keyerTab, text='Keyer')
        self.add(self.challengeModeTab, text='Challenge Mode')
        self.add(self.networkingTab, text='Networking')
        
        self.populate_tabs()

    def populate_tabs(self):
        textFrame = Text(self.textTranslatorTab, text = 'HELLO!')
        textFrame.grid(row = 0, column = 0, sticky = 'nw')
        textFrame.tkraise()

        textFrame2 = Text(self.textTranslatorTab, text = 'GOODBYE!')
        textFrame2.grid(row = 1, column = 0, sticky = 'nw')
        textFrame2.tkraise()


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