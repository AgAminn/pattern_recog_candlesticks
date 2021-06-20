import csv, os
import pandas

company_symbol = {}
with open(r'tr/Equity_BSE.csv', 'r') as file:
    reader = csv.reader(file)
    
    for row in reader:
        print(row)
        # BSE row 2 and 3
        # NSE row 0 and 1
        company_symbol[row[2]+'.BO']=row[3]   #yfinance website only acctept symbol with suffix .SE for NSE and BO for BSE

with open(r'tr/myfileBSE_ed2.txt', 'w') as f:
    print(company_symbol, file=f)
'''
print(reader[1])

print(type(reader))
'''
