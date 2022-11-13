from sklearn.ensemble import IsolationForest
from data_loader import read_data, get_VibVol, get_RefVol
from pre_processing import smooth, KMF, normalise, detrend

import numpy as np
import pandas as pd
import scipy as sc
import matplotlib.pyplot as plt

emitter = 11

# Load in all of the hits of the emission location as a single 1-D array for training
data = read_data((emitter))
training_data = normalise(data[4].flatten())
train_Ref = np.reshape(training_data, (-1, 1))
trainer_Ref = IsolationForest(contamination=0.0005).fit(train_Ref) # contamination= 1/len(data[0])

test = get_RefVol(emitter, 5)
temp = np.reshape(test[1], (-1, 1))
outcome = trainer_Ref.predict(temp)
print(outcome)
np.savetxt("outcome.csv", outcome, delimiter=",")

plt.plot(test[0], smooth(test[1]))
plt.scatter(test[0], outcome)
plt.show()