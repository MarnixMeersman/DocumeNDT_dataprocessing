import scipy.io
import obspy
import pandas as pd
import scipy as sc
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.io.wavfile import write
from obspy.signal.detrend import spline # spline(array, order=4, dspline=2000, plot=True)
from data_loader import read_data, get_VibVol, get_RefVol
from numpy.linalg import norm
from scipy.fft import rfft, rfftfreq, irfft
from scipy.signal import fftconvolve
import pywt
from pylab import *

def KMF(timeseries_array):
    data = timeseries_array
    def oavar(data, rate, numpoints=30):

        x = np.cumsum(data)

        max_ratio = 1 / 9
        num_points = 30
        ms = np.unique(
            np.logspace(0, np.log10(len(x) * max_ratio), numpoints
                        ).astype(int))

        oavars = np.empty(len(ms))
        for i, m in enumerate(ms):
            oavars[i] = (
                                (x[2 * m:] - 2 * x[m:-m] + x[:-2 * m]) ** 2
                        ).mean() / (2 * m ** 2)

        return ms / rate, oavars

    def ln_NKfit(ln_tau, ln_N, ln_K):
        tau = np.exp(ln_tau)
        N, K = np.exp([ln_N, ln_K])
        oadev = N ** 2 / tau + K ** 2 * (tau / 3)
        return np.log(oadev)

    def get_NK(data, rate):
        taus, oavars = oavar(data, rate)

        ln_params, ln_varmatrix = (
            curve_fit(ln_NKfit, np.log(taus), np.log(oavars)))
        return np.exp(ln_params)

    # Initialize state and uncertainty
    state = data[0]
    output = np.empty(len(data))

    rate = 1  # We can set this to 1, if we're calculating N, K internally
    # N and K will just be scaled relative to the sampling rate internally
    dt = 1 / rate

    N, K = get_NK(data, rate)

    process_noise = K ** 2 * dt
    measurement_noise = N ** 2 / dt

    covariance = measurement_noise

    for index, measurement in enumerate(data):
        # 1. Predict state using system's model

        covariance += process_noise

        # Update
        kalman_gain = covariance / (covariance + measurement_noise)

        state += kalman_gain * (measurement - state)
        covariance = (1 - kalman_gain) * covariance

        output[index] = state

    return output

def smooth(timeseries_array, box_pts=10):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(timeseries_array, box, mode='same')
    return y_smooth

def too_smooth(timeseries_array): # I'm too smooth ;)
    return smooth(smooth(timeseries_array))

def tooo_smooth(timeseries_array): # I'm tooo smooth ;)
    return smooth(smooth(smooth(timeseries_array)))

def toooo_smooth(timeseries_array): # I'm tooo smooth ;)
    return too_smooth(too_smooth(too_smooth(timeseries_array)))


def normalise(timeseries_array):
    div = norm(timeseries_array)
    vector = timeseries_array / div
    return vector

def detrend(timeseries_array):
    return spline(timeseries_array, order=4, dspline=2000, plot=False)

def compute_first_derivative(timeseries_array):
    gradients = np.gradient(timeseries_array)
    return gradients

# def find_vib_start(index_of_emitting_point, index_of_receiving_point):
#     data = get_VibVol(index_of_emitting_point, index_of_receiving_point) # [0] for time, [1] for amplitude
#     slopes = compute_first_derivative(data[1])
#     for slope in slopes:

def filtfilt_filter(timeseries_array, poles = 3, nyquist_frequency_multiplier = 0.1):
    # apply a 3-pole lowpass filter at 0.1x Nyquist frequency to compensate for shift
    b, a = scipy.signal.butter(poles, nyquist_frequency_multiplier)
    filtered = scipy.signal.filtfilt(b, a, timeseries_array)
    return filtered

def butter_highpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = sc.signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a
def butter_highpass_filter(data, cutoff, fs, order=1):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = sc.signal.filtfilt(b, a, data)
    return y

def butter_lowpass(cutoff, fs, order):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = sc.signal.butter(order, normal_cutoff, btype='low', analog = False)
    return b, a

