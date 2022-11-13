import pandas as pd
from fbprophet import Prophet
import datetime
import matplotlib.pyplot as plt
import numpy as np

def prophet(df, index_of_emitting_point, sticker_id, prediction_plot=False):
    index0 = int(df['index0'][0])
    signal = np.asarray(df['signal'])
    sig_len = len(signal)
    diff = sig_len-index0+100

    # drop unimportant values for prediction
    df.drop(['time','og_signal', 'boxcar+hanning', 'transformed', 'ref', 'index0', 'index1', 'prediction', 'max_line', 'trigger_line'], axis=1, inplace=True)
    df = df.head(index0)
    df = df.iloc[100:]
    df['date'] = (pd.date_range(start=datetime.datetime(2019, 3, 1),
                                periods=df.shape[0],
                                freq='d'))

    df.columns = ['y', 'ds']

    m = Prophet()
    model = m.fit(df)

    future = m.make_future_dataframe(periods=diff, freq='D')
    forecast = m.predict(future)

    if prediction_plot == True:
        m.plot(forecast)
        plt.savefig("plots/prediction_plots/" + str(index_of_emitting_point) + "_" + str(sticker_id), dpi=400)
        plt.clf()
    else:
        pass

    original = pd.read_pickle('./plots/pickles/'+str(index_of_emitting_point)+'_'+str(sticker_id)+'.pkl')
    original['prediction'] = np.asarray(forecast['yhat'])


    original.to_pickle('./plots/pickles/' + str(index_of_emitting_point) + "_" + str(sticker_id) + '.pkl')

    return np.asarray(forecast['yhat']), model, original

# df = pd.read_pickle('./plots/pickles/11_0.pkl')
# print(df)