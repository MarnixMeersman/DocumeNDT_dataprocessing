import numpy as np
import scipy as sc
import matplotlib.pyplot as plt


import scipy.signal

from scipy.signal import find_peaks, peak_prominences
from data_loader import *
from pre_processing import *




def get_Ref_t0(index_of_emitting_point):
    data = read_data(index_of_emitting_point)
    time = data[0]
    ref = data[4]
    j = 0
    print("\nFinding t0 for all laser timeseries originating from solenoid point: " + str(
        index_of_emitting_point))
    indexes = []
    for signal in ref:
        print("Analysing signal " + str(j) + " . . .", flush=True, end=" ")
        j += 1
        norm_signal = normalise(signal)
        new_signal = normalise(butter_highpass_filter(signal, 10000, 250000))

        i = 0
        while new_signal[i] <= 0.01: # threshold value
            i += 1
        indexes.append(i)
        print("FOUND! t0 at: ", np.round(time[i], 6), " [seconds]")

        # Uncommented this if you want to visually check

        # xlim = 0.02
        # fig, axs = plt.subplots(2, 1)
        # axs[0].plot(time, norm_signal)
        # axs[0].axvline(x = time[i], c = 'r')
        # axs[1].plot(time, new_signal)
        # axs[1].axvline(x = time[i], c='r')
        # axs[0].set_xlim(0.0, xlim)
        # axs[1].set_xlim(0.0, xlim)
        # axs[0].set_xlabel('time')
        # axs[0].set_ylabel('Amplitude')
        # axs[0].grid(True)
        # axs[1].grid(True)

        # plt.show()

    print("Done.")
    return np.array(indexes)

