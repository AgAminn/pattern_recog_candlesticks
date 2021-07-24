#from typing import List
from flask import Flask, render_template, request, escape,jsonify

import talib
#from werkzeug.exceptions import MethodNotAllowed
import yfinance as yf
import pandas as pd
from yfinance import ticker
#import os, csv

#from yfinance import ticker

#from comapny_symbol_dic import company_stock_symbol as company_dictionary
from app.patterns_dic import candlestick_patterns,pattern_of_interest
#from app.pattern_detector import load_data,qtoday,pattern_check,load_data_df,rsi_calc,trend_detector,adv_patterns,data_loader_df
from app.pattern_detector import qtoday,pattern_check, rsi_calc,trend_detector,adv_patterns,data_loader_df
from app.harmonics import harmonics_list
from app.comapnies_dic_ed02 import company_stock_symbol
from app.company_symbol_dic import company_stock_symbol as full_tickers_list
from app.pattern_detector import import_all_data
from app.HarmonicPatterns.harmonic_functions import search_func

app = Flask(__name__)
'''
@app.route('/update_companies_info/<tkr0>',methods=['GET'])
def update_companies_info(tkr0):
    

    #msft = yf.Ticker("MSFT",)
    #company_name = msft.info['longName']
    #print(company_name)
    

    if request.method == 'GET':
        #tkr = request.form['ticker']
        #c_name = yf.Ticker(str(tkr0))
        #print(c_name)
        try:
            c_name = yf.Ticker(str(tkr0))
        except:
            raise ValueError('Loading data failed , check the stock name and date')
        
        data = load_data_df(ticker_st=tkr0)
        data_l = adv_patterns(ticker_company=tkr0)
        print(data.head(5))
        #print('data date ',)
        new_ib = {
            'date' : qtoday,
            'ticker/Symbol' : tkr0,
            'company_name' : c_name.info['longName']
        }
        for pat in pattern_of_interest.keys():
            label = pattern_check(data=data,pattern_name=pat)
            new_ib[pattern_of_interest[pat]]=label
        
        rsi_df = rsi_calc(data=data)
        new_ib['RSI']=rsi_df.tail(1).values[0]

        new_ib['Trend']=trend_detector(data=data)
        
        new_ib['Head and Shoulders']=data_l.find_patterns_HS('Head and Shoulders')
        new_ib['Inv Head and Shoulders']=data_l.find_patterns_HS('Inv Head and Shoulders')
        new_ib['Double Bottom']=data_l.find_patterns_D('Double Bottom')
        new_ib['Double Top']=data_l.find_patterns_D('Double Top')
        new_ib['Bullish penant']=data_l.find_patterns_flag('Bullish penant')
        new_ib['Bearish penant']=data_l.find_patterns_flag('Bearish penant')
        new_ib['Falling wedge']=data_l.find_patterns_flag('Falling wedge')
        new_ib['Rising wedge']=data_l.find_patterns_flag('Rising wedge')
        new_ib['Bullish flag']=data_l.find_patterns_flag('Bullish flag')
        new_ib['Bearish flag']=data_l.find_patterns_flag('Bearish flag')
        #info_c.append(new_ib)

    return jsonify(new_ib)
'''

