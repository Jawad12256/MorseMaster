'''SOUND TRANSLATION AND VALIDATION MODULE'''
import numpy as np
import wavio as wv
from matplotlib import pyplot as plt
import fastFourierTransform as fft

def sineWave(frequency, sampleRate, duration):
    t = np.linspace(0, duration, sampleRate * duration, endpoint=False)
    f = np.sin((2 * np.pi) * t * frequency)
    return f

tone1 = sineWave(1, 2000, 5)
tone2 = sineWave(70, 2000, 5)
noisyTone = tone1 + tone2 * 0.3
scaledTone = np.int16((noisyTone / noisyTone.max()) * 32767)


def gen_sig(sampleRate):
    t = np.arange(0,1,1.0/sampleRate)
    freq = 1.
    x = 3*np.sin(2*np.pi*freq*t)
    return x

samplingRate = 2000
X = fft.DFT(scaledTone)

# t = np.arange(0,1,1.0/samplingRate)
# w = 3*np.sin(2*np.pi*1*t) + 1*np.sin(2*np.pi*15*t) + 0.5*np.sin(2*np.pi*45*t)

# X = fft.DFT(w)

plt.stem(X[1],abs(X[0]))
plt.show()