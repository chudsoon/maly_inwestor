import math

from gui import draw_main_screen
from datetime import datetime
from database import load_wallet, load_stock_maket
from models import Wallet, Share, Transaction
from menu_mananger import MenuManager
from api_provider import fetch_gpw_data_list



def stock_market_update_list(stock_market :dict):
    today = datetime.today().strftime("%Y-%m-%d")
    tickers = list(stock_market.keys())
    quotes = fetch_gpw_data_list(tickers)
    for key in stock_market.keys():
        try:
            val = quotes.loc[today, ('Close', key)]
            if math.isnan(val):
                stock_market[key].price = 0.0
            else:
                stock_market[key].price = round(val, 2)
        except KeyError:
            stock_market[key].price = 0.0
    return stock_market
    


if __name__ == "__main__":
    messages = []
    stock_market = stock_market_update_list(load_stock_maket())
    wallet = load_wallet(stock_market).get('primary')
    tickers = []
    for key in stock_market.keys():
        tickers.append(key)


    stock_market_update_list(stock_market)

    
    menu = MenuManager(wallet, stock_market)

    while True:
        draw_main_screen(wallet, stock_market, messages, menu)
        result = menu.process_input()

        if result:
            messages.append(result)


