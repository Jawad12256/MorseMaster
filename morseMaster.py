from guiManager import *

app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,350)

textTranslatorWidgetObjects = app.tabBar.textTranslatorTab.winfo_children()
textTranslatorObject = {}
for widgetObject in textTranslatorWidgetObjects:
    if hasattr(widgetObject, 'Name'):
        textTranslatorObject[widgetObject.Name] = widgetObject

def switch():
    mainLabel, inputLabel, outputLabel = textTranslatorObject['translationDirectionLabel'], textTranslatorObject['inputTextLabel'], textTranslatorObject['outputTextLabel']
    if mainLabel.getText() == 'English Plaintext -----> Morse Code Ciphertext':
        mainLabel.setText('Morse Code Ciphertext -----> English Plaintext')
        inputLabel.setText('Input Morse Code Ciphertext')
        outputLabel.setText('Output English Plaintext')
    else:
        mainLabel.setText('English Plaintext -----> Morse Code Ciphertext')
        inputLabel.setText('Input English Plaintext:')
        outputLabel.setText('Output Morse Code Ciphertext:')

textTranslatorObject['translationDirectionButton'].button.configure(command = switch)

app.mainloop()