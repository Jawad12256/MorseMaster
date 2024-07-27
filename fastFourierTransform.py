'''FAST FOURIER TRANSFORM MODULE'''
import numpy as np

def DFT(x):
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    X = np.dot(e, x)
    
    N = len(X)
    n = np.arange(N)
    T = N/100
    freq = n/T 
    return (X, freq)