from models import Wallet
from api_provider import fetch_gpw_data_list
from datetime import datetime

from database import load_stock_maket, load_wallet

def stock_market_update_list(stock_market :dict):
    today = datetime.today().strftime("%Y-%m-%d")
    tickers = list(stock_market.keys())
    quotes = fetch_gpw_data_list(tickers)
    for key in stock_market.keys():
        stock_market[key].price = round(quotes.loc[today, ('Close', key)], 2)


wallet = load_wallet().get('primary')
stock_market = load_stock_maket()
stock_market_update_list(stock_market)





def get_shares_value(wallet :Wallet, stock_market :dict):
    total_value = 0.0

    for ticker, data in wallet.portfolio.items():
        if ticker in stock_market:
            current_price = stock_market[ticker].price
            quantity = data['quantity']

            total_value += current_price * quantity

    return total_value

def get_total_profit(wallet, stock_market :dict):
    total_profit = 0.0

    for ticker, data in wallet.portfolio.items():
        if ticker in stock_market:
            current_value = stock_market[ticker].price * data['quantity']
            purchase_value = data['price'] * data['quantity']
            total_profit += (current_value - purchase_value)

    return round(total_profit, 2)
        



print(get_total_profit(wallet, stock_market))