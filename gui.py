from rich.console import Console, Group
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table

from models import Wallet, Share, Transaction
from menu_manager import MenuManager


def draw_portfolio(wallet :Wallet,  stock_market :dict, transaction_history: dict):
    table = Table(title="Twój Portfel")
    table.add_column(header="Lp")
    table.add_column(header="Ticker")
    table.add_column(header="Spólka")
    table.add_column(header="Liczba")
    table.add_column(header="Cena zakupu")
    table.add_column(header="Aktualna cena")
    table.add_column(header="Wartość")
    table.add_column(header="Zysk")

    wallet.refresh_satate(transaction_history)
    
    for index, ticker in enumerate(wallet.portfolio, 1):
        data = wallet.portfolio.get(ticker)
        profit_in_percent = stock_market[ticker].price / data['avg_price'] * 100 - 100
        if profit_in_percent > 0:
            color = "green"
        elif profit_in_percent < 0:
            color = "red"
        else:
            color = "white"
        if data:
            table.add_row(
                str(index), 
                ticker, 
                str(stock_market[ticker].name),
                str(data['quantity']),
                str(round(data['avg_price'], 2)),
                str(stock_market[ticker].price),
                str(round(stock_market[ticker].price * data['quantity'], 2)),
                f"[{color}]{str(round(profit_in_percent, 2))} %[/{color}]"
            )
    return table

def draw_transaction_history(transaction_history :dict):
    table = Table(title="Historia transakcji")
    table.add_column(header="Lp")
    table.add_column(header="Typ")
    table.add_column(header="Ticker")
    table.add_column(header="Liczba")
    table.add_column(header="Wartość")

    history = transaction_history

    for index, i in enumerate(history, 1):
        table.add_row(str(index), history[i]['type'], history[i]['ticker'], str(history[i]['quantity']), str(round(history[i]['value'], 2)))
    
    return table

def draw_maket(stock_makret :dict):
    table = Table(title="Rynek - WIG20")
    table.add_column(header="Lp")
    table.add_column(header="Skrót")
    table.add_column(header="Spółka")
    table.add_column(header="Cena akcji")

    for index, i in enumerate(stock_makret, 1):
       share = stock_makret[i]
       table.add_row(str(index), i, share.name, str(share.price))
    
    return table

def draw_log(messages :list):
    elements = [f"> {item}" for item in messages]
    content = Group(*elements)
    return content







def draw_main_screen(wallet :Wallet, transaction_history :dict,  stock_market :dict,  messages :list, menu :MenuManager):
    console = Console()

    main_screen = Layout()
    #podział ekranu na trzy
    main_screen.split_column(
        Layout(name="top", ratio=1, size=5),
        Layout(name="mid", ratio=2),
        Layout(name="bottom", ratio=1, size=5)
    )

    #podział lewa prawa
    main_screen["mid"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )

    # zasilenie paneli danymi
    main_screen["left"].split_row(
        Layout(name="leftpanel_left", ratio=1), 
        Layout(name="leftpanel_right", ratio=1)
    )

    if menu.current_state == "main":
        profit, profit_in_percent = wallet.get_total_profit(stock_market, transaction_history)
        if profit and profit_in_percent > 0:
            color = "green"
        elif profit and profit_in_percent < 0:
            color = "red"
        else:
            color = "white"
        main_screen["right"].update(Panel(Group(Panel(draw_portfolio(wallet, stock_market, transaction_history), title="Portfolio"), 
                                            Panel(f"Dostępna gotówka: [bold green]{round(wallet.cash, 2)} PLN[/bold green] Wartość zakupu akcji: {wallet.shares_value} Obecna wartość akcji: {wallet.get_shares_value(transaction_history, stock_market)} Wynik: [bold {color}]{round(profit, 2)} PLN ({round(profit_in_percent, 2)}%[/bold {color}])  ", title="Saldo"))))
    elif menu.current_state == "transaction_history":
        main_screen["right"].update(Panel(Group(Panel(draw_transaction_history(transaction_history), title="Historia transakcji"), 
                                            Panel(f"Dostępna gotówka: [bold green]{round(wallet.cash, 2)} PLN[/bold green] Wartość akcji: {wallet.shares_value} ", title="Portfel"))))
    main_screen["leftpanel_left"].update(Panel(draw_maket(stock_market), title="Rynek"))
    main_screen["leftpanel_right"].update(Panel(draw_log(messages), title="Log"))

    menu = menu.get_current_menu()
    menu_text = " | ".join(f"({k}) {v['label']}" for k, v in menu.items())
    main_screen["bottom"].update(Panel(menu_text, title="Menu"))
                            


    # print całego ekranu
    console.print(main_screen)
