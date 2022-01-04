from getTicker import redditTicker
from records import *
from IBapi import IBKRorders
import accounts
import records

# Get top 5 tickers from WSB using Reddit API (buyStocks -> list of tickers)
obj = redditTicker(accounts.reddituser, accounts.redditpass)
reddStocks = obj.getWSBTicker()
print("Most mentioned stocks: ")
print(reddStocks)

# Check current_holdings to eliminate currently held stocks (buy_stocks -> list of tickers)
buy_stocks = check_records(reddStocks)
print("Stocks to buy: ")
print(buy_stocks)

# Buy stocks in buy_stocks list using Interactive Brokers API ( -> list of tickers actually bought)
IBKRobj = IBKRorders()
purchased_stocks = IBKRobj.market_order(buy_stocks)
print("Purchased stocks: ")
print(purchased_stocks)

# Check current_holdings for potential sells and sell if meets target
sold_stocks = IBKRobj.market_sell()
print("Sold stocks: ")
print(sold_stocks)

# Update sell_transactions sheet



