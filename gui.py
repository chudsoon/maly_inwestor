from rich.console import Console, Group
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table

from models import Wallet, Share, Transaction
from menu_mananger import MenuManager


def draw_portfolio(wallet :Wallet,  stock_market :dict):
    table = Table(title="Twój Portfel")
    table.add_column(header="Lp")
    table.add_column(header="Ticker")
    table.add_column(header="Spólka")
    table.add_column(header="Liczba")
    table.add_column(header="Cena zakupu")
    table.add_column(header="Aktualna cena")
    table.add_column(header="Wartość")

    portfolio = wallet.portfolio
    
    for index, i in enumerate(wallet.portfolio, 1):
        table.add_row(str(index), portfolio[i]['ticker'], portfolio[i]['name'], str(portfolio[i]['quantity']), str(portfolio[i]['price']), str(stock_market[i].price), str(round(stock_market[i].price * portfolio[i]['quantity'], 2)))

    return table

def draw_transaction_history(wallet :Wallet):
    table = Table(title="Historia transakcji")
    table.add_column(header="Lp")
    table.add_column(header="Typ")
    table.add_column(header="Ticker")
    table.add_column(header="Liczba")
    table.add_column(header="Wartość")

    history = wallet.transaction_history

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







def draw_main_screen(wallet :Wallet, stock_market :dict,  messages :list, menu :MenuManager):
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
        main_screen["right"].update(Panel(Group(Panel(draw_portfolio(wallet, stock_market), title="Portfolio"), 
                                            Panel(f"Dostępna gotówka: [bold green]{round(wallet.cash, 2)} PLN[/bold green] Wartość akcji: {wallet.get_shares_value(stock_market)} Wynik: {wallet.get_total_profit(stock_market)}", title="Portfel"))))
    elif menu.current_state == "transaction_history":
        main_screen["right"].update(Panel(Group(Panel(draw_transaction_history(wallet), title="Historia transakcji"), 
                                            Panel(f"Dostępna gotówka: [bold green]{round(wallet.cash, 2)} PLN[/bold green] Wartość akcji: {wallet.get_shares_value(stock_market)} ", title="Portfel"))))
    main_screen["leftpanel_left"].update(Panel(draw_maket(stock_market), title="Rynek"))
    main_screen["leftpanel_right"].update(Panel(draw_log(messages), title="Log"))

    menu = menu.get_current_menu()
    menu_text = " | ".join(f"({k}) {v['label']}" for k, v in menu.items())
    main_screen["bottom"].update(Panel(menu_text, title="Menu"))
                            


    # print całego ekranu
    console.print(main_screen)
