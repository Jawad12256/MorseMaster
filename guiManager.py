'''GUI MANAGER'''
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Scale, Combobox
from tkinter import ttk

class MorseMaster(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        s = ttk.Style()
        s.configure('TNotebook.Tab', font = ('Verdana',10), padding = [10, 2])

        self.tabBar = TabBar(self)
        self.tabBar.pack(side='top', fill='both', expand=True)
        self.grid_columnconfigure(1, weight=1)

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
        self.soundGeneratorTab = tk.ttk.Frame(self)
        self.soundDecoderTab = tk.ttk.Frame(self)
        self.keyerTab = tk.ttk.Frame(self)
        self.challengeModeTab = tk.ttk.Frame(self)
        self.networkingTab = tk.ttk.Frame(self)
        
        self.add(self.textTranslatorTab, text='Text Translator')
        self.add(self.soundGeneratorTab, text='Sound Generator')
        self.add(self.soundDecoderTab, text = 'Sound Decoder')
        self.add(self.keyerTab, text='Keyer')
        self.add(self.challengeModeTab, text='Challenge Mode')
        self.add(self.networkingTab, text='Networking')
        
        self.populateTextTranslatorTab()
        self.populateSoundGeneratorTab()
        self.populateSoundDecoderTab()
        self.populateKeyerTab()
        self.populateChallengeModeTab()
        self.populateNetworkingTab()

    def populateTextTranslatorTab(self):
        translationDirectionLabel = TextLabelDynamic(self.textTranslatorTab, Name = 'translationDirectionLabel', anchor = 'e', pady = (5,10))
        translationDirectionLabel.grid(row = 0, column = 0)
        translationDirectionLabel.setText('English Plaintext -----> Morse Code Ciphertext')
        translationDirectionLabel.tkraise()

        translationDirectionButton = ButtonText(self.textTranslatorTab, Name = 'translationDirectionButton', text = 'Switch', command = None, pady = (3,10))
        translationDirectionButton.grid(row = 0, column = 1, sticky = 'nw')
        translationDirectionButton.tkraise()

        inputTextLabel = TextLabelDynamic(self.textTranslatorTab, Name ='inputTextLabel')
        inputTextLabel.grid(row = 1, column = 0, sticky = 'nw')
        inputTextLabel.setText('Input English Plaintext:')
        inputTextLabel.tkraise()

        uploadTextLabel = TextLabelStatic(self.textTranslatorTab, Name ='uploadTextLabel', text = 'Or upload a text file:', padx = (45,0))
        uploadTextLabel.grid(row = 1, column = 2, sticky = 's')
        uploadTextLabel.tkraise()

        uploadButton = ButtonIcon(self.textTranslatorTab, Name = 'uploadButton', filename = 'iconAssets/upload.png', command = None)
        uploadButton.grid(row = 2, column = 2, sticky = 'n', padx = (45,0))
        uploadButton.tkraise()

        inputTextArea = TextEntry(self.textTranslatorTab, Name = 'inputTextArea')
        inputTextArea.grid(row = 2, column = 0, sticky = 'nw')
        inputTextArea.tkraise()

        inputTextShortcutsFrame = tk.Frame(self.textTranslatorTab, width=30, height=85)
        inputTextShortcutsFrame.pack_propagate(False)
        inputTextShortcutsFrame.grid(row = 2, column = 1, sticky = 'nw')
        inputTextShortcutsFrame.tkraise()

        pasteButton = ButtonIcon(inputTextShortcutsFrame, Name = 'pasteButton', filename = 'iconAssets/paste.png', command = None)
        pasteButton.pack(side = 'top', fill = 'x', expand = True)
        pasteButton.tkraise()

        deleteButton = ButtonIcon(inputTextShortcutsFrame, Name = 'deleteButton', filename = 'iconAssets/delete.png', command = None)
        deleteButton.pack(side = 'bottom', fill = 'x', expand = True)
        deleteButton.tkraise()

        translateButton = ButtonText(self.textTranslatorTab, Name = 'translateButton', text = 'Translate', command = None, pady = (10,0))
        translateButton.grid(row = 3, column = 1, sticky = 'nw')
        translateButton.tkraise()

        outputTextLabel = TextLabelDynamic(self.textTranslatorTab, Name = 'outputTextLabel', pady = (20,0))
        outputTextLabel.grid(row = 3, column = 0, sticky = 'nw')
        outputTextLabel.setText('Output Morse Code Ciphertext:')
        outputTextLabel.tkraise()

        downloadTextLabel = TextLabelStatic(self.textTranslatorTab, Name = 'downloadTextLabel', text = 'Download as a text file:', padx = (45,0))
        downloadTextLabel.grid(row = 3, column = 2, sticky = 's')
        downloadTextLabel.tkraise()

        downloadButton = ButtonIcon(self.textTranslatorTab, Name = 'downloadButton', filename = 'iconAssets/download.png', command = None)
        downloadButton.grid(row = 4, column = 2, sticky = 'n', padx = (45,0))
        downloadButton.tkraise()

        outputTextArea = TextEntry(self.textTranslatorTab, Name = 'outputTextArea')
        outputTextArea.grid(row = 4, column = 0, sticky = 'nw')
        outputTextArea.tkraise()

        outputTextShortcutsFrame = tk.Frame(self.textTranslatorTab, width=30, height=85)
        outputTextShortcutsFrame.pack_propagate(False)
        outputTextShortcutsFrame.grid(row = 4, column = 1, sticky = 'nw')
        outputTextShortcutsFrame.tkraise()

        copyButton = ButtonIcon(outputTextShortcutsFrame, Name = 'copyButton', filename = 'iconAssets/copy.png', command = None)
        copyButton.pack(side = 'top', fill = 'x', expand = True)
        copyButton.tkraise()

        lightButton = ButtonIcon(outputTextShortcutsFrame, Name = 'lightButton', filename = 'iconAssets/light.png', command = None)
        lightButton.pack(side = 'bottom', fill = 'x', expand = True)
        lightButton.tkraise()

    def populateSoundGeneratorTab(self):
        translationDirectionLabel = TextLabelDynamic(self.soundGeneratorTab, Name = 'translationDirectionLabel', anchor = 'w', pady = (10,10))
        translationDirectionLabel.grid(row = 0, column = 0)
        translationDirectionLabel.setText('English Plaintext -----> Morse Code Sound File')
        translationDirectionLabel.tkraise()

        inputTypeTextLabel = TextLabelStatic(self.soundGeneratorTab, Name = 'inputTypeTextLabel', text = 'Input:', anchor = 'e')
        inputTypeTextLabel.grid(row = 0, column = 1, sticky = 'e')
        inputTypeTextLabel.tkraise()

        translationDropdown = Dropdown(self.soundGeneratorTab, Name = 'translationDropdown', valueTuple = ('English Plaintext Input', 'Morse Code Ciphertext Input'))
        translationDropdown.grid(row = 0, column = 2)
        translationDropdown.setDropdownValue('English Plaintext Input')
        translationDropdown.tkraise()

        inputTextLabel = TextLabelDynamic(self.soundGeneratorTab, Name ='inputTextLabel')
        inputTextLabel.grid(row = 1, column = 0, sticky = 'nw')
        inputTextLabel.setText('Input English Plaintext:')
        inputTextLabel.tkraise()

        uploadTextLabel = TextLabelStatic(self.soundGeneratorTab, Name ='uploadTextLabel', text = 'Or upload a text file:', padx = (60,0))
        uploadTextLabel.grid(row = 1, column = 2, sticky = 'sw')
        uploadTextLabel.tkraise()

        inputTextArea = TextEntry(self.soundGeneratorTab, Name = 'inputTextArea')
        inputTextArea.grid(row = 2, column = 0, sticky = 'nw')
        inputTextArea.tkraise()

        inputTextShortcutsFrame = tk.Frame(self.soundGeneratorTab, width=30, height=85)
        inputTextShortcutsFrame.pack_propagate(False)
        inputTextShortcutsFrame.grid(row = 2, column = 1, sticky = 'nw')
        inputTextShortcutsFrame.tkraise()

        pasteButton = ButtonIcon(inputTextShortcutsFrame, Name = 'pasteButton', filename = 'iconAssets/paste.png', command = None)
        pasteButton.pack(side = 'top', fill = 'x', expand = True)
        pasteButton.tkraise()

        deleteButton = ButtonIcon(inputTextShortcutsFrame, Name = 'deleteButton', filename = 'iconAssets/delete.png', command = None)
        deleteButton.pack(side = 'bottom', fill = 'x', expand = True)
        deleteButton.tkraise()

        uploadButton = ButtonIcon(self.soundGeneratorTab, Name = 'uploadButton', filename = 'iconAssets/upload.png', command = None)
        uploadButton.grid(row = 2, column = 2, sticky = 'n')
        uploadButton.tkraise()

        outputTextLabel = TextLabelStatic(self.soundGeneratorTab, Name = 'outputTextLabel', text = 'Output Morse Code sound file:')
        outputTextLabel.grid(row = 3, column = 0, sticky = 'nw')
        outputTextLabel.tkraise()

        resetButton = ButtonText(self.soundGeneratorTab, Name = 'resetButton', text = 'Reset', command = None)
        resetButton.grid(row = 3, column = 1, sticky = 'w')
        resetButton.tkraise()

        generateFrame = tk.Frame(self.soundGeneratorTab)
        generateFrame.grid(row = 3, column = 2)
        generateFrame.tkraise()

        generateButton = ButtonText(generateFrame, Name = 'generateButton', text = 'Generate', command = None)
        generateButton.grid(row = 0, column = 0)
        generateButton.tkraise()

        generateTextLabel = TextLabelDynamic(generateFrame, Name = 'generateTextLabel', colour = 'red')
        generateTextLabel.grid(row = 0, column = 1)
        generateTextLabel.setText('Not Generated')
        generateTextLabel.tkraise()

        sliderFrame = tk.Frame(self.soundGeneratorTab)
        sliderFrame.grid(row = 4, column = 0, columnspan = 2, sticky = 'nw')
        sliderFrame.tkraise()

        frequencyTextLabel = TextLabelStatic(sliderFrame, Name = 'frequencyTextLabel', text = 'Frequency', anchor = 'e')
        frequencyTextLabel.grid(row = 0, column = 0, sticky = 'w')
        frequencyTextLabel.tkraise()

        frequencySlider = Slider(sliderFrame, Name = 'frequencySlider', minValue = 400, maxValue = 1000, defaultValue = 600)
        frequencySlider.grid(row = 0, column = 1)
        frequencySlider.tkraise()

        wpmTextLabel = TextLabelStatic(sliderFrame, Name = 'wpmTextLabel', text = 'WPM', anchor = 'e')
        wpmTextLabel.grid(row = 1, column = 0, sticky = 'w')
        wpmTextLabel.tkraise()

        wpmSlider = Slider(sliderFrame, Name = 'wpmSlider', minValue = 5, maxValue = 20, defaultValue = 10)
        wpmSlider.grid(row = 1, column = 1)
        wpmSlider.tkraise()

        volumeTextLabel = TextLabelStatic(sliderFrame, Name = 'volumeTextLabel', text = 'Volume', anchor = 'e')
        volumeTextLabel.grid(row = 2, column = 0, sticky = 'w')
        volumeTextLabel.tkraise()

        volumeSlider = Slider(sliderFrame, Name = 'volumeSlider', minValue = 1, maxValue = 100, defaultValue = 50)
        volumeSlider.grid(row = 2, column = 1)
        volumeSlider.tkraise()

        frequencyTextEntry = SmallTextEntry(sliderFrame, Name = 'frequencyTextEntry')
        frequencyTextEntry.grid(row = 0, column = 2)
        frequencyTextEntry.tkraise()

        wpmTextEntry = SmallTextEntry(sliderFrame, Name = 'wpmTextEntry')
        wpmTextEntry.grid(row = 1, column = 2)
        wpmTextEntry.tkraise()

        volumeTextEntry = SmallTextEntry(sliderFrame, Name = 'frequencyTextEntry')
        volumeTextEntry.grid(row = 2, column = 2)
        volumeTextEntry.tkraise()

        downloadFrame = tk.Frame(self.soundGeneratorTab)
        downloadFrame.grid(row = 4, column = 2)
        downloadFrame.tkraise()

        downloadTextLabel = TextLabelStatic(downloadFrame, Name = 'downloadTextLabel', text = 'Download as a .wav file:')
        downloadTextLabel.grid(row = 0, column = 0, sticky = 's')
        downloadTextLabel.tkraise()

        downloadButton = ButtonIcon(downloadFrame, Name = 'downloadButton', filename = 'iconAssets/download.png', command = None)
        downloadButton.grid(row = 1, column = 0, sticky = 'n')
        downloadButton.tkraise()

        playbackFrame = tk.Frame(self.soundGeneratorTab, pady = 15)
        playbackFrame.grid(row = 5, column = 0, columnspan = 2, sticky = 'w')
        playbackFrame.tkraise()

        playbackTextLabel = TextLabelStatic(playbackFrame, Name = 'playbackTextLabel', text = 'Playback:')
        playbackTextLabel.grid(row = 0, column = 0, sticky = 'w')
        playbackFrame.tkraise()

        playButton = ButtonIcon(playbackFrame, Name = 'playButton', filename = 'iconAssets/play.png', padx = 5 , command = None)
        playButton.grid(row = 0, column = 1)
        playButton.tkraise()

        pauseButton = ButtonIcon(playbackFrame, Name = 'pauseButton', filename = 'iconAssets/pause.png', padx = 5, command = None)
        pauseButton.grid(row = 0, column = 2)
        pauseButton.tkraise()

        rewindButton = ButtonIcon(playbackFrame, Name = 'rewindButton', filename = 'iconAssets/rewind.png', padx = 5 , command = None)
        rewindButton.grid(row = 0, column = 3)
        rewindButton.tkraise()

        waveformButton = ButtonIcon(playbackFrame, Name = 'waveformButton', filename = 'iconAssets/waveform.png', padx = 5, command = None)
        waveformButton.grid(row = 0, column = 4)
        waveformButton.tkraise()

        playbackTimeTextLabel = TextLabelDynamic(playbackFrame, Name = 'playbackTimeTextLabel', padx = (20,0))
        playbackTimeTextLabel.grid(row = 0, column = 5)
        playbackTimeTextLabel.setText('00.00.00 / 00.00.00')
        playbackTimeTextLabel.tkraise()

    def populateSoundDecoderTab(self):
        pass

    def populateKeyerTab(self):
        pass

    def populateChallengeModeTab(self):
        pass

    def populateNetworkingTab(self):
        pass

class TextLabelDynamic(tk.Frame):
    def __init__(self, parent, Name = 'TextLabelDynamic', fontSize = 10, fontType = 'Verdana', colour = 'black', anchor = 'w', pady = 5, padx = 10):
        self.Name = Name
        self.fontSize = fontSize
        self.fontType = fontType
        self.textvariable = tk.StringVar()
        self.anchor = anchor
        self.colour = colour
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, textvariable = self.textvariable, font = (self.fontType, self.fontSize), anchor = self.anchor, fg = self.colour)
        self.label.pack(pady = self.pady, padx = self.padx)

    def setText(self, text):
        self.textvariable.set(text)

    def setColour(self, newColour):
        self.label.configure(fg = newColour)

    def getText(self):
        return self.textvariable.get()


