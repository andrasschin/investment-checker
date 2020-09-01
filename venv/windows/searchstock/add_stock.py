from tkinter import *
from controllers.controllers import create_widget, config_widgets, check_input, excel_sheet_setup
from windows.error import display_error_window
import csv


def display_add_stock_window(stock_ticker, stock_name, stock_currency, stock_currency_symbol):
    root = Tk()
    root.title("Add Stock")
    root.config(padx="20", pady="10")

    def add_stock(ticker, name, quantity, buying_price, date_bought, currency, currency_symbol):
        if check_input(quan=quantity, price=buying_price, date=date_bought):
            market_value = int(quantity) * float(buying_price)

            # Write data to stocks.csv
            with open("data/stocks.csv", "a", newline="") as stocks_data:
                writer = csv.writer(stocks_data, delimiter="|")
                writer.writerow([ticker, name, quantity, buying_price, market_value, currency_symbol, currency, date_bought])

            # Create excel worksheet for stock
            excel_sheet_setup(ticker, name, quantity, currency, date_bought, buying_price, market_value)

            # Close window
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
                            comm=lambda: add_stock(ticker=stock_ticker.upper(),
                                                   name=label_stock_custom_name_data.get(),
                                                   quantity=label_stock_quantity_data.get(),
                                                   buying_price=label_stock_buying_price_data.get(),
                                                   date_bought=label_stock_bought_date_data.get(),
                                                   currency=stock_currency,
                                                   currency_symbol=stock_currency_symbol))

    # Widget styling
    basic_config = {
        "font": "44",
    }

    config_widgets(widgets=Labels, basic_cfg=basic_config, additional_cfg={"padx": "8", "pady": "8"})
    config_widgets(widgets=Buttons, basic_cfg=basic_config, additional_cfg={"padx": "8", "pady": "4"})
    config_widgets(widgets=Entries, basic_cfg=basic_config)

    root.mainloop()
