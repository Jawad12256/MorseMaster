'''TEXT VALIDATION MODULE'''

def formatMorse(text): #points A3.2, A3.3., A3.4, A3.5
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


def validateMorse(): #points A3.1
    pass