@app.route('/update_stock_info/<tkr0>')
def update_stock_info(tkr0):

    data0 = data_loader_df(ticker_st=tkr0)
    if type(data0.data_full) == type(None):
        print('-- Failed loading data --')
        return jsonify({'Error':'Failed loading data'})
    print('** Data loaded successfully **')

    data = data0.data_portion(n_days=30)
    new_ib = {
        'date' : qtoday,
        'ticker/Symbol' : tkr0,
        'company_name' : data0.company_name
    }
    print('initialisation date ',qtoday)
    for pat in pattern_of_interest.keys():
        label = pattern_check(data=data,pattern_name=pat)
        new_ib[pattern_of_interest[pat]]=label
    
    data = data0.data_portion(n_days=120)
    rsi_df = rsi_calc(data=data)
    new_ib['RSI']=rsi_df.tail(1).values[0]

    new_ib['Trend']=trend_detector(data=data)
    data = data0.data_portion(n_days=6*30)
    data_l = adv_patterns(data_orig=data,sampling_ratio=10) # one year of data for HS & inv HS
    new_ib['Head and Shoulders']=data_l.find_patterns_HS('Head and Shoulders')
    new_ib['Inv Head and Shoulders']=data_l.find_patterns_HS('Inv Head and Shoulders')
    data_l = adv_patterns(data_orig=data,n_days_data=3*30 ,sampling_ratio=5) # 3 x months of data for DT & DB
    new_ib['Double Bottom']=data_l.find_patterns_D('Double Bottom')
    new_ib['Double Top']=data_l.find_patterns_D('Double Top')
    data_l = adv_patterns(data_orig=data,n_days_data=1*30,sampling_ratio=2) # 1 x month of data for HS & inv HS
    new_ib['Bullish penant']=data_l.find_patterns_flag('Bullish penant')
    new_ib['Bearish penant']=data_l.find_patterns_flag('Bearish penant')
    data_l = adv_patterns(data_orig=data,n_days_data=6*30,sampling_ratio=5) # 6 x months of data for wedges
    new_ib['Falling wedge']=data_l.find_patterns_flag('Falling wedge')
    new_ib['Rising wedge']=data_l.find_patterns_flag('Rising wedge')
    data_l = adv_patterns(data_orig=data,n_days_data=3*7,sampling_ratio=2) # 3x weeks of data for flags
    new_ib['Bullish flag']=data_l.find_patterns_flag('Bullish flag')
    new_ib['Bearish flag']=data_l.find_patterns_flag('Bearish flag')

    data = data0.data_portion(n_days=6*30)
    #new_ib['Harmonics']=harmonics_list(data)
    #new_ib['Harmonics']=search_func(data)
    new_ib = {**new_ib,**search_func(data)}
    #info_c.append(new_ib)

    return jsonify(new_ib)






    

# the below pages aren't required; for testing and display
@app.route('/update_stock_info_5000/')
def update_stock_info_500():


    def process_data(data_orig,st_name='goog'):

        if st_name in list(full_tickers_list.keys()):
            company_name = full_tickers_list[st_name]
        else:
            company_name = 'Not found in repo'
        
        new_ib = {
            'date' : qtoday,
            'ticker/Symbol' : st_name,
            'company_name' : company_name
        }
        data = data_orig.tail(300)
        for pat in pattern_of_interest.keys():
            label = pattern_check(data=data,pattern_name=pat)
            new_ib[pattern_of_interest[pat]]=label
        
        data = data_orig.tail(300)#data0.data_portion(n_days=120)
        rsi_df = rsi_calc(data=data)
        new_ib['RSI']=rsi_df.tail(1).values[0]

        new_ib['Trend']=trend_detector(data=data)
        data = data_orig.tail(6*30)#data0.data_portion(n_days=6*30)
        data_l = adv_patterns(data_orig=data,sampling_ratio=10) # one year of data for HS & inv HS
        new_ib['Head and Shoulders']=data_l.find_patterns_HS('Head and Shoulders')
        new_ib['Inv Head and Shoulders']=data_l.find_patterns_HS('Inv Head and Shoulders')
        data_l = adv_patterns(data_orig=data,n_days_data=3*30 ,sampling_ratio=5) # 3 x months of data for DT & DB
        new_ib['Double Bottom']=data_l.find_patterns_D('Double Bottom')
        new_ib['Double Top']=data_l.find_patterns_D('Double Top')
        data_l = adv_patterns(data_orig=data,n_days_data=1*30,sampling_ratio=2) # 1 x month of data for HS & inv HS
        new_ib['Bullish penant']=data_l.find_patterns_flag('Bullish penant')
        new_ib['Bearish penant']=data_l.find_patterns_flag('Bearish penant')
        data_l = adv_patterns(data_orig=data,n_days_data=6*30,sampling_ratio=5) # 6 x months of data for wedges
        new_ib['Falling wedge']=data_l.find_patterns_flag('Falling wedge')
        new_ib['Rising wedge']=data_l.find_patterns_flag('Rising wedge')
        data_l = adv_patterns(data_orig=data,n_days_data=3*7,sampling_ratio=2) # 3x weeks of data for flags
        new_ib['Bullish flag']=data_l.find_patterns_flag('Bullish flag')
        new_ib['Bearish flag']=data_l.find_patterns_flag('Bearish flag')

        data = data_orig.tail(6*30)#data0.data_portion(n_days=6*30)
        #new_ib['Harmonics']=harmonics_list(data)
        #new_ib['Harmonics']=search_func(data)
        new_ib = {**new_ib,**search_func(data)}
        return new_ib

    full_stock_data={}
    stock_list=list(full_tickers_list.keys())
    stock_list = stock_list[:5]
    print('stock list ',stock_list)
    dfs = import_all_data(ticker_list=stock_list,start_date=400,end_date='2021-07-15')
    for st in stock_list:
        df = dfs[st]
        print(df.head(5))
        if len(df)>1:
            print('lennnnnnnnnn',len(df))
            full_stock_data[st]=process_data(df,st_name=st)
        
    #info_c.append(new_ib)

    return jsonify(full_stock_data)

