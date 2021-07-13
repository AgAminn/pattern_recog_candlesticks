#from os import P_DETACH, stat
#import os
#import re
import numpy as np
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import talib
import trendet
#from yfinance import ticker
from app.patterns_dic import candlestick_patterns

#2021-06-21
#"MERCURYLAB.BO"
qtoday = datetime.date(datetime.now())
today = datetime.date(datetime.now()) + timedelta(days=2)
three_months_ago = today - timedelta(days=180)
print('Today + 2',today)
#print('3 months ago ',three_months_ago)

def load_data(ticker_st,start_date=three_months_ago,end_date=today, pattern_name=''):
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

def load_data_df(ticker_st,start_date=three_months_ago,end_date=today):
    
    #df_date = pd.to_datetime(data.index)
    #tips_filtered = data.reindex(columns =  ['Open', 'High', 'Low', 'Close'])
    #col_names = list(data.index)
    try:
        tik_dum = yf.Ticker(ticker_st)
        tikp=tik_dum.info['longName']
        data = yf.download(ticker_st, start=start_date, end=end_date)
    except:
        raise ValueError('Loading data failed , check the stock name and date')
    return data

class data_loader_df ():

    def __init__(self,ticker_st,n_days=365,end_date=today):
        try:
            #tik_dum = yf.Ticker(ticker_st)
            
            self.company_name=ticker_st #tik_dum.info['longName']
            end__date = end_date
            if type(end_date)==str :
                end__date =datetime.strptime(end_date,'%Y-%m-%d')

            start_date = end__date - timedelta(days=n_days)
            #print('start date :',start_date)
            #print('end date   :',end__date)
            self.data_full = yf.download(ticker_st, start=start_date, end=end__date)
            if (len(self.data_full)>1)==False:
                end__date.strftime(fmt='%Y-%m-%d')
                start_date.strftime(fmt='%Y-%m-%d')
                self.data_full = self.backup_loader(ticker=ticker_st,start_date=start_date,end_date=end__date)
                if (len(self.data_full)>1)==False:
                    raise ValueError('Loading data failed , check the stock name and date')
                else:
                    print('second attempt worked')
        except:
            #raise ValueError('Loading data failed , check the stock name and date')
            print('Loading data failed , 2 x attempts failed -- pass to next step / next stock ')
            pass
    
    def data_portion(self,n_days=7):
        '''start date should be inserted in days''' 
        #s_d = datetime.strptime(start_date, '%Y-%m-%d').date() #start_date='2020-07-21'
        return self.data_full.tail(n_days)
    
    @staticmethod
    def backup_loader(ticker='TOAL.BO',start_date='2020-12-01',end_date='2021-07-10'):
        '''In case yfçnance fails to load the data
            for internal issues (and not because the ticker isn't listed'''
        #import requests
        #import io
        #import pandas as pd
        refmultiply = 86400
        refdateyahoo = 1420156800  # This is 1/2/2015
        date_frmt = '%Y-%m-%d'
        refdate = datetime.strptime('2015-01-02', date_frmt)
        enddate = datetime.date(datetime.now())
        startdate = start_date
        enddatetoday = end_date
        #if type(start_date) == str:
        startdate = datetime.strptime(start_date, date_frmt).date()
        #if type(end_date) == str:
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
        #print(url)
        fullLoad = pd.read_csv(url)
        #print('dataframe presnt',fullLoad.tail(1))
        #print(fullLoad.head(1))
        fullLoad['Date'] = pd.to_datetime(fullLoad['Date'])
        fullLoad = fullLoad.set_index('Date')
        '''
        # ------------ DISPLAYING RESULTS -------------
        headers = list(fullLoad.columns.values)
        print(tabulate(fullLoad.sort_index(ascending=False), headers, tablefmt="simple"))

        ticker = input('Ticker: ').upper()
        '''
        return fullLoad
    
        

