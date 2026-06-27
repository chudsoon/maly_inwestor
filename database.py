import os
import json

from models import Wallet, Share, Transaction

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
TRANSACTION_HISTORY_PATH = os.path.join(BASE_DIR, "transaction_history.json")
STOCK_MARKET_PATH = os.path.join(BASE_DIR, "stock_market.json")



    
def load_stock_maket():
    if os.path.join(STOCK_MARKET_PATH):
        with open(STOCK_MARKET_PATH, 'r') as file: 
            json_dict = json.load(file)
            stock_market = {}
            for key, v in json_dict.items():
                stock_market[key] = Share(key, v['name'], v['price'])
            return stock_market
    else:
        return {}
    
def load_wallet(stock_market :dict):
    if os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as file:
            json_dict = json.load(file)
            wallet = {}
            for key, v in json_dict.items():
                wallet[key] = Wallet(v['cash'], stock_market, v['shares_value'], v['transaction_history'], v['portfolio'])
            return wallet
    else:
        return {}

def save_wallet(wallet :Wallet):
    if os.path.join(CONFIG_PATH):
        with open(CONFIG_PATH, 'w', encoding='utf-8') as file:
            json.dump({"primary": wallet.to_dict()}, file, ensure_ascii=False, indent=4)
            
    else:
        return "Plik config nie istnieje"
    

def load_transaction_history():
    if os.path.isfile(TRANSACTION_HISTORY_PATH):
        with open(TRANSACTION_HISTORY_PATH, 'r') as file:
            json_dict = json.load(file)
            transaction_history = {}
            for key, v in json_dict.items():
                 transaction_history[key] = Transaction(v['id'], v['time'], v['value'], v['ticker'], v['quantity'], v['type'])
    else:
        return {}

def save_trasaction_history(transaction: Transaction):
    if os.path.join(TRANSACTION_HISTORY_PATH):
        transaction_dict = {}
        transaction_dict[transaction.id] = transaction.to_dict()
        with open(TRANSACTION_HISTORY_PATH, 'w', encoding='utf-8') as file:
            json.dump(transaction_dict, file, ensure_ascii=False, indent=4)
    else:
        return "Plik Transaction_History nie istnieje"