@app.route('/talib_info/<tkr0>',methods=['GET'])
def talib_info(tkr0):

    if request.method == 'GET':
        try:
            c_name = yf.Ticker(str(tkr0))
        except:
            c_name = tkr0
            raise ValueError('Loading data failed , check the stock name and date')
        
        #data = load_data_df(ticker_st=tkr0)
        data0 = data_loader_df(ticker_st=tkr0,n_days=120)
        data = data0.data_portion(n_days=110)
        new_ib = {
            'date' : qtoday,
            'ticker/Symbol' : tkr0,
            'company_name' : c_name.info['longName']
        }
        for pat in candlestick_patterns.keys():
            label = pattern_check(data=data,pattern_name=pat)
            new_ib[candlestick_patterns[pat]]=label
    return jsonify(new_ib)


@app.route('/')
def index():
    companies_symbols = company_stock_symbol.keys()
    #print(companies_symbols)
    pattern_res =''
    tiker_stock=''
    start_date = request.args.get('start',False)
    end_date = request.args.get('end',False)
    pattern  = request.args.get('pattern', False)
    tiker_stock = request.args.get('ticker_c', False)
    print('info d1 ', type(start_date))
    print('info d2 ', end_date)
    print('ticker ',tiker_stock)
    print('inf pattern',pattern)
    if (tiker_stock!='') & (pattern!=False):
        #msft = yf.Ticker(tiker_stock)
        #company_name = msft.info['longName']........
        #print('rest' , company_name)
        list_feed = load_data(ticker_st=tiker_stock,start_date=start_date,end_date=end_date,pattern_name=pattern)
        pattern_res = 0#result_analysis(res_list=list_feed,pattern_name=pattern)
    return render_template('index02.html',companies_symbols=company_stock_symbol, candlestick_patterns=candlestick_patterns,
pattern_res=pattern_res,stock=tiker_stock)