class TextLabelStatic(tk.Frame):
    def __init__(self, parent, Name = 'TextLabelStatic', text = 'MorseMaster', fontSize = 10, fontType = 'Verdana', anchor = 'w', pady = 5, padx = 10):
        self.Name = Name
        self.fontSize = fontSize
        self.fontType = fontType
        self.text = text
        self.anchor = anchor
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = self.text, font = (self.fontType, self.fontSize), anchor = self.anchor)
        label.pack(pady = self.pady, padx = self.padx)


class ButtonText(tk.Frame):
    def __init__(self, parent, Name = 'ButtonText', command = None, text = 'Button', fontSize = 10, fontType = 'Verdana', pady = 0, padx = 0):
        self.Name = Name
        self.command = command
        self.text = text
        self.fontSize = fontSize
        self.fontType = fontType
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.button = tk.Button(self, text = self.text, font = (self.fontType, self.fontSize, 'bold'), command = self.command)
        self.button.pack(pady = self.pady, padx = self.padx)

    def setCommand(self, newCommand):
        self.button.configure(command = newCommand)


class ButtonIcon(tk.Frame):
    def __init__(self, parent, Name = 'ButtonIcon', command = None, filename = '', iconSize = (1,1), pady = 0, padx = 0):
        self.Name = Name
        self.command = command
        self.filename = filename
        self.iconSize = iconSize
        self.pady = pady
        self.padx = padx
        icon = tk.PhotoImage(file = (self.filename)).subsample(self.iconSize[0])
        tk.Frame.__init__(self, parent)
        self.button = tk.Button(self, image = icon, command = self.command)
        self.button.image = icon
        self.button.pack(pady = self.pady, padx = self.padx)

    def setCommand(self, newCommand):
        self.button.configure(command = newCommand)


