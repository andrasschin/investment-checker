from tkinter import *
from controllers.controllers import create_widget, check_input
from windows.error import display_error_window
import csv


def display_add_stock_window(stock_ticker, stock_name, stock_currency, stock_currency_symbol):
    root = Tk()
    root.title("Add Stock")
    root.config(padx="20", pady="10")

    def add_stock(ticker, name, quantity, buying_price, date_bought, curr, curr_symbol):
        if check_input(quan=quantity, price=buying_price, date=date_bought):
            market_value = int(quantity) * float(buying_price)
            with open("data/stocks.csv", "a", newline="") as stocks_data:
                writer = csv.writer(stocks_data, delimiter="|")
                writer.writerow([ticker, name, quantity, buying_price, market_value, curr_symbol, curr, date_bought])
            root.destroy()
        else:
            display_error_window(err_msg="Incorrect input format. Please try again.")

    Labels = []
    Entries = []
    Buttons = []

    label_stock_name = create_widget("label", Labels, root, txt="Stock name:", r=1, c=1)
    label_stock_custom_name = create_widget("label", Labels, root, txt="Custom stock name:", r=2, c=1)
    label_stock_quantity = create_widget("label", Labels, root, txt="Quantity:", r=3, c=1)
    label_stock_buying_price = create_widget("label", Labels, root, txt=f"Buying price ({stock_currency_symbol})", r=4,
                                             c=1)
    label_stock_bought_date = create_widget("label", Labels, root, txt="Date bought (YYYY.MM.DD): ", r=5, c=1)

    label_stock_name_data = create_widget("label", Labels, root, txt=stock_name, r=1, c=2)
    label_stock_custom_name_data = create_widget("entry", Entries, root, w=30, r=2, c=2)
    label_stock_custom_name_data.insert(0, stock_name)
    label_stock_quantity_data = create_widget("entry", Entries, root, w=30, r=3, c=2)
    label_stock_buying_price_data = create_widget("entry", Entries, root, w=30, r=4, c=2)
    label_stock_bought_date_data = create_widget("entry", Entries, root, w=30, r=5, c=2)

    btn_add = create_widget("button", Buttons, root, txt="Add", r=6, c=2,
                            comm=lambda: add_stock(ticker=stock_ticker,
                                                   name=label_stock_custom_name_data.get(),
                                                   quantity=label_stock_quantity_data.get(),
                                                   buying_price=label_stock_buying_price_data.get(),
                                                   date_bought=label_stock_bought_date_data.get(),
                                                   curr=stock_currency,
                                                   curr_symbol=stock_currency_symbol))

    # Configure widgets
    CONFIG = {
        "font": "44",
    }

    for label in Labels:
        label.config(padx="8", pady="8", **CONFIG)
    for button in Buttons:
        button.config(padx="8", pady="4", **CONFIG)
    for entry in Entries:
        entry.config(**CONFIG)

    root.mainloop()