@app.route('/test0')
def index2():
    def stock_data(date_q,tickers):
        res = []
        for tkr0 in tickers:
            data0 = data_loader_df(ticker_st=tkr0,n_days=6*30,end_date=date_q)
            data = data0.data_portion(n_days=90)
            new_ib = {
                'date' : date_q,
                'ticker/Symbol' : tkr0,
            }
            for pat in pattern_of_interest.keys():
                label = pattern_check(data=data,pattern_name=pat)
                new_ib[pattern_of_interest[pat]]=label
            
            data = data0.data_portion(n_days=120)
            rsi_df = rsi_calc(data=data)
            new_ib['RSI']=rsi_df.tail(1).values[0]

            new_ib['Trend']=trend_detector(data=data)
            
            data = data0.data_portion(n_days=6*30)
            data_l = adv_patterns(data_orig=data,sampling_ratio=10) # one year of data for HS & inv HS
            new_ib['Head and Shoulders']=data_l.find_patterns_HS('Head and Shoulders')
            new_ib['Inv Head and Shoulders']=data_l.find_patterns_HS('Inv Head and Shoulders')
            data_l = adv_patterns(data_orig=data,n_days_data=3*30 ,sampling_ratio=5) # 3 x months of data for DT & DB
            new_ib['Double Bottom']=data_l.find_patterns_D('Double Bottom')
            new_ib['Double Top']=data_l.find_patterns_D('Double Top')
            data_l = adv_patterns(data_orig=data,n_days_data=1*30,sampling_ratio=2) # 1 x month of data for HS & inv HS
            new_ib['Bullish penant']=data_l.find_patterns_flag('Bullish penant')
            new_ib['Bearish penant']=data_l.find_patterns_flag('Bearish penant')
            data_l = adv_patterns(data_orig=data,n_days_data=6*30,sampling_ratio=5) # 6 x months of data for wedges
            new_ib['Falling wedge']=data_l.find_patterns_flag('Falling wedge')
            new_ib['Rising wedge']=data_l.find_patterns_flag('Rising wedge')
            data_l = adv_patterns(data_orig=data,n_days_data=3*7,sampling_ratio=2) # 3x weeks of data for flags
            new_ib['Bullish flag']=data_l.find_patterns_flag('Bullish flag')
            new_ib['Bearish flag']=data_l.find_patterns_flag('Bearish flag')

            data = data0.data_portion(n_days=6*29)
            #new_ib['Harmonics']=harmonics_list(data)
            #new_ib['Harmonics']=search_func(data)
            dicH =search_func(data)
            for k in list(dicH.keys() ):
                new_ib[k]=dicH[k]
            res.append(new_ib)
            new_ib = {}
        return res

    print('test page start')
    companies_symbols = list(company_stock_symbol.keys())
    end_date = request.args.get('end',False)
    
    print('info date ', end_date)
    if (end_date!=False) :
        import numpy as np
        tab = stock_data(date_q=end_date,tickers=companies_symbols)
        #print(list(tab[0].keys()))
        #df = pd.DataFrame(tab)
        '''
        #df = df.groupby(list(tab[0].keys())).sum()
        df= df.pivot(index='ticker/Symbol',columns=['date','Closing Marubozu', 'Marubozu', 'Engulfing Pattern', 'Evening Star', 'Hammer', 'Inverted Hammer', 'Hanging Man', 
                                                    'Shooting Star', 'Spinning Top', 'Doji', 'Doji Star', 
                                                    'Dragonfly Doji', 'Evening Doji Star', 'Gravestone Doji', 'Morning Doji Star',
                                                    'Morning Star', 'Piercing Pattern', 'Dark Cloud Cover', 'Three Black Crows',
                                                    'Three Advancing White Soldiers', 'RSI', 'Trend', 'Head and Shoulders', 
                                                    'Inv Head and Shoulders', 'Double Bottom', 'Double Top', 'Bullish penant', 
                                                    'Bearish penant', 'Falling wedge', 'Rising wedge', 'Bullish flag', 'Bearish flag',
                                                    'Harmonics'], aggfunc=np.sum,margins=True, fill_value=0,ag)
        '''
        #print(df.head(2))
        #df.to_html('app/templates/index04.html')
        n_com = [i for i in range(len(tab))]
        return render_template('index04.html', tab=tab, n_comp=n_com)
    
    return render_template('index04.html',tab={}, n_comp=5)
