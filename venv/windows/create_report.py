from tkinter import *
from controllers.controllers import create_widget, config_widgets
from classes.classes import Stock
import csv

def display_create_report_window():
    root = Tk()
    root.title("Report")
    root.config(padx="20", pady="10")

    Labels = []
    Buttons = []

    with open("data/stocks.csv", newline="") as stocks_data:
        reader = csv.reader(stocks_data, delimiter="|")
        header = next(reader)
        stocks = [Stock(row) for row in reader]

    root.mainloop()