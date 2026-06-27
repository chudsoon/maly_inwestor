
import os

from rich.prompt import Prompt
from rich.panel import Panel

from models import Wallet, Share, Transaction, InsuffincientSharesError
from database import save_wallet, save_trasaction_history

from utils import generate_transaction_id

class MenuManager:
    def __init__(self, wallet :Wallet, stock_market :dict):
        self.wallet = wallet
        self.stock_makret = stock_market
        self.current_state = "main"

    def get_main_menu(self):
        return {
            "1": {"label": "Kup", "func": self.handle_buy},
            "2": {"label": "Sprzedaj", "func": self.handle_sell},
            "3": {"label": "Historia transakcji", "func": self.handle_transaction_history},
            "4": {"label": "Koniec", "func": self.handle_exit}
        }
    
    def get_transaction_history_menu(self):
        return {
            "b": {"label": "Wróc", "func": self.handle_back_to_main_menu}
        }
    def handle_transaction_history(self):
        self.current_state = "transaction_history"

    def handle_buy(self):
        try:
            share_ticker  = Prompt.ask("Podaj skrót spółki, którą chcesz kupić", choices=self.stock_makret.keys())
            quantity = Prompt.ask("Ile akcji chesz kupić?")

            message, transaction = self.wallet.buy(generate_transaction_id(), self.stock_makret[share_ticker], int(quantity))
            save_trasaction_history(transaction)
            return message
        except ValueError as e:
            return f"[bold red]Bład: {e}[/bold red]"
    def handle_sell(self):
        try:
            share_ticker = Prompt.ask("Podaj skrótki spółki, którą chcesz sprzedać", choices=self.wallet.portfolio.keys())
            quantity = int(Prompt.ask("Ile akcji checsz sprzedać?"))
            message, transaction =  self.wallet.sell(generate_transaction_id(), self.stock_makret[share_ticker], quantity)
            save_trasaction_history(transaction)
            return message
        except InsuffincientSharesError as e:
            return f"[bold red]Problem z ilością: {e}[/bold red]"
        except ValueError as e:
            return f"[bold red]Błędne dane: {e}[/bold red]"
    def handle_back_to_main_menu(self):
        self.current_state = "main"
    def handle_exit(self):
        save_wallet(self.wallet)
        os._exit(0)
    
    def get_current_menu(self):
        if self.current_state == "main":
            return self.get_main_menu()
        elif self.current_state == "transaction_history":
            return self.get_transaction_history_menu()
        
       
    def process_input(self):
        # główna metoda sterujaca
        if self.current_state == "main":
            actions = self.get_main_menu()
        elif self.current_state == "transaction_history":
            actions = self.get_transaction_history_menu()

        # Lista wyborów dla Rich Prompt
        choices = list(actions.keys())

        choice = Prompt.ask("[bold yellow]Wybierz akcję[/]", choices=choices)

        # wywołanie fukcji przypisanej do wyboru
        action_func = actions[choice]["func"]
        return action_func()