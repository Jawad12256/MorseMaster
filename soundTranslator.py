'''SOUND TRANSLATION AND VALIDATION MODULE'''
import numpy as np
import wavio as wv
from matplotlib import pyplot as plt
from scipy.signal import hilbert
from scipy.io import wavfile
import fastFourierTransform as fft
sampleRate = 128
print('_')

def sineWave(frequency, ampScale, sampleRate):
    t = np.arange(0,1,1.0/sampleRate)
    sine = ampScale*np.sin((2 * np.pi) * t * frequency)
    return sine

def filterFrequencies(fftList): #point B2
    fftList = list(fftList)
    fftList[0], fftList[1] = list(fftList[0]), list(fftList[1])
    newList = [[],[]]
    threshold = 1.0
    for i in range(len(fftList[0])):
        if np.abs(fftList[0][i]) >= threshold:
            newList[0].append(fftList[0][i])
            newList[1].append(fftList[1][i])
    return newList

def validateFrequencies(fftList): #point B1.3
    ampltiudeRatioThreshold = 0.5 #amplitude ratio threshold hyperparameter
    fftList = filterFrequencies(fftList)
    if len(fftList[0]) == 0:
        return False
    if len(fftList[0]) == 1:
        return True
    pairedList = [[np.abs(fftList[0][i]),fftList[1][i]] for i in range(len(fftList[0]))]
    pairedList.sort(key = lambda x:x[0])
    if pairedList[-2][0]/pairedList[-1][0] > ampltiudeRatioThreshold:
        return False
    return True

def findGaps(data): #point B3
    amplitudeThreshold = 0.8 #amplitude threshold hyperparameter
    windowSize = 5 #smoothing hyperparameter
    amplitudeEnvelope = np.abs(hilbert(data))
    amplitudeEnvelope = list(amplitudeEnvelope)
    smoothedEnvelope = []
    for i in range(windowSize,len(amplitudeEnvelope)-windowSize):
        smoothingList = amplitudeEnvelope[i-windowSize:i+windowSize+1]
        smoothedEnvelope.append(max(smoothingList))
    startCopy = smoothedEnvelope[0]
    endCopy = smoothedEnvelope[-1]
    for i in range(windowSize):
        smoothedEnvelope.insert(0,startCopy)
        smoothedEnvelope.append(endCopy)
    threshold = np.mean(smoothedEnvelope)*amplitudeThreshold
    gaps = []
    for x in smoothedEnvelope:
        if x > threshold:
            gaps.append(False)
        else:
            gaps.append(True)
    gapFrames = []
    startGap = None
    for i, value in enumerate(gaps):
        if value:
            if startGap == None:
                startGap = i
        else:
            if startGap != None:
                gapFrames.append((startGap, (i - 1)))
                startGap = None
    if startGap != None:
        gapFrames.append((startGap, (len(gaps) - 1)))
    return gapFrames

rate, data = wavfile.read('myMorseWave.wav')

def isSoundValid(data, rate): #points B1.1, B1.3
    try:
        if len(data) == 0:
            return False
        gapFrames = findGaps(data)
        sampleStart = 0
        sampleEnd = len(gapFrames)-1
        if len(gapFrames) > 0:
            sampleStart = gapFrames[0][1]
            if len(gapFrames) > 1:
                sampleEnd = gapFrames[1][0]
        if (validateFrequencies(fft.FFT(data[sampleStart:sampleEnd], rate))):
            return True
        else:
            return False
    except:
        return False
    
def processSound(data, rate): #point B3
    wpm = 10 #words per minute hyperparameter
    unit = 60/(50*wpm) #unit time length
    
    gapFrames = findGaps(data)
    totalDuration = len(gapFrames)/rate

    gapTimes = [(x[0]/rate,x[1]/rate) for x in gapFrames]
    gapDurations = [x[1]-x[0] for x in gapTimes]
    