class TextEntry(tk.Frame):
    def __init__(self, parent, Name = 'TextEntry', fontSize = 10, fontType = 'Verdana', width = 40, height = 5, pady = 0, padx = 10):
        self.Name = Name
        self.fontSize = fontSize
        self.fontType = fontType
        self.width = width
        self.height = height
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.textBox = ScrolledText(self, font = (self.fontType, self.fontSize), width = self.width, height = self.height)
        self.textBox.pack(pady = self.pady, padx = self.padx, fill='y')

    def setText(self, text):
        self.textBox.delete('1.0','end')
        self.textBox.insert(tk.INSERT, text)

    def getText(self):
        return self.textBox.get('1.0','end-1c')
    
    def clearText(self):
        self.textBox.delete('1.0','end')


class SmallTextEntry(tk.Frame):
    def __init__(self, parent, Name = 'SmallTextEntry', fontSize = 10, fontType = 'Verdana', width = 5, pady = 0, padx = (15,0)):
        self.Name = Name
        self.fontSize = fontSize
        self.fontType = fontType
        self.width = width
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.textBox = tk.Entry(self, font = (self.fontType, self.fontSize), width = self.width)
        self.textBox.pack(pady = self.pady, padx = self.padx)

    def setText(self, text):
        self.textBox.delete('1.0','end')
        self.textBox.insert(tk.INSERT, text)

    def getText(self):
        return self.textBox.get('1.0','end-1c')