def result_analysis(pattern_name,res_list):
    
    trend_st = None # for every other type
    trend_bl_br = None # ofr engulfing only 
    #if res_list:
    #if pattern_name == 'CDLENGULFING':............
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

    last = res_list.tail(1).values[0]
    if last != 0:
        trend_st = 'True'#candlestick_patterns[pattern_name]
        
    return trend_st#,trend_bl_br

def pattern_check(data,pattern_name):
    
    pattern_function = getattr(talib, pattern_name)
    res_list = None
    try:
        res_list = pattern_function(data['Open'],data['High'],data['Low'],data['Close'])
    except:
        print('failed ?!')
        raise ValueError('Loading data failed, problem with data or pattern name')
    last = res_list.tail(1).values[0]
    if pattern_name in ['CDLKICKINGBYLENGTH','CDLMARUBOZU','CDLENGULFING','CDLCLOSINGMARUBOZU']:
        #last = res_list.tail(1).values[0]
        if last > 0:
            return 'bullish'
            #trend_st = candlestick_patterns[pattern_name]
        elif last < 0:
            return 'bearish'
            #trend_st = candlestick_patterns[pattern_name]
        else:
            return False
    else:
        if last != 0:
            return True
        else:
            return False

'''
def trend_detector():


class patten_detected():

    def __init__(self):
        pass
'''     

def rsi_calc(data) :
    #df = yf.download("MERCURYLAB.BO", start=start_date, end=end_date)
    df=data
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
    
    return df['RSI']



def trend_detector(data):

    df1 = trendet.identify_df_trends(df=data,column='Close',window_size=4)
    
    lastU = df1['Up Trend'].tail(1).values[0]
    lastD = df1['Down Trend'].tail(1).values[0]
    if lastU != None:
        return 'UpTrend'
    elif lastD != None:
        return 'DownTrend'
    else:
        return 'SW'


