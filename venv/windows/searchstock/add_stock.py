from tkinter import *
from classes.classes import Stock
from controllers.controllers import create_widget


def display_add_stock_window(stock):
    root = Tk()
    root.title("Add Stock")
    root.config(padx="20", pady="10")

    def add_stock():
        pass

    Labels = []
    Entries = []
    Buttons = []

    label_stock_name = create_widget("label", Labels, root, txt="Stock name:", r=1, c=1)
    label_stock_custom_name = create_widget("label", Labels, root, txt="Custom stock name:", r=2, c=1)
    label_stock_quantity = create_widget("label", Labels, root, txt="Quantity:", r=3, c=1)
    label_buying_price = create_widget("label", Labels, root, txt=f"Buying price ({stock.currency_symbol})", r=4, c=1)

    label_stock_name_data = create_widget("label", Labels, root, txt=stock.name, r=1, c=2)
    label_stock_custom_name_data = create_widget("entry", Entries, root, w=30, r=2, c=2)
    label_stock_custom_name_data.insert(0, stock.name)
    label_stock_quantity_data = create_widget("entry", Entries, root, w=30, r=3, c=2)
    label_stock_buying_price_data = create_widget("entry", Entries, root, w=30, r=4, c=2)

    btn_add = create_widget("button", Buttons, root, txt="Add", r=5, c=2, comm=add_stock)

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