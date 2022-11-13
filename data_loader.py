# Dependencies import
import scipy.io as scio
import numpy as np

# Hitting locations naming convention for the .mat files
# locations = ['11', '14', '17', '21', '22', '23', '25', '26', '27', '31', '32', '33', '35', '36', '37', '41', '44',
#              '47']



def flatten(list):
    array = np.array(list)
    return array.flatten()

def read_data(loc):
    loc = str(loc)
    data = scio.loadmat('raw_data/' + loc + '.mat')

    # Extract data and write in numpy array

    t = flatten(data['xVibVol'])  # time
    X, Y = flatten(data['X']), flatten(data['Y'])

    VibVol, RefVol = data['yVibVol'], data['yRefVol']  # Voltage

    print('EMITTING LOCATION ' + loc)
    print('Reading from file: ' + '\033[1m' + 'raw_data/' + loc + '.mat' + '\033[0m')
    print('# Laser Points in this file: ', len(X))
    print('# Time samples per laser point: ', len(t))
    print('# Time samples per trigger:', len(RefVol[0][:]))
    # Safety precausion
    if len(VibVol) != len(RefVol):
        print("\n\n***** WARNING *****")
        print("The size of the Ref array is not equal to the size of the Vib array. This is unlogical!")
    elif len(X) != len(Y):
        print("\n\n***** WARNING *****")
        print("The size of the X array is not equal to the size of the Y array. This is unlogical!")
    else:
        print('\033[1;3m' + 'Output data sanity check: ' + '\033[0m' + 'OK')

    return t, X, Y, VibVol, RefVol

def get_VibVol(index_of_emitting_point, index_of_receiving_point):
    temp = read_data(index_of_emitting_point)
    t = temp[0]
    x = temp[1][index_of_receiving_point]
    y = temp[2][index_of_receiving_point]
    print("\nJUST TO VERIFY WITH YOU :)")
    print("You are calling data captured by the Vibrometer.")
    print("Index of emitting point: ", index_of_emitting_point)
    print("Index of receiving point: ", index_of_receiving_point)
    print("Location of this receiving point (as outputted by vibrometer): ", x, y)
    vib_time_series = temp[3][index_of_receiving_point]
    print("0-th returned array of this function is time, 1-st array is the original Amplitude")
    return t, vib_time_series

def get_RefVol(index_of_emitting_point, index_of_receiving_point):
    temp = read_data(index_of_emitting_point)
    t = temp[0]
    x = temp[1][index_of_receiving_point]
    y = temp[2][index_of_receiving_point]
    print("\nJUST TO VERIFY WITH YOU :)")
    print("You are calling data captured by the Reference.")
    print("Index of emitting point: ", index_of_emitting_point)
    print("Index of receiving point: ", index_of_receiving_point)
    print("Location of this receiving point (as outputted by vibrometer): ", x, y)
    ref_time_series = temp[4][index_of_receiving_point]
    print("0-th returned array of this function is time, 1-st array is the original Amplitude")
    return t, ref_time_series