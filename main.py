# Imports
import numpy as np
import pandas as pd
import scipy as sc
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from data_loader import * # Functions to read out all data contained in folder raw_data
from align_waveforms import * # Functions to align waveforms from the same sticker and filter out bad SNR signals
from pre_processing import * # Filters etc.
from time_extraction_for_solenoid import * # Finding t_0 for the solenoid



# define the following
locations = [11, 14, 17, 21, 22, 23, 25, 26, 27, 31, 32, 33, 35, 36, 37, 41, 44, 47]

def main(list_of_emitting_locations, number_of_stickers, save_results_to_csv = True,
         make_plots = False, neglect_low_SNR_signals = True, SNR_threshold=0.1, tp=17.5):
    results = get_time_differences(list_of_emitting_locations, number_of_stickers,
         make_plots = make_plots, neglect_low_SNR_signals = neglect_low_SNR_signals, SNR_threshold=SNR_threshold, tp=tp)

    if save_results_to_csv == True:
        export_to_csv(results, "time_differences.csv")


if __name__ == "__main__":
    locations = locations
    number_of_stickers = 22

    # Do you want to save the results?
    # I would always put this on true as it doesn't take much time and it would be a shame having to rerun it in order to save
    save_csv = True

    # Do you want to visualise what the program is doing?
    # The results are saved in the plots directory
    make_plots = False

    # When processing all the signals do you want to disregard signals below a certain SNR? Select yes and specify a value
    disregard_bad_signals = True
    SNR_threshold = 0.2

    # What should the variance threshold (as a percentage of the median variance before t0) be to trigger t1?
    tp = 16.0 # percent %

    main(locations, number_of_stickers, save_csv, make_plots, disregard_bad_signals, SNR_threshold, tp)