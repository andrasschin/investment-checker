from tkinter import *
from controllers.controllers import create_widget, config_widgets, color_difference, create_line_chart, style_gain_loss
from classes.classes import Stock
import csv
import datetime
from openpyxl import load_workbook
from openpyxl.styles import numbers, Font
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties

def display_create_report_window():
    root = Tk()
    root.title("Report")
    root.config(padx="20", pady="10")

    def log(today, stocks):
        wb = load_workbook(filename="data/stocks.xlsx")
        for stock in stocks:
            # This step deletes the chart
            worksheet = wb[stock.name]
            ws = wb.copy_worksheet(worksheet)
            wb.remove_sheet(worksheet)
            ws.title = stock.name

            next_row = ws.max_row + 1
            prev_row = next_row - 1

            # Get previous log data
            previous_price          = ws.cell(prev_row, 5).value
            previous_market_value   = previous_price * stock.quantity

            # Create log data
            price_change                    = stock.current_price - stock.buying_price
            price_change_to_latest          = stock.current_price - previous_price
            market_value_change             = stock.current_market_value - stock.market_value
            market_value_change_to_latest   = stock.current_market_value - previous_market_value
            change_percentage               =  stock.current_price/stock.buying_price - 1
            change_percentage_to_latest     = stock.current_price/previous_price - 1

            # Write log line
            log_data = {
                3: datetime.date(today.year, today.month, today.day), # Date
                4: datetime.time(today.hour, today.minute, today.second), # Time
                5: stock.current_price, # Price
                6: price_change, # Change
                7: price_change_to_latest, # Change to latest
                8: stock.current_market_value, # Market value
                9: market_value_change, # Change
                10: market_value_change_to_latest, # Change to latest
                11: change_percentage, # Change (%)
                12: change_percentage_to_latest, # Change to latest (%)
                13: stock.buying_price, # Buying price (for chart)
                14: stock.market_value # Market value (for chart)
            }
            ws.append(log_data)

            # Apply gain/loss styles
            change_cols_1 = [6, 9, 11]
            change_cols_2 = [7, 10, 12]
            style_gain_loss(worksheet=ws,
                            current=stock.current_price,
                            previous=stock.buying_price,
                            cols=[6, 9, 11],
                            row=next_row)

            style_gain_loss(worksheet=ws,
                            current=price_change_to_latest,
                            previous=0,
                            cols=[7, 10, 12],
                            row=next_row)

            # Apply formats
            ws.cell(next_row, 3).number_format = "YYYY.MM.DD"
            ws.cell(next_row, 4).number_format = "HH:MM:SS"
            ws.cell(next_row, 5).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 6).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 7).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 8).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 9).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 10).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 11).number_format = "0.00%"
            ws.cell(next_row, 12).number_format = "0.00%"

            # Create charts

            # Price chart

            # Data to be plotted
            values          = Reference(ws, min_col=5, min_row=14, max_col=5, max_row=next_row)
            comparison_line = Reference(ws, min_col=13, min_row=14, max_col=13, max_row=next_row)
            dates           = Reference(ws, min_col=3, min_row=15, max_col=3, max_row=next_row)

            # Create chart
            chart_price = create_line_chart(title="Price change in time",
                                            y_axis_title="Price",
                                            values=values,
                                            comparison_line=comparison_line,
                                            dates=dates)

            # Add chart to worksheet
            ws.add_chart(chart_price, "P5")


            # Market value chart

            # Date to be plotted
            values          = Reference(ws, min_col=8, min_row=14, max_col=8, max_row=next_row)
            comparison_line = Reference(ws, min_col=14, min_row=14, max_col=14, max_row=next_row)
            dates           = Reference(ws, min_col=3, min_row=15, max_col=3, max_row=next_row)

            # Create chart
            chart_mv = create_line_chart(title="Market value change in time",
                                         y_axis_title="Market value",
                                         values=values,
                                         comparison_line=comparison_line,
                                         dates=dates)

            # Add chart to worksheet
            ws.add_chart(chart_mv, "P30")


        # Update summary
        for currency in currencies:
            ws = wb[f"Summary ({currency})"]

            next_row = ws.max_row + 1
            prev_row = next_row - 1

            # Get previous log data
            if type(ws.cell(prev_row, 13).value) is not float:
                previous_capital = initial_capitals[currency]
            else:
                previous_capital = ws.cell(prev_row, 13).value

            # Create log data
            capital_change                          = current_capitals[currency] - initial_capitals[currency]
            capital_change_percentage               = current_capitals[currency]/initial_capitals[currency] - 1
            try:
                capital_change_to_latest            = current_capitals[currency] - previous_capital
                capital_change_to_latest_percentage = current_capitals[currency]/previous_capital - 1
            except:
                capital_change_to_latest            = 0
                capital_change_to_latest_percentage = 0

            # Write log line
            log_data = {
                10: datetime.date(today.year, today.month, today.day), # Date
                11: datetime.time(today.hour, today.minute, today.second), # Time
                12: initial_capitals[currency], # Initial capital
                13: current_capitals[currency], # Current capital
                14: capital_change, # Capital change to initial
                15: capital_change_to_latest, # Capital change to latest
                16: capital_change_percentage, # Change (%)
                17: capital_change_to_latest_percentage # Change to latest (%)
            }
            ws.append(log_data)

            # Apply formats
            ws.cell(next_row, 10).number_format = "YYYY.MM.DD"
            ws.cell(next_row, 11).number_format = "HH:MM:SS"
            ws.cell(next_row, 12).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 13).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 14).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 15).number_format = numbers.BUILTIN_FORMATS[4]
            ws.cell(next_row, 16).number_format = "0.00%"
            ws.cell(next_row, 17).number_format = "0.00%"

            # Apply gain/loss styles
            style_gain_loss(worksheet=ws,
                            current=current_capitals[currency],
                            previous=initial_capitals[currency],
                            cols=[14, 16], # 14, 16: Change
                            row=next_row)

            style_gain_loss(worksheet=ws,
                            current=current_capitals[currency],
                            previous=previous_capital,
                            cols=[15, 17], # 15, 17: Change to latest
                            row=next_row)

            # Add chartsheet
            if f"Summary ({currency}) Chart" in wb.sheetnames:
                cs = wb[f"Summary ({currency}) Chart"]
                wb.remove_sheet(cs)
            cs = wb.create_chartsheet(f"Summary ({currency}) Chart")

            # Data to be plotted
            values          = Reference(ws, min_col=13, max_col=13, min_row=12, max_row=next_row)
            comparison_line = Reference(ws, min_col=12, max_col=12, min_row=12, max_row=next_row)
            dates           = Reference(ws, min_col=10, min_row=13, max_col=10, max_row=next_row)

            # Create chart
            chart_summary = create_line_chart(title=f"Change of capital in {currency} in time",
                                              y_axis_title="Capital",
                                              values=values,
                                              comparison_line=comparison_line,
                                              dates=dates)

            # Add chart to worksheet
            cs.add_chart(chart_summary)


        # Save the workbook
        wb.save(filename="data/stocks.xlsx")

        # Disable log button
        btn_log.config(state="disabled")

    row_count   = 0
    today       = datetime.datetime.today()
    Labels      = []
    Buttons     = []

    with open("data/stocks.csv", newline="") as stocks_data:
        reader = csv.reader(stocks_data, delimiter="|")
        next(reader) # Ignore the titles
        stocks = [Stock(row) for row in reader]
        stocks.sort(key=lambda stock: stock.currency) # Sort by currency

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
    if row_count:
        row_count += 3
    else: row_count = 3

    label_initial_capital_value = create_widget("label", Labels, root, txt="Initial capital value", r=row_count, c=2)
    label_current_capital_value = create_widget("label", Labels, root, txt="Current capital value", r=row_count, c=3)
    label_capital_difference    = create_widget("label", Labels, root, txt="Difference", r=row_count, c=4)
    label_change                = create_widget("label", Labels, root, txt="Change", r=row_count, c=5)

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

    btn_log = create_widget("button", Buttons, root, txt="Log", r=row_count+1, c=6, comm=lambda: log(today, stocks))

    basic_config = {
        "font": "44",
        "padx": "10",
        "pady": "8"
    }
    config_widgets(Labels, basic_cfg=basic_config)
    config_widgets(Buttons, basic_cfg=basic_config)

    root.mainloop()
