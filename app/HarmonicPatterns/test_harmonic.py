from yfinance import ticker
from harmonic_functions import HarmonicDetector, kline_to_df#*#app.HarmonicPatterns.
#from settings import NOTIFY_URL
from settings import MAIN_SYMBOLS, ALT_SYMBOLS, PERIODS, ERROR_RATE
from settings import PROCESS_COUNT

from functools import partial
import pandas as pd
#from harmonic_functions import kline_to_df
from datetime import datetime, timedelta


def search_function(detector, symbols, savefig=False, predict=True, only_last=False, alert=False, plot=False):
    
    resdic = {
        'gartley':False,
        'shark':False,
        'cypher':False,
        'butterfly':False,
        'deepcrab': False,
        'crab':False,
        'abcd':False,
        '5o':False,
        'altbat':False,
        'bat':False
    }
    list_H =list(resdic.keys())
    print(list_H)
    RETRY_TIMES=3
    for symbol in symbols:
    
        df = kline_to_df(ticker_st=symbol,start_date=s_day,end_date=e_day)

        patterns, predict_patterns = detector.search_patterns(df, only_last=only_last, last_n=4, plot=plot, predict=predict)
        #print('Tyoe and shape of var patterns',type(patterns))
        #print(len(patterns))
        for pat in patterns:
            msg = f'{symbol} {100} \npatterns found: {pat[1]}, {pat[0]}, \n {pat[2]}, {pat[3]}'
            print('Found pattern :')
            #print(msg)
            '''logger.info(msg)
            if alert and pat[0][-1][2] == len(df)-1:
                send_alert(f'Pattern_Found_{symbol}_{period}', msg)'''

        
        for pat in predict_patterns:
            print('Found pattern ::::::')
            msg = '\n'.join([f'{p} {v}' for p,v in list(zip([str(dt) for dt in pat[1]], [p for p in pat[0]]))])
            msg = f'{symbol} {888} {msg} {pat[2]} {pat[3]}'
            #print(msg)
            print('p    tern found ----------->',pat[2])
            key_res = pat[2]
            res = key_res.split('predict')
            print('actual results :',res[0])

            for q in list_H:
                if q in res[0]:
                    resdic[q]= res[0]
                    break
        print('final dic res *****')
        print(resdic)

        '''
            logger.info(msg)
            if alert:
                send_alert(f'Pattern_Predict_{symbol}_{period}', msg)'''



def search_func(detector, df, only_last=False):
    
    resdic = {
        'gartley':False,
        'shark':False,
        'cypher':False,
        'butterfly':False,
        'deepcrab': False,
        'crab':False,
        'abcd':False,
        '5o':False,
        'altbat':False,
        'bat':False
    }
    list_H =list(resdic.keys())

    #df = kline_to_df(ticker_st=tkr_stock,start_date=s_day,end_date=e_day)

    _, predict_patterns = detector.search_patterns(df, only_last=only_last, last_n=4, plot=False, predict=True)
    
    for pat in predict_patterns:
        #msg = '\n'.join([f'{p} {v}' for p,v in list(zip([str(dt) for dt in pat[1]], [p for p in pat[0]]))])
        #msg = f'{symbol} {888} {msg} {pat[2]} {pat[3]}'
        #print(msg)
        #print('p    tern found ----------->',pat[2])
        key_res = pat[2]
        res = key_res.split('predict')
        print('actual results :',res[0])

        for q in list_H:
            if q in res[0]:
                resdic[q]= res[0]
                break
    print('final dic res *****')
    print(resdic)
    return resdic




today = datetime.date(datetime.now()) + timedelta(days=2)
e_day = today - timedelta(days=20)
s_day = today - timedelta(days=600)

data = kline_to_df(ticker_st="TATAMOTORS.NS",start_date=s_day,end_date=today)

detector = HarmonicDetector(error_allowed=ERROR_RATE, strict=True)
#symbols = [*MAIN_SYMBOLS, *ALT_SYMBOLS]
symbols = ['TATAMOTORS.NS','aapl','goog']
search = partial(search_function, detector)
#test0 = search_function(detector=detector,symbols=symbols)

s = search_func(detector=detector,df=data)