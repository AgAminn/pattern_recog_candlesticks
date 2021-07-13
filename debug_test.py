from yfinance import ticker
from company_symbol_dic import company_stock_symbol
import requests
import pytest
import yfinance as yf
list_stocks = list(company_stock_symbol.keys())
from app.pattern_detector import data_loader_df
from datetime import datetime
import pandas as pd

def backup_loader(ticker='TOAL.BO',start_date="2020-12-01",end_date='2021-07-10'):
    '''In case yfçnance fails to load the data
        for internal issues (and not because the ticker isn't listed'''
    
    refmultiply = 86400
    refdateyahoo = 1420156800  # This is 1/2/2015
    date_frmt = '%Y-%m-%d'
    #start_dt="2020-09-01"
    #start = datetime.strptime(start_dt, date_fmt).date()
    refdate = datetime.strptime('2015-01-02', date_frmt).date()
    startdate = datetime.strptime(start_date, date_frmt).date()
    enddate = datetime.date(datetime.now())
    enddatetoday = datetime.strptime(end_date, date_frmt).date()
    if refdate == startdate:
        startdateyahoo = refdateyahoo
    else:
        startdateyahoo = refdateyahoo + (startdate - refdate).days * refmultiply

    if refdate == enddate:
        enddateyahoo = refdateyahoo
    elif enddate == datetime.date(datetime.now()):
        enddateyahoo = refdateyahoo + ((enddatetoday - refdate).days+1) * refmultiply #+1 is constant for correction, normally not needed
    else:
        enddateyahoo = refdateyahoo + ((enddate - refdate).days+1) * refmultiply #+1 is constant for correction, normally not needed

    
    url = "https://query1.finance.yahoo.com/v7/finance/download/" + ticker + \
        "?period1=" + str(startdateyahoo) + "&period2=" + str(enddateyahoo) + "&interval=1d&events=history"
    fullLoad = pd.read_csv(url)
    fullLoad['Date'] = pd.to_datetime(fullLoad['Date'])
    fullLoad = fullLoad.set_index('Date')
    print('alt method', len(fullLoad))
    return fullLoad

print("length of list of stocks for testing",len(list_stocks))
#print((list_stocks[0]))
print('start testing , it may take a while (10 minute)')

def check_app_load(ticker_st=list_stocks):
    cnt =0
    for i in ticker_st:
        r = requests.head("https://indian-tiger.herokuapp.com/update_stock_info/"+i)
        if r.status_code == 200:
            cnt+=1
        else:
            print("https://indian-tiger.herokuapp.com/update_stock_info/"+i)
    return cnt
        #return r.status_code ==200
        #assert(r.status_code ==200)


def check_app_02(ticker_st=list_stocks):
    cnt =0
    err=0
    readable_stocks = []
    for i in ticker_st:
        try :
            dt = yf.download(i,start='2021-04-01',end='2021-04-11')
            if len(dt)>1:
                cnt+=1
            else:
                readable_stocks.append(i)
        except:
            err+=1
    print('error in exc ', err)

    return cnt,readable_stocks
        #return r.status_code ==200
        #assert(r.status_code ==200)

def check_app_03(ticker_st=list_stocks):
    cnt =0
    err=0
    readable_stocks = []
    for i in ticker_st:
        try :
            dt = data_loader_df(ticker_st=i,n_days=7,end_date='2021-04-11')
            if len(dt.data_full)>1:
                cnt+=1
            else:
                readable_stocks.append(i)
        except:
            err+=1
    print('error in exc ', err)

    return cnt,readable_stocks
        #return r.status_code ==200
        #assert(r.status_code ==200)
'''
dta = data_loader_df(ticker_st='aapl',n_days=20,end_date='2021-06-06')
f = dta.data_full
print(len(dta.data_full))
'''
#import pandas_datareader as pdr 
res_dic = {}
def check_app_05(ticker_st):
    cnt =0
    
    try :
        dt = yf.download(ticker_st,start='2021-04-01',end='2021-04-11',)
        if len(dt)>1:
            cnt +=1
            res_dic[ticker_st]= True
        else:
            print('failed fo 2')
            dt= backup_loader(ticker=ticker_st,start_date='2021-04-01',end_date='2021-04-11')
            if len(dt)>1:
                cnt +=1
    except:
        pass
    return cnt
from multiprocessing import Pool
def chad_method(tikers=list_stocks):
    from multiprocessing import Pool
    
    with Pool(5) as p :
        p.map(check_app_05,tikers)
    
    return res_dic,0


#res,readable_stks = chad_method()#check_app_03()#check_app_load()

#tickers = ['msft', 'aapl', 'twtr', 'intc', 'tsm', 'goog', 'amzn', 'fb', 'nvda']
#df = pdr.DataReader(tickers, data_source='yahoo', start='2017-01-01', end='2020-09-28')

'''
print('finsih testing')
#res = check_app_load()
print('N tests           ',len(list_stocks))
print('N successful test ',res)
'''
#with open('your_file.txt', 'w') as f:
#    for item in readable_stks:
#        f.write("%s\n" % item)
'''
file1 = open('your_file.txt', 'r')
Lines = file1.readlines()
linesx = [l.strip() for l in Lines]
print('res :',len(linesx))
#print(linesx)
res_list = list(set(list_stocks)-set(linesx) )
print('result disjoint list ',len(res_list))
'''
#with open('working_stocks.txt', 'w') as f:
#    for item in res_list:
#        f.write("%s\n" % item)

if __name__=='__main__':
    file1 = open('not_working_stocks.txt', 'r')
    Lines = file1.readlines()
    linesx = [l.strip() for l in Lines]

    #tikers = list_stocks#['msft', 'aapl', 'twtr', 'intc', 'tsm', 'goog', 'amzn', 'fb', 'nvda']
    tikers = linesx
    with Pool(5) as p :
        res_v = p.map(check_app_05,tikers)
    print(res_dic)
    print(len(res_v))
    print(sum(res_v))