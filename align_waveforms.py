import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.io
import pickle
import pandas as pd

from data_loader import *
from pre_processing import *
from time_extraction_for_solenoid import *
from sklearn.linear_model import LinearRegression
from adtk.transformer import *
from adtk.data import *
from adtk.visualization import *



def transformer(signal, show_plot=False):
    # root_signal = normalise(boxcar_bandpass(signal, 250_000, 10, 1000, apply_hanning=True))
    root_signal = normalise(tooo_smooth(signal))

    # Store data
    df = pd.DataFrame(root_signal, columns=['value'], index=pd.date_range("20180101", periods=len(root_signal)))
    df.index.name = 'Time'
    df.to_csv('./dynamic_text_files/df.csv')

    s = pd.read_csv('./dynamic_text_files/df.csv', index_col="Time", parse_dates=True, squeeze=True)
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
        window=(100, 10),  # The tuple specifies the left window to be 3, and right window to be 1
        diff="l1").transform(s).rename("results")

    results = pd.DataFrame(s_transformed)
    # print(results)
    # results.to_csv('./dynamic_text_files/results.csv')

    # Reshape into readable array
    temp = results.iloc[:, :1].values
    temp[np.isnan(temp)] = 0  # Nan values = 0

    if show_plot == True:
        plot(pd.concat([s, s_transformed], axis=1), ts_linewidth=1, ts_markersize=0.1)
        plt.show()
    else:
        pass

    return temp.flatten()
def nrootstack(multi_d_array, N):
    matrix = multi_d_array.T
    J = len(multi_d_array)
    # perform the stacking over the rows

    sommen = []
    for row in matrix:
        sommetjes = []
        for value in row:
            getal = np.sign(value) * np.abs(value)**(1/N)
            sommetjes.append(getal)
        de_medium_som = sum(sommetjes)
        sommen.append(de_medium_som)
    stack = [(i/J)**N for i in sommen]
    return np.array(stack)


def signaltonoise(timeseries_array, axis=0, ddof=0):
    a = np.asanyarray(timeseries_array)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

def get_t_moved_away(index0, timeseries_array, amplitude_array, number_of_std_for_trigger = 2):
    # Linear Regression
    time_for_model = timeseries_array[:index0].reshape((-1, 1))
    vib_for_model = amplitude_array[:index0]
    model = LinearRegression().fit(time_for_model, vib_for_model)
    a = model.coef_
    b = model.intercept_
    line = a * timeseries_array + b # simply y(t) = a * x + b

    # Compute standard deviations
    residuals = np.subtract(timeseries_array, line)
    # print(residuals)
    # plt.plot(residuals)
    # plt.show()

    return line




