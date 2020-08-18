from tkinter import *
from classes.classes import Stock
from controllers.controllers import create_widget, config_widgets
import csv


def display_my_stocks_window():
    root = Tk()
    root.title("My Stocks")
    root.config(padx="20", pady="10")

    Labels = []

    with open("data/stocks.csv", newline="") as stocks_data:
        reader = csv.reader(stocks_data, delimiter="|")

        # Create grid and fill in the data
        for count, row in enumerate(reader):
            num_of_columns = len(row)
            row_index = count + 1
            for col in range(num_of_columns):
                create_widget("label", Labels, root, txt=row[col], r=row_index, c=col)

    # Style labels
    basic_config = {
        "font": "44",
        "padx": "10",
        "pady": "8"
    }
    config_widgets(Labels, basic_cfg=basic_config)

    root.mainloop()
