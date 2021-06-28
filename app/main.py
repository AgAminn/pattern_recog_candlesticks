from typing import List
from flask import Flask, render_template, request, escape,jsonify

import talib
from werkzeug.exceptions import MethodNotAllowed
import yfinance as yf

import os, csv

from yfinance import ticker

from comapny_symbol_dic import company_stock_symbol as company_dictionary
from patterns_dic import candlestick_patterns,pattern_of_interest
from pattern_detector import load_data,result_analysis,qtoday,pattern_check,load_data_df,rsi_calc,trend_detector,adv_patterns

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
        
        new_ib['Head and Shoulders']=data_l.find_patterns('Head and Shoulders')
        new_ib['Inv Head and Shoulders']=data_l.find_patterns('Inv Head and Shoulders')
        new_ib['Double Bottom']=data_l.find_patterns('Double Bottom')
        new_ib['Double Top']=data_l.find_patterns('Double Top')
        new_ib['Bullish penant']=data_l.find_patterns('Bullish penant')
        new_ib['Bearish pennant']=data_l.find_patterns('Bearish pennant')
        new_ib['falling wedge']=data_l.find_patterns('falling wedge')
        new_ib['Rising wedge']=data_l.find_patterns('Rising wedge')
        new_ib['bullish flag']=data_l.find_patterns('bullish flag')
        new_ib['Bearish flag']=data_l.find_patterns('Bearish flag')
        #info_c.append(new_ib)

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
        pattern_res = result_analysis(res_list=list_feed,pattern_name=pattern)
    return render_template('index02.html',companies_symbols=company_dictionary, candlestick_patterns=candlestick_patterns,
pattern_res=pattern_res,stock=tiker_stock)