def get_averaged_aligned_VibVol(index_of_emitting_point, sticker_id, number_of_laserpoints_per_sticker = 10, neglect_low_SNR_signals = True, SNR_threshold = 0.06, make_plots=False):
    indexes = []
    for i in range(number_of_laserpoints_per_sticker):
        index = i + sticker_id * 10
        indexes.append(index)

    og_data = read_data(index_of_emitting_point)
    og_t = og_data[0]

    t0_s = get_Ref_t0(index_of_emitting_point)
    t0_to_average = t0_s[indexes[0] : indexes[-1]+1]
    t0_minimum = min(t0_to_average) # samples
    time_to_average = [og_t[i] for i in t0_to_average]
    time0_minimum = og_t[t0_minimum]

    print("\nThe sticker_id, (ID: ", str(sticker_id), "),  you entered corresponds all wavesforms from signal ", indexes[0], "untill and including signal", indexes[-1])
    print("The shortest solenoid trigger time in sticker ", sticker_id, ' is ', og_t[t0_minimum], " [seconds]." )
    print("Average trigger time: ", np.average(time_to_average), " ---  Median trigger time: ", np.median(time_to_average))

    # Start shifting all vibrometer data to the minimal t_0
    og_vib = og_data[3] # original vibrometer data
    og_vib_to_average = og_vib[indexes[0] : indexes[-1]+1]
    og_ref = og_data[4]
    og_ref_to_average = og_ref[indexes[0]:indexes[-1]+1]


    # Compute to difference of each series compared to t0_minimum (in samples)
    diff = [t-t0_minimum for t in t0_to_average]
    # Shift all the arrays
    shifted_vibs = []
    c = 0
    for d in diff:
        shifted_vib = np.array(og_vib_to_average[c][d:]) # cut-off "d"-amount of samples from the beginning
        shifted_vib = np.pad(shifted_vib, (0, d), constant_values=0) # pad zeros to the back of the signal to make sure the arrays retain equal dimensionality
        shifted_vibs.append(list(shifted_vib))
        c += 1
    shifted_vibs = np.array(shifted_vibs)

    shifted_refs = []
    c = 0
    for d in diff:
        shifted_ref = np.array(og_ref_to_average[c][d:]) # cut-off "d"-amount of samples from the beginning
        shifted_ref = np.pad(shifted_ref, (0, d), constant_values=0) # pad zeros to the back of the signal to make sure the arrays retain equal dimensionality
        shifted_refs.append(list(shifted_ref))
        c += 1
    shifted_refs = np.array(shifted_refs)

    # get the SNR of the signals and delete the one with a too low SNR
    if neglect_low_SNR_signals == True:
        snrs = []
        remove_lst = []
        index_counter = 0
        for signal in og_vib_to_average:
            SNR = np.abs(signaltonoise(signal))
            snrs.append(SNR)
            if SNR <= SNR_threshold:
                remove_lst.append(index_counter)
            index_counter += 1
        print("\n>>>  REMOVED VIBROMETER SIGNALS: ", remove_lst, "with SNR's of: ", [snrs[i] for i in remove_lst])
        print(">>>  MEDIAN of all SNR's in this sticker: ", np.median(np.array(snrs)))
        print(">>>  If you do not want to remove these signals, set neglect_low_SNR_signals=False\n")

    else:
        remove_lst = []
    og_vib_to_average = np.delete(og_vib_to_average, remove_lst, axis=0)
    shifted_vibs = np.delete(shifted_vibs, remove_lst, axis=0)

    averaged_signal = np.mean(shifted_vibs, axis=0)


    if make_plots==True:
        # plot all og_vibs
        i = 0
        for signal in og_vib_to_average:
            plt.plot(og_t, smooth(signal), label="Signal "+str(i))
            i +=1
        plt.title("Original Signals")
        plt.legend()
        plt.grid()
        plt.show()
        plt.clf()

        # plot all shifted vibs
        i = 0
        for signal in shifted_vibs:
            plt.plot(og_t, smooth(signal), label=str(i))
            i += 1
        plt.title("Shifted Signals")
        plt.legend()
        plt.grid()
        plt.show()
        plt.clf()

        # Average all signals
        plt.plot(og_t, smooth(averaged_signal))
        plt.title("Averaged Shifted Filtered Signal")
        plt.grid()
        plt.show()
    else:
        pass

    # Make an n-root stack
    '''stack = nrootstack(shifted_vibs, 3)
    searchers = []
    searcher = 0
    while stack[searcher] <= 0.:
        searchers.append(searchers)
        searcher += 1
    t1_index = len(searchers)'''
    # t0_minimum = index of the sample where t0 is triggered, time0_minimum = time value [s] of the t0 triggerpoint
    return og_t, averaged_signal, t0_minimum, time0_minimum, shifted_vibs, shifted_refs


