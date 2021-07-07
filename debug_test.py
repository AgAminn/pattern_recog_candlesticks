from company_symbol_dic import company_stock_symbol
import requests
import pytest
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

res = check_app_load()

print('finsih testing')
#res = check_app_load()
print('N tests           ',len(list_stocks))
print('N successful test ',res)