class LightBox:
    pass


class Slider(tk.Frame):
    def __init__(self, parent, Name = 'Slider', orient='horizontal', width = 250, minValue = 0, maxValue = 100, defaultValue = 50, pady = 0, padx = 0):
        self.Name = Name
        self.orient = orient
        self.width = width
        self.minValue = minValue
        self.maxValue = maxValue
        self.defaultValue = defaultValue
        self.value = tk.DoubleVar()
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.slider = Scale(self, from_ = self.minValue, to = self.maxValue, value = self.defaultValue, variable = self.value, orient = self.orient, length = self.width, command = self.sliderChanged())
        self.slider.pack(pady = self.pady, padx = self.padx)

    def sliderChanged(self):
        pass

    def setSliderValue(self, newValue):
        try:
            if newValue >= self.slider.from_ and newValue <= self.slider.to:
                self.value.set(newValue)
        except:
            pass

    def disableSlider(self):
        self.slider.configure(state = 'disabled')
    
    def enableSlider(self):
        self.slider.configure(state = 'enabled')


class Dropdown(tk.Frame):
    def __init__(self, parent, Name = 'Dropdown', valueTuple = ('Select Option'), fontSize = 10, fontType = 'Verdana', width = 30, pady = 0, padx = 0):
        self.Name = Name
        self.valueTuple = valueTuple
        self.value = tk.StringVar()
        self.fontSize = fontSize
        self.fontType = fontType
        self.width = width
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.dropdown = Combobox(self, width = self.width, font = (self.fontType, self.fontSize), values = self.valueTuple, textvariable = self.value)
        self.dropdown.pack(pady = self.pady, padx = self.padx)

    def dropdownChanged(self):
        pass

    def getDropdownValue(self):
        return self.value.get()
    
    def setDropdownValue(self, newValue):
        self.value.set(newValue)