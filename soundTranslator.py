'''SOUND TRANSLATION AND VALIDATION MODULE'''
import numpy as np
import wavio as wv
from matplotlib import pyplot as plt
from scipy.signal import hilbert, argrelextrema
from scipy.io import wavfile
from sklearn.ensemble import IsolationForest
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

def getEnvelope(data):
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
    return smoothedEnvelope, threshold

def findGaps(data): #point B3
    smoothedEnvelope, threshold = getEnvelope(data)
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

def findSignals(data): #point B3
    smoothedEnvelope, threshold = getEnvelope(data)
    signals = []
    for x in smoothedEnvelope:
        if x > threshold:
            signals.append(True)
        else:
            signals.append(False)
    signalFrames = []
    startSignal = None
    for i, value in enumerate(signals):
        if value:
            if startSignal == None:
                startSignal = i
        else:
            if startSignal != None:
                signalFrames.append((startSignal, (i - 1)))
                startSignal = None
    if startSignal != None:
        signalFrames.append((startSignal, (len(signals) - 1)))
    return signalFrames

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

def findUnit(signalDurations):
    cont = 1/len(signalDurations) #contamination hyperparameter
    signals = np.array(signalDurations).reshape(-1, 1)
    isoForest = IsolationForest(contamination=cont)
    isoForest.fit(signals)
    outliers = isoForest.predict(signals)
    filteredDurations = [d for d, o in zip(signals, outliers) if o == 1]
    unit = 0.75*min(filteredDurations)
    return unit

def processSound(data, rate, auto=True, wpm=10): #point B3
    if not auto:
        unit = 60/(50*wpm) #unit time length determined by wpm
    gapFrames = findGaps(data)
    signalFrames = findSignals(data)
    gapTimes = [(x[0]/rate,x[1]/rate) for x in gapFrames]
    if gapTimes[0][0] == 0.0:
        gapTimes.pop(0)
    signalTimes = [(x[0]/rate,x[1]/rate) for x in signalFrames]
    gapDurations = [x[1]-x[0] for x in gapTimes]
    signalDurations = [x[1]-x[0] for x in signalTimes]
    if auto:
        unit = findUnit(signalDurations)

    durationView = []
    for i in range(0,len(gapDurations)):
        durationView.append(signalDurations[i])
        durationView.append(gapDurations[i])
    if len(signalDurations) > len(gapDurations):
        durationView.append(signalDurations[-1])

    #time length definitions
    dit = 1*unit
    dah = 3*unit
    intraChar = 1.5*unit
    interChar = 3*unit
    wordBreak = 7*unit
    
    textView = []
    for i, value in enumerate(durationView):
        if i%2 == 0:
            if value >= dah:
                textView.append('-')
            elif value >= dit:
                textView.append('.')
        else:
            if value >= interChar and value < wordBreak:
                textView.append(' ')
            elif value >= wordBreak:
                textView.append(' / ')
    text = ''
    for c in textView:
        text += c
    return text

rate, data = wavfile.read('myMorseWave2.wav')
print(processSound(data, rate))