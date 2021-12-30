from getTicker import redditTicker
from records import *
from IBapi import market_order, market_sell
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
purchased_stocks = market_order(buy_stocks)
print("Purchased stocks: ")
print(purchased_stocks)

# # Update current_holdings sheet with stocks bought
# update_current_holdings(purchased_stocks)

# update_buys(stocks that were actually bought)

# Check current_holdings for potential sells and sell if meets target
market_sell()

# Update sell_transactions sheet



