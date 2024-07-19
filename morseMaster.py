from guiManager import *
import textParser, textValidator
import pyperclip
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfile

app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,350)
print('_')

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
        self.tabObject['translateButton'].setCommand(self.translate)
        self.tabObject['pasteButton'].setCommand(self.pasteText)
        self.tabObject['deleteButton'].setCommand(self.clearBoxes)
        self.tabObject['copyButton'].setCommand(self.copyText)

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

    def translate(self):
        inputEntry, outputEntry = self.tabObject['inputTextArea'], self.tabObject['outputTextArea']
        if self.states['textTranslator_MorseToEnglish'] == False:
            plaintext = inputEntry.getText()
            validatedPlaintext = textValidator.validateEnglish(plaintext)
            if validatedPlaintext != False:
                ciphertext = textParser.parseEnglish(validatedPlaintext)
                outputEntry.setText(ciphertext)
        else:
            ciphertext = inputEntry.getText()
            validatedCiphertext = textValidator.validateMorse(ciphertext)
            if validatedCiphertext != False:
                plaintext = textParser.parseMorse(validatedCiphertext)
                outputEntry.setText(plaintext)

    def pasteText(self):
        inputEntry = self.tabObject['inputTextArea']
        inputEntry.setText(pyperclip.paste())

    def copyText(self):
        outputEntry = self.tabObject['outputTextArea']
        pyperclip.copy(outputEntry.getText())

    def clearBoxes(self):
        inputEntry, outputEntry = self.tabObject['inputTextArea'], self.tabObject['outputTextArea']
        inputEntry.clearText()
        outputEntry.clearText()


textTranslator = TextTranslator(app.tabBar.textTranslatorTab.winfo_children())

app.mainloop()