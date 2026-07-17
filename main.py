import math

from gui import draw_main_screen
from datetime import datetime
from database import load_wallet, load_stock_market, load_transaction_history
from models import Wallet, Share, Transaction
from menu_manager import MenuManager
from api_provider import fetch_gpw_data_list



def stock_market_update_list(stock_market :dict):
    today = datetime.today().strftime("%Y-%m-%d")
    tickers = list(stock_market.keys())
    quotes = fetch_gpw_data_list(tickers)
  
    for key in stock_market.keys():
        try:
            val = quotes['Close'][key].iloc[-1]
            if math.isnan(val):
                stock_market[key].price = 0.0
            else:
                stock_market[key].price = round(val, 2)
        except KeyError:
            stock_market[key].price = 0.0
    return stock_market
    


if __name__ == "__main__":
    messages = []
    stock_market = stock_market_update_list(load_stock_market())
    wallet = load_wallet(stock_market).get('primary')
    transaction_history = load_transaction_history()
    tickers = []
    for key in stock_market.keys():
        tickers.append(key)


    stock_market_update_list(stock_market)

    
    menu = MenuManager(wallet, stock_market, transaction_history)

    while True:
        transaction_history = load_transaction_history()
        draw_main_screen(wallet, transaction_history, stock_market, messages, menu)

        result = menu.process_input()

        if result:
            messages.append(result)


