from tkinter import *
from controllers.controllers import create_widget, config_widgets, color_difference
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
        next(reader)
        stocks = [Stock(row) for row in reader]
        stocks.sort(key=lambda stock: stock.currency)

    header = ["Stock ticker", "Stock name", "Quantity", "Buying price", "Current Price", "Price difference",
              "Market Value", "Current Market Value", "Market value difference", "Currency", "Date Bought"]
    for col_count, item in enumerate(header):
        create_widget("label", Labels, root, txt=item, r=1, c=col_count+1)

    for row_count, stock in enumerate(stocks):
        stock_data = stock.get_stock_data()
        for col_count, item in enumerate(header):
            widget = create_widget("label", Labels, root, txt=stock_data[col_count], r=row_count+2, c=col_count+1)

            # Check if in profit and color accordingly
            if header[col_count] == "Price difference":
                color_difference(stock_data[col_count], widget)

            # Check if in profit and color accordingly
            if header[col_count] == "Market value difference":
                color_difference(stock_data[col_count], widget)

    # Summary
    row_count += 3
    label_initial_capital_value = create_widget("label", Labels, root, txt="Initial capital value", r=row_count, c=2)
    label_current_capital_value = create_widget("label", Labels, root, txt="Current capital value", r=row_count, c=3)
    label_capital_difference = create_widget("label", Labels, root, txt="Difference", r=row_count, c=4)
    label_change = create_widget("label", Labels, root, txt="Change", r=row_count, c=5)

    currencies = {stock.currency for stock in stocks}
    initial_capitals = {}
    current_capitals = {}
    for currency in currencies:
        row_count += 1

        initial_capitals[currency] = round(sum([float(stock.market_value) for stock in stocks if stock.currency==currency]), 3)
        current_capitals[currency] = round(sum([float(stock.current_market_value) for stock in stocks if stock.currency==currency]), 3)

        create_widget("label", Labels, root, txt=currency, r=row_count, c=1)
        create_widget("label", Labels, root, txt=initial_capitals[currency], r=row_count, c=2)
        label_current_capital_value_data = create_widget("label", Labels, root, txt=current_capitals[currency], r=row_count, c=3)

        difference = current_capitals[currency] - initial_capitals[currency]
        label_capital_difference_data = create_widget("label", Labels, root, txt=f"{difference:.2f}", r=row_count, c=4)

        change = (current_capitals[currency] / initial_capitals[currency] - 1) * 100
        label_change_data = create_widget("label", Labels, root, txt=f"{change:.2f}%", r=row_count, c=5)

        # Color widgets accordingly
        color_difference(difference, label_current_capital_value_data)
        color_difference(difference, label_capital_difference_data)
        color_difference(difference, label_change_data)


    basic_config = {
        "font": "44",
        "padx": "10",
        "pady": "8"
    }
    config_widgets(Labels, basic_cfg=basic_config)
    config_widgets(Buttons, basic_cfg=basic_config)

    root.mainloop()
