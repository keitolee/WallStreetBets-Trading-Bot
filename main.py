from getTicker import redditTicker
from records import check_records
import accounts
import records

# Get top 5 tickers from WSB using Reddit API
obj = redditTicker(accounts.reddituser, accounts.redditpass)
buyStocks = obj.getWSBTicker()

# Check current_holdings to eliminate currently held stocks 
buy_stocks = check_records(buyStocks)

# Buy stocks in buy_stocks list using Interactive Brokers API


# Update buy_transactions and current_holdings sheet


# Check current_holdings sheet for potential sells and sell if meets target


# Update sell_transactions sheet



