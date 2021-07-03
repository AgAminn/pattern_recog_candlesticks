#from typing import List
from flask import Flask, render_template, request, escape,jsonify

import talib
#from werkzeug.exceptions import MethodNotAllowed
import yfinance as yf

#import os, csv

#from yfinance import ticker

#from comapny_symbol_dic import company_stock_symbol as company_dictionary
from app.patterns_dic import candlestick_patterns,pattern_of_interest
from app.pattern_detector import load_data,qtoday,pattern_check,load_data_df,rsi_calc,trend_detector,adv_patterns,data_loader_df
from app.harmonics import harmonics_list

from app.HarmonicPatterns.harmonic_functions import search_func

app = Flask(__name__)

@app.route('/update_companies_info/<tkr0>',methods=['GET'])
def update_companies_info(tkr0):
    '''
    with open('datasets/companies.csv') as f:
        for line in f:
            if "," not in line :
                continue
            symbol = line.split(',')[0]
    '''

    #msft = yf.Ticker("MSFT",)
    #company_name = msft.info['longName']
    #print(company_name)
    '''
    info_j = {
        'ticker' : '',
        'date' :'',
        'engulfing':''
    }
    '''

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


@app.route('/update_stock_info/<tkr0>')
def update_stock_info(tkr0):

    data0 = data_loader_df(ticker_st=tkr0)
    data = data0.data_portion()
    new_ib = {
        'date' : qtoday,
        'ticker/Symbol' : tkr0,
        'company_name' : data0.company_name
    }
    for pat in pattern_of_interest.keys():
        label = pattern_check(data=data,pattern_name=pat)
        new_ib[pattern_of_interest[pat]]=label
    
    data = data0.data_portion(n_days=120)
    rsi_df = rsi_calc(data=data)
    new_ib['RSI']=rsi_df.tail(1).values[0]

    new_ib['Trend']=trend_detector(data=data)
    
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
    new_ib['Harmonics']=search_func(data)
    #info_c.append(new_ib)

    return jsonify(new_ib)



@app.route('/talib_info/<tkr0>',methods=['GET'])
def talib_info(tkr0):

    if request.method == 'GET':
        try:
            c_name = yf.Ticker(str(tkr0))
        except:
            raise ValueError('Loading data failed , check the stock name and date')
        
        #data = load_data_df(ticker_st=tkr0)
        data0 = data_loader_df(ticker_st=tkr0,n_days=15)
        data = data0.data_portion()
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
    companies_symbols = company_dictionary.keys()
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
    return render_template('index02.html',companies_symbols=company_dictionary, candlestick_patterns=candlestick_patterns,
pattern_res=pattern_res,stock=tiker_stock)
