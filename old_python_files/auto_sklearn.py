from backend_code.time_extraction_for_solenoid import *
from adtk.transformer import *
from adtk.data import validate_series
from adtk.visualization import plot

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def transformer(signal, show_plot = False):
    # root_signal = normalise(smooth(signal))
    # root_signal = normalise(signal)
    root_signal = normalise(boxcar_bandpass(signal, 250_000, 10, 2000, apply_hanning=True))

    # Store data
    df = pd.DataFrame(root_signal, columns=['value'], index=pd.date_range("20180101", periods=len(root_signal)))
    df.index.name = 'Time'
    df.to_csv('./dynamic_text_files/df.csv')

    s = pd.read_csv('../dynamic_text_files/df.csv', index_col="Time", parse_dates=True, squeeze=True)
    s = validate_series(s)

    # Variability detector
    '''volatility_shift_ad = VolatilityShiftAD(
        agg='std',
        c=6.0,
        side='positive',
        window=400)
    anomalies = volatility_shift_ad.fit_detect(s)
    print("\nANOMALIES!\n")
    print(pd.Series(anomalies))
    plot(s, anomaly=anomalies, anomaly_color='red')
    plt.show()'''

    # Level shift tracker
    '''s_transformed = DoubleRollingAggregate(
        agg="median",
        window=1000,
        diff="diff").transform(s).rename("Diff rolling median (mm)")

    plot(pd.concat([s, s_transformed], axis=1))
    plt.show()'''

    # Double window transformer
    s_transformed = DoubleRollingAggregate(
        agg="mean",
        window=(10, 3),  # The tuple specifies the left window to be 3, and right window to be 1
        diff="l1").transform(s).rename("results")

    results = pd.DataFrame(s_transformed)
    # print(results)
    # results.to_csv('./dynamic_text_files/results.csv')

    # Reshape into readable array
    temp = results.iloc[:, :1].values
    temp[np.isnan(temp)] = 0 #Nan values = 0


    if show_plot == True:
        plot(pd.concat([s, s_transformed], axis=1), ts_linewidth=1, ts_markersize=0.1)
        plt.show()
    else:
        pass

    return temp.flatten()




