from ib_insync import *
from numpy import fill_diagonal, floor
import yfinance as yf
import csv
import pandas as pd
import math
import json
import datetime

class IBKRorders:

    def __init__(self) -> None:
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)


    def market_order(self, tickers):

        acc_vals = [v.value for v in self.ib.accountValues() if v.tag == 'CashBalance' and v.currency == 'USD']
        curr_balance = float(acc_vals[0])

        purchased_tickers = []

        for ticker in tickers:
            
            stock = Stock(ticker, 'SMART', 'USD')

            # check price of stock
            self.ib.qualifyContracts(stock)
            data = self.ib.reqMktData(stock)
            self.ib.sleep(5)
            curr_price = data.last

            # if enough balance in account buy stock with max $200, buy stock
            if curr_balance >= curr_price and curr_price <= 200:
                buy_amount = floor(200/curr_price)

                order = MarketOrder('BUY', buy_amount)
                trade = self.ib.placeOrder(stock, order)
                purchased_tickers.append(ticker)
                print(order)

                ticker_info = {"priceBought": curr_price,"quantityBought": buy_amount}

                # add purchased ticekrs into current holdings
                with open('current_holdings.json','r+') as json_file:
                    file_data = json.load(json_file)
                    file_data[ticker] = ticker_info
                    json_file.seek(0)
                    json.dump(file_data, json_file, indent = 4)
                
                # update transactions.csv
                self.update_transactions("BUY", ticker, curr_price, buy_amount)

            else: 
                print(ticker + " higher than $200 or not enough balance")

        return purchased_tickers


    def market_sell(self):

        sell_list = []

        with open('current_holdings.json','r+') as json_file:
            file_data = json.load(json_file)

            # check every stock currently held
            for ticker in list(file_data):
                purchase_price = file_data[ticker]["priceBought"]

                stock = Stock(ticker, 'SMART', 'USD')

                # get current price of stock
                self.ib.qualifyContracts(stock)
                data = self.ib.reqMktData(stock)
                self.ib.sleep(5)
                curr_price = data.last

                # sell all holding amounts if price has gone up by at least 10%
                if (curr_price - purchase_price) / purchase_price > 0.10:
                    sell_amount = file_data[ticker]["quantityBought"]
                    order = MarketOrder('SELL', sell_amount)
                    trade = self.ib.placeOrder(stock, order)
                    print(order)

                    # remove stock from current_holdings 
                    del file_data[ticker]

                    # add stock to return list
                    sell_list.append(ticker)

                    # update transactions.csv
                    self.update_transactions("SELL", ticker, curr_price, sell_amount)
        
        # write updated list to json file
        with open('current_holdings.json', 'w') as data_file:
            data = json.dump(file_data, data_file)

        return sell_list

    
    def update_transactions(self, action, ticker, price, amount):
        
        row = [str(datetime.datetime.now()), action, ticker, price, amount]

        with open('transactions.csv', mode='a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(row)



# if __name__ == "__main__":
#     buys = ["GME", "AMD"]
#     obj = IBKRorders()

#     obj.update_transactions("BUY", "GRE", "100", "40")

    # market_sell()

    # with open('current_holdings.json','r+') as json_file:
    #     file_data = json.load(json_file)
    #     json_file.seek(0)

    # # for ticker in list(file_data):
    # #     del file_data[ticker]

    # del file_data['AMD']
    
    # with open('current_holdings.json', 'w') as data_file:
    #     data = json.dump(file_data, data_file)

