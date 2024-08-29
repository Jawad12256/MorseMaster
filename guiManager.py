'''GUI MANAGER'''
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Combobox
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

        outputTextLabel = TextLabelStatic(self.soundGeneratorTab, Name = 'outputTextLabel', text = 'Output Morse Code sound file:', pady = (10,0))
        outputTextLabel.grid(row = 3, column = 0, sticky = 'nw')
        outputTextLabel.tkraise()

        resetButton = ButtonText(self.soundGeneratorTab, Name = 'resetButton', text = 'Reset', pady = (10,0), command = None)
        resetButton.grid(row = 3, column = 1, sticky = 'w')
        resetButton.tkraise()

        generateFrame = tk.Frame(self.soundGeneratorTab)
        generateFrame.grid(row = 3, column = 2)
        generateFrame.tkraise()

        generateButton = ButtonText(generateFrame, Name = 'generateButton', text = 'Generate', pady = (10,0), command = None)
        generateButton.grid(row = 0, column = 0)
        generateButton.tkraise()

        generateTextLabel = TextLabelDynamic(generateFrame, Name = 'generateTextLabel', colour = 'red', pady = (10,0))
        generateTextLabel.grid(row = 0, column = 1)
        generateTextLabel.setText('Not Generated')
        generateTextLabel.tkraise()

        sliderFrame = tk.Frame(self.soundGeneratorTab)
        sliderFrame.grid(row = 4, column = 0, columnspan = 2, sticky = 'nw')
        sliderFrame.tkraise()

        frequencyTextLabel = TextLabelStatic(sliderFrame, Name = 'frequencyTextLabel', text = 'Frequency', anchor = 'e')
        frequencyTextLabel.grid(row = 0, column = 0, sticky = 'sw')
        frequencyTextLabel.tkraise()

        frequencySlider = Slider(sliderFrame, Name = 'frequencySlider', minValue = 400, maxValue = 1000)
        frequencySlider.grid(row = 0, column = 1, sticky = 'n')
        frequencySlider.setSliderValue(600)
        frequencySlider.tkraise()

        wpmTextLabel = TextLabelStatic(sliderFrame, Name = 'wpmTextLabel', text = 'WPM', anchor = 'e')
        wpmTextLabel.grid(row = 1, column = 0, sticky = 'sw')
        wpmTextLabel.tkraise()

        wpmSlider = Slider(sliderFrame, Name = 'wpmSlider', minValue = 5, maxValue = 20)
        wpmSlider.grid(row = 1, column = 1, sticky = 'n')
        wpmSlider.setSliderValue(10)
        wpmSlider.tkraise()

        volumeTextLabel = TextLabelStatic(sliderFrame, Name = 'volumeTextLabel', text = 'Volume', anchor = 'e')
        volumeTextLabel.grid(row = 2, column = 0, sticky = 'sw')
        volumeTextLabel.tkraise()

        volumeSlider = Slider(sliderFrame, Name = 'volumeSlider', minValue = 1, maxValue = 300)
        volumeSlider.grid(row = 2, column = 1, sticky = 'n')
        volumeSlider.setSliderValue(100)
        volumeSlider.tkraise()

        frequencyTextEntry = SmallTextEntry(sliderFrame, Name = 'frequencyTextEntry')
        frequencyTextEntry.grid(row = 0, column = 2, sticky = 's')
        frequencyTextEntry.setText('600')
        frequencyTextEntry.tkraise()

        wpmTextEntry = SmallTextEntry(sliderFrame, Name = 'wpmTextEntry')
        wpmTextEntry.grid(row = 1, column = 2, sticky = 's')
        wpmTextEntry.setText('10')
        wpmTextEntry.tkraise()

        volumeTextEntry = SmallTextEntry(sliderFrame, Name = 'volumeTextEntry')
        volumeTextEntry.grid(row = 2, column = 2, sticky = 's')
        volumeTextEntry.setText('100')
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

        stopButton = ButtonIcon(playbackFrame, Name = 'stopButton', filename = 'iconAssets/stop.png', padx = 5 , command = None)
        stopButton.grid(row = 0, column = 3)
        stopButton.tkraise()

        waveformButton = ButtonIcon(playbackFrame, Name = 'waveformButton', filename = 'iconAssets/waveform.png', padx = 5, command = None)
        waveformButton.grid(row = 0, column = 4)
        waveformButton.tkraise()

    def populateSoundDecoderTab(self):
        translationDirectionLabel = TextLabelDynamic(self.soundDecoderTab, Name = 'translationDirectionLabel', anchor = 'w', pady = (10,10))
        translationDirectionLabel.grid(row = 0, column = 0)
        translationDirectionLabel.setText('Morse Code Sound File -----> English Plaintext')
        translationDirectionLabel.tkraise()

        outputTypeTextLabel = TextLabelStatic(self.soundDecoderTab, Name = 'outputTypeTextLabel', text = 'Output:', anchor = 'e', padx = (15,0))
        outputTypeTextLabel.grid(row = 0, column = 1, sticky = 'e')
        outputTypeTextLabel.tkraise()

        translationDropdown = Dropdown(self.soundDecoderTab, Name = 'translationDropdown', valueTuple = ('English Plaintext Output', 'Morse Code Ciphertext Output'), padx = (10,0))
        translationDropdown.grid(row = 0, column = 2)
        translationDropdown.setDropdownValue('English Plaintext Output')
        translationDropdown.tkraise()

        uploadTextLabel = TextLabelStatic(self.soundDecoderTab, Name ='uploadTextLabel', text = 'Upload Morse Code Sound File:', anchor = 'w', padx = (10,0))
        uploadTextLabel.grid(row = 1, column = 0, sticky = 'sw')
        uploadTextLabel.tkraise()

        resetButton = ButtonText(self.soundDecoderTab, Name = 'resetButton', text = 'Reset', pady = (10,0), padx = (45,0), command = None)
        resetButton.grid(row = 1, column = 1, sticky = 'w')
        resetButton.tkraise()

        wpmFrame = tk.Frame(self.soundDecoderTab)
        wpmFrame.grid(row = 2, column = 0, columnspan = 2)
        wpmFrame.tkraise()

        wpmRadioButtons = RadioButtons(wpmFrame, Name = 'wpmRadioButtons', valueTuple = ('Auto-Determine WPM','WPM'), padx = (10,0), pady = (10,0))
        wpmRadioButtons.grid(row = 0, column = 0)
        wpmRadioButtons.tkraise()

        wpmSlider = Slider(wpmFrame, Name = 'wpmSlider', minValue = 5, maxValue = 20, width = 200)
        wpmSlider.grid(row = 1, column = 1)
        wpmSlider.setSliderValue(10)
        wpmSlider.disableSlider()
        wpmSlider.tkraise()

        wpmTextEntry = SmallTextEntry(wpmFrame, Name = 'wpmTextEntry', pady = (15,0))
        wpmTextEntry.grid(row = 1, column = 2)
        wpmTextEntry.setText('10')
        wpmTextEntry.disableEntry()
        wpmTextEntry.tkraise()

        translateFrame = tk.Frame(self.soundDecoderTab)
        translateFrame.grid(row = 2, column = 2)
        translateFrame.tkraise()

        audioLoadedTextLabel = TextLabelDynamic(translateFrame, Name = 'audioLoadedTextLabel', pady = (15,0))
        audioLoadedTextLabel.grid(row = 0, column = 0)
        audioLoadedTextLabel.setText('No Audio Loaded')
        audioLoadedTextLabel.setColour('red')
        audioLoadedTextLabel.tkraise()

        translateButton = ButtonText(translateFrame, Name = 'translateButton', text = 'Translate', pady = (10,0), command = None)
        translateButton.grid(row = 1, column = 0)
        translateButton.tkraise()

        uploadRecordFrame = tk.Frame(self.soundDecoderTab)
        uploadRecordFrame.grid(row = 3, column = 0, columnspan = 2)
        uploadRecordFrame.tkraise()

        uploadSoundFileLabel = TextLabelStatic(uploadRecordFrame, Name = 'uploadSoundFileLabel', text = 'Upload .wav sound file:', pady = (10,0))
        uploadSoundFileLabel.grid(row = 0, column = 0)
        uploadSoundFileLabel.tkraise()

        uploadButton = ButtonIcon(uploadRecordFrame, Name = 'uploadButton', filename = 'iconAssets/upload.png', pady = (10,0), command = None)
        uploadButton.grid(row = 0, column = 1)
        uploadButton.tkraise()

        recordTextLabel = TextLabelStatic(uploadRecordFrame, Name = 'recordTextLabel', text = 'Or record a sound file:', pady = (10,0), padx = (25,0))
        recordTextLabel.grid(row = 0, column = 2)
        recordTextLabel.tkraise()

        recordButton = ButtonIcon(uploadRecordFrame, Name = 'recordButton', filename = 'iconAssets/record.png', pady = (10,0), padx = (15,0), command = None)
        recordButton.grid(row = 0, column = 3)
        recordButton.tkraise()

        playbackFrame = tk.Frame(self.soundDecoderTab)
        playbackFrame.grid(row = 3, column = 2)
        playbackFrame.tkraise()

        playButton = ButtonIcon(playbackFrame, Name = 'playButton', filename = 'iconAssets/play.png', pady = (10,0), padx = 5, command = None)
        playButton.grid(row = 0, column = 0)
        playButton.tkraise()

        pauseButton = ButtonIcon(playbackFrame, Name = 'pauseButton', filename = 'iconAssets/pause.png', pady = (10,0), padx = 5, command = None)
        pauseButton.grid(row = 0, column = 1)
        pauseButton.tkraise()

        stopButton = ButtonIcon(playbackFrame, Name = 'stopButton', filename = 'iconAssets/stop.png', pady = (10,0), padx = 5 , command = None)
        stopButton.grid(row = 0, column = 2)
        stopButton.tkraise()

        outputTextLabel = TextLabelDynamic(self.soundDecoderTab, Name = 'outputTextLabel', pady = (20,0))
        outputTextLabel.grid(row = 4, column = 0, sticky = 'nw')
        outputTextLabel.setText('Output English Plaintext:')
        outputTextLabel.tkraise()

        outputTextArea = TextEntry(self.soundDecoderTab, Name = 'outputTextArea')
        outputTextArea.grid(row = 5, column = 0, sticky = 'nw')
        outputTextArea.tkraise()

        outputTextShortcutsFrame = tk.Frame(self.soundDecoderTab, width=30, height=85)
        outputTextShortcutsFrame.pack_propagate(False)
        outputTextShortcutsFrame.grid(row = 5, column = 1, sticky = 'nw')
        outputTextShortcutsFrame.tkraise()

        copyButton = ButtonIcon(outputTextShortcutsFrame, Name = 'copyButton', filename = 'iconAssets/copy.png', command = None)
        copyButton.pack(side = 'top', fill = 'x', expand = True)
        copyButton.tkraise()

        lightButton = ButtonIcon(outputTextShortcutsFrame, Name = 'lightButton', filename = 'iconAssets/light.png', command = None)
        lightButton.pack(side = 'bottom', fill = 'x', expand = True)
        lightButton.disableButton()
        lightButton.tkraise()

        downloadFrame = tk.Frame(self.soundDecoderTab)
        downloadFrame.grid(row = 5, column = 2)
        downloadFrame.tkraise()

        downloadTextLabel = TextLabelStatic(downloadFrame, Name = 'downloadTextLabel', text = 'Download as a text file:')
        downloadTextLabel.grid(row = 0, column = 0, sticky = 's')
        downloadTextLabel.tkraise()

        downloadButton = ButtonIcon(downloadFrame, Name = 'downloadButton', filename = 'iconAssets/download.png', command = None)
        downloadButton.grid(row = 1, column = 0, sticky = 'n')
        downloadButton.tkraise()


    def populateKeyerTab(self):
        translateFrame = tk.Frame(self.keyerTab)
        translateFrame.grid(row = 0, column = 0)
        translateFrame.tkraise()

        translationDirectionLabel = TextLabelStatic(translateFrame, Name = 'translationDirectionLabel', text = 'Morse Code Keyer -----> English Plaintext', anchor = 'w', pady = (15,10))
        translationDirectionLabel.grid(row = 0, column = 0, columnspan = 2, sticky = 'nw')
        translationDirectionLabel.tkraise()

        paddleModeLabel = TextLabelDynamic(translateFrame, Name = 'paddleModeLabel')
        paddleModeLabel.grid(row = 1, column = 0)
        paddleModeLabel.setText('Paddle Mode A')
        paddleModeLabel.setColour('dark blue')
        paddleModeLabel.tkraise()

        switchButton = ButtonText(translateFrame, Name = 'switchButton', text = 'Switch Mode', command = None)
        switchButton.grid(row = 1, column = 1)
        switchButton.tkraise()
        
        sliderFrame = tk.Frame(self.keyerTab)
        sliderFrame.grid(row = 0, column = 1, columnspan = 2)
        sliderFrame.tkraise()

        frequencyTextLabel = TextLabelStatic(sliderFrame, Name = 'frequencyTextLabel', text = 'Frequency', anchor = 'e')
        frequencyTextLabel.grid(row = 0, column = 0, sticky = 'sw')
        frequencyTextLabel.tkraise()

        frequencySlider = Slider(sliderFrame, Name = 'frequencySlider', minValue = 400, maxValue = 1000, width = 200)
        frequencySlider.grid(row = 0, column = 1, sticky = 'n')
        frequencySlider.setSliderValue(600)
        frequencySlider.tkraise()

        wpmTextLabel = TextLabelStatic(sliderFrame, Name = 'wpmTextLabel', text = 'WPM', anchor = 'e')
        wpmTextLabel.grid(row = 1, column = 0, sticky = 'sw')
        wpmTextLabel.tkraise()

        wpmSlider = Slider(sliderFrame, Name = 'wpmSlider', minValue = 5, maxValue = 20, width = 200)
        wpmSlider.grid(row = 1, column = 1, sticky = 'n')
        wpmSlider.setSliderValue(10)
        wpmSlider.tkraise()

        frequencyTextEntry = SmallTextEntry(sliderFrame, Name = 'frequencyTextEntry')
        frequencyTextEntry.grid(row = 0, column = 2, sticky = 's')
        frequencyTextEntry.setText('600')
        frequencyTextEntry.tkraise()

        wpmTextEntry = SmallTextEntry(sliderFrame, Name = 'wpmTextEntry')
        wpmTextEntry.grid(row = 1, column = 2, sticky = 's')
        wpmTextEntry.setText('10')
        wpmTextEntry.tkraise()

        englishCurrentLabel = TextLabelDynamic(self.keyerTab, Name ='englishCurrentLabel', fontSize = 30)
        englishCurrentLabel.grid(row = 1, column = 0, columnspan = 3)
        englishCurrentLabel.setText('')
        englishCurrentLabel.tkraise()

        morseCurrentLabel = TextLabelDynamic(self.keyerTab, Name ='morseCurrentLabel', fontSize = 30)
        morseCurrentLabel.grid(row = 2, column = 0, columnspan = 3)
        morseCurrentLabel.setText('')
        morseCurrentLabel.tkraise()

        outputTextLabel = TextLabelDynamic(self.keyerTab, Name = 'outputTextLabel', pady = (20,0))
        outputTextLabel.grid(row = 3, column = 0, sticky = 'nw')
        outputTextLabel.setText('Output Morse Code Ciphertext:')
        outputTextLabel.tkraise()

        downloadTextLabel = TextLabelStatic(self.keyerTab, Name = 'downloadTextLabel', text = 'Download as a text file:')
        downloadTextLabel.grid(row = 3, column = 2, sticky = 's')
        downloadTextLabel.tkraise()

        downloadButton = ButtonIcon(self.keyerTab, Name = 'downloadButton', filename = 'iconAssets/download.png', command = None)
        downloadButton.grid(row = 4, column = 2, sticky = 'n')
        downloadButton.tkraise()

        outputTextArea = TextEntry(self.keyerTab, Name = 'outputTextArea')
        outputTextArea.grid(row = 4, column = 0, sticky = 'nw')
        outputTextArea.tkraise()

        outputTextShortcutsFrame = tk.Frame(self.keyerTab, width=30, height=85)
        outputTextShortcutsFrame.pack_propagate(False)
        outputTextShortcutsFrame.grid(row = 4, column = 1, sticky = 'nw')
        outputTextShortcutsFrame.tkraise()

        copyButton = ButtonIcon(outputTextShortcutsFrame, Name = 'copyButton', filename = 'iconAssets/copy.png', command = None)
        copyButton.pack(side = 'top', fill = 'x', expand = True)
        copyButton.tkraise()

        deleteButton = ButtonIcon(outputTextShortcutsFrame, Name = 'deleteButton', filename = 'iconAssets/delete.png', command = None)
        deleteButton.pack(side = 'bottom', fill = 'x', expand = True)
        deleteButton.tkraise()

        keyFrame = tk.Frame(self.keyerTab)
        keyFrame.grid(row = 5, column = 0, columnspan = 2, sticky = 'w')
        keyFrame.tkraise()

        keyButton1 = ButtonIcon(keyFrame, Name = 'keyButton1', filename = 'iconAssets/key.png', command = None, pady = (10,0), padx = (15,0))
        keyButton1.grid(row = 0, column = 0, sticky = 'w')
        keyButton1.tkraise()

        keyButton2 = ButtonIcon(keyFrame, Name = 'keyButton2', filename = 'iconAssets/keyDash.png', command = None, pady = (10,0), padx = (15,0))
        keyButton2.grid(row = 0, column = 1, sticky = 'w')
        keyButton2.disableButton()
        keyButton2.tkraise()

        keyTextLabel = TextLabelStatic(keyFrame, Name = 'keyTextLabel', text = 'Tap button or press spacebar / comma / full stop')
        keyTextLabel.grid(row = 0, column = 2)
        keyTextLabel.tkraise()

        legendButton = ButtonText(self.keyerTab, Name = 'legendButton', text = 'Show Legend', command = None)
        legendButton.grid(row = 5, column = 2, sticky = 'w')
        legendButton.tkraise()


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

    def setCommand(self, newCommand, *args):
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

    def setCommand(self, newCommand, *args):
        self.button.configure(command = newCommand)

    def setBinding(self, event, command, *args):
        self.button.bind(event, command)

    def setImage(self, newFilename):
        newIcon = tk.PhotoImage(file = (newFilename)).subsample(self.iconSize[0])
        self.button.configure(image = newIcon)
        self.button.image = newIcon
    
    def disableButton(self):
        self.button.configure(state = 'disabled')
    
    def enableButton(self):
        self.button.configure(state = 'normal')


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

    def setCommand(self, event, newCommand):
        self.textBox.bind(event, newCommand)


