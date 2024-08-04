'''TEXT TRANSLATION AND PARSING MODULE'''

morseDict = {
    'A':'.-',
    'B':'-...',
    'C':'-.-.',
    'D':'-..',
    'E':'.',
    'É':'..-..',
    'F':'..-.',
    'G':'--.',
    'H':'....',
    'I':'..',
    'J':'.---',
    'K':'-.-',
    'L':'.-..',
    'M':'--',
    'N':'-.',
    'O':'---',
    'P':'.--.',
    'Q':'--.-',
    'R':'.-.',
    'S':'...',
    'T':'-',
    'U':'..-',
    'V':'...-',
    'W':'.--',
    'X':'-..-',
    'Y':'-.--',
    'Z':'--..',
    '0':'-----',
    '1':'.----',
    '2':'..---',
    '3':'...--',
    '4':'....-',
    '5':'.....',
    '6':'-....',
    '7':'--...',
    '8':'---..',
    '9':'----.',
    '.':'.-.-.-',
    ',':'--..--',
    '?':'..--..',
    '!':'-.-.--',
    '+':'.-.-.',
    '-':'-....-',
    '=':'-...-',
    '/':'-..-.',
    '@':'.--.-.',
    '(':'-.--.',
    ')':'-.--.-',
    '\'':'.----.',
    '\"':'.-..-.',
    '&':'.-...',
    ':':'---...',
    ';':'-.-.-.',
    '_':'..--.-',
    '$':'...-..-'
}

englishDict = dict((b,a) for a,b in morseDict.items())

def parseMorse(text): #points A4, A5
    if text == False:
        return False
    phrase = ''
    chars = text.split(' / ')
    for i,c in enumerate(chars):
        chars[i] = c.split(' ')
        for j,x in enumerate(chars[i]):
            chars[i][j] = englishDict[x]
        word = ''.join(chars[i]) + ' '
        phrase += word
    phrase = phrase[:-1]
    return phrase

def parseEnglish(text): #point A2
    if text == False:
        return False
    phrase = ''
    chars = text.split(' ')
    for i,c in enumerate(chars):
        word = ''
        chars[i] = [char for char in c]
        for j,x in enumerate(chars[i]):
            chars[i][j] = morseDict[x]
            word += chars[i][j]
            word += ' '
        phrase += word
        phrase += '/ '
    phrase = phrase[:-3]
    return phrase