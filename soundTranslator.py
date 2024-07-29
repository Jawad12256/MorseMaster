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

def filterFrequencies(fftList):
    fftList = list(fftList)
    fftList[0], fftList[1] = list(fftList[0]), list(fftList[1])
    newList = [[],[]]
    threshold = 1.0
    for i in range(len(fftList[0])):
        if np.abs(fftList[0][i]) >= threshold:
            newList[0].append(fftList[0][i])
            newList[1].append(fftList[1][i])
    return newList

def validateFrequencies(fftList):
    ampltiudeRatioThreshold = 0.5
    if len(fftList[0]) == 0:
        return False
    if len(fftList[0]) == 1:
        return True
    pairedList = [[np.abs(fftList[0][i]),fftList[1][i]] for i in range(len(fftList[0]))]
    pairedList.sort(key = lambda x:x[0])
    if pairedList[-2][0]/pairedList[-1][0] > ampltiudeRatioThreshold:
        return False
    return True

def findGaps(data, rate):
    amplitudeThreshold = 0.8
    windowSize = 5
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
    plt.plot(list(range(0,len(smoothedEnvelope))),smoothedEnvelope)
    plt.show()
    threshold = np.mean(smoothedEnvelope)*amplitudeThreshold
    gaps = []
    for x in smoothedEnvelope:
        if x > threshold:
            gaps.append(False)
        else:
            gaps.append(True)

    gapTimes = []
    startGap = None
    for i, value in enumerate(gaps):
        if value:
            if startGap == None:
                startGap = i
        else:
            if startGap != None:
                gapTimes.append((startGap / rate, (i - 1) / rate))
                startGap = None

    if startGap != None:
        gapTimes.append((startGap / rate, (len(gaps) - 1) / rate))

    print('Threshold value:', threshold)
    print("Detected gaps (start, end) in seconds:", gapTimes)

myWave = sineWave(1, 3, sampleRate) + sineWave(4, 1, sampleRate) + sineWave(7, 0.5, sampleRate)

Y = fft.FFT(myWave, sampleRate)
Y = filterFrequencies(Y)
print(validateFrequencies(Y))

rate, data = wavfile.read('myMorseWave2.wav')

# plt.plot(list(range(0,len(data))),data)
# plt.show()

findGaps(data, rate)