def butter_lowpass_filter(timeseries_array, cutoff, fs, order=1, show_figure = False):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = sc.signal.filtfilt(b, a, timeseries_array)
    if show_figure == True:
        plt.plot(y)
        plt.title("Phase Shift compensated Low Pass Filter [Hz]\nCut-off frequency at "+ str(cutoff)+" [Hz]")
        plt.grid()
        plt.ylabel("Amplitude [V]")
        plt.xlabel("Samples [#]")
        plt.show()
    return y

def PSD(array):
    return scipy.signal.welch(array, 250000, average='median')

def get_FFT(array, sample_rate, show_figure = False):
    normalized_array = normalise(array)
    N  = len(normalized_array)
    yf = rfft(normalized_array)
    xf = rfftfreq(N, 1/sample_rate)
    if show_figure == True:
        plt.plot(xf, np.abs(yf), c='red')
        plt.title("Fast Fourier Transform at sampling rate " + str(sample_rate) + " [Hz]\n A peak at 0 Hz is most likely present due to signal bias, therefore this peak can be neglected.")
        plt.grid()
        plt.ylabel("normalized power [-]")
        plt.xlabel("Frequency [Hz]")
        plt.show()
    else:
        pass
    return xf, yf

def get_fftconvolve(timeseries_array_emitter, timeseries_array_receiver):
    return fftconvolve(timeseries_array_receiver, timeseries_array_emitter, mode='same')

def export_to_csv(two_orsingle_dimensional_array, filename):
    print("Saving " + filename + "...")
    array = two_orsingle_dimensional_array
    np.savetxt(filename, array)
    print("Done.")
    return None

def hanning(timeseries_array):
    size = len(timeseries_array)
    window  = np.hanning(size)
    return np.multiply(timeseries_array, window)

# def inv_hamming(timeseries_array):
#     size = len(timeseries_array)
#     window  = 1/np.hamming(size)
#     return np.multiply(timeseries_array, window)

def boxcar_bandpass(timeseries, sample_rate, f_begin, f_end, apply_hanning = True,  plot_FFT = False, plot_IFFT = False):
    og = timeseries
    if apply_hanning == True:
        timeseries = hanning(timeseries)
    else:
        pass

    # Fast Fourier Transform
    fft = get_FFT(timeseries, sample_rate, False)

    if plot_FFT == True:

        plt.plot(fft[0], np.abs(fft[1]), label='original FFT', c='grey')

        # Apply Boxcar
        for i in range(len(fft[0])):
            if f_begin < fft[0][i] < f_end:
                pass
            else:
                fft[1][i] = 0
        plt.plot(fft[0], np.abs(fft[1]), label='BandPassed FFT (Boxcar)', c='r')
        plt.legend()
        plt.grid()
        plt.title("FFT")
        plt.show()
    else:
        # Apply Boxcar
        for i in range(len(fft[0])):
            if f_begin < fft[0][i] < f_end:
                pass
            else:
                fft[1][i] = 0

    # Inverse Fast Fourier Transform
    inverse_fft = irfft(fft[1])
    if plot_IFFT == True:
        plt.plot(normalise(timeseries), label="norm-hann-unfiltered", c='grey')
        plt.plot(normalise(too_smooth(og)), label="Old Smooth signal")
        plt.plot(normalise(inverse_fft), label="norm-hann-boxcar", c='r')
        plt.title("Original Signal (HANN) vs Inverse FFT (HANN)")
        plt.legend()
        plt.show()
    else:
        pass

    return inverse_fft



'''
If you want to test a signal: get_VibVol(a, b) or get_RefVol(a, b) 
will produce a signal for which a = emission index, b = laser index
See example below:
'''
# Load in data
# signal = get_VibVol(11, 0)
# time = signal[0]
# signal = signal[1]

# Load in any function you like such as the boxcar filter with or without Hanning window applied
# boxcar = boxcar_bandpass(amplitude, 250_000, 100, 800, apply_hanning=True, plot_FFT=True, plot_IFFT=True)



