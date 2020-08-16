from tkinter import *
from windows.searchstock.search_stock import display_search_stock_window

root = Tk()
root.title("Investment Checker")

CONFIG = {
    "font": ("Helvetica", "25"),
    "pady": "20",
    "fg": "#FAFFFD",
    "width": "30",
    "borderwidth": "0"
          }

def my_stocks():
    pass

def create_report():
    pass

my_stocks = Button(root, text="My Stocks", command=my_stocks)
add_stock = Button(root, text="Add Stock", command=lambda: display_search_stock_window())
create_report = Button(root, text="Create Report", command=create_report)

my_stocks.config(bg="#3C91E6",**CONFIG)
add_stock.config(bg="#A2D729", **CONFIG)
create_report.config(bg="#FA824C", **CONFIG)

my_stocks.pack()
add_stock.pack()
create_report.pack()

root.mainloop()