class adv_patterns():
    def __init__(self,data_orig,n_days_data=5*30,sampling_ratio= 5):
        '''
        import numpy as np
        self.tkr = ticker_company
        try:
            data_orig = yf.download(self.tkr, start=today-timedelta(n_months_data*30), end=today)
        except:
            print('error loading data')
            raise ValueError('Loading data failed , check the stock name and date')
        '''
        data_o = data_orig[today - timedelta(days=n_days_data ):]
        Xt,Yt,data_ed = self.init_data(data=data_o.copy(),sampling=sampling_ratio)

        ptx_m,pty_m = self.local_min(x_data=Xt,y_data=Yt,data=data_ed['SMA'])
        print(pty_m)
        ptx_M,pty_M = self.local_max(x_data=Xt,y_data=Yt,data=data_ed['SMA'])

        self.Xt , self.Yt = self.filter_pt(ptx_min=ptx_m,pty_min=pty_m,ptx_max=ptx_M,pty_max=pty_M)



    @staticmethod
    def init_data(data,sampling=5):
        data['SMA'] = data['Close'].rolling(sampling).mean()
        
        y_sma = data['SMA'].values.tolist()
        xt = list(data.index)
        x_data = []
        y_data = []
        
        for i in range(len(y_sma)):
            if y_sma[i] != None:
                x_data.append(xt[i])
                y_data.append(y_sma[i])
        
        return x_data,y_data,data
    @staticmethod
    def local_min(x_data,y_data,data):
        #           ___ detection of local minimums and maximums ___
        l_min = (np.diff(np.sign(np.diff(y_data))) > 0).nonzero()[0] + 1      # local min
        
        y_min = []
        x_min_d =[]
        for v in l_min:
            y_min.append(y_data[v])
            x_min_d.append(x_data[v])

        #extend the suspected x range:
        delta = 10   # how many ticks to the left and to the right from local minimum on x axis

        dict_i = dict()
        dict_x = dict()

        df_len = len(data.index)                    # number of rows in dataset

        for element in l_min:                            # x coordinates of suspected minimums
            l_bound = element - delta                    # lower bound (left)
            u_bound = element + delta                    # upper bound (right)
            x_range = range(l_bound, u_bound + 1)        # range of x positions where we SUSPECT to find a low
            dict_x[element] = x_range                    # just helpful dictionary that holds suspected x ranges for further visualization strips
            
            #print('x_range: ', x_range)
            
            y_loc_list = list()
            for x_element in x_range:
                #print('-----------------')
                if x_element > 0 and x_element < df_len:                # need to stay within the dataframe
                    #y_loc_list.append(ticker_df.Low.iloc[x_element])   # list of suspected y values that can be a minimum
                    y_loc_list.append(data.iloc[x_element])
                    #print(y_loc_list)
                    #print('ticker_df.Low.iloc[x_element]', ticker_df.Low.iloc[x_element])
            dict_i[element] = y_loc_list                 # key in element is suspected x position of minimum
                                                        # to each suspected minimums we append the price values around that x position
                                                        # so 40: [53.70000076293945, 53.93000030517578, 52.84000015258789, 53.290000915527344]
                                                        # x position: [ 40$, 39$, 41$, 45$]
        #print('DICTIONARY for l_min: ', dict_i)
        y_delta = 0.12                               # percentage distance between average lows
        threshold = min(data) * 1.15      # setting threshold higher than the global low

        y_dict = dict()
        mini = list()
        suspected_bottoms = list()
                                                    #   BUG somewhere here
        for key in dict_i.keys():                     # for suspected minimum x position  
            mn = sum(dict_i[key])/len(dict_i[key])    # this is averaging out the price around that suspected minimum
                                                    # if the range of days is too high the average will not make much sense
                
            price_min = min(dict_i[key])    
            mini.append(price_min)                    # lowest value for price around suspected 
            
            l_y = mn * (1.0 - y_delta)                #these values are trying to get an U shape, but it is kinda useless 
            u_y = mn * (1.0 + y_delta)
            y_dict[key] = [l_y, u_y, mn, price_min]

        for key_i in y_dict.keys():    
            for key_j in y_dict.keys():    
                if (key_i != key_j) and (y_dict[key_i][3] < threshold):
                    suspected_bottoms.append(key_i)
        y_min = []
        x_min_d =[]
        for v in l_min:
            y_min.append(y_data[v])
            x_min_d.append(x_data[v])
        
        return x_min_d,y_min
    
    @staticmethod
    def local_max(x_data,y_data,data):
        #           ___ detection of local minimums and maximums ___
        l_max = (np.diff(np.sign(np.diff(y_data))) < 0).nonzero()[0] + 1      # local max
        
        y_max = []
        x_max_d =[]
        for v in l_max:
            y_max.append(y_data[v])
            x_max_d.append(x_data[v])

        #extend the suspected x range:
        delta = 10                                       # how many ticks to the left and to the right from local minimum on x axis

        dict_i = dict()
        dict_x = dict()

        df_len = len(data.index)                    # number of rows in dataset

        for element in l_max:                            # x coordinates of suspected minimums
            l_bound = element - delta                    # lower bound (left)
            u_bound = element + delta                    # upper bound (right)
            x_range = range(l_bound, u_bound + 1)        # range of x positions where we SUSPECT to find a low
            dict_x[element] = x_range                    # just helpful dictionary that holds suspected x ranges for further visualization strips
            
            #print('x_range: ', x_range)
            
            y_loc_list = list()
            for x_element in x_range:
                #print('-----------------')
                if x_element > 0 and x_element < df_len:                # need to stay within the dataframe
                    #y_loc_list.append(ticker_df.Low.iloc[x_element])   # list of suspected y values that can be a minimum
                    y_loc_list.append(data.iloc[x_element])
                    #print(y_loc_list)
                    #print('ticker_df.Low.iloc[x_element]', ticker_df.Low.iloc[x_element])
            dict_i[element] = y_loc_list                 # key in element is suspected x position of minimum
                                                        # to each suspected minimums we append the price values around that x position
                                                        # so 40: [53.70000076293945, 53.93000030517578, 52.84000015258789, 53.290000915527344]
                                                        # x position: [ 40$, 39$, 41$, 45$]
        #print('DICTIONARY for l_min: ', dict_i)
        y_delta = 0.12                               # percentage distance between average lows
        threshold = max(data) * 1.15      # setting threshold higher than the global low

        y_dict = dict()
        mini = list()
        suspected_bottoms = list()
                                                    #   BUG somewhere here
        for key in dict_i.keys():                     # for suspected minimum x position  
            mn = sum(dict_i[key])/len(dict_i[key])    # this is averaging out the price around that suspected minimum
                                                    # if the range of days is too high the average will not make much sense
                
            price_min = max(dict_i[key])    
            mini.append(price_min)                    # lowest value for price around suspected 
            
            l_y = mn * (1.0 - y_delta)                #these values are trying to get an U shape, but it is kinda useless 
            u_y = mn * (1.0 + y_delta)
            y_dict[key] = [l_y, u_y, mn, price_min]

        #print('SCREENING FOR DOUBLE BOTTOM:')    
            
        for key_i in y_dict.keys():    
            for key_j in y_dict.keys():    
                if (key_i != key_j) and (y_dict[key_i][3] < threshold):
                    suspected_bottoms.append(key_i)

        y_min = []
        x_min_d =[]
        for v in l_max:
            y_min.append(y_data[v])
            x_min_d.append(x_data[v])
        #print('min dates  ',x_min_d)
        return x_min_d,y_min

    @staticmethod
    def filter_pt (ptx_min,pty_min,ptx_max,pty_max):
        ptx = ptx_min+ptx_max
        pty = pty_min+pty_max
        #print('len ptx --------------------- ',len(pty))
        #sorting
        #print('date ',ptx)
        PTs = []
        for i in range(len(ptx)):
            PTs.append((ptx[i],pty[i]))
        ptx = sorted(ptx) #ptx.sort()
        #print('rest pts ++++++++++++++++++', pty)
        PTsx = [tuple for x in ptx for tuple in PTs if tuple[0] == x]
        #print('rest pts_X ++++++++++++++++++', PTsx)
        pty = []
        for y in PTsx:
            pty.append(y[1])
        #filter
        ptX_s = []
        ptY_s = []
        #print('len ptx --------------------- ',len(pty))
        for i in range(len(ptx)-1):
            if abs( pty[i]-pty[i+1] ) > 0.5:
                ptX_s.append(ptx[i])
                ptY_s.append(pty[i])

        return ptX_s,ptY_s

    def find_patterns(self,pat_name):
        from collections import defaultdict  
        max_min = self.Yt
        patterns = defaultdict(list)
        date_patterns = {}
        
        
        # Window range is 5 units
        res_i = 0
        for i in range(5, len(max_min)):  
            window = max_min[i-5:i]
            
            # Pattern must play out in less than n units
            if window[-1] - window[0] > 100:  
                #print('pass *')    
                continue   
                
            a, b, c, d, e = window[0:5]
            mini_pat_dic = {
                #'Head and Shoulders' : (a>b and c>a and c>e and c>d and e>d and abs(b-d)<=np.mean([b,d])*0.1),
                #'Inv Head and Shoulders': (a<b and c<a and c<e and c<d and e<d and abs(b-d)<=np.mean([b,d])*0.1),
                'Double Bottom' : (c<a and b<c and d<c and c<e and abs(b-d)<=np.mean([b,d])*0.1),
                'Double Top' : (c>a and b>c and d>c and c>e and abs(b-d)<=np.mean([b,d])*0.1),
                'Bullish penant' :(a<b and c<a and c<b and c<d and d<b and e<d and e>c and (b-d)>=np.mean([b,d])*0.1 and (e-c)>=np.mean([c,e])*0.1 and (abs(b-d)in [abs(e-c)*0.8,abs(e-c)*1.2])  ), # Bu - pen
                'Bearish pennant' :(a>b and c>a and c>b and c>d and d>b and e>d and e<c and (d-b)>=np.mean([b,d])*0.1 and (c-e)>=np.mean([c,e])*0.1 and (abs(b-d)in [abs(e-c)*0.8,abs(e-c)*1.2]) ), # Be - pen
                'falling wedge' :(a>c and c>e and c>b and e>b and b>d and c>b and (b-d)>=np.mean([b,d])*0.1 and (c-e)>=np.mean([c,e])*0.1 and (abs(b-d)in [abs(e-c)*0.8,abs(e-c)*1.2]) ), # falling wedge
                'Rising wedge' :(a<c and c<e and e<b and b<d and b<d and (d-b)>=np.mean([b,d])*0.1 and (e-c)>=np.mean([c,e])*0.1 and abs(b-d)<abs(e-c) ), #rising wedge
                'bullish flag' :(a>c and c>b and b>d and c<e and abs(b-d)in[abs(a-c)*0.8,abs(a-c)*1.2]), #bu flag
                'Bearish flag' : (a<c and c<b and b<d and c>e  and abs(b-d)in[abs(a-c)*0.8,abs(a-c)*1.2] )
            }

            if mini_pat_dic[pat_name]:
                patterns['IHS'].append((window[0], window[-1]))
                date_patterns[pat_name]=(self.Xt[i-5],self.Xt[i])
            
        if patterns != {}:
            return date_patterns

        return False#patterns

    
    def find_patterns_HS(self,pat_name):
        from collections import defaultdict  
        max_min = self.Yt
        patterns = defaultdict(list)
        date_patterns = {}
        
        
        # Window range is 5 units
        for i in range(7, len(max_min)):  
            window = max_min[i-7:i]
            
            # Pattern must play out in less than n units
            if window[-1] - window[0] > 100:  
                #print('pass *')    
                continue   
                
            a, b, c, d, e ,f ,g = window[0:7]
            mini_pat_dic = {
                'Head and Shoulders' : (a<c and c<b and b<d and d>f and f>e and g<e and abs(e-c)<=np.mean([e,c])*0.1),
                'Inv Head and Shoulders': (a>c and c>b and b>d and e>b and f<e and f>d and g>e #and h<g and h > f and j>g
                and abs(e-c)<=np.mean([c,e])*0.1  ) #and h in [e*0.85,e*1.15]
                }

            if mini_pat_dic[pat_name]:
                #patterns['IHS'].append((window[0], window[-1]))
                date_patterns=(self.Xt[i-5],self.Xt[i])
            
        if date_patterns != {}:
            return date_patterns

        return False#patterns

    def find_patterns_flag(self,pat_name):
        from collections import defaultdict  
        max_min = self.Yt
        patterns = defaultdict(list)
        date_patterns = {}
        
        
        # Window range is 5 units
        for i in range(6, len(max_min)):  
            window = max_min[i-6:i]
            
            # Pattern must play out in less than n units
            if window[-1] - window[0] > 100:  
                #print('pass *')    
                continue   
                
            a, b, c, d, e ,f = window[0:6]
            mini_pat_dic = {
                'Bullish penant' : (a<c and c<e and e<d and d<b and b<f and abs(b-d)in [abs(c-e)*0.9,abs(c-e)*1.1]),
                'Bearish penant': (a>c and c>e and e>d and d>b and b>f and abs(b-d)in [abs(c-e)*0.9,abs(c-e)*1.1]),

                'Rising wedge' : (a<c and c<e and e<b and b<d and d<f and abs(b-d)in [abs(d-f)*0.9,abs(d-f)*1.1]),
                'Falling wedge': (a>c and c>e and e>b and b>d and d>f and abs(b-d)in [abs(d-f)*0.9,abs(d-f)*1.1]),

                'Bullish flag': (a<e and e<c and c<d and d<b and b<f and abs(b-d)in [abs(c-e)*0.9,abs(c-e)*1.1]),
                'Bearish flag': (a>e and e>c and e>d and d>b and b>f and abs(b-d)in [abs(c-e)*0.9,abs(c-e)*1.1])
                }

            if mini_pat_dic[pat_name]:
                #patterns['IHS'].append((window[0], window[-1]))
                date_patterns=(self.Xt[i-6],self.Xt[i])
            
        if date_patterns != {}:
            return date_patterns

        return False#patterns

    def find_patterns_flag_wedge(self,pat_name):
        from collections import defaultdict  
        max_min = self.Yt
        patterns = defaultdict(list)
        date_patterns = {}
        
        
        # Window range is 5 units
        for i in range(7, len(max_min)):  
            window = max_min[i-7:i]
            
            # Pattern must play out in less than n units
            if window[-1] - window[0] > 100:  
                #print('pass *')    
                continue   
                
            a, b, c, d, e ,f,g = window[0:7]
            mini_pat_dic = {
                'Rising wedge' : (a<c and c<e and e<b and b<d and d<f and abs(b-d)in [abs(d-f)*0.9,abs(d-f)*1.1]),
                'Falling wedge': (a>c and c>e and e>b and b>d and d>f and abs(b-d)in [abs(d-f)*0.9,abs(d-f)*1.1])
                }

            if mini_pat_dic[pat_name]:
                #patterns['IHS'].append((window[0], window[-1]))
                date_patterns=(self.Xt[i-6],self.Xt[i])
            
        if date_patterns != {}:
            return date_patterns

        return False#patterns

    def find_patterns_D(self,pat_name):
        from collections import defaultdict  
        max_min = self.Yt
        date_patterns = {}
        
        
        # Window range is 5 units
        for i in range(5, len(max_min)):  
            window = max_min[i-5:i]
            
            # Pattern must play out in less than n units
            if window[-1] - window[0] > 100:  
                #print('pass *')    
                continue   
                
            a, b, c, d, e = window[0:5]
            mini_pat_dic = {
                'Double Bottom' : (c<a and b<c and d<c and c<e and abs(b-d)<=np.mean([b,d])*0.1),
                'Double Top' : (c>a and b>c and d>c and c>e and abs(b-d)<=np.mean([b,d])*0.1)
                }

            if mini_pat_dic[pat_name]:
                date_patterns=(self.Xt[i-5],self.Xt[i])
            
        if date_patterns != {}:
            return date_patterns

        return False


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
    #data = load_data_df(ticker_st="MERCURYLAB.BO")
    
    t2 = datetime.date(datetime.now()) + timedelta(days=2)
    t1 = datetime.date(datetime.now()) - timedelta(days=30 )
    #sata = data[t1:t2]
    ssata = data_loader_df(ticker_st="IWEL.NS",n_days=30,end_date='2021-05-30')
    ssata01=ssata.data_portion(n_days=5)

    print('test portion data : ',ssata01)
    
    #tr = trend_detector(data=data)
    
    #print(tr)
    '''
    rsi = rsi_calc(data=data)
    print('test RSI',type(rsi))
    print(rsi[-20:])
    print(len(rsi))
    df_date = pd.to_datetime(rsi[-20:].index)
    print(len(df_date))
    print('official resulrs : ',rsi.tail(1).values[0])
    '''
    '''
    #res = pattern_check(data=data,pattern_name='CDLMARUBOZU')
    #print(res)
    data_l = adv_patterns(data_orig=data)
    new_ib = {}
    new_ib['Head and Shoulders']=data_l.find_patterns_HS('Head and Shoulders')
    
    new_ib['Inv Head and Shoulders']=data_l.find_patterns_HS('Inv Head and Shoulders')
    new_ib['Double Bottom']=data_l.find_patterns_D('Double Bottom')
    new_ib['Double Top']=data_l.find_patterns_D('Double Top')
    print(new_ib)
    new_ib['Bullish penant']=data_l.find_patterns_flag('Bullish penant')
    new_ib['Bearish penant']=data_l.find_patterns_flag('Bearish penant')
    new_ib['Falling wedge']=data_l.find_patterns_flag('Falling wedge')
    new_ib['Rising wedge']=data_l.find_patterns_flag('Rising wedge')
    new_ib['Bullish flag']=data_l.find_patterns_flag('Bullish flag')
    new_ib['Bearish flag']=data_l.find_patterns_flag('Bearish flag')
    '''