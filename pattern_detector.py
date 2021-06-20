from os import P_DETACH
import os
import re
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime
import talib

from patterns_dic import candlestick_patterns

#2021-06-21
#"MERCURYLAB.BO"
def load_data(ticker_st,start_date,end_date, pattern_name):
    data = yf.download(ticker_st, start=start_date, end=end_date)
    df_date = pd.to_datetime(data.index)
    tips_filtered = data.reindex(columns =  ['Open', 'High', 'Low', 'Close'])
    col_names = list(data.index)    

    
    #(data['Open'],data['High'],data['Low'],data['close'])
    pattern_function = getattr(talib, pattern_name)

    #print(tips_filtered.head(5))
    #res0 = talib.CDLENGULFING(data['Open'],data['High'],data['Low'],data['Close'])
    results = None
    try:
        results = pattern_function(data['Open'],data['High'],data['Low'],data['Close'])
    except:
        print('failed ?!')
        pass
    return results

def result_analysis(res_list,pattern_name):
    trend_st = None # for every other type
    trend_bl_br = None # ofr engulfing only 
    #if res_list:
    #if pattern_name == 'CDLENGULFING':
    if pattern_name == 'CDLENGULFING':
        last = res_list.tail(1).values[0]
        if last > 0:
            trend_bl_br = 'bullish'
            return trend_bl_br
            trend_st = candlestick_patterns[pattern_name]
        elif last < 0:
            trend_bl_br = 'bearish'
            return trend_bl_br
            trend_st = candlestick_patterns[pattern_name]
        else:
            trend_bl_br = None
            trend_st = None
    '''
    if pattern_name == 'CDLHAMMER':
        last = res_list.tail(1).values[0]
        if last > 0:
            trend_st = 'Hammer'
        else:
            trend_st = None
    if pattern_name == 'CDLINVERTEDHAMMER':
        last = res_list.tail(1).values[0]
        if last > 0:
            trend_st = 'Inverted Hammer'
        else:
            trend_st = None
    if pattern_name == 'CDLHANGINGMAN':
        last = res_list.tail(1).values[0]
        if last < 0:
            trend_st = 'Hanging Man'
        else:
            trend_st = None
    '''
    last = res_list.tail(1).values[0]
    if last != 0:
        trend_st = 'True'#candlestick_patterns[pattern_name]
        
    return trend_st#,trend_bl_br


def trend_detector():
    

class patten_detected():

    def __init__(self):
        pass
        

def rsi_calc(start_date,end_date) :
    df = yf.download("MERCURYLAB.BO", start=start_date, end=end_date)
    df_date = pd.to_datetime(df.index)
    df['Up Move'] = np.nan
    df['Down Move'] = np.nan
    df['Average Up'] = np.nan
    df['Average Down'] = np.nan
    # Relative Strength
    df['RS'] = np.nan
    # Relative Strength Index
    df['RSI'] = np.nan
    ## Calculate Up Move & Down Move
    for x in range(1, len(df)):
        df['Up Move'][x] = 0
        df['Down Move'][x] = 0
        
        if df['Close'][x] > df['Close'][x-1]:
            df['Up Move'][x] = df['Close'][x] - df['Close'][x-1]
            
        if df['Close'][x] < df['Close'][x-1]:
            df['Down Move'][x] = abs(df['Close'][x] - df['Close'][x-1])  
            
    ## Calculate initial Average Up & Down, RS and RSI
    df['Average Up'][14] = df['Up Move'][1:15].mean()
    df['Average Down'][14] = df['Down Move'][1:15].mean()
    df['RS'][14] = df['Average Up'][14] / df['Average Down'][14]
    df['RSI'][14] = 100 - (100/(1+df['RS'][14]))
    ## Calculate rest of Average Up, Average Down, RS, RSI
    for x in range(15, len(df)):
        df['Average Up'][x] = (df['Average Up'][x-1]*13+df['Up Move'][x])/14
        df['Average Down'][x] = (df['Average Down'][x-1]*13+df['Down Move'][x])/14
        df['RS'][x] = df['Average Up'][x] / df['Average Down'][x]
        df['RSI'][x] = 100 - (100/(1+df['RS'][x]))
    
    return df['RSI'],df_date


if __name__=='__main__':
    '''
    pattern_name = 'CDLMARUBOZU'
    res_f = load_data(start_date='2020-06-01',end_date='2021-05-17', pattern_name=pattern_name)
    last = res_f.tail(1).values[0]

    print('res last ',last)
    
    print(res_f)
    cntr = 0
    for r in res_f:
        cntr+=1
        dum = res_f[:cntr]
        if r!=0:
            print('final results',r)
            print('judge trend',result_analysis(dum,pattern_name))
    q_res,q_tr = result_analysis(res_f,pattern_name)
    print('querry result ',q_res)
    '''
    rsi,y_t = rsi_calc(start_date='2020-06-01',end_date='2021-05-17')
    print('test RSI',type(rsi))
    print(rsi[-20:])
    print(len(rsi))
    df_date = pd.to_datetime(rsi[-20:].index)
    print(len(df_date))