def get_t1(index_of_emitting_point, sticker_id, SNR_threshold = 0.085, tp = 17.5, make_plots=False, neglect_low_SNR_signals = True):
    sticker_time_and_signal = get_averaged_aligned_VibVol(index_of_emitting_point, sticker_id, SNR_threshold = SNR_threshold, make_plots=False, neglect_low_SNR_signals=neglect_low_SNR_signals)
    time   = sticker_time_and_signal[0]
    signal = sticker_time_and_signal[1]
    index0 = sticker_time_and_signal[2]
    time0  = sticker_time_and_signal[3]
    shifted_refs = sticker_time_and_signal[5]


    s_transformed = transformer(signal)
    s_tranformed_before_t0 = s_transformed[:index0+1]

    max_before_t0 = np.max(s_tranformed_before_t0[int(0.25 * len(s_tranformed_before_t0)):]) # * 0.25 is to remove boundary errors

    s_tranformed_containing_t1 = s_transformed[index0+1:]
    multipl_tresh = 1+tp/100
    temp_index = np.argmax(s_tranformed_containing_t1 > multipl_tresh * max_before_t0)
    index1 = index0 + 1 + temp_index


    '''
    # # Make a linear regression model
    # time_for_model = time[:index0].reshape((-1, 1))
    # vib_for_model = root_signal[:index0+1]
    # model = LinearRegression().fit(time_for_model, vib_for_model)
    # line = time * model.coef_ + model.intercept_
    #
    # # line = np.zeros(len(time))'''

    '''
    ###### Define smoothed signal
    

    residuals = np.subtract(root_signal[:half], line[:half])
    t0_len = len(time[:index0])
    percentage = 0.5
    back_propagation = t0_len*percentage
    std_res_to_t0 = np.std(residuals[int(index0-back_propagation):index0])

    indexes_for_t1 = []
    std_counter = 0
    new_std = 0.
    while new_std <= std_res_to_t0*2.0:
        new_std = np.std(residuals[int(index0-back_propagation):index0 + std_counter])
        indexes_for_t1.append(std_counter)
        std_counter += 1
        # print("old std:", std_res_to_t0, "new std: ", new_std)

    indexes_for_t1 = np.array(indexes_for_t1)
    index1 = index0 + (len(indexes_for_t1)-1)

    time1 = time[index1]
    
    '''

    '''
    # From time 1 go back to search for cross with zero line
    # Find the zero crossing line
    reversed_signal = np.array(list(reversed(root_signal[:index1]))) # reverse the order of the signal to start looking from trigger backwards
    zero_crossings = np.where(np.diff(np.sign(reversed_signal)))[0] # export indexes where sign changes
    cross_point = zero_crossings[0] # take the first index since this is the first time the sign changes
    '''

    ''' 
    # find the bottom, or top of the curve
    first_d = np.gradient(root_signal)
    if first_d[index1] > 0: # if the slope is increasing a t1
        j = 0
        for i in reversed(first_d[:index1]):
            if i < 0: # wait until the slope decreases for the first time, then return the point before it
                print("Found: j=", j)
                cross_point = j-1
                break
            else:
                pass
            j += 1
    else:
        j = 0
        for i in reversed(first_d[:index1]):
            if i > 0: # wait until the slope decreases for the first time, then return the point before it
                print("Found: j=", j)
                cross_point = j-1
                break
            else:
                pass
            j += 1
    '''


    # save plots efficiently
    d = {
        'time': time,
        'og_signal': normalise(signal),
        'signal': toooo_smooth(normalise(signal)),
        'transformed': normalise(s_transformed),
        'ref': normalise(shifted_refs[0]),
        'boxcar+hanning': normalise(boxcar_bandpass(signal, 250_000, 5, 1000, apply_hanning=True)),
        'prediction': np.zeros(len(time)),
        'trigger_line': np.ones(len(time)) * max_before_t0 * multipl_tresh / norm(s_transformed),
        'max_line': np.ones(len(time)) * max_before_t0 / norm(s_transformed),
        'index0': np.ones(len(time))*index0,
        'index1': np.ones(len(time))*index1

    }
    df = pd.DataFrame(data=d)
    df.to_pickle('./plots/pickles/'+str(index_of_emitting_point) + "_" + str(sticker_id)+'.pkl')





    if make_plots == True:
        print("Be aware that the RefVoltage is actually just the first ref agains the average vibs(because this would otherwise require extra argument and coding for a simple visualisation)")

        fig = sns.set_theme(context='paper', color_codes=True, rc=None)
        plt.plot(time, too_smooth(normalise(signal)), label = 'vib:norm-smooth', c = 'maroon', linewidth=0.3)
        plt.plot(time, normalise(shifted_refs[0]), label='ref:norm', c='mediumblue', linewidth=0.3)
        # plt.plot(time, normalise(boxcar_bandpass(signal, 250_000, 10, 2000, apply_hanning=True)), label='vib:norm-hann-boxcar[10-2000Hz]', c='royalblue', linewidth=0.5)
        # plt.plot(time, line, label = 'zero-line', linestyle="dashdot", c='royalblue', linewidth=0.3)
        plt.plot(time, normalise(s_transformed), label = 'vib:tranformer', c='orangered', linestyle='dotted', linewidth=0.3)
        plt.axvline(x=time0, linestyle="--",  c='mediumblue', label = 't0 [\u03BCs] = ' + str(np.round(time[index0]*10**6, 5)), linewidth=0.3)
        # plt.axvline(x=time1, linestyle="--",  c='yellowgreen', label = 't1 [\u03BCs] = ' + str(np.round(time[index1]*10**6, 5)))
        plt.axvline(x=time[index1], linestyle="--",  c='maroon', label = 't1 [\u03BCs] = ' + str(np.round(time[index1]*10**6, 5)), linewidth=0.3)
        plt.grid()
        plt.xlim(0, 0.02)
        plt.legend()
        plt.title("Emission = "+ str(index_of_emitting_point)+ " Sticker = "+str(sticker_id))
        plt.grid()
        # plt.show()
        plt.savefig("plots/"+str(index_of_emitting_point) + "_" + str(sticker_id), dpi = 400)
        plt.clf()
    else:
        pass


    return time0, time[index1], time[index1] - time0 # this is t0 and t1, and dt = t1-t0

# # # Hitting locations naming convention for the .mat files
# loc = [11, 14, 17, 21, 22, 23, 25, 26, 27, 31, 32, 33, 35, 36, 37, 41, 44,
#              47]
# for i in range(22):
#     get_t1(loc[0], i, make_plots=True, neglect_low_SNR_signals=True, SNR_threshold=0.25)



def get_time_differences(loc, number_of_stickers, make_plots = False, neglect_low_SNR_signals = True, SNR_threshold=0.1, tp = 17.5):
    time_differences = []
    for l in loc:
        time_differences_single_emitter = []
        for i in range(number_of_stickers):
            temp = get_t1(l, i, make_plots=make_plots, neglect_low_SNR_signals=neglect_low_SNR_signals, SNR_threshold=SNR_threshold, tp=tp)
            time_differences_single_emitter.append(temp[2])
        time_differences.append(time_differences_single_emitter)
    print("\n\n\n\n\n\n\n\n")
    print("*** Time Differences ***")
    print("___Each row corresponds to an emission point.___")
    print("___Each Column corresponds to an reception point. (sticker)___\n\n")
    print(time_differences)
    return np.array(time_differences)

# np.savetxt("time_differences.csv", get_time_differences(loc, 22))