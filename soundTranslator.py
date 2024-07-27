'''SOUND TRANSLATION AND VALIDATION MODULE'''
import numpy as np
import wavio as wv
from matplotlib import pyplot as plt
import fastFourierTransform as fft

def sineWave(frequency, ampScale, sampleRate):
    t = np.arange(0,1,1.0/sampleRate)
    sine = ampScale*np.sin((2 * np.pi) * t * frequency)
    return sine

myWave128 = sineWave(1, 3, 128) + sineWave(4, 1, 128) + sineWave(7, 0.5, 128)

Y = fft.FFT(myWave128, 128)

plt.stem(Y[1],abs(Y[0]))
plt.show()
