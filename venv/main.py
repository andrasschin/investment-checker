from tkinter import *
from windows.searchstock.search_stock import display_search_stock_window
from windows.my_stocks import display_my_stocks_window
from windows.create_report import display_create_report_window

root = Tk()
root.title("Investment Checker")

my_stocks = Button(root, text="My Stocks", command=lambda: display_my_stocks_window())
add_stock = Button(root, text="Add Stock", command=lambda: display_search_stock_window())
create_report = Button(root, text="Create Report", command=lambda: display_create_report_window())

# Widget styling
basic_config = {
    "font": ("Helvetica", "25"),
    "pady": "20",
    "fg": "#FAFFFD",
    "width": "30",
    "borderwidth": "0"
}

my_stocks.config(bg="#3C91E6", **basic_config)
add_stock.config(bg="#A2D729", **basic_config)
create_report.config(bg="#FA824C", **basic_config)

my_stocks.pack()
add_stock.pack()
create_report.pack()

root.mainloop()
