'''MORSEMASTER MAIN APPLICATION'''
from guiManager import *
import textParser, textValidator, soundTranslator, networkManager
import pyperclip
import numpy as np
import tempfile
import threading
import wave, struct
import time
import os
import random
from pygame import mixer, sndarray
os.system('cls' if os.name == 'nt' else "printf '\033c'")
from pynput import keyboard
from scipy.io import wavfile
from just_playback import Playback
from pvrecorder import PvRecorder

from tkinter import messagebox, Toplevel, Frame, Label
from tkinter.filedialog import askopenfilename, asksaveasfile, asksaveasfilename

app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,400)

def killAll():
    keyer.listener.stop()
    keyer.keyboardThread = None
    keyer.wordTerminatorThread = None
    networking.myNode.killPeer()
    networking.networkThread = None
    app.destroy()

app.protocol('WM_DELETE_WINDOW', killAll)

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
            'textTranslator_MorseToEnglish':False,
            'isDisplayingLight':False
        }
        self.lightThread = None

        self.tabObject['translationDirectionButton'].setCommand(self.switch)
        self.tabObject['pasteButton'].setCommand(self.pasteText)
        self.tabObject['deleteButton'].setCommand(self.clearBoxes)
        self.tabObject['copyButton'].setCommand(self.copyText)
        self.tabObject['lightButton'].setCommand(self.activateLightThread)
        self.tabObject['uploadButton'].setCommand(self.openFileDialog)
        self.tabObject['downloadButton'].setCommand(self.saveFileDialog)
        self.tabObject['inputTextArea'].setCommand("<KeyRelease>", (self.translate))

    def switch(self):
        mainLabel, inputLabel, outputLabel = self.tabObject['translationDirectionLabel'], self.tabObject['inputTextLabel'], self.tabObject['outputTextLabel']
        inputEntry, outputEntry, lightButton = self.tabObject['inputTextArea'], self.tabObject['outputTextArea'], self.tabObject['lightButton']
        temp = inputEntry.getText()
        inputEntry.setText(outputEntry.getText())
        outputEntry.setText(temp)
        if self.states['textTranslator_MorseToEnglish'] == False:
            mainLabel.setText('Morse Code Ciphertext -----> English Plaintext')
            inputLabel.setText('Input Morse Code Ciphertext')
            outputLabel.setText('Output English Plaintext')
            self.states['textTranslator_MorseToEnglish'] = True
            lightButton.disableButton()
        else:
            mainLabel.setText('English Plaintext -----> Morse Code Ciphertext')
            inputLabel.setText('Input English Plaintext:')
            outputLabel.setText('Output Morse Code Ciphertext:')
            self.states['textTranslator_MorseToEnglish'] = False
            lightButton.enableButton()
        self.translate()

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

    def activateLightThread(self):
        if self.states['isDisplayingLight'] == False:
            self.lightThread = threading.Thread(target = self.showLight)
            self.lightThread.start()

    def showLight(self):
        try:
            outputEntry = self.tabObject['outputTextArea']
            text = textValidator.validateMorse(outputEntry.getText())
            if text != False:
                self.states['isDisplayingLight'] = True
                text = text.replace(' / ','/')
                text = text.replace('.','.#')
                text = text.replace('-','-#')
                text = text.replace('# ',' ')
                text = text.replace('#/','/')
                timeConvert = {
                    '.':0.480,
                    '-':1.440,
                    '#':0.480,
                    ' ':1.440,
                    '/':3.360
                }
                appLight = Toplevel(app)
                appLight.iconbitmap('iconAssets/morseMasterIcon.ico')
                appLight.title('Light Representation')
                light = Frame(appLight, background = 'white', width = 300, height = 300)
                light.pack()
                light.tkraise()

                def lightOn():
                    light.configure(background = 'white')

                def lightOff():
                    light.configure(background = 'black')
                
                appLight.update()
                time.sleep(0.5)
                lightOff()
                appLight.update()
                for i,c in enumerate(text):
                    time.sleep(timeConvert[c])
                    if c in ('.','-'):
                        lightOn()
                        appLight.update()
                    else:
                        if i < len(text)-1:
                            lightOff()
                            appLight.update()
                time.sleep(0.5)
                self.states['isDisplayingLight'] = False
                appLight.destroy()
            else:
                messagebox.showerror('Light Representer Error', 'Cannot represent invalid text output in light form')
            self.lightThread = None
        except:
            self.states['isDisplayingLight'] = False
            self.lightThread = None

    def openFileDialog(self):
        filePath = askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.openFileProcess(filePath)
        elif filePath != '':
            messagebox.showerror('Upload Error', 'Invalid file path')
            
    def openFileProcess(self, filePath):
        inputEntry = self.tabObject['inputTextArea']
        try:
            with open(filePath, 'r') as f:
                inputEntry.setText(f.read())
            self.translate()
        except:
            messagebox.showerror('File Read Error', 'Error while trying to read the file contents')

    def saveFileDialog(self):
        filePath = asksaveasfile(defaultextension=".txt", title="Save As", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.saveFileProcess(filePath)
        elif filePath != None:
            messagebox.showerror('Download Error', 'Invalid file path')

    def saveFileProcess(self, filePath):
        outputEntry = self.tabObject['outputTextArea']
        if outputEntry.getText() != '' and outputEntry.getText() != ' ':
            with open(filePath.name, 'w') as f:
                f.write(outputEntry.getText())
        else:
            messagebox.showerror('Download Error', 'Cannot save empty text output')


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
        mainLabel, inputLabel, translationDropdown = self.tabObject['translationDirectionLabel'], self.tabObject['inputTextLabel'], self.tabObject['translationDropdown']
        currentValue = translationDropdown.getDropdownValue()
        if self.states['soundGenerator_MorseToSound'] == False and currentValue == 'Morse Code Ciphertext Input':
            mainLabel.setText('Morse Code Ciphertext --> Morse Code Sound File')
            inputLabel.setText('Input Morse Code Ciphertext')
            self.states['soundGenerator_MorseToSound'] = True
        elif self.states['soundGenerator_MorseToSound'] == True and currentValue == 'English Plaintext Input':
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
        if text != '' and text != ' ':
            if self.states['soundGenerator_MorseToSound'] == False:
                validatedText = textValidator.validateEnglish(text)
                if validatedText != False:
                    ciphertext = textParser.parseEnglish(validatedText)
                    self.soundData = soundTranslator.generateSound(ciphertext, frequency, volume, wpm)
            else:
                validatedText = textValidator.validateMorse(text)
                if validatedText != False:
                    self.soundData = soundTranslator.generateSound(validatedText, frequency, volume, wpm)
            if validatedText != False:
                generateTextLabel = self.tabObject['generateTextLabel']
                generateTextLabel.setText('Generated!')
                generateTextLabel.setColour('green')
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                    wavfile.write(tmpfile.name, self.soundRate, self.normaliseData(self.soundData))
                    self.tempDataFilePath = tmpfile.name
                self.playbackManager.load_file(self.tempDataFilePath)
                self.states['generated'] = True
            else:
                messagebox.showerror('Sound Generation Error', 'Invalid text input')
        else:
            messagebox.showerror('Sound Generation Error', 'Invalid text input')

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
        elif filePath != '':
            messagebox.showerror('Upload Error', 'Invalid file path')
            
    def openFileProcess(self, filePath):
        inputEntry = self.tabObject['inputTextArea']
        try:
            with open(filePath, 'r') as f:
                inputEntry.setText(f.read())
        except:
            messagebox.showerror('File Read Error', 'Error while trying to read the file contents')
    
    def saveFileDialog(self):
        if self.states['generated'] == True:
            filePath = asksaveasfilename(defaultextension=".wav", title="Save As", filetypes=[("Audio files", "*.wav")])
            if filePath:
                self.saveFileProcess(filePath)
            elif filePath != None:
                messagebox.showerror('Download Error', 'Invalid file path')
        else:
            messagebox.showerror('Download Error', 'No generated audio to download')

    def saveFileProcess(self, filePath):
        if not(self.soundData is None):
            data = self.normaliseData(self.soundData)
            wavfile.write(filePath, self.soundRate, data)
        else:
            messagebox.showerror('Download Error', 'Cannot save empty sound output')

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
            messagebox.showerror('Playback Error', 'No generated audio to play')

    def pauseSoundFile(self):
        if self.states['generated'] == True:
            self.playbackManager.pause()
        else:
            messagebox.showerror('Playback Error', 'No generated audio to pause')

    def stopSoundFile(self):
        if self.states['generated'] == True:
            self.playbackManager.stop()
            self.playbackManager.seek(0)
        else:
            messagebox.showerror('Playback Error', 'No generated audio to stop')

    def waveformSoundFile(self):
        if self.states['generated'] == True:
            soundTranslator.showWaveform(self.soundData, self.soundRate)
        else:
            messagebox.showerror('Waveform Error', 'No generated audio to show waveform of')


class SoundDecoder(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        self.states = {
            'soundDecoder_SoundToMorse':False,
            'wpmAuto':True,
            'loaded':False,
            'isRecording':False,
            'isDisplayingLight':False
        }
        self.soundData = None
        self.soundRate = 8000
        self.playbackManager = Playback()
        self.tempDataFilePath = None
        self.recorder = PvRecorder(device_index=-1, frame_length=512)
        self.recordThread = None
        self.lightThread = None

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
        self.tabObject['lightButton'].setCommand(self.activateLightThread)
        self.tabObject['downloadButton'].setCommand(self.saveFileDialog)

    def switch(self, *args):
        mainLabel, outputLabel, outputEntry, translationDropdown = self.tabObject['translationDirectionLabel'], self.tabObject['outputTextLabel'], self.tabObject['outputTextArea'], self.tabObject['translationDropdown']
        lightButton = self.tabObject['lightButton']
        currentValue = translationDropdown.getDropdownValue()
        if self.states['soundDecoder_SoundToMorse'] == False and currentValue == 'Morse Code Ciphertext Output':
            mainLabel.setText('Morse Code Sound File --> Morse Code Ciphertext')
            outputLabel.setText('Output Morse Code Ciphertext')
            validatedText = textValidator.validateEnglish(outputEntry.getText())
            if validatedText != False:
                outputEntry.setText(textParser.parseEnglish(validatedText))
            lightButton.enableButton()
            self.states['soundDecoder_SoundToMorse'] = True
        elif self.states['soundDecoder_SoundToMorse'] == True and currentValue == 'English Plaintext Output':
            mainLabel.setText('Morse Code Sound File -----> English Plaintext')
            outputLabel.setText('Output English Plaintext:')
            validatedText = textValidator.validateMorse(outputEntry.getText())
            if validatedText != False:
                outputEntry.setText(textParser.parseMorse(validatedText))
            lightButton.disableButton()
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
        self.soundData = []
        self.recorder.start()
        while self.states['isRecording'] == True:
            frame = self.recorder.read()
            self.soundData.extend(frame)
        self.recorder.stop()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            with wave.open(tmpfile.name, 'w') as f:
                f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
                f.writeframes(struct.pack("h" * len(self.soundData), *self.soundData))
            self.tempDataFilePath = tmpfile.name
        self.playbackManager.load_file(self.tempDataFilePath)
        self.soundData = np.array([[x] for x in self.soundData])
        audioLoadedTextLabel = self.tabObject['audioLoadedTextLabel']
        audioLoadedTextLabel.setText('Audio Loaded!')
        audioLoadedTextLabel.setColour('green')
        self.states['loaded'] = True
        self.recordThread = None

    def recordStartStop(self):
        recordButton = self.tabObject['recordButton']
        if self.states['isRecording'] == False:
            self.states['isRecording'] = True
            recordButton.setImage('iconAssets/recordstop.png')
            audioLoadedTextLabel = self.tabObject['audioLoadedTextLabel']
            audioLoadedTextLabel.setText('Recording Audio...')
            audioLoadedTextLabel.setColour('black')
            self.recordThread = threading.Thread(target = self.recordStart)
            self.recordThread.start()
        else:
            self.states['isRecording'] = False
            recordButton.setImage('iconAssets/record.png')

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
                messagebox.showerror('Decoding Error', 'Invalid sound input')
        else:
            messagebox.showerror('Decoding Error', 'No loaded audio to decode')

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
            messagebox.showerror('Playback Error', 'No loaded audio to play')

    def pauseSoundFile(self):
        if self.states['loaded'] == True:
            self.playbackManager.pause()
        else:
            messagebox.showerror('Playback Error', 'No loaded audio to pause')

    def stopSoundFile(self):
        if self.states['loaded'] == True:
            self.playbackManager.stop()
            self.playbackManager.seek(0)
        else:
            messagebox.showerror('Playback Error', 'No loaded audio to stop')

    def copyText(self):
        outputEntry = self.tabObject['outputTextArea']
        pyperclip.copy(outputEntry.getText())

    def activateLightThread(self):
        if self.states['isDisplayingLight'] == False:
            self.lightThread = threading.Thread(target = self.showLight)
            self.lightThread.start()

    def showLight(self):
        try:
            outputEntry = self.tabObject['outputTextArea']
            text = textValidator.validateMorse(outputEntry.getText())
            if text != False:
                self.states['isDisplayingLight'] = True
                text = text.replace(' / ','/')
                text = text.replace('.','.#')
                text = text.replace('-','-#')
                text = text.replace('# ',' ')
                text = text.replace('#/','/')
                timeConvert = {
                    '.':0.480,
                    '-':1.440,
                    '#':0.480,
                    ' ':1.440,
                    '/':3.360
                }
                appLight = Toplevel(app)
                appLight.iconbitmap('iconAssets/morseMasterIcon.ico')
                appLight.title('Light Representation')
                light = Frame(appLight, background = 'white', width = 300, height = 300)
                light.pack()
                light.tkraise()

                def lightOn():
                    light.configure(background = 'white')

                def lightOff():
                    light.configure(background = 'black')
                
                appLight.update()
                time.sleep(0.5)
                lightOff()
                appLight.update()
                for i,c in enumerate(text):
                    time.sleep(timeConvert[c])
                    if c in ('.','-'):
                        lightOn()
                        appLight.update()
                    else:
                        if i < len(text)-1:
                            lightOff()
                            appLight.update()
                time.sleep(0.5)
                self.states['isDisplayingLight'] = False
                appLight.destroy()
            else:
                messagebox.showerror('Light Representer Error', 'Cannot represent invalid text output in light form')
            self.lightThread = None
        except:
            self.states['isDisplayingLight'] = False
            self.lightThread = None

    def openFileDialog(self):
        filePath = askopenfilename(title="Select a File", filetypes=[("Audio files", "*.wav")])
        if filePath:
            self.openFileProcess(filePath)
        elif filePath != '':
            messagebox.showerror('Upload Error', 'Invalid file path')

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
            messagebox.showerror('File Read Error', 'Error while reading the file')
    
    def saveFileDialog(self):
        filePath = asksaveasfile(defaultextension=".txt", title="Save As", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.saveFileProcess(filePath)
        elif filePath != None:
            messagebox.showerror('Download Error', 'Invalid file path')

    def saveFileProcess(self, filePath):
        outputEntry = self.tabObject['outputTextArea']
        if outputEntry.getText() != '' and outputEntry.getText() != ' ':
            with open(filePath.name, 'w') as f:
                f.write(outputEntry.getText())
        else:
            messagebox.showerror('Download Error', 'Cannot save empty text output')


class Keyer(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        self.states = {
            'paddleMode':'A',
            'isKeying':False,
            'doBeep':False,
            'doStartBeep':False,
            'isBlockingBeep':False,
            'doStartBeepType':False,
            'isBlockingRelease':False,
        }
        self.keyDownTimes = {}
        self.keyUpTime = -1
        mixer.init()
        self.beepSound = self.getBeepSound(600)
        self.beepThread = threading.Thread(target = self.activateBeep)
        self.beepThread.daemon = True
        self.beepThread.start()
        self.keyboardThread = threading.Thread(target = self.activateKeyboardListener)
        self.keyboardThread.daemon = True
        self.keyboardThread.start()
        self.wordTerminatorThread = threading.Thread(target = self.activateWordTerminatorThread)
        self.wordTerminatorThread.daemon = True
        self.wordTerminatorThread.start()

        self.tabObject['keyButton1'].setBinding('<Button-1>', self.button1Down)
        self.tabObject['keyButton1'].setBinding('<ButtonRelease-1>', self.button1Up)
        self.tabObject['keyButton2'].setBinding('<Button-1>', self.button2Down)
        self.tabObject['keyButton2'].setBinding('<ButtonRelease-1>', self.button2Up)
        def tryFocusSet(event):
            try:
                event.widget.focus_set()
            except:
                pass
        app.tabBar.keyerTab.bind_all('<Button-1>', lambda event: tryFocusSet(event))
        self.tabObject['switchButton'].setCommand(self.switch)
        self.tabObject['frequencySlider'].setCommand(self.matchTextEntries)
        self.tabObject['wpmSlider'].setCommand(self.matchTextEntries)
        f = self.tabObject['frequencyTextEntry']
        w = self.tabObject['wpmTextEntry']
        f.text.trace_add('write', self.matchSliders)
        w.text.trace_add('write', self.matchSliders)
        self.tabObject['deleteButton'].setCommand(self.clearBoxes)
        self.tabObject['copyButton'].setCommand(self.copyText)
        self.tabObject['downloadButton'].setCommand(self.saveFileDialog)
        self.tabObject['legendButton'].setCommand(self.showLegend)

    def getBeepSound(self, frequency):
        beepSoundData = np.sin(2 * np.pi * frequency * (np.linspace(0, 20, 882000)))
        beepSoundData = beepSoundData / np.max(np.abs(beepSoundData))
        beepSoundData = np.column_stack((beepSoundData, beepSoundData))
        beepSound = sndarray.make_sound((beepSoundData * 32767).astype(np.int16))
        return beepSound

    def activateKeyboardListener(self):
        with keyboard.Listener(on_press = self.keyDown, on_release = self.keyUp) as self.listener:
            self.listener.join()

    def activateBeep(self):
        while True:
            time.sleep(0.01)
            if self.states['paddleMode'] == 'A':
                if self.states['doStartBeep'] == True:
                    self.states['doStartBeep'] = False
                    try:
                        sound = mixer.Sound(self.beepSound)
                        sound.play()
                    except:
                        pass
                if self.states['doBeep'] == False:
                    if mixer.get_busy():
                        try:
                            sound.stop()
                        except:
                            pass
            else:
                if self.states['doStartBeepType'] != False:
                    self.states['isBlockingBeep'] = True
                    if self.states['doStartBeepType'] == '.':
                        sound = mixer.Sound(self.beepSound)
                        sound.play()
                        time.sleep(self.getUnit())
                        sound.stop()
                    else:
                        sound = mixer.Sound(self.beepSound)
                        sound.play()
                        time.sleep(self.getUnit()*2.5)
                        sound.stop()
                    self.states['isBlockingBeep'] = False
                    self.states['doStartBeepType'] = False

    def button1Down(self, *args):
        if self.states['isBlockingBeep'] == False:
            T = time.time()
            duration = 0
            if self.keyUpTime != -1:
                t = self.keyUpTime
                duration = round(T - t, 2)
            self.keyDownTimes['button1'] = T
            if self.states['paddleMode'] == 'A':
                self.updateDisplay(duration, None, True)
                self.states['doBeep'], self.states['doStartBeep'] = True, True
            else:
                self.updateDisplay(duration, None, True)
                self.states['doStartBeepType'] = '.'
        else:
            self.states['isBlockingRelease'] = True

    def button1Up(self, *args):
        if self.states['isBlockingRelease'] == False:
            t = self.keyDownTimes.pop('button1')
            T = time.time()
            duration = round(T - t, 2)
            self.keyUpTime = T
            self.updateDisplay(duration, 'button1', False)
            if self.states['paddleMode'] == 'A':
                self.states['doBeep'] = False
        else:
            self.states['isBlockingRelease'] = False

    def button2Down(self, *args):
        if self.states['isBlockingBeep'] == False:
            T = time.time()
            duration = 0
            if self.keyUpTime != -1:
                t = self.keyUpTime
                duration = round(T - t, 2)
            self.keyDownTimes['button2'] = T
            self.updateDisplay(duration, None, True)
            self.states['doStartBeepType'] = '-'
        else:
            self.states['isBlockingRelease'] = True

    def button2Up(self, *args):
        if self.states['isBlockingRelease'] == False:
            t = self.keyDownTimes.pop('button2')
            T = time.time()
            duration = round(T - t, 2)
            self.keyUpTime = T
            self.updateDisplay(duration, 'button2', False)
        else:
            self.states['isBlockingRelease'] = False

    def keyDown(self, key):
        if app.tabBar.select() == '.!tabbar.!frame4' and app.focus_displayof() != None:
            if self.states['isBlockingBeep'] == False:
                if key not in self.keyDownTimes and app.tabBar.tab(app.tabBar.select(), "text") == 'Keyer' and not(str(self.tabObject['outputTextArea']) in str(app.focus_get())):
                    T = time.time()
                    isKey = False
                    if hasattr(key, 'char'):
                        if key.char in ('.',','):
                            isKey = True
                            keyName = key.char
                    elif hasattr(key, 'name'):
                        if key.name == 'space' and self.states['paddleMode'] == 'A':
                            isKey = True
                            keyName = key.name
                    if isKey:
                        if self.keyUpTime != -1:
                            t = self.keyUpTime
                            duration = round(T - t, 2)
                            self.updateDisplay(duration, keyName, True)
                        if self.states['paddleMode'] == 'A':
                            self.states['doBeep'], self.states['doStartBeep'] = True, True
                        else:
                            if keyName == '.':
                                self.states['doStartBeepType'] = '-'
                            else:
                                self.states['doStartBeepType'] = '.'
                    self.keyDownTimes[key] = T
            else:
                self.states['isBlockingRelease'] = True
    
    def keyUp(self, key):
        if app.tabBar.select() == '.!tabbar.!frame4' and app.focus_displayof() != None:
            if self.states['isBlockingRelease'] == False:
                if key in self.keyDownTimes:
                    t = self.keyDownTimes.pop(key)
                    T = time.time()
                    duration = round(T - t, 2)
                    isKey = False
                    if hasattr(key, 'char'):
                        if key.char in ('.',','):
                            isKey = True
                            keyName = key.char
                    elif hasattr(key, 'name'):
                        if key.name == 'space' and self.states['paddleMode'] == 'A':
                            isKey = True
                            keyName = key.name
                    if isKey:
                        if self.states['paddleMode'] == 'A':
                            time.sleep(0.001)
                            self.updateDisplay(duration, keyName, False)
                            self.states['doBeep'] = False
                        else:
                            self.updateDisplay(duration, keyName, False)
                    self.keyUpTime = T
            else:
                self.states['isBlockingRelease'] = False

    def activateWordTerminatorThread(self):
        while True:
            time.sleep(0.01)
            if self.states['isKeying'] == True:
                self.tabObject['switchButton'].disableButton()
                self.tabObject['frequencySlider'].disableSlider()
                self.tabObject['wpmSlider'].disableSlider()
                self.tabObject['frequencyTextEntry'].disableEntry()
                self.tabObject['wpmTextEntry'].disableEntry()
                ut = self.keyUpTime
                dt = 0.0
                if len(self.keyDownTimes.values()) > 0:
                    dt = max(self.keyDownTimes.values())
                if ut != -1:
                    T = time.time()
                    unit = self.getUnit()
                    if T - ut >= float(8*unit) and T - dt >= float(8*unit):
                        self.keyDownTimes = {}
                        self.keyUpTime = -1
                        self.tabObject['outputTextArea'].setText(self.tabObject['outputTextArea'].getText() + self.tabObject['englishCurrentLabel'].getText() + ' ')
                        self.tabObject['englishCurrentLabel'].setText('')
                        self.tabObject['morseCurrentLabel'].setText('')
                        self.tabObject['switchButton'].enableButton()
                        self.tabObject['frequencySlider'].enableSlider()
                        self.tabObject['wpmSlider'].enableSlider()
                        self.tabObject['frequencyTextEntry'].enableEntry()
                        self.tabObject['wpmTextEntry'].enableEntry()
                        self.states['isKeying'] = False
                        self.states['doBeep'] = False
                        self.states['doStartBeep'] = False
                        self.states['isBlockingBeep'] = False
                        self.states['doStartBeepType'] = False
                        self.states['isBlockingRelease'] = False
                        mixer.stop()

    def updateDisplay(self, duration, keyName, isGap):
        englishCurrentLabel, morseCurrentLabel = self.tabObject['englishCurrentLabel'], self.tabObject['morseCurrentLabel']
        self.states['isKeying'] = True
        if self.states['paddleMode'] == 'A':
            unit = self.getUnit()
            if isGap:
                if duration > 2.5*unit:
                    morseCurrentLabel.setText(morseCurrentLabel.getText() + ' ')
            else:
                if duration > 2*unit:
                    newText = morseCurrentLabel.getText() + '-'
                else:
                    newText = morseCurrentLabel.getText() + '.'
                morseCurrentLabel.setText(newText)
                englishCurrentLabel.setText(textParser.parseMorseKeying(newText))
        else:
            unit = self.getUnit()
            if isGap:
                if duration > 2.5*unit:
                    morseCurrentLabel.setText(morseCurrentLabel.getText() + ' ')
            else:
                if keyName in (',', 'button1'):
                    newText = morseCurrentLabel.getText() + '.'
                else:
                    newText = morseCurrentLabel.getText() + '-'
                morseCurrentLabel.setText(newText)
                englishCurrentLabel.setText(textParser.parseMorseKeying(newText))
    
    def getUnit(self):
        wpmSlider = self.tabObject['wpmSlider']
        wpm = wpmSlider.getSliderValue()
        unit = 60/(50*wpm)
        return unit

    def switch(self):
        paddleModeLabel, keyButton2, keyTextLabel = self.tabObject['paddleModeLabel'], self.tabObject['keyButton2'], self.tabObject['keyTextLabel']
        if self.states['paddleMode'] == 'A':
            self.states['paddleMode'] = 'B'
            paddleModeLabel.setText('Paddle Mode B')
            paddleModeLabel.setColour('Green')
            keyButton2.enableButton()
            keyTextLabel.setText('Tap buttons or press comma / full stop')
        else:
            self.states['paddleMode'] = 'A'
            paddleModeLabel.setText('Paddle Mode A')
            paddleModeLabel.setColour('Dark Blue')
            keyButton2.disableButton()
            keyTextLabel.setText('Tap button or press spacebar / comma / full stop')
        app.focus_set()
    
    def matchSliders(self, *args):
        frequencyEntry, wpmEntry = self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry']
        frequency, wpm = frequencyEntry.getText(), wpmEntry.getText(),
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider']]
        try:
            frequency = float(frequency)
            sliders[0].setSliderValue(frequency)
            if frequency >= 400 and frequency <= 1000:
                self.beepSound = self.getBeepSound(int(frequency))
        except ValueError:
            pass
        try:
            wpm = float(wpm)
            sliders[1].setSliderValue(wpm)
        except ValueError:
            pass

    def matchTextEntries(self, *args):
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider']]
        frequency, wpm = str(sliders[0].getSliderValue()), str(sliders[1].getSliderValue())
        frequencyEntry, wpmEntry = self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry']
        frequencyEntry.setText(frequency)
        self.beepSound = self.getBeepSound(int(frequency))
        wpmEntry.setText(wpm)

    def copyText(self):
        outputEntry = self.tabObject['outputTextArea']
        pyperclip.copy(outputEntry.getText())
        app.focus_set()

    def clearBoxes(self):
        outputEntry = self.tabObject['outputTextArea']
        outputEntry.clearText()
        app.focus_set()

    def saveFileDialog(self):
        app.focus_set()
        filePath = asksaveasfile(defaultextension=".txt", title="Save As", filetypes=[("Text files", "*.txt")])
        if filePath:
            self.saveFileProcess(filePath)
        elif filePath != None:
            messagebox.showerror('Download Error', 'Invalid file path')

    def saveFileProcess(self, filePath):
        outputEntry = self.tabObject['outputTextArea']
        if outputEntry.getText() != '' and outputEntry.getText() != ' ':
            with open(filePath.name, 'w') as f:
                f.write(outputEntry.getText())
        else:
            messagebox.showerror('Download Error', 'Cannot save empty text output')

    def showLegend(self):
        app.focus_set()
        englishChars = list(textParser.morseDict.keys())
        morseChars = list(textParser.morseDict.values())
        column1 = [englishChars[i] + '   ' + morseChars[i] for i in range(0,19)]
        column2 = [englishChars[i] + '   ' + morseChars[i] for i in range(19,38)]
        column3 = [englishChars[i] + '   ' + morseChars[i] for i in range(38,len(englishChars))]
        appLegend = Toplevel(app)
        appLegend.iconbitmap('iconAssets/morseMasterIcon.ico')
        appLegend.title('Legend')
        frame1, frame2, frame3 = Frame(appLegend), Frame(appLegend), Frame(appLegend)
        frame1.grid(row = 0, column = 0, sticky = 'n', padx = (5,30))
        frame2.grid(row = 0, column = 1, sticky = 'n', padx = 30)
        frame3.grid(row = 0, column = 2, sticky = 'n', padx = (30,5))
        frame1.tkraise()
        frame2.tkraise()
        frame3.tkraise()
        for c in column1:
            newLabel = Label(frame1, text = c, font = ('Verdana', 10), anchor = 'w')
            newLabel.pack()
            newLabel.tkraise()
        for c in column2:
            newLabel = Label(frame2, text = c, font = ('Verdana', 10), anchor = 'w')
            newLabel.pack()
            newLabel.tkraise()
        for c in column3:
            newLabel = Label(frame3, text = c, font = ('Verdana', 10), anchor = 'w')
            newLabel.pack()
            newLabel.tkraise()


class ChallengeMode(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        self.states = {
            'paddleMode':'A',
            'isKeying':False,
            'doBeep':False,
            'doStartBeep':False,
            'isBlockingBeep':False,
            'doStartBeepType':False,
            'isBlockingRelease':False,
            'acceptFullWordOnly':False,
            'randomiseWordOrder':False,
            'limitWordCount':False,
            'challengeModeStarted':False,
            'doStartTimer':False,
            'hasPlayed':False,
        }
        self.keyDownTimes = {}
        self.currentWordList = self.parseWordList('wordLists/wordList1.txt')
        self.finalWordList = []
        self.incorrectWordList = []
        self.wordListPointer = 0
        self.currentWord = ''
        self.currentWordListType = 'Challenge List 1 - Easy'
        self.wordLimit = 10
        self.timerTime = 0.0
        self.startTime = 0.0
        self.lastResultTime = 0.0
        self.lastResultScore = ''
        self.bestTime = None
        mixer.init()
        self.keyUpTime = -1
        self.beepSound = self.getBeepSound(600)
        self.beepThread = threading.Thread(target = self.activateBeep)
        self.beepThread.daemon = True
        self.beepThread.start()
        self.keyboardThread = threading.Thread(target = self.activateKeyboardListener)
        self.keyboardThread.daemon = True
        self.keyboardThread.start()
        self.wordTerminatorThread = threading.Thread(target = self.activateWordTerminatorThread)
        self.wordTerminatorThread.daemon = True
        self.wordTerminatorThread.start()
        self.timerThread = threading.Thread(target = self.activateTimer)
        self.timerThread.daemon = True
        self.timerThread.start()

        self.tabObject['keyButton1'].setBinding('<Button-1>', self.button1Down)
        self.tabObject['keyButton1'].setBinding('<ButtonRelease-1>', self.button1Up)
        self.tabObject['keyButton2'].setBinding('<Button-1>', self.button2Down)
        self.tabObject['keyButton2'].setBinding('<ButtonRelease-1>', self.button2Up)
        def tryFocusSet(event):
            try:
                event.widget.focus_set()
            except:
                pass
        app.tabBar.challengeModeTab.bind_all('<Button-1>', lambda event: tryFocusSet(event))
        self.tabObject['switchButton'].setCommand(self.switch)
        self.tabObject['wordListButton'].setCommand(self.wordListSettings)
        self.tabObject['modeSettingsButton'].setCommand(self.challengeModeSettings)
        self.tabObject['frequencySlider'].setCommand(self.matchTextEntries)
        self.tabObject['wpmSlider'].setCommand(self.matchTextEntries)
        f = self.tabObject['frequencyTextEntry']
        w = self.tabObject['wpmTextEntry']
        f.text.trace_add('write', self.matchSliders)
        w.text.trace_add('write', self.matchSliders)
        self.tabObject['startButton'].setCommand(self.startChallengeMode)
        self.tabObject['endButton'].setCommand(self.endChallengeMode)
        self.tabObject['endButton'].disableButton()
        self.tabObject['statsButton'].setCommand(self.challengeModeStats)
        self.tabObject['legendButton'].setCommand(self.showLegend)

    def getBeepSound(self, frequency):
        beepSoundData = np.sin(2 * np.pi * frequency * (np.linspace(0, 20, 882000)))
        beepSoundData = beepSoundData / np.max(np.abs(beepSoundData))
        beepSoundData = np.column_stack((beepSoundData, beepSoundData))
        beepSound = sndarray.make_sound((beepSoundData * 32767).astype(np.int16))
        return beepSound

    def activateKeyboardListener(self):
        with keyboard.Listener(on_press = self.keyDown, on_release = self.keyUp) as self.listener:
            self.listener.join()

    def activateBeep(self):
        while True:
            time.sleep(0.01)
            if self.states['paddleMode'] == 'A':
                if self.states['doStartBeep'] == True:
                    self.states['doStartBeep'] = False
                    try:
                        sound = mixer.Sound(self.beepSound)
                        sound.play()
                    except:
                        pass
                if self.states['doBeep'] == False:
                    if mixer.get_busy():
                        try:
                            sound.stop()
                        except:
                            pass
            else:
                if self.states['doStartBeepType'] != False:
                    self.states['isBlockingBeep'] = True
                    if self.states['doStartBeepType'] == '.':
                        sound = mixer.Sound(self.beepSound)
                        sound.play()
                        time.sleep(self.getUnit())
                        sound.stop()
                    else:
                        sound = mixer.Sound(self.beepSound)
                        sound.play()
                        time.sleep(self.getUnit()*2.5)
                        sound.stop()
                    self.states['isBlockingBeep'] = False
                    self.states['doStartBeepType'] = False

    def button1Down(self, *args):
        if self.states['challengeModeStarted'] == True:
            if self.states['isBlockingBeep'] == False:
                T = time.time()
                duration = 0
                if self.keyUpTime != -1:
                    t = self.keyUpTime
                    duration = round(T - t, 2)
                self.keyDownTimes['button1'] = T
                if self.states['paddleMode'] == 'A':
                    self.updateDisplay(duration, None, True)
                    self.states['doBeep'], self.states['doStartBeep'] = True, True
                else:
                    self.updateDisplay(duration, None, True)
                    self.states['doStartBeepType'] = '.'
            else:
                self.states['isBlockingRelease'] = True

    def button1Up(self, *args):
        if self.states['challengeModeStarted'] == True:
            if self.states['isBlockingRelease'] == False:
                t = self.keyDownTimes.pop('button1')
                T = time.time()
                duration = round(T - t, 2)
                self.keyUpTime = T
                self.updateDisplay(duration, 'button1', False)
                if self.states['paddleMode'] == 'A':
                    self.states['doBeep'] = False
            else:
                self.states['isBlockingRelease'] = False

    def button2Down(self, *args):
        if self.states['challengeModeStarted'] == True:
            if self.states['isBlockingBeep'] == False:
                T = time.time()
                duration = 0
                if self.keyUpTime != -1:
                    t = self.keyUpTime
                    duration = round(T - t, 2)
                self.keyDownTimes['button2'] = T
                self.updateDisplay(duration, None, True)
                self.states['doStartBeepType'] = '-'
            else:
                self.states['isBlockingRelease'] = True

    def button2Up(self, *args):
        if self.states['challengeModeStarted'] == True:
            if self.states['isBlockingRelease'] == False:
                t = self.keyDownTimes.pop('button2')
                T = time.time()
                duration = round(T - t, 2)
                self.keyUpTime = T
                self.updateDisplay(duration, 'button2', False)
            else:
                self.states['isBlockingRelease'] = False

    def keyDown(self, key):
        if app.tabBar.select() == '.!tabbar.!frame5' and app.focus_displayof() != None:
            if self.states['challengeModeStarted'] == True:
                if self.states['isBlockingBeep'] == False:
                    if key not in self.keyDownTimes and app.tabBar.tab(app.tabBar.select(), "text") == 'Challenge Mode':
                        T = time.time()
                        isKey = False
                        if hasattr(key, 'char'):
                            if key.char in ('.',','):
                                isKey = True
                                keyName = key.char
                        elif hasattr(key, 'name'):
                            if key.name == 'space' and self.states['paddleMode'] == 'A':
                                isKey = True
                                keyName = key.name
                        if isKey:
                            if self.keyUpTime != -1:
                                t = self.keyUpTime
                                duration = round(T - t, 2)
                                self.updateDisplay(duration, keyName, True)
                            if self.states['paddleMode'] == 'A':
                                self.states['doBeep'], self.states['doStartBeep'] = True, True
                            else:
                                if keyName == '.':
                                    self.states['doStartBeepType'] = '-'
                                else:
                                    self.states['doStartBeepType'] = '.'
                        self.keyDownTimes[key] = T
                else:
                    self.states['isBlockingRelease'] = True
    
    def keyUp(self, key):
        if app.tabBar.select() == '.!tabbar.!frame5' and app.focus_displayof() != None:
            if self.states['challengeModeStarted'] == True:
                if self.states['isBlockingRelease'] == False:
                    if key in self.keyDownTimes:
                        t = self.keyDownTimes.pop(key)
                        T = time.time()
                        duration = round(T - t, 2)
                        isKey = False
                        if hasattr(key, 'char'):
                            if key.char in ('.',','):
                                isKey = True
                                keyName = key.char
                        elif hasattr(key, 'name'):
                            if key.name == 'space' and self.states['paddleMode'] == 'A':
                                isKey = True
                                keyName = key.name
                        if isKey:
                            if self.states['paddleMode'] == 'A':
                                self.updateDisplay(duration, keyName, False)
                                self.states['doBeep'] = False
                            else:
                                self.updateDisplay(duration, keyName, False)
                        self.keyUpTime = T
                else:
                    self.states['isBlockingRelease'] = False

    def activateWordTerminatorThread(self):
        while True:
            time.sleep(0.01)
            if self.states['isKeying'] == True:
                self.tabObject['switchButton'].disableButton()
                self.tabObject['frequencySlider'].disableSlider()
                self.tabObject['wpmSlider'].disableSlider()
                self.tabObject['frequencyTextEntry'].disableEntry()
                self.tabObject['wpmTextEntry'].disableEntry()
                ut = self.keyUpTime
                dt = 0.0
                if len(self.keyDownTimes.values()) > 0:
                    dt = max(self.keyDownTimes.values())
                if ut != -1:
                    T = time.time()
                    unit = self.getUnit()
                    if T - ut >= float(8*unit) and T - dt >= float(8*unit):
                        self.keyDownTimes = {}
                        self.keyUpTime = -1
                        morseText = self.tabObject['morseCurrentLabel'].getText()
                        self.tabObject['morseCurrentLabel'].setText('')
                        self.tabObject['switchButton'].enableButton()
                        self.tabObject['frequencySlider'].enableSlider()
                        self.tabObject['wpmSlider'].enableSlider()
                        self.tabObject['frequencyTextEntry'].enableEntry()
                        self.tabObject['wpmTextEntry'].enableEntry()
                        self.states['isKeying'] = False
                        self.states['doBeep'] = False
                        self.states['doStartBeep'] = False
                        self.states['isBlockingBeep'] = False
                        self.states['doStartBeepType'] = False
                        self.states['isBlockingRelease'] = False
                        mixer.stop()
                        self.checkAnswer(morseText)

    def updateDisplay(self, duration, keyName, isGap):
        morseCurrentLabel =  self.tabObject['morseCurrentLabel']
        self.states['isKeying'] = True
        if self.states['paddleMode'] == 'A':
            unit = self.getUnit()
            if isGap:
                if duration > 2.5*unit:
                    morseCurrentLabel.setText(morseCurrentLabel.getText() + ' ')
            else:
                if duration > 2*unit:
                    newText = morseCurrentLabel.getText() + '-'
                else:
                    newText = morseCurrentLabel.getText() + '.'
                morseCurrentLabel.setText(newText)
        else:
            unit = self.getUnit()
            if isGap:
                if duration > 2.5*unit:
                    morseCurrentLabel.setText(morseCurrentLabel.getText() + ' ')
            else:
                if keyName in (',', 'button1'):
                    newText = morseCurrentLabel.getText() + '.'
                else:
                    newText = morseCurrentLabel.getText() + '-'
                morseCurrentLabel.setText(newText)
    
    def getUnit(self):
        wpmSlider = self.tabObject['wpmSlider']
        wpm = wpmSlider.getSliderValue()
        unit = 60/(50*wpm)
        return unit

    def switch(self):
        paddleModeLabel, keyButton2, keyTextLabel = self.tabObject['paddleModeLabel'], self.tabObject['keyButton2'], self.tabObject['keyTextLabel']
        if self.states['paddleMode'] == 'A':
            self.states['paddleMode'] = 'B'
            paddleModeLabel.setText('Paddle Mode B')
            paddleModeLabel.setColour('Green')
            keyButton2.enableButton()
            keyTextLabel.setText('Tap buttons or press comma / full stop')
        else:
            self.states['paddleMode'] = 'A'
            paddleModeLabel.setText('Paddle Mode A')
            paddleModeLabel.setColour('Dark Blue')
            keyButton2.disableButton()
            keyTextLabel.setText('Tap button or press spacebar / comma / full stop')
        app.focus_set()

    def matchSliders(self, *args):
        frequencyEntry, wpmEntry = self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry']
        frequency, wpm = frequencyEntry.getText(), wpmEntry.getText(),
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider']]
        try:
            frequency = float(frequency)
            sliders[0].setSliderValue(frequency)
            if frequency >= 400 and frequency <= 1000:
                self.beepSound = self.getBeepSound(int(frequency))
        except ValueError:
            pass
        try:
            wpm = float(wpm)
            sliders[1].setSliderValue(wpm)
        except ValueError:
            pass

    def matchTextEntries(self, *args):
        sliders = [self.tabObject['frequencySlider'], self.tabObject['wpmSlider']]
        frequency, wpm = str(sliders[0].getSliderValue()), str(sliders[1].getSliderValue())
        frequencyEntry, wpmEntry = self.tabObject['frequencyTextEntry'], self.tabObject['wpmTextEntry']
        frequencyEntry.setText(frequency)
        self.beepSound = self.getBeepSound(int(frequency))
        wpmEntry.setText(wpm)

    def showLegend(self):
        app.focus_set()
        englishChars = list(textParser.morseDict.keys())
        morseChars = list(textParser.morseDict.values())
        column1 = [englishChars[i] + '   ' + morseChars[i] for i in range(0,19)]
        column2 = [englishChars[i] + '   ' + morseChars[i] for i in range(19,38)]
        column3 = [englishChars[i] + '   ' + morseChars[i] for i in range(38,len(englishChars))]
        appLegend = Toplevel(app)
        appLegend.iconbitmap('iconAssets/morseMasterIcon.ico')
        appLegend.title('Legend')
        frame1, frame2, frame3 = Frame(appLegend), Frame(appLegend), Frame(appLegend)
        frame1.grid(row = 0, column = 0, sticky = 'n', padx = (5,30))
        frame2.grid(row = 0, column = 1, sticky = 'n', padx = 30)
        frame3.grid(row = 0, column = 2, sticky = 'n', padx = (30,5))
        frame1.tkraise()
        frame2.tkraise()
        frame3.tkraise()
        for c in column1:
            newLabel = Label(frame1, text = c, font = ('Verdana', 10), anchor = 'w')
            newLabel.pack()
            newLabel.tkraise()
        for c in column2:
            newLabel = Label(frame2, text = c, font = ('Verdana', 10), anchor = 'w')
            newLabel.pack()
            newLabel.tkraise()
        for c in column3:
            newLabel = Label(frame3, text = c, font = ('Verdana', 10), anchor = 'w')
            newLabel.pack()
            newLabel.tkraise()

    def wordListSettings(self):
        def ok():
            #OK button to modify word list variable
            if self.checkTextEntry(WLSentry.getText()):
                self.currentWordList = [word for word in WLSentry.getText().replace('\n',' ').split(' ')]
                self.currentWordListType = WLSdropdown.getDropdownValue()
                appWLS.destroy()
            else:
                messagebox.showerror('Word List Error', 'Invalid format for word list')
        
        def overwriteWithTemplate(*args):
            #overwrite text entry contents with the template word lists when selected
            dropdownValue = WLSdropdown.getDropdownValue()
            if dropdownValue == 'Challenge List 1 - Easy':
                text = '\n'.join(self.parseWordList('wordLists/wordList1.txt'))
                WLSentry.setText(text)
            elif dropdownValue == 'Challenge List 2 - Intermediate':
                text = '\n'.join(self.parseWordList('wordLists/wordList2.txt'))
                WLSentry.setText(text)
            elif dropdownValue == 'Challenge List 3 - Hard':
                text = '\n'.join(self.parseWordList('wordLists/wordList3.txt'))
                WLSentry.setText(text)

        def cancel():
            #Cancel button to destroy window without saving any changes to the variables
            appWLS.destroy()

        def defaultToCustomWordList(*args):
            #default to custom word list on initialisation
            WLSdropdown.setDropdownValue('Custom Word List')

        def openFileProcess(filePath):
            #Reads in text from text file, and writes it straight to the text box
            try:
                with open(filePath, 'r') as f:
                    WLSentry.setText(f.read())
                    uploadTextPrompt.setColour('green')
                    uploadTextPrompt.setText('File Uploaded')
                    defaultToCustomWordList()
                    appWLS.lift()
            except:
                messagebox.showerror('File Read Error', 'Error while trying to read the file contents')

        def openFileDialog(*args):
            #checks file path is valid, then calls openFileProcess on that filepath
            filePath = askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt")])
            if filePath:
                openFileProcess(filePath)
            elif filePath != '':
                messagebox.showerror('Upload Error', 'Invalid file path')
        
        app.focus_set()
        appWLS = Toplevel(app)
        appWLS.iconbitmap('iconAssets/morseMasterIcon.ico')
        appWLS.title('Word List Settings')
        wordListTextPrompt = Label(appWLS, text = 'Enter Word List:', font = ('Verdana', 10), anchor = 'w')
        WLSentry = TextEntry(appWLS)
        WLSentry.setCommand('<Button-1>', defaultToCustomWordList)
        #this binding ensures that the dropdown automatically switches to 'Custom Word List' upon clicking the entry boxes
        currentText = '\n'.join(self.currentWordList)
        WLSentry.setText(currentText)
        WLSdropdown = Dropdown(appWLS, valueTuple = ('Challenge List 1 - Easy', 'Challenge List 2 - Intermediate', 'Challenge List 3 - Hard', 'Custom Word List'))
        WLSdropdown.setDropdownValue(self.currentWordListType)
        WLSdropdown.setCommand('<<ComboboxSelected>>', overwriteWithTemplate)
        #this binding ensures that the entry box is overwritten with the template word lists when they are selected
        uploadButton = ButtonIcon(appWLS, filename = 'iconAssets/upload.png', command = openFileDialog)
        uploadTextPrompt = TextLabelDynamic(appWLS, colour = 'red')
        uploadTextPrompt.setText('No File Uploaded')
        cancelButton = ButtonText(appWLS, text = 'Cancel', command = cancel)
        okButton = ButtonText(appWLS, text = 'OK', command = ok)

        wordListTextPrompt.grid(row = 0, column = 0, columnspan = 2, sticky = 'nw', pady = (5,0), padx = 10)
        WLSentry.grid(row = 1, column = 0, columnspan = 2, pady = (10,20))
        WLSdropdown.grid(row = 2, column = 0, columnspan = 2, pady = (0,20))
        uploadButton.grid(row = 3, column = 0, pady = (0,20))
        uploadTextPrompt.grid(row = 3, column = 1, pady = (0, 20), padx = (20,0), sticky = 'w')
        okButton.grid(row = 4, column = 1, padx = (0, 40), pady = (0, 10))
        cancelButton.grid(row = 4, column = 0, pady = (0, 10))
        wordListTextPrompt.tkraise()
        uploadTextPrompt.tkraise()
        WLSdropdown.tkraise()
        WLSentry.tkraise()
        okButton.tkraise()
        cancelButton.tkraise()

    def sanitiseWordList(self, wordList):
        #sanitisation in case of invalid input for English plaintext
        newWordList = []
        for word in wordList:
            newWord = textValidator.validateEnglish(word)
            if newWord:
                newWordList.append(newWord)
        return newWordList

    def parseWordList(self, filePath):
        #parse the word list from the text file and validate that it follows the proper data formatting
        #show warning messagebox if validation fails
        try:
            f = open(filePath, 'r')
            contents = f.read()
            contents = contents.replace('\n',' ')
            if contents.replace(' ','') == '':
                messagebox.showerror('File Read Error', 'Error while reading the file')
            else:
                wordList = contents.split(' ')
                wordList = self.sanitiseWordList(wordList)
                if wordList == []:
                    messagebox.showerror('File Read Error', 'Error while reading the file')
                else:
                    return wordList
        except:
            messagebox.showerror('File Read Error', 'Error while reading the file')
    
    def checkTextEntry(self, textEntry):
        #checks if word list in the text entry box is not empty and contains only valid characters
        textEntry = textEntry.replace('\n', ' ')
        if textEntry.replace(' ','') == '':
            return False
        wordList = [word for word in textEntry.split(' ')]
        for word in wordList:
            if textValidator.validateEnglish(word) != word:
                return False
        return True

    def challengeModeSettings(self):
        def ok():
            #OK button to modify challenge mode states
            acceptFullWordOnly = acceptFullWordOnlyCheckbox.getValue()
            randomiseWordOrder = randomiseWordOrderCheckbox.getValue()
            limitWordCount = limitWordCountCheckbox.getValue()
            limitWordCountValue = noOfWordsSpinbox.getValue()
            self.states['acceptFullWordOnly'] = acceptFullWordOnly
            self.states['randomiseWordOrder'] = randomiseWordOrder
            self.states['limitWordCount'] = limitWordCount
            self.wordLimit = int(limitWordCountValue)
            appCMS.destroy()

        def cancel():
            #Cancel buutton to destroy subwindow without saving any changes to the variables
            appCMS.destroy()

        def matchSpinbox():
            newState = limitWordCountCheckbox.getValue()
            if newState == True:
                noOfWordsSpinbox.enableSpinbox()
            else:
                noOfWordsSpinbox.disableSpinbox()
        
        app.focus_set()
        appCMS = Toplevel(app)
        appCMS.iconbitmap('iconAssets/morseMasterIcon.ico')
        appCMS.title('Word List Settings')
        acceptFullWordOnlyCheckbox = Checkbox(appCMS, text = 'Accept full word only', initialState = True)
        randomiseWordOrderCheckbox = Checkbox(appCMS, text = 'Randomise word order', initialState = False)
        limitWordCountCheckbox = Checkbox(appCMS, text = 'Limit number of words', initialState = False, command = matchSpinbox)
        noOfWordsTextPrompt = Label(appCMS, text = 'Number of words:', font = ('Verdana', 10), anchor = 'e')
        noOfWordsSpinbox = Spinbox(appCMS)
        acceptFullWordOnlyCheckbox.setValue(self.states['acceptFullWordOnly'])
        randomiseWordOrderCheckbox.setValue(self.states['randomiseWordOrder'])
        limitWordCountCheckbox.setValue(self.states['limitWordCount'])
        noOfWordsSpinbox.setValue(self.wordLimit)
        if not self.states['limitWordCount']:
            noOfWordsSpinbox.disableSpinbox()
        cancelButton = ButtonText(appCMS, text = 'Cancel', command = cancel)
        okButton = ButtonText(appCMS, text = 'OK', command = ok)

        acceptFullWordOnlyCheckbox.grid(row = 0, column = 0, columnspan = 2, padx = (20,15), pady = (20,0))
        randomiseWordOrderCheckbox.grid(row = 1, column = 0, columnspan = 2, padx = (20,15), pady = (5,0))
        limitWordCountCheckbox.grid(row = 2, column = 0, columnspan = 2, padx = (20,15), pady = (5,0))
        noOfWordsTextPrompt.grid(row = 3, column = 0, padx = (40,0), pady = (5,0))
        noOfWordsSpinbox.grid(row = 3, column = 1, pady = (3,0), padx = (0,10))
        cancelButton.grid(row = 4, column = 0, padx = (25,0), pady = (15,15), sticky = 'w')
        okButton.grid(row = 4, column = 1, padx = (0,20), pady = (15,15), sticky = 'w')

        acceptFullWordOnlyCheckbox.tkraise()
        randomiseWordOrderCheckbox.tkraise()
        limitWordCountCheckbox.tkraise()
        noOfWordsTextPrompt.tkraise()
        noOfWordsSpinbox.tkraise()
        cancelButton.tkraise()
        okButton.tkraise()
    
    def startChallengeMode(self):
        #initialise Challenge Mode
        #enable keying options, start the timer, and begin asking words
        app.focus_set()
        self.tabObject['wordListButton'].disableButton()
        self.tabObject['modeSettingsButton'].disableButton()
        self.tabObject['statsButton'].disableButton()
        self.tabObject['startButton'].disableButton()
        self.tabObject['endButton'].enableButton()
        self.states['challengeModeStarted'] = True
        self.initialiseWordList()
        self.toggleTimer()
        self.states['doStartTimer'] = True
        self.displayNextWord()

    def toggleTimer(self):
        #toggles timer to reset and start, or stop
        #depends on the challenge mode started state
        timer, counter = self.tabObject['timerLabel'], self.tabObject['counterLabel']
        if self.states['challengeModeStarted'] == True:
            self.startTime = time.time()
            timer.setText('0.0')
            self.states['doStartTimer'] = True
        else:
            self.states['doStartTimer'] = False
            self.lastResultTime = float(timer.getText())
            self.lastResultScore = counter.getText()

    def activateTimer(self):
        #manages timer thread to ensure the correct time is displayed
        timer = self.tabObject['timerLabel']
        while True:
            time.sleep(0.005)
            if self.states['challengeModeStarted'] == True and self.states['doStartTimer'] == True:
                newTime = time.time()
                timeDifference = round(newTime - self.startTime, 2)
                timer.setText(str(timeDifference))

    def initialiseWordList(self):
        #pulls word list from word list settings
        #applies relevant settings to the list
        #including randomisation and word limit
        allWords = self.currentWordList
        if self.states['randomiseWordOrder'] == True:
            random.shuffle(allWords)
        if self.states['limitWordCount'] == True and len(allWords) > self.wordLimit:
            allWords = allWords[:self.wordLimit]
        self.finalWordList = allWords
        self.incorrectWordList = []
        self.wordListPointer = 0

    def displayNextWord(self):
        #get the next word from the word list
        #display this on the screen, updating GUI as appropriate
        nextWord = self.finalWordList[self.wordListPointer]
        self.currentWord = nextWord
        self.tabObject['englishCurrentLabel'].setText(nextWord)
        self.tabObject['counterLabel'].setText(f"{self.wordListPointer+1}/{len(self.finalWordList)}")

    def checkAnswer(self, answer):
        #trace back the user input to check if they keyed the correct word
        #depends on acceptFullWordOnly
        englishCurrentLabel = self.tabObject['englishCurrentLabel']
        englishAnswer = textParser.parseMorseKeying(answer)
        if self.states['acceptFullWordOnly'] == True:
            if englishAnswer == self.currentWord:
                englishCurrentLabel.flash('#65fe08')
                self.wordListPointer += 1
                if self.wordListPointer == len(self.finalWordList):
                    self.endChallengeMode()
                else:
                    self.displayNextWord()
            else:
                if self.currentWord not in self.incorrectWordList:
                    self.incorrectWordList.append(self.currentWord)
                englishCurrentLabel.flash('#ff474c')
        else:
            answerLength = len(englishAnswer)
            remaining = englishCurrentLabel.getRemainingText()
            if answerLength <= len(remaining) and englishAnswer == remaining[:answerLength]:
                englishCurrentLabel.shiftText(answerLength)
            else:
                if self.currentWord not in self.incorrectWordList:
                    self.incorrectWordList.append(self.currentWord)
                englishCurrentLabel.flashRemaining('#ff474c')
            if englishCurrentLabel.isFullyHighlighted():
                time.sleep(0.75)
                self.wordListPointer += 1
                if self.wordListPointer == len(self.finalWordList):
                    self.endChallengeMode()
                else:
                    self.displayNextWord()


    def endChallengeMode(self):
        #ends Challenge Mode and returns to default tab settings
        self.tabObject['startButton'].enableButton()
        self.tabObject['endButton'].disableButton()
        self.tabObject['wordListButton'].enableButton()
        self.tabObject['modeSettingsButton'].enableButton()
        self.tabObject['statsButton'].enableButton()
        self.tabObject['englishCurrentLabel'].setText('')
        self.tabObject['morseCurrentLabel'].setText('')
        self.states['challengeModeStarted'] = False
        self.states['doStartTimer'] = False
        self.lastResultTime = float(self.tabObject['timerLabel'].getText())
        self.lastResultScore = self.tabObject['counterLabel'].getText()
        self.states['hasPlayed'] = True
        self.challengeModeStats()
    
    def challengeModeStats(self):
        #displays statistics (if available) on the previous challenge mode playthrough this session
        #also keeps track of the best time
        def saveFileDialog():
            filePath = asksaveasfile(defaultextension=".txt", title="Save As", filetypes=[("Text files", "*.txt")])
            if filePath:
                saveFileProcess(filePath)
            elif filePath != None:
                messagebox.showerror('Download Error', 'Invalid file path')

        def saveFileProcess(filePath):
            if missedWordsEntry.getText() != '' and missedWordsEntry.getText() != ' ':
                with open(filePath.name, 'w') as f:
                    f.write(missedWordsEntry.getText())
            else:
                messagebox.showerror('Download Error', 'Cannot save empty text output')

        if self.states['hasPlayed'] == True:
            app.focus_set()
            appStats = Toplevel(app)
            appStats.iconbitmap('iconAssets/morseMasterIcon.ico')
            appStats.title('Challenge Mode Stats')
            minutes = str(int(self.lastResultTime // 60.0))
            if len(minutes) < 2:
                minutes = '0' + minutes
            seconds = str(int((self.lastResultTime % 60.0) // 1.0))
            if len(seconds) < 2:
                seconds = '0' + seconds
            milliseconds = str(int(((self.lastResultTime % 60.0) % 1.0)*100))
            if len(milliseconds) < 2:
                milliseconds = '0' + milliseconds
            score = float(self.lastResultScore.split('/')[0])
            lastRecordedTime = TextLabelStatic(appStats, text = f"Last Recorded Time: {minutes}:{seconds}:{milliseconds}")
            lastRecordedScore = TextLabelStatic(appStats, text = f"Last Recorded Score: {self.lastResultScore}")
            averageTimePerWord = TextLabelStatic(appStats, text = f"Average Time Per Word: {round(self.lastResultTime / score, 2)}")
            missedWordsLabel = TextLabelStatic(appStats, text = 'Missed Words:')
            missedWordsEntry = TextEntry(appStats)
            missedWordsEntry.setText('\n'.join(self.incorrectWordList))
            downloadFrame = tk.Frame(appStats)
            downloadLabel = TextLabelStatic(downloadFrame, text = 'Download list as a text file: ')
            downloadButton = ButtonIcon(downloadFrame, filename = 'iconAssets/download.png', command = saveFileDialog)

            lastRecordedTime.grid(row = 0, column = 0, pady = 5, padx = 5, sticky = 'w')
            lastRecordedScore.grid(row = 1, column = 0, pady = 5, padx = 5, sticky = 'w')
            averageTimePerWord.grid(row = 2, column = 0, pady = 5, padx = 5, sticky = 'w')
            missedWordsLabel.grid(row = 3, column = 0, pady = (20,5), padx = 5, sticky = 'w')
            missedWordsEntry.grid(row = 4, column = 0, padx = 5, sticky = 'w')
            downloadFrame.grid(row = 5, column = 0, pady = 5, sticky = 'w')
            downloadLabel.grid(row = 0, column = 0, pady = 5, padx = (5,0), sticky = 'w')
            downloadButton.grid(row = 0, column = 1, pady = 5, sticky = 'w')

            lastRecordedTime.tkraise()
            lastRecordedScore.tkraise()
            averageTimePerWord.tkraise()
            missedWordsLabel.tkraise()
            missedWordsEntry.tkraise()
            downloadLabel.tkraise()
            downloadButton.tkraise()
        else:
            messagebox.showerror('Chellenge Mode Stats Error','No play data available for this session.')


class Networking(TabEventsManager):
    def __init__(self, ref):
        TabEventsManager.__init__(self, ref)
        
        self.tabObject['prepareMessageButton'].setCommand(self.prepareMessage)
        self.tabObject['nicknameTextArea'].setCommand("<KeyRelease>", (self.updateNickname))
        self.nickname = 'MR SAVAGE'
        self.networkThread = threading.Thread(target = self.initialisePeer)
        self.networkThread.daemon = True
        self.networkThread.start()
        self.recipients = {}
        self.morseCodeMessage = '.... .- .--. .--. -.-- / -... .. .-. - .... -.. .- -.-- / -- .-. / ... .- ...- .- --. .'

    def initialisePeer(self):
        self.myNode = networkManager.Peer()

    def prepareMessage(self):
        app.focus_set()
        appPrepareMessage = Toplevel(app)
        appPrepareMessage.iconbitmap('iconAssets/morseMasterIcon.ico')
        appPrepareMessage.title('Challenge Mode Stats')
        sendMessageLabel = TextLabelStatic(appPrepareMessage, text = 'Send Morse Code Message:', anchor = 'w')
        myNicknameLabel = TextLabelStatic(appPrepareMessage, text = f'My Nickname: {self.nickname}', anchor = 'w')
        messageTextArea = TextEntry(appPrepareMessage)
        messageTextArea.setText(self.morseCodeMessage)
        messageTextArea.disableEntry()
        messageRecipientsLabel = TextLabelStatic(appPrepareMessage, text = 'Select Message Recipients', anchor = 'w')
        recipientsListbox = Listbox(appPrepareMessage, width = 40)
        recipientButtonFrame = tk.Frame(appPrepareMessage)
        selectButtonFrame = tk.Frame(recipientButtonFrame)
        refreshButton = ButtonText(selectButtonFrame, text = 'Refresh', command = refresh)
        selectAllButton = ButtonText(selectButtonFrame, text = 'Select All', command = None)
        deselectAllButton = ButtonText(selectButtonFrame, text = 'Deselect All', command = None)
        addFriendButton = ButtonText(recipientButtonFrame, text = 'Add Friend', command = None)
        removeFriendButton = ButtonText(recipientButtonFrame, text = 'Remove Friend', command = None)
        sendButton = ButtonIcon(recipientButtonFrame, filename = 'iconAssets/send.png', command = None)
        
        sendMessageLabel.grid(row = 0, column = 0, sticky = 'w', padx = (10,0))
        myNicknameLabel.grid(row = 1, column = 0, columnspan = 2, sticky = 'w', padx = (10,0))
        messageTextArea.grid(row = 2, column = 0, columnspan = 2, sticky = 'w', padx = (10,0))
        messageRecipientsLabel.grid(row = 3, column = 0, sticky = 'w', pady = (10,0), padx = (10,0))
        recipientsListbox.grid(row = 4, column = 0, columnspan = 2, sticky = 'w', padx = (20,0))
        recipientButtonFrame.grid(row = 5, column = 0, rowspan = 2, columnspan = 2)
        selectButtonFrame.grid(row = 0, column = 0, columnspan = 2)
        refreshButton.grid(row = 0, column = 0, pady = (10,0), padx = (5,0))
        selectAllButton.grid(row = 0, column = 1, pady = (10,0), padx = (15,0))
        deselectAllButton.grid(row = 0, column = 2, pady = (10,0), padx = (15,0))
        addFriendButton.grid(row = 1, column = 0, pady = (10,15), padx = (25,0))
        removeFriendButton.grid(row = 1, column = 1, pady = (10,15), padx = (15,0))
        sendButton.grid(row = 1, column = 2, pady = (10,15), padx = (15,15))

        sendMessageLabel.tkraise()
        myNicknameLabel.tkraise()
        messageRecipientsLabel.tkraise()
        recipientsListbox.tkraise()
        recipientButtonFrame.tkraise()
        refreshButton.tkraise()
        selectAllButton.tkraise()
        deselectAllButton.tkraise()
        addFriendButton.tkraise()
        removeFriendButton.tkraise()
        sendButton.tkraise()
    
        def refresh(self):
            pass
    
    def updateNickname(self):
        newNickname = self.tabObject['nicknameTextArea']
        if newNickname != '':
            self.nickname = newNickname
        else:
            self.nickname = 'MR SAVAGE'


class MenuBarManager:
    def __init__(self, app):
        app.menuBar.options.add_command(label = 'Word List Settings', command = self.wordListSettings)
        app.menuBar.options.add_command(label = 'Challenge Mode Settings', command = self.challengeModeSettings)
        app.menuBar.options.add_command(label = 'See Challenge Stats', command = self.challengeModeStats)
        app.menuBar.help_.add_command(label = 'Show Legend', command = self.showLegend)

    def wordListSettings(self):
        challengeMode.wordListSettings()

    def challengeModeSettings(self):
        challengeMode.challengeModeSettings()

    def showLegend(self):
        keyer.showLegend()
    
    def challengeModeStats(self):
        challengeMode.challengeModeStats()


textTranslator = TextTranslator(app.tabBar.textTranslatorTab.winfo_children())
soundGenerator = SoundGenerator(app.tabBar.soundGeneratorTab.winfo_children())
soundDecoder = SoundDecoder(app.tabBar.soundDecoderTab.winfo_children())
keyer = Keyer(app.tabBar.keyerTab.winfo_children())
challengeMode = ChallengeMode(app.tabBar.challengeModeTab.winfo_children())
networking = Networking(app.tabBar.networkingTab.winfo_children())
menuBarManager = MenuBarManager(app)

app.mainloop()