class SmallTextEntry(tk.Frame):
    def __init__(self, parent, Name = 'SmallTextEntry', fontSize = 10, fontType = 'Verdana', width = 5, pady = 0, padx = (15,0)):
        self.Name = Name
        self.text = tk.StringVar()
        self.fontSize = fontSize
        self.fontType = fontType
        self.width = width
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.textBox = tk.Entry(self, textvariable = self.text, font = (self.fontType, self.fontSize), width = self.width, command = None)
        self.textBox.pack(pady = self.pady, padx = self.padx)

    def setText(self, text):
        self.textBox.delete('0','end')
        self.textBox.insert(tk.INSERT, text)

    def getText(self):
        return self.textBox.get()

    def disableEntry(self):
        self.textBox.configure(state = 'disabled')
    
    def enableEntry(self):
        self.textBox.configure(state = 'normal')


class LightBox:
    pass


class Slider(tk.Frame):
    def __init__(self, parent, Name = 'Slider', orient='horizontal', width = 250, minValue = 0, maxValue = 100, pady = 0, padx = 0):
        self.Name = Name
        self.orient = orient
        self.width = width
        self.minValue = minValue
        self.maxValue = maxValue
        self.value = tk.DoubleVar()
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.slider = tk.Scale(self, from_ = self.minValue, to = self.maxValue, variable = self.value, orient = self.orient, length = self.width, command = None)
        self.slider.pack(pady = self.pady, padx = self.padx)

    def setSliderValue(self, newValue):
        if newValue >= self.minValue and newValue <= self.maxValue:
            self.slider.set(newValue)

    def getSliderValue(self):
        return self.slider.get()

    def disableSlider(self):
        self.slider.configure(state = 'disabled')
        self.slider.configure(troughcolor = '#f4f4f4')
        self.slider.configure(fg = 'grey')
    
    def enableSlider(self):
        self.slider.configure(state = 'normal')
        self.slider.configure(troughcolor = 'light grey')
        self.slider.configure(fg = 'black')

    def setCommand(self, newCommand):
        self.slider.configure(command = newCommand)


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
        self.dropdown = Combobox(self, width = self.width, font = (self.fontType, self.fontSize), values = self.valueTuple, textvariable = self.value, state = 'readonly')
        self.dropdown.pack(pady = self.pady, padx = self.padx)

    def setCommand(self, event, newCommand):
        self.dropdown.bind(event, newCommand)

    def getDropdownValue(self):
        return self.value.get()
    
    def setDropdownValue(self, newValue):
        self.value.set(newValue)


class RadioButtons(tk.Frame):
    def __init__(self, parent, Name = 'RadioButtons', valueTuple = ('Option 1', 'Option 2'), fontSize = 10, fontType = 'Verdana', anchor = 'w', pady = 0, padx = 0):
        self.Name = Name
        self.valueTuple = valueTuple
        self.value = tk.StringVar(parent, '0')
        self.fontSize = fontSize
        self.fontType = fontType
        self.anchor = anchor
        self.pady = pady
        self.padx = padx
        tk.Frame.__init__(self, parent)
        self.valueDictionary = {}
        self.radioButtonsList = []
        for i in range(len(self.valueTuple)):
            self.valueDictionary[self.valueTuple[i]] = str(i)
        for (text, value) in self.valueDictionary.items():
            self.radioButtonsList.append(tk.Radiobutton(parent, text = text, variable = self.value, value = value, font = (self.fontType, self.fontSize)))
        for i,x in enumerate(self.radioButtonsList):
            x.grid(row = i, column = 0, pady = self.pady, padx = self.padx, sticky = 'nw')
    
    def setCommand(self, newCommand):
        for x in self.radioButtonsList:
            x.configure(command = newCommand)

    def getValue(self):
        return self.value.get()

    