
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
import synt


def musitic(t, fileName: str, plot = False):
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

    if plot:
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
    #time_s = t #0.358
    time_s = length_in_s
    if t > 0.0:
        time_s = t
    duration = int(sampFreq * time_s)

    smooth = np.array(signal0[0:duration])
    mx, mn = synt.findLocalMaxMin(smooth)
    for id in range(len(mx)-1):
        id0 = mx[id]
        id1 = mx[id+1]
        if id1 - id0 <= 20:
            aprox = np.linspace(signal0[id0], signal0[id1], id1 - id0)
            smooth[id0:id1] = max(signal0[id0], signal0[id1])


    if plot:
        plt.plot(time[0:duration], signal0[0:duration], 'b')
        #plt.plot(time[0:duration], smooth[0:duration], 'r')
        plt.xlabel("time, s")
        plt.ylabel("Signal, relative units")
        plt.suptitle("Bump")
        plt.show()

    ###############################################################
    # frequency content with FFT:
    fft_spectrum_0 = np.fft.rfft(signal0[0:duration])
    fft_spectrum_1 = np.fft.rfft(signal1[0:duration])

    freq = np.fft.rfftfreq(duration, d=1./sampFreq)

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

    # Thus, the spectrum of the sound (frequency domain) looks like:
    # A human can hear a sound that is in the 20-20,000 Hz range. However, our sound doesn't contain frequencies greater than 3 kHz. 
    # It's interesting. Let's zoom in on the highest peaks:

    # filter electric noise:
    #for i, f in enumerate(freq):
    #    if f < 70 and f > 60:
    #        fft_spectrum_0[i] = 0.0
    #    if f < 21 or f > 20000:
    #        fft_spectrum_0[i] = 0.0

    fft_spectrum_abs_0 = np.abs(fft_spectrum_0)
    fft_spectrum_abs_1 = np.abs(fft_spectrum_1)

    # Apply range[0:3000]
    #################

    for i, f in enumerate(fft_spectrum_abs_0):
        if f > 350: #looking at amplitudes of the spikes higher than 350 
            print('frequency = {} Hz with amplitude {} '.format(np.round(freq[i], 1), np.round(f)))

    # Recreate the original signal via an inverse FFT:
    original_signal = np.fft.irfft(fft_spectrum_0)
    wavfile.write("track-" + str(t) + ".wav", sampFreq, original_signal)

    sz = 3000
    if True:
        plt.plot(freq[:sz], fft_spectrum_abs_0[:sz], 'r')
        plt.plot(freq[:sz], fft_spectrum_abs_1[:sz], 'b')
        plt.xlabel("frequency, Hz")
        plt.ylabel("Amplitude, units")
        plt.suptitle("FFT-spectr (L/R): " + fileName)
        plt.show()        

    return fft_spectrum_abs_0, freq

def test():
    spectrum_abs1, freq1 = musitic(0, 'audio/short-serial-1.wav')

    spectrum_abs2, freq2 = musitic(0, 'audio/short-serial-2.wav')
    spectrum_abs3, freq3 = musitic(0, 'audio/short-serial-3.wav')

    spectrum_abs4, freq4 = musitic(0, 'audio/short-serial-4.wav')
    spectrum_abs5, freq5 = musitic(0, 'audio/short-serial-5.wav')
    spectrum_abs6, freq6 = musitic(0, 'audio/short-serial-6.wav')

    sz = 2000

    if False:
        plt.plot(freq1[:sz], spectrum_abs1[:sz], 'r')
        plt.plot(freq2[:sz], spectrum_abs2[:sz], 'g')
        plt.plot(freq3[:sz], spectrum_abs3[:sz], 'b')
        plt.plot(freq4[:sz], spectrum_abs4[:sz], 'm')
        plt.plot(freq5[:sz], spectrum_abs5[:sz], 'c')
        plt.plot(freq6[:sz], spectrum_abs6[:sz], 'k')

        plt.xlabel("frequency, Hz")
        plt.ylabel("Amplitude, units")
        plt.suptitle("FFT-spectr")
        plt.show()

def main():
    
    spectrum_orig0, freq0 = musitic(0, 'data/original_a3s.wav', plot = False)
    spectrum_orig1, freq1 = musitic(0, 'data/unknown.wav', plot = False)

    sz = 3000
    plt.plot(freq0[:sz], spectrum_orig0[:sz], 'r')
    plt.plot(freq1[:sz], spectrum_orig1[:sz], 'g')
    plt.xlabel("frequency, Hz")
    plt.ylabel("Amplitude, units")
    plt.suptitle("FFT-spectr")
    plt.show()

if __name__ == "__main__":
    main()
