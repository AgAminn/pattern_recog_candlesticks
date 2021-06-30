#import matplotlib.pyplot as plt
from app.harmonic_func import *
#from app.pattern_detector import data_loader_df
# Importing Data
#tkr0 = 'GOOG'
# data0 = data_loader_df(ticker_st=tkr0,n_days=12*30)
#data = data0.data_portion()    
def harmonics_list(data):
    
    label_res = {
        'Gartley':False,
        'Butterfly':False,
        'Bat':False,
        'Crab':False
    }

    #data['time'] = pd.to_datetime(data['time'], format='%d.%m.%Y %H:%M:%S.%f')
    #data = data.set_index(data['time'])
    data = data.drop_duplicates(keep=False)
    price = data['Close'].copy()

    err_allowed = 10.0/100

    # Find peaks
    for i in range(100, len(price)):
        current_idx, current_pat, start, end = peak_detect(price.values[:i])

        XA = current_pat[1] - current_pat[0]
        AB = current_pat[2] - current_pat[1]
        BC = current_pat[3] - current_pat[2]
        CD = current_pat[4] - current_pat[3]

        moves = [XA, AB, BC, CD]

        gartley = is_Gartley(moves, err_allowed)
        butterfly = is_Butterfly(moves, err_allowed)
        bat = is_Bat(moves, err_allowed)
        crab = is_Crab(moves, err_allowed)

        harmonics = np.array([gartley, butterfly, bat, crab])
        labels = [
            'Gartley',
            'Butterfly',
            'Bat',
            'Crab'
        ]

        if np.any(harmonics == 1) or np.any(harmonics == -1):
            for j in range(0, len(harmonics)):
                if harmonics[j] == 1 or harmonics[j] == -1:
                    sense = 'Bearish ' if harmonics[j] == -1 else 'Bullish '
                    label = sense + labels[j] + ' Found'
                    label_res[harmonics[j]] = sense
    return label_res

'''                #plt.title(label)
                #plt.plot(np.arange(start, i+15), price.values[start:i+15])
                #plt.scatter(current_idx, current_pat, c='r')
                #plt.show()
'''