'''TEXT VALIDATION MODULE'''
from textParser import morseDict
englishDict = dict((b,a) for a,b in morseDict.items())

def formatMorse(text): #points A3.2, A3.3, A3.4, A3.5
    t = text.replace('\n',' / ')
    for i in range(len(t)-1):
        if t[i] == ' ':
            charPointer = i+1
            while charPointer <= len(t)-1 and t[charPointer] == ' ':
                t = t[:charPointer] + t[(charPointer+1):]
        elif t[i] == '/':
            charPointer = i+1
            while charPointer <= len(t)-1 and t[charPointer] == '/':
                t = t[:charPointer] + t[(charPointer+1):]
    allowedCharacters = [' ','.','-','/']

def validateMorse(text): #points A3.1
    while True:
        if text == '':
            return False
        else:
            pass

def fixInvalidCharacters(text):
    allowedCharacters = [' ','.','-','/']
    characters = [char for char in text]
    newText = ''
    for char in characters:
        if char in allowedCharacters:
            newText += char
    return newText

def fixLineBreaks(text):
    return text.replace('\n',' / ')

def fixRepeatedSpaces(text):
    left = 0
    right = len(text)-1
    while text[left] == ' ':
        left += 1
    while text[right] == ' ':
        right -= 1
    text = text[left:right+1]
    newText = ''
    characters = [char for char in text]
    charPointer = 0
    while charPointer < len(characters)-1:
        if not(characters[charPointer] == ' ' and characters[charPointer+1] == ' '):
            newText += characters[charPointer]
        charPointer += 1
    newText += characters[-1]
    return newText

def fixAdjacentRepeatedWordBreaks(text):
    left = 0
    right = len(text)-1
    while text[left] == '/':
        left += 1
    while text[right] == '/':
        right -= 1
    text = text[left:right+1]
    newText = ''
    characters = [char for char in text]
    charPointer = 0
    while charPointer < len(characters)-1:
        if not(characters[charPointer] == '/' and characters[charPointer+1] == '/'):
            newText += characters[charPointer]
        charPointer += 1
    newText += characters[-1]
    return newText

def fixNonAdjacentRepeatedWordBreaks(text):
    left = 0
    right = len(text)-1
    while text[left] not in ('.','-'):
        left += 1
    while text[right] not in ('.','-'):
        right -= 1
    text = text[left:right+1]
    characters = [char for char in text]
    charPointer = 0
    while charPointer < len(characters):
        if characters[charPointer] == '/':
            replacePointer = charPointer + 1
            while not(characters[replacePointer] in ('.','-') or replacePointer == len(characters)-1):
                replacePointer += 1
            characters = characters[:charPointer+1] + [' '] + characters[replacePointer:]
        charPointer += 1
    newText = ''
    for char in characters:
        newText += char
    return newText

def fixWordBreakSpacing(text):
    characters = [char for char in text]
    spaced = False
    while not spaced:
        spaced = True
        charPointer = 0
        while spaced and charPointer < len(characters):
            if characters[charPointer] == '/':
                if characters[charPointer-1] != ' ':
                    characters.insert(charPointer,' ')
                    spaced = False
                elif characters[charPointer+1] != ' ':
                    characters.insert(charPointer+1,' ')
                    spaced = False
            charPointer += 1
    newText = ''
    for char in characters:
        newText += char
    return newText

def fixInvalidMorseSequence(text):
    if ' / ' in text:
        characters2D = text.split(' / ')
    else:
        characters2D = [text]
    for wordNo, word in enumerate(characters2D):
        characters2D[wordNo] = word.split(' ')
        characterPointer = 0
        while characterPointer < len(word):
            if characters2D[wordNo][characterPointer] not in englishDict.keys():
                characters2D[wordNo].pop(characterPointer)
            else:
                characterPointer += 1
    while [] in characters2D:
        characters2D.remove([])
    wordList = []
    for word in characters2D:
        newWord = ''
        for char in word:
            newWord += char
            newWord += ' '
        wordList.append(newWord)
    newText = ''
    for word in wordList:
        newText += word
        newText += ' / '
    newText = newText[:-3]
    return newText