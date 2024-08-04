'''MORSEMASTER MAIN APPLICATION'''
from guiManager import *
import textParser, textValidator, soundTranslator
import pyperclip
import numpy as np
import tempfile
from scipy.io import wavfile
from just_playback import Playback
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename

app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,400)

class TabEventsManager:
    def __init__(self, ref):
        self.tabWidgetObjects = ref
        self.tabObject = {}
        for widgetObject in self.tabWidgetObjects:
            if hasattr(widgetObject, 'Name'):
                self.tabObject[widgetObject.Name] = widgetObject
            else:
                children = widgetObject.winfo_children()
                for child in children:
                    if hasattr(child, 'Name'):
                        self.tabObject[child.Name] = child


class TextTranslator(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        self.states = {
            'textTranslator_MorseToEnglish':False
        }
        self.tabObject['translationDirectionButton'].setCommand(self.switch)
        self.tabObject['pasteButton'].setCommand(self.pasteText)
        self.tabObject['deleteButton'].setCommand(self.clearBoxes)
        self.tabObject['copyButton'].setCommand(self.copyText)
        self.tabObject['uploadButton'].setCommand(self.openFileDialog)
        self.tabObject['downloadButton'].setCommand(self.saveFileDialog)
        self.tabObject['inputTextArea'].setCommand("<KeyRelease>", (self.translate))

    def switch(self):
        mainLabel, inputLabel, outputLabel = self.tabObject['translationDirectionLabel'], self.tabObject['inputTextLabel'], self.tabObject['outputTextLabel']
        inputEntry, outputEntry = self.tabObject['inputTextArea'], self.tabObject['outputTextArea']
        temp = inputEntry.getText()
        inputEntry.setText(outputEntry.getText())
        outputEntry.setText(temp)
        if self.states['textTranslator_MorseToEnglish'] == False:
            mainLabel.setText('Morse Code Ciphertext -----> English Plaintext')
            inputLabel.setText('Input Morse Code Ciphertext')
            outputLabel.setText('Output English Plaintext')
            self.states['textTranslator_MorseToEnglish'] = True
        else:
            mainLabel.setText('English Plaintext -----> Morse Code Ciphertext')
            inputLabel.setText('Input English Plaintext:')
            outputLabel.setText('Output Morse Code Ciphertext:')
            self.states['textTranslator_MorseToEnglish'] = False

    def translate(self, *args):
        inputEntry, outputEntry = self.tabObject['inputTextArea'], self.tabObject['outputTextArea']
        if self.states['textTranslator_MorseToEnglish'] == False:
            plaintext = inputEntry.getText().replace('\n',' ')
            if plaintext == '' or plaintext == ' ':
                outputEntry.clearText()
            else:
                validatedPlaintext = textValidator.validateEnglish(plaintext)
                if validatedPlaintext != False:
                    ciphertext = textParser.parseEnglish(validatedPlaintext)
                    outputEntry.setText(ciphertext)
        else:
            ciphertext = inputEntry.getText()
            if ciphertext == '' or ciphertext == ' ':
                outputEntry.clearText()
            else:
                validatedCiphertext = textValidator.validateMorse(ciphertext)
                if validatedCiphertext != False:
                    plaintext = textParser.parseMorse(validatedCiphertext)
                    outputEntry.setText(plaintext)

    def pasteText(self):
        inputEntry = self.tabObject['inputTextArea']
        inputEntry.setText(pyperclip.paste())
        self.translate()

    def copyText(self):
        outputEntry = self.tabObject['outputTextArea']
        pyperclip.copy(outputEntry.getText())

    def clearBoxes(self):
        inputEntry, outputEntry = self.tabObject['inputTextArea'], self.tabObject['outputTextArea']
        inputEntry.clearText()
        outputEntry.clearText()

    def openFileDialog(self):
        filePath = askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.openFileProcess(filePath)
            
    def openFileProcess(self, filePath):
        inputEntry = self.tabObject['inputTextArea']
        try:
            with open(filePath, 'r') as f:
                inputEntry.setText(f.read())
        except:
            pass

    def saveFileDialog(self):
        filePath = asksaveasfile(defaultextension=".txt", title="Save As", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.saveFileProcess(filePath)

    def saveFileProcess(self, filePath):
        outputEntry = self.tabObject['outputTextArea']
        if outputEntry.getText() != '' and outputEntry.getText() != ' ':
            with open(filePath.name, 'w') as f:
                f.write(outputEntry.getText())
        else:
            pass


class SoundGenerator(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        self.states = {
            'soundGenerator_MorseToSound':False,
            'generated':False
        }
        self.soundData = None
        self.soundRate = 8000
        self.playbackManager = Playback()
        self.tempDataFilePath = None

        self.tabObject['translationDropdown'].setCommand('<<ComboboxSelected>>', self.switch)
        self.tabObject['pasteButton'].setCommand(self.pasteText)
        self.tabObject['deleteButton'].setCommand(self.clearBoxes)
        self.tabObject['resetButton'].setCommand(self.reset)
        self.tabObject['generateButton'].setCommand(self.generate)
        self.tabObject['uploadButton'].setCommand(self.openFileDialog)
        self.tabObject['downloadButton'].setCommand(self.saveFileDialog)
        self.tabObject['frequencySlider'].setCommand(self.matchTextEntries)
        self.tabObject['wpmSlider'].setCommand(self.matchTextEntries)
        self.tabObject['volumeSlider'].setCommand(self.matchTextEntries)
        f = self.tabObject['frequencyTextEntry']
        w = self.tabObject['wpmTextEntry']
        v = self.tabObject['volumeTextEntry']
        f.text.trace_add('write', self.matchSliders)
        w.text.trace_add('write', self.matchSliders)
        v.text.trace_add('write', self.matchSliders)
        self.tabObject['playButton'].setCommand(self.playSoundFile)
        self.tabObject['pauseButton'].setCommand(self.pauseSoundFile)
        self.tabObject['stopButton'].setCommand(self.stopSoundFile)
        self.tabObject['waveformButton'].setCommand(self.waveformSoundFile)

    def pasteText(self):
        inputEntry = self.tabObject['inputTextArea']
        inputEntry.setText(pyperclip.paste())

    def clearBoxes(self):
        inputEntry= self.tabObject['inputTextArea']
        inputEntry.clearText()

    def switch(self, *args):
        mainLabel, inputLabel = self.tabObject['translationDirectionLabel'], self.tabObject['inputTextLabel']
        if self.states['soundGenerator_MorseToSound'] == False:
            mainLabel.setText('Morse Code Ciphertext --> Morse Code Sound File')
            inputLabel.setText('Input Morse Code Ciphertext')
            self.states['soundGenerator_MorseToSound'] = True
        else:
            mainLabel.setText('English Plaintext -----> Morse Code Sound File')
            inputLabel.setText('Input English Plaintext:')
            self.states['soundGenerator_MorseToSound'] = False

    def reset(self):
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider'], self.tabObject['volumeSlider']]
        textEntries = [self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry'], self.tabObject['volumeTextEntry']]
        sliders[0].setSliderValue(600)
        sliders[1].setSliderValue(10)
        sliders[2].setSliderValue(100)
        textEntries[0].setText(600)
        textEntries[1].setText(10)
        textEntries[2].setText(100)

    def generate(self):
        inputEntry, frequencySlider, wpmSlider, volumeSlider = self.tabObject['inputTextArea'], self.tabObject['frequencySlider'], self.tabObject['wpmSlider'], self.tabObject['volumeSlider']
        text = inputEntry.getText()
        frequency, wpm, volume = int(frequencySlider.getSliderValue()), int(wpmSlider.getSliderValue()), int(volumeSlider.getSliderValue())/100
        if self.states['soundGenerator_MorseToSound'] == False:
            validatedText = textValidator.validateEnglish(text)
            if validatedText != False:
                ciphertext = textParser.parseEnglish(validatedText)
                self.soundData = soundTranslator.generateSound(ciphertext, frequency, volume, wpm)
        else:
            validatedText = textValidator.validateMorse(text)
            if validatedText != False:
                self.soundData = soundTranslator.generateSound(validatedText, frequency, volume, wpm)
        generateTextLabel = self.tabObject['generateTextLabel']
        generateTextLabel.setText('Generated!')
        generateTextLabel.setColour('green')
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            wavfile.write(tmpfile.name, self.soundRate, self.normaliseData(self.soundData))
            self.tempDataFilePath = tmpfile.name
        self.playbackManager.load_file(self.tempDataFilePath)
        self.states['generated'] = True

    def matchSliders(self, *args):
        frequencyEntry, wpmEntry, volumeEntry = self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry'], self.tabObject['volumeTextEntry']
        frequency, wpm, volume = frequencyEntry.getText(), wpmEntry.getText(), volumeEntry.getText()
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider'], self.tabObject['volumeSlider']]
        try:
            frequency = float(frequency)
            sliders[0].setSliderValue(frequency)
        except ValueError:
            pass
        try:
            wpm = float(wpm)
            sliders[1].setSliderValue(wpm)
        except ValueError:
            pass
        try:
            volume = float(volume)
            sliders[2].setSliderValue(volume)
        except ValueError:
            pass

    def matchTextEntries(self, *args):
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider'], self.tabObject['volumeSlider']]
        frequency, wpm, volume = str(sliders[0].getSliderValue()), str(sliders[1].getSliderValue()), str(sliders[2].getSliderValue())
        frequencyEntry, wpmEntry, volumeEntry = self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry'], self.tabObject['volumeTextEntry']
        frequencyEntry.setText(frequency)
        wpmEntry.setText(wpm)
        volumeEntry.setText(volume)

    def openFileDialog(self):
        filePath = askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.openFileProcess(filePath)
            
    def openFileProcess(self, filePath):
        inputEntry = self.tabObject['inputTextArea']
        try:
            with open(filePath, 'r') as f:
                inputEntry.setText(f.read())
        except:
            pass
    
    def saveFileDialog(self):
        if self.states['generated'] == True:
            filePath = asksaveasfilename(defaultextension=".wav", title="Save As", filetypes=[("Audio files", "*.wav")])
            if filePath:
                self.saveFileProcess(filePath)

    def saveFileProcess(self, filePath):
        if self.soundData != None:
            data = self.normaliseData(self.soundData)
            wavfile.write(filePath, self.soundRate, data)
        else:
            pass

    def normaliseData(self, data):
        if data.dtype != np.int16:
            if np.issubdtype(data.dtype, np.floating):
                maxFloat = np.max(np.abs(data))
                if maxFloat > 0:
                    data = data / maxFloat
                maxVal = np.iinfo(np.int16).max
                data = (data * maxVal).astype(np.int16)
            else:
                maxVal = np.iinfo(data.dtype).max
                data = (data / maxVal * np.iinfo(np.int16).max).astype(np.int16)
        return data

    def playSoundFile(self):
        if self.states['generated'] == True:
            if float(self.playbackManager.curr_pos) != 0.0:
                self.playbackManager.resume()
            else:
                self.playbackManager.play()
        else:
            pass

    def pauseSoundFile(self):
        if self.states['generated'] == True:
            self.playbackManager.pause()
        else:
            pass

    def stopSoundFile(self):
        if self.states['generated'] == True:
            self.playbackManager.stop()
            self.playbackManager.seek(0)
        else:
            pass

    def waveformSoundFile(self):
        if self.states['generated'] == True:
            soundTranslator.showWaveform(self.soundData, self.soundRate)
        else:
            pass


class SoundDecoder(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        self.states = {
            'soundDecoder_SoundToMorse':False,
            'wpmAuto':True,
            'loaded':False
        }
        self.soundData = None
        self.soundRate = 8000
        self.playbackManager = Playback()
        self.tempDataFilePath = None

        self.tabObject['translationDropdown'].setCommand('<<ComboboxSelected>>', self.switch)
        self.tabObject['resetButton'].setCommand(self.reset)
        self.tabObject['wpmRadioButtons'].setCommand(self.updateSliderEntry)
        self.tabObject['wpmSlider'].setCommand(self.matchTextEntry)
        w = self.tabObject['wpmTextEntry']
        w.text.trace_add('write', self.matchSlider)
        self.tabObject['uploadButton'].setCommand(self.openFileDialog)
        self.tabObject['recordButton'].setCommand(self.recordStartStop)
        self.tabObject['translateButton'].setCommand(self.translate)
        self.tabObject['playButton'].setCommand(self.playSoundFile)
        self.tabObject['pauseButton'].setCommand(self.pauseSoundFile)
        self.tabObject['stopButton'].setCommand(self.stopSoundFile)
        self.tabObject['copyButton'].setCommand(self.copyText)
        self.tabObject['downloadButton'].setCommand(self.saveFileDialog)

    def switch(self, *args):
        mainLabel, outputLabel, outputEntry = self.tabObject['translationDirectionLabel'], self.tabObject['outputTextLabel'], self.tabObject['outputTextArea']
        if self.states['soundDecoder_SoundToMorse'] == False:
            mainLabel.setText('Morse Code Sound File --> Morse Code Ciphertext')
            outputLabel.setText('Output Morse Code Ciphertext')
            validatedText = textValidator.validateEnglish(outputEntry.getText())
            if validatedText != False:
                outputEntry.setText(textParser.parseEnglish(validatedText))
            self.states['soundDecoder_SoundToMorse'] = True
        else:
            mainLabel.setText('Morse Code Sound File -----> English Plaintext')
            outputLabel.setText('Output English Plaintext:')
            validatedText = textValidator.validateMorse(outputEntry.getText())
            if validatedText != False:
                outputEntry.setText(textParser.parseMorse(validatedText))
            self.states['soundDecoder_SoundToMorse'] = False

    def reset(self):
        wpmSlider, wpmTextEntry = self.tabObject['wpmSlider'], self.tabObject['wpmTextEntry']
        wpmSlider.setSliderValue(10)
        wpmTextEntry.setText('10')

    def updateSliderEntry(self):
        radioButtons, wpmSlider, wpmTextEntry = self.tabObject['wpmRadioButtons'], self.tabObject['wpmSlider'], self.tabObject['wpmTextEntry']
        if radioButtons.getValue() == '0':
            wpmSlider.disableSlider()
            wpmTextEntry.disableEntry()
            self.states['wpmAuto'] = True
        else:
            wpmSlider.enableSlider()
            wpmTextEntry.enableEntry()
            self.states['wpmFalse'] = False

    def matchSlider(self, *args):
        wpmSlider, wpmTextEntry = self.tabObject['wpmSlider'], self.tabObject['wpmTextEntry']
        try:
            wpm = int(wpmTextEntry.getText())
            wpmSlider.setSliderValue(wpm)
        except ValueError:
            pass

    def matchTextEntry(self, *args):
        wpmSlider, wpmTextEntry = self.tabObject['wpmSlider'], self.tabObject['wpmTextEntry']
        wpm = str(wpmSlider.getSliderValue())
        wpmTextEntry.setText(wpm)

    def recordStart(self):
        pass

    def recordStop(self):
        pass

    def recordStartStop(self):
        pass

    def translate(self):
        if self.states['loaded'] == True:
            if self.states['wpmAuto'] == True:
                text = textValidator.validateMorse(soundTranslator.processSound(self.soundData, self.soundRate))
            else:
                wpmSlider = self.tabObject['wpmSlider']
                text = textValidator.validateMorse(soundTranslator.processSound(self.soundData, self.soundRate, auto = False, wpm = int(wpmSlider.getSliderValue())))
            if self.states['soundDecoder_SoundToMorse'] == False:
                text = textParser.parseMorse(text)
            if text != False:
                outputEntry = self.tabObject['outputTextArea']
                outputEntry.setText(text)
            else:
                pass
        else:
            pass

    def normaliseData(self, data):
        if data.dtype != np.int16:
            if np.issubdtype(data.dtype, np.floating):
                maxFloat = np.max(np.abs(data))
                if maxFloat > 0:
                    data = data / maxFloat
                maxVal = np.iinfo(np.int16).max
                data = (data * maxVal).astype(np.int16)
            else:
                maxVal = np.iinfo(data.dtype).max
                data = (data / maxVal * np.iinfo(np.int16).max).astype(np.int16)
        return data
    
    def playSoundFile(self):
        if self.states['loaded'] == True:
            if float(self.playbackManager.curr_pos) != 0.0:
                self.playbackManager.resume()
            else:
                self.playbackManager.play()
        else:
            pass

    def pauseSoundFile(self):
        if self.states['loaded'] == True:
            self.playbackManager.pause()
        else:
            pass

    def stopSoundFile(self):
        if self.states['loaded'] == True:
            self.playbackManager.stop()
            self.playbackManager.seek(0)
        else:
            pass

    def copyText(self):
        outputEntry = self.tabObject['outputTextArea']
        pyperclip.copy(outputEntry.getText())

    def openFileDialog(self):
        filePath = askopenfilename(title="Select a File", filetypes=[("Audio files", "*.wav")])
        if filePath:
            self.openFileProcess(filePath)

    def openFileProcess(self, filePath):
        try:
            self.soundRate, self.soundData = wavfile.read(filePath)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                wavfile.write(tmpfile.name, self.soundRate, self.normaliseData(self.soundData))
                self.tempDataFilePath = tmpfile.name
            self.playbackManager.load_file(self.tempDataFilePath)
            audioLoadedTextLabel = self.tabObject['audioLoadedTextLabel']
            audioLoadedTextLabel.setText('Audio Loaded!')
            audioLoadedTextLabel.setColour('green')
            self.states['loaded'] = True
        except:
            pass
    
    def saveFileDialog(self):
        pass

    def saveFileProcess(self, filePath):
        pass


textTranslator = TextTranslator(app.tabBar.textTranslatorTab.winfo_children())
soundGenerator = SoundGenerator(app.tabBar.soundGeneratorTab.winfo_children())
soundDecoder = SoundDecoder(app.tabBar.soundDecoderTab.winfo_children())

app.mainloop()