import tkinter as tk
from tkinter.scrolledtext import ScrolledText
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
        
        self.populateTextTranslatorTab()
        self.populateSoundTranslatorTab()
        self.populateKeyerTab()
        self.populateChallengeModeTab()
        self.populateNetworkingTab()

    def populateTextTranslatorTab(self):
        inputTextLabel = TextLabel(self.textTranslatorTab, text = 'Input English Plaintext:')
        inputTextLabel.grid(row = 0, column = 0, sticky = 'nw')
        inputTextLabel.tkraise()

        inputTextArea = TextEntry(self.textTranslatorTab)
        inputTextArea.grid(row = 1, column = 0, sticky = 'nw')
        inputTextArea.tkraise()

        outputTextLabel = TextLabel(self.textTranslatorTab, text = 'Output Morse Code Ciphertext:', pady = (20,0))
        outputTextLabel.grid(row = 2, column = 0, sticky = 'nw')
        outputTextLabel.tkraise()

        outputTextArea = TextEntry(self.textTranslatorTab)
        outputTextArea.grid(row = 3, column = 0, sticky = 'nw')
        outputTextArea.tkraise()

        copyButton = ButtonIcon(self.textTranslatorTab, filename = 'iconAssets/copy.png')
        copyButton.grid(row = 3, column = 1, sticky = 'nw')
        copyButton.tkraise()

    def populateSoundTranslatorTab(self):
        pass

    def populateKeyerTab(self):
        pass

    def populateChallengeModeTab(self):
        pass

    def populateNetworkingTab(self):
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


class TextLabel(tk.Frame):
    def __init__(self, parent, text = 'MorseMaster', fontSize = 10, fontType = 'Verdana', anchor = 'w', pady = 5, padx = 10):
        self.fontSize = fontSize
        self.fontType = fontType
        self.text = text
        self.anchor = anchor
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = self.text, font = (self.fontType, self.fontSize), anchor = self.anchor)
        label.pack(pady = self.pady, padx = self.padx)


class ButtonText():
    pass

class ButtonIcon(tk.Frame):
    def __init__(self, parent, command = None, filename = '', iconSize = (1,1), pady = 0, padx = 0):
        self.command = command
        self.filename = filename
        self.iconSize = iconSize
        self.pady = pady
        self.padx = padx
        icon = tk.PhotoImage(file = (self.filename)).subsample(self.iconSize[0])
        tk.Frame.__init__(self, parent)
        button = tk.Button(self, image = icon, command = self.command)
        button.image = icon
        button.pack(pady = self.pady, padx = self.padx)


class TextEntry(tk.Frame):
    def __init__(self, parent, fontSize = 10, fontType = 'Verdana', width = 40, height = 5, pady = 0, padx = 10):
        self.fontSize = fontSize
        self.fontType = fontType
        self.width = width
        self.height = height
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        textBox = ScrolledText(self, font = (self.fontType, self.fontSize), width = self.width, height = self.height)
        textBox.pack(pady = self.pady, padx = self.padx, fill='y')


class LightBox:
    pass


app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,300)
app.mainloop()