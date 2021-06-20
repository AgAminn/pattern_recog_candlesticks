from typing import List
from flask import Flask, render_template, request, escape

import talib
import yfinance as yf

import os, csv

from yfinance import ticker

from comapny_symbol_dic import company_stock_symbol as company_dictionary
from patterns_dic import candlestick_patterns
from pattern_detector import load_data,result_analysis

app = Flask(__name__)

@app.route('/update_companies_info')
def update_companies_info():
    '''
    with open('datasets/companies.csv') as f:
        for line in f:
            if "," not in line :
                continue
            symbol = line.split(',')[0]
    '''

    msft = yf.Ticker("MSFT",)
    company_name = msft.info['longName']
    print(company_name)
    return {
        "code": "success"
    }

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