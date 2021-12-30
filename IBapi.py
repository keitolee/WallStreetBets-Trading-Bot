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
        else: 
            print(ticker + " higher than $200 or not enough balance")

    return purchased_tickers


def market_sell():
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    with open('current_holdings.json','r+') as json_file:
        file_data = json.load(json_file)

        # check every stock currently held
        for ticker in list(file_data):
            purchase_price = file_data[ticker]["priceBought"]

            stock = Stock(ticker, 'SMART', 'USD')

            # get current price of stock
            ib.qualifyContracts(stock)
            data = ib.reqMktData(stock)
            ib.sleep(5)
            curr_price = data.last

            # sell all holding amounts if price has gone up by at least 10%
            if (curr_price - purchase_price) / purchase_price > 0.10:
                sell_amount = file_data[ticker]["quantityBought"]
                order = MarketOrder('SELL', sell_amount)
                trade = ib.placeOrder(stock, order)
                print(order)

                # remove stock from current_holdings 
                del file_data[ticker]
    
    # write updated list to json file
    with open('current_holdings.json', 'w') as data_file:
        data = json.dump(file_data, data_file)



# if __name__ == "__main__":
#     buys = ["GME", "AMD"]
#     # market_sell()

#     with open('current_holdings.json','r+') as json_file:
#         file_data = json.load(json_file)
#         json_file.seek(0)

#     # for ticker in list(file_data):
#     #     del file_data[ticker]

#     del file_data['AMD']
    
#     with open('current_holdings.json', 'w') as data_file:
#         data = json.dump(file_data, data_file)

