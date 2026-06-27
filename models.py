from dataclasses import dataclass, asdict
from datetime import datetime



@dataclass
class Share:
    ticker: str 
    name: str
    price: float

    def to_dict(self):
        return asdict(self)




class Transaction:
    def __init__(self, id :str, time :datetime, value :float, ticker :str, quantity :int, type :str):
        self.id = id
        self.time = time
        self.value = value
        self.ticker = ticker
        self.quantity = quantity
        self.type = type


    def __repr__(self):
        return f"Transakcja {self.type} (id='{self.id}', time='{self.time}',  papier={self.share.name}, w liczbie={self.quantity} szt. wartosć={self.value} PLN)"

    def to_dict(self):
        return asdict(self)

class InsuffincientSharesError(Exception):
    """Wyjątek rzucany, gdy uzytkownik chce sprzedac wiecej akcji niz posiada"""
    pass


@dataclass
class Wallet:
    cash: float
    market: dict
    shares_value: float
    transaction_history: dict 
    portfolio: dict 

    def to_dict(self):
        return asdict(self)
    
    def buy(self, transaction_id :str, share :Share, quantity_to_buy :int):
            transaction = Transaction(transaction_id, datetime.timestamp, share.price *quantity_to_buy, share.ticker, quantity_to_buy, "buy")
            if quantity_to_buy < 1:
                raise ValueError("Liczba akcji musi być większa od 0.")
            if share.price <= 0:
                raise ValueError("Nie mozna kupic akcji o cenie zerowej.")
            
            if transaction.value > self.cash:
                raise ValueError("Nie masz wystarczającej ilości gotówki.")
    
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
            transaction = Transaction(transaction_id, share.price * quantity_to_sell, share.ticker, quantity_to_sell, "sell")

            self.cash += transaction.value
            self.transaction_history[transaction_id] = transaction.__dict__

            # odejmnowanie akcji w portfolio
            self.portfolio[share.ticker]["quantity"] -= quantity_to_sell

            # jezeli sprzedano wyszystkie akacji spółki usuwa ją z portfolio
            if self.portfolio[share.ticker]["quantity"] == 0:
                del self.portfolio[share.ticker]

            return f"Sprzedano {quantity_to_sell} akcji {share.name} za {transaction.value} PLN"
        else:
            return f"Nie masz tylu akcji w portfelu (posiadasz: {self.portfolio[share.ticker]['quantity']} szt.)"

        
    def get_shares_value(self, stock_market :dict):
        total_value = 0.0

        for ticker, data in self.portfolio.items():
            if ticker in stock_market:
                current_price = stock_market[ticker].price
                quantity = data['quantity']

                total_value += current_price * quantity

        return round(total_value, 2)
    
    def get_total_profit(self, stock_market :dict):
        total_profit = 0.0

        for ticker, data in self.portfolio.items():
            if ticker in stock_market:
                current_value = stock_market[ticker].price * data['quantity']
                purchase_value = data['price'] * data['quantity']
                total_profit += (current_value - purchase_value)

        return round(total_profit, 2)
        







