from ib_insync import *
from numpy import fill_diagonal, floor
import yfinance as yf
import csv
import pandas as pd
import math
import json

def market_order(tickers):
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    acc_vals = [v.value for v in ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD']
    curr_balance = float(acc_vals[0])

    purchased_tickers = []

    for ticker in tickers:
        
        stock = Stock(ticker, 'SMART', 'USD')

        # check price of stock
        ib.qualifyContracts(stock)
        data = ib.reqMktData(stock)
        ib.sleep(5)
        curr_price = data.last

        # if enough balance in account buy stock with max $200, buy stock
        if curr_balance >= curr_price and curr_price <= 200:
            buy_amount = floor(200/curr_price)

            order = MarketOrder('BUY', buy_amount)
            trade = ib.placeOrder(stock, order)
            purchased_tickers.append(ticker)
            print(order)

            ticker_info = {"priceBought": curr_price,"quantityBought": buy_amount}

            # add purchased ticekrs into current holdings
            with open('current_holdings.json','r+') as json_file:
                file_data = json.load(json_file)
                file_data[ticker] = ticker_info
                json_file.seek(0)
                json.dump(file_data, json_file, indent = 4)
    
    return purchased_tickers



# # Check for enough balance to pay for stock
# stock = yf.Ticker("GME")
# current_price = stock.history(period="1m", interval='1m')['Close'].mean()

# with open('current_balance.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             line_count += 1
#         else:
#             balance = float(f'{row[0]}')
#             line_count += 1

# if(balance >= current_price):
    
#     contract = Stock('GME', 'SMART', 'USD')


# stock = Stock('AMC', 'SMART', 'USD')

# bars = ib.reqHistoricalData(
#     stock, endDateTime='', durationStr='30 D',
#     barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True
# )


# def orderFilled(order, fill):
#     print('order has been filled')
#     print(order)
#     print(fill)

# trade.fillEvent += orderFilled

# ib.run()

# bars = ib.reqHistoricalData(
#         stock, endDateTime='', durationStr='30 D',
#     barSizeSetting='1 hour', whatToShow='MIDPOINT', useRTH=True)

# df = util.df(bars)
# print(df)
