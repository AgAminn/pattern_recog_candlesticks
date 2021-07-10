from company_symbol_dic import company_stock_symbol
import requests
import pytest
import yfinance as yf
list_stocks = list(company_stock_symbol.keys())

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

'''
res,readable_stks = check_app_02()#check_app_load()

print('finsih testing')
#res = check_app_load()
print('N tests           ',len(list_stocks))
print('N successful test ',res)

with open('your_file.txt', 'w') as f:
    for item in readable_stks:
        f.write("%s\n" % item)
'''
file1 = open('your_file.txt', 'r')
Lines = file1.readlines()
linesx = [l.strip() for l in Lines]
print('res :',len(linesx))
#print(linesx)
res_list = list(set(list_stocks)-set(linesx) )
print('result disjoint list ',len(res_list))

with open('working_stocks.txt', 'w') as f:
    for item in res_list:
        f.write("%s\n" % item)