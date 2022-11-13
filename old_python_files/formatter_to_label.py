import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import read_data, get_VibVol, get_RefVol
from pre_processing import smooth, too_smooth, tooo_smooth, KMF, normalise, detrend

# Hitting locations naming convention for the .mat files
locations = [11, 14, 17, 21, 22, 23, 25, 26, 27, 31, 32, 33, 35, 36, 37, 41, 44,
             47]

for e in locations:
    data = read_data(e)

    number_of_samples = len(data[0]) * len(data[1])
    samples = np.linspace(0, number_of_samples, number_of_samples)
    vib = normalise(data[3].flatten())
    ref = normalise(data[4].flatten())
    # vib_KF = normalise(KMF(vib))
    vib_smooth = smooth(vib)

    # plt.plot(samples, ref)
    # plt.plot(samples, vib_smooth)
    #
    # plt.show()

    series_names = ["Vibrometer_Original"] * len(vib) + ["Reference_Original"] * len(ref) + ["Vibrometer_Smoothed"] * len(vib_smooth)
    samples_timestamp = list(samples) + list(samples) + list(samples)
    values = list(vib) + list(ref) + list(vib_smooth)


    d = {
        'series': series_names,
        'timestamp': samples_timestamp,
        'value': values
    }
    df = pd.DataFrame(data=d)
    df["label"] = ""
    df.to_csv("label_df/" + str(e) + ".csv")