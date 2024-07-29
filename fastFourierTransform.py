'''FAST FOURIER TRANSFORM MODULE'''
import numpy as np

def DFT(x, sampleRate):
    N = len(x) #number of samples
    n = np.arange(N) #list of integers up to N non-inclusive
    k = n.reshape((N, 1)) #use views to reduce memory use
    e = np.exp(-2j * np.pi * k * n / N)
    X = np.dot(e, x) #multiply across by list of sine values
    T = N/sampleRate
    freq = n/T #calculate frequencies list
    return (X, freq)

def FFTrecurse(x):
    N = len(x)

    if np.log2(N) % 1 > 0:
        x = np.pad(x, (0, 2**int(np.ceil(np.log2(N))) - N))
        N = len(x)
    
    if N == 1:
        return x
    else:
        even = FFTrecurse(x[::2])
        odd = FFTrecurse(x[1::2])
        factor = np.exp(-2j*np.pi*np.arange(N)/ N)
        
        X = np.concatenate([even+factor[:int(N/2)]*odd, even+factor[int(N/2):]*odd])
        return X
    
def FFT(x, sampleRate):
    X = FFTrecurse(x)
    N = len(X)
    mid = N//2
    n = np.arange(N)
    T = N/sampleRate
    freq = n/T
    return (X[:mid],freq[:mid])
