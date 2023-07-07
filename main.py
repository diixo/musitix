
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


def musitic(fileName: str):
    plt.rcParams['figure.dpi'] = 72
    plt.rcParams['figure.figsize'] = (14, 8)

    sampFreq, sound = wavfile.read(fileName)

    # Convert our sound (numpy) array to floating point values ranging from -1 to 1 as follows:
    sound = sound / (2.0**15.0)

    # graph by signal bitrate:
    #plt.subplot(2,1,1)
    #plt.plot(sound[:,0], 'r')
    #plt.xlabel("left channel, sample #")
    #plt.subplot(2,1,2)
    #plt.plot(sound[:,1], 'b')
    #plt.xlabel("right channel, sample #")
    #plt.tight_layout()
    #plt.show()

    # graph by time:
    length_in_s = sound.shape[0] / sampFreq
    print(length_in_s)

    time = np.arange(sound.shape[0]) / sound.shape[0] * length_in_s

    plt.subplot(2,1,1)
    plt.plot(time, sound[:,0], 'r')
    plt.xlabel("time, s [left channel]")
    plt.ylabel("signal, relative units")
    plt.subplot(2,1,2)
    plt.plot(time, sound[:,1], 'b')
    plt.xlabel("time, s [right channel]")
    plt.ylabel("signal, relative units")
    plt.tight_layout()
    plt.suptitle("Waveform:" + fileName)
    plt.show()

    ###############################################################
    # select separated signals from each channel:
    signal0 = sound[:,0]    # left channel
    signal1 = sound[:,1]    # right channel

    # duration = sampFreq * time_s
    duration = int(sampFreq * 0.358)

    plt.plot(time[0:duration], signal0[0:duration], 'r')
    plt.plot(time[0:duration], signal1[0:duration], 'b')

    plt.xlabel("time, s")
    plt.ylabel("Signal, relative units")
    plt.suptitle("Bump")
    plt.show()

    ###############################################################
    # frequency content with FFT:
    fft_spectrum = np.fft.rfft(signal0)
    freq = np.fft.rfftfreq(signal0.size, d=1./sampFreq)

    '''
    To simplify the concept without going deeply into the theorical part, let's say that when we performe the fft to get:
       `X = fft(x)`, 
    we usually need to use the signal magnitude in the spectral domain:
       `A = |X| = sqrt(real(X)^2+ imag(X)^2)`. 
    As for the imaginary part of the transform, it can be used to compute the signal phase:
       `Phi = Arg(X) = arctg(imag(X)/real(X))`. 
    Today we do not need the phase part. So, to obtain the Amplitude vs. 
    Frequency spectrum we find the absolute value of the fourier transform:
    '''
    fft_spectrum_abs = np.abs(fft_spectrum)

    # Thus, the spectrum of the sound (frequency domain) looks like:
    # A human can hear a sound that is in the 20-20,000 Hz range. However, our sound doesn't contain frequencies greater than 3 kHz. 
    # It's interesting. Let's zoom in on the highest peaks:

    # Apply range[0:3000]
    plt.plot(freq[:3000], fft_spectrum_abs[:3000])
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.suptitle("FFT-spectr")
    plt.show()

    #################
    return

    for i, f in enumerate(fft_spectrum_abs):
        if f > 350: #looking at amplitudes of the spikes higher than 350 
            print('frequency = {} Hz with amplitude {} '.format(np.round(freq[i], 1), np.round(f)))

    # filter electric noise:
    for i,f in enumerate(freq):
        if f < 62 and f > 58:# (1)
            fft_spectrum[i] = 0.0
        if f < 21 or f > 20000:# (2)
            fft_spectrum[i] = 0.0

    plt.plot(freq[:1000], fft_spectrum_abs[:1000])
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.suptitle("FFT-spectr LOW-filtered")
    plt.show()

    pass


def main():
    musitic('data/mix2.wav')
    #musitic('audio/32943-short.wav')
    pass
    
if __name__ == "__main__":
    main()
