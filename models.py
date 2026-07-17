from dataclasses import dataclass, asdict
import time
from datetime import datetime


from exeptions import InsuffincientSharesError, InsufficientCashError

@dataclass
class Share:
    ticker: str 
    name: str
    price: float


    def to_dict(self):
        return asdict(self)



@dataclass
class Transaction:
    id :str
    time :str
    value :float
    ticker :str
    quantity :int
    type :str


    def to_dict(self):
        return asdict(self)



@dataclass
class Wallet:
    cash: float
    market: dict
    shares_value: float
    portfolio: dict 

    def to_dict(self):
        return asdict(self)
    
    def buy(self, transaction_id :str, share :Share, quantity_to_buy :int):
            ts = time.time()
            timestamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            transaction = Transaction(transaction_id, timestamp, share.price *quantity_to_buy, share.ticker, quantity_to_buy, "buy")
            if quantity_to_buy < 1:
                raise ValueError("Liczba akcji musi być większa od 0.")
            if share.price <= 0:
                raise ValueError("Nie mozna kupic akcji o cenie zerowej.")
            
            if transaction.value > self.cash:
                raise InsufficientCashError(
                    f"Nie masz wystarczającej ilości gotówki."
                    f"\nTwoje saldo to: {round(self.cash, 2)} PLN"
                    f"\nWartość transkcji to: {round(transaction.value, 2)} PLN"
                    f"\nBrakuje: [bold red]{round((self.cash - transaction.value)*(-1), 2)} PLN[/bold red]")
    
            self.cash -= transaction.value

            # Jako klucza uzywam unikalnego skrótu share.ticker zamiast nazwy
            if share.ticker in self.portfolio:
                self.portfolio[share.ticker]["quantity"] += quantity_to_buy
      
            else:
                self.portfolio[share.ticker] = {
                    "ticker": share.ticker,
                    "name": share.name,
                    "quantity": quantity_to_buy,
                    "price": share.price
                }
            message =  f"Zakupiono {quantity_to_buy} szt. akcji spółki {share.name} o wartości {transaction.value} PLN"
            return message, transaction
              
        
    def sell(self, transaction_id :str, share :Share, quantity_to_sell :int):
        if share.ticker not in self.portfolio:
            raise ValueError("Nie posiadasz takiego papieru w portfolio")
        
        if quantity_to_sell > self.portfolio[share.ticker]["quantity"]:
            raise InsuffincientSharesError(
                f"Błąd sprzedazy: Posiadasz {self.portfolio[share.ticker]['quantity']} szt., "
                f"a chcesz sprzedać {quantity_to_sell}."
            )
        if self.portfolio[share.ticker]["quantity"] >= quantity_to_sell:
            ts = time.time()
            timestamp = str(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
            transaction = Transaction(transaction_id, timestamp, share.price * quantity_to_sell, share.ticker, quantity_to_sell, "sell")

            self.cash += transaction.value

            # odejmnowanie akcji w portfolio
            self.portfolio[share.ticker]["quantity"] -= quantity_to_sell

            # jezeli sprzedano wyszystkie akacji spółki usuwa ją z portfolio
            if self.portfolio[share.ticker]["quantity"] == 0:
                del self.portfolio[share.ticker]

            message = f"Sprzedano {quantity_to_sell} akcji {share.name} za {transaction.value} PLN"
    
            return message, transaction
        else:
            return f"Nie masz tylu akcji w portfelu (posiadasz: {self.portfolio[share.ticker]['quantity']} szt.)"

        
    def get_shares_value(self, transaction_history :dict, stock_market :dict):
        total_value = 0.0
        self.refresh_satate(transaction_history)

        for ticker, data in self.portfolio.items():
            if ticker in stock_market:
                current_price = stock_market[ticker].price
                quantity = data['quantity']

                total_value += current_price * quantity

        return round(total_value, 2)
    
    def get_total_profit(self, stock_market :dict, transaction_history :dict):
        portfolio, cash, assets_buy_value = self.calculate_portfolio_state(transaction_history)
        current_assets_value = self.get_shares_value(transaction_history, stock_market)

        profit = current_assets_value - assets_buy_value

        profit_in_percent = (profit * 100) / assets_buy_value

        return profit, profit_in_percent
    

    def calculate_portfolio_state(self, transaction_history: dict):
        sorted_transactions = sorted(transaction_history.values(), key=lambda x: x["time"])
        assets_portfolio = {}
        assets_value = 0
        cash = 1000
        tickers_to_remove = []


        for t in sorted_transactions:
            ticker = t["ticker"]

            if ticker not in assets_portfolio:
                assets_portfolio[ticker] = {"quantity": 0, "value": 0}


            if t["type"] == "buy":
                cash -= t["value"]
                assets_portfolio[ticker]["quantity"] += t["quantity"]
                assets_portfolio[ticker]["value"] += t["value"]
                assets_portfolio[ticker]["avg_price"] = assets_portfolio[ticker]["value"] / assets_portfolio[ticker]["quantity"]
            elif t["type"] == "sell":
                cash += t["value"]
                assets_portfolio[ticker]["quantity"] -= t["quantity"]
                assets_portfolio[ticker]["value"] -= (assets_portfolio[ticker]["avg_price"] * t["quantity"])
                
                if assets_portfolio[ticker]["quantity"] > 0:
                    assets_portfolio[ticker]["avg_price"] = assets_portfolio[ticker]["value"] / assets_portfolio[ticker]["quantity"]
                else:
                    # usuń ticker ze słownika jeeli go nie posiadasz
                    if ticker in self.portfolio:
                        tickers_to_remove.append(ticker)
                    
        for ticker in tickers_to_remove:
            del self.portfolio[ticker]
            del assets_portfolio[ticker]
                    
            
        total_assets_value = sum(item["value"] for item in assets_portfolio.values())
        
        return  assets_portfolio, round(cash,2 ), round(total_assets_value, 2)
    
    def refresh_satate(self, transaction_history :dict):
        portfolio, cash, total_assets_value = self.calculate_portfolio_state(transaction_history)
        self.cash = cash
        self.portfolio = portfolio
        self.shares_value = total_assets_value


 
               
               

    





