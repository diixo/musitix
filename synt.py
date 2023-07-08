# equal-tempered: https://pages.mtu.edu/~suits/notefreqs.html

import numpy as np
import matplotlib.pyplot as plt

fr_eq = np.array(
    [
        [16.35, 18.35, 20.50, 22.50, 24.50, 27.50, 30.50], #0
        [32.50, 36.50, 41.00, 43.50, 49.0,  55.0,  61.50], #1
        [65.50, 73.50, 82.50, 87.50, 98.0,  110.0, 124.0], #2
        [131.0, 147.0, 165.0, 175.0, 196.0, 220.0, 245.0], #3
        [262.0, 294.0, 330.0, 350.0, 392.0, 440.0, 494.0], #4
        [523.0, 587.0, 660.0, 700.0, 784.0, 880.0, 988.0]  #5
    ]
)

fr_eq_mid = np.array(
    [
        [17.50, 19.50, 23.00, 26.00, 29.00], #0
        [35.00, 39.00, 46.00, 52.0,  58.00], #1
        [69.50, 78.50, 92.50, 104.0, 116.0], #2
        [139.0, 155.0, 185.0, 208.0, 233.0], #3
        [277.0, 311.0, 370.0, 415.0, 466.0], #4
        [554.0, 622.0, 740.0, 830.0, 932.0]  #5
    ]
)

def f0(arr):
    window_sz = 5
    i=0
    buff = arr[0: window_sz]

    while i < len(arr) - window_sz + 1:

        buff = np.array(buff[1: window_sz])
        buff = np.append(buff, arr[i + window_sz - 1])
        arr[i + window_sz - 1] = buff.max()

        print(buff.max())

        i += 1
    pass

def findLocalMaxMin(arr: np.array):
    n = len(arr)
    # Empty lists to store points of
    # local maxima and minima
    mx = []
    mn = []
 
    # Checking whether the first point is
    # local maxima or minima or neither
    if(arr[0] > arr[1]):
        mx.append(0)
    elif(arr[0] < arr[1]):
        mn.append(0)
 
    # Iterating over all points to check
    # local maxima and local minima
    for i in range(1, n-1):
 
        # Condition for local minima
        if(arr[i-1] > arr[i] < arr[i + 1]):
            mn.append(i)
 
        # Condition for local maxima
        elif(arr[i-1] < arr[i] > arr[i + 1]):
            mx.append(i)
 
    # Checking whether the last point is
    # local maxima or minima or neither
    if(arr[-1] > arr[-2]):
        mx.append(n-1)
    elif(arr[-1] < arr[-2]):
        mn.append(n-1)

    return mx, mn
 