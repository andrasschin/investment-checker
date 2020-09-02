from tkinter import *
import re
import datetime
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Alignment, Font, numbers
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import column_index_from_string
from openpyxl.chart import LineChart, Reference
from openpyxl.chart.shapes import GraphicalProperties


def create_widget(type, widget_list, root, txt="", r=0, c=0, w=0, comm="", state="normal"):
    if type == "label":
        widget = Label(root, text=txt)
        widget_list.append(widget)
    if type == "entry":
        widget = Entry(root, width=w)
        widget_list.append(widget)
    if type == "button":
        widget = Button(root, text=txt, command=comm, state=state)
        widget_list.append(widget)

    widget.grid(row=r, column=c)

    return widget


def config_widgets(widgets=[], basic_cfg={}, additional_cfg={}):
    for widget in widgets:
        widget.config(**basic_cfg, **additional_cfg)


def check_input(quan="", price="", date=""):
    quan_pattern = re.compile("^\d+$")
    price_pattern = re.compile("^(\d+(\.\d+)?)$")
    date_pattern = re.compile("\d{4}\.\d{2}\.\d{2}$")

    if quan_pattern.match(quan) == None or price_pattern.match(price) == None or date_pattern.match(date) == None:
        return False

    return True


def color_difference(value_to_check, widget):
    if value_to_check > 0:
        widget.config(fg="#149911")
    if value_to_check < 0:
        widget.config(fg="#B23A48")


def excel_sheet_setup(ticker, name, quantity, currency, date_bought, buying_price, market_value):
    # Create stocks.xlsx if doesn't exist
    try:
        wb = load_workbook("data/stocks.xlsx")
    except FileNotFoundError:
        wb = Workbook()

    # Convert variables
    quantity = int(quantity)
    buying_price = float(buying_price)
    date_b = datetime.datetime.strptime(date_bought, "%Y.%m.%d").date()

    # Create sheet
    ws = wb.create_sheet(name)

    # Size columns
    used_columns = ["C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"]
    for col in used_columns:
        ws.column_dimensions[col].width = 20

    # Styles
    font_bold = Font(bold=True)
    align_center = Alignment(horizontal="center")

    # Formats

    # Date format
    date_format = "YYYY.MM.DD"
    date_cells = [(15, 3), (8, 7)]

    # Apply date format
    for r, c in (date_cells):
        ws.cell(r, c).number_format = date_format

    # Number format
    number_format = numbers.BUILTIN_FORMATS[4]
    number_cells = [(6, 10), (8, 10), (15, 5), (15, 8)]

    # Apply number format
    for r, c in (number_cells):
        ws.cell(r, c).number_format = number_format

    # Horizontally center cells
    center_cells = [(4, 9),
                    (6, 7), (7, 7),
                    (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12),
                    (14, 13), (14, 14)]
    for r, c in (center_cells):
        ws.cell(r, c).alignment = align_center

    # Write and style stock name
    ws["H4"] = "Name:"
    ws["I4"] = name
    ws["I4"].font = font_bold
    ws.merge_cells(start_row=4, start_column=9, end_row=4, end_column=10)

    # Write rest of the necesarry info
    basic_info = {
        "F6": "Ticker:",
        "G6": ticker,
        "F7": "Currency:",
        "G7": currency,
        "F8": "Date bought:",
        "G8": date_b,
        "I6": "Buying price:",
        "J6": buying_price,
        "I7": "Quantity:",
        "J7": quantity,
        "I8": "Market Value:",
        "J8": market_value,
        "L6": "Importance:"
    }

    for cell, data in basic_info.items():
        ws[cell] = data

    log_header = {
        "C14": "Date",
        "D14": "Time",
        "E14": "Price",
        "F14": "Change",
        "G14": "Change to latest",
        "H14": "Market value",
        "I14": "Change",
        "J14": "Change to latest",
        "K14": "Change (%)",
        "L14": "Change to latest (%)",
        "M14": "Buying price",
        "N14": "Initial market value"
    }

    for cell, data in log_header.items():
        ws[cell] = data
        ws[cell].font = font_bold

    basic_log = {
        "C15": date_b,
        "E15": buying_price,
        "H15": market_value,
        "M15": buying_price,
        "N15": market_value
    }

    for cell, data in basic_log.items():
        ws[cell] = data

    # Create summary for currency if it doesn't exist
    if not f"Summary ({currency})" in wb.sheetnames:
        ws = wb.create_sheet(f"Summary ({currency})")

        # Size columns
        used_columns = ["J", "K", "L", "M", "N", "O", "P", "Q", "R"]
        for col in used_columns:
            ws.column_dimensions[col].width = 20

        header = ["Date", "Time", "Initial capital", "Current capital", "Change", "Change to latest", "Change (%)", "Change to latest (%)"]
        write_line(ws, start_col="J", start_row=12, data=header, style={"bold": True, "center": True})

    wb.save("data/stocks.xlsx")


# This function might be superflous
def write_line(ws, start_col, start_row, data, style):
    if type(start_col) is str:
        col = column_index_from_string(start_col)
    else:
        col = start_col
    row = start_row

    for count, c in enumerate(range(col, col + len(data))):
        cell = ws.cell(row, c)
        cell.value = data[count]

        # Styles
        font_bold = Font(bold=True)
        align_center = Alignment(horizontal="center")
        if style["bold"]:
            cell.font = font_bold
        if style["center"]:
            cell.alignment = align_center


def create_line_chart(title="", y_axis_title="", values="", comparison_line="", dates=""):
    """
    Creates a line chart with two lines (one is the changing values, the other is the comparison line). On the x axis are dates.
    :param title: The title of the chart (string)
    :param y_axis_title: The title of the y axis (string)
    :param values: The changing values to be plotted (Reference object)
    :param comparison_line: The comparison values to be plotted (Reference object)
    :param dates: Dates for the x axis (Reference object)
    :return: LineChart object
    """
    chart = LineChart()
    chart.title = title
    chart.height = 10
    chart.width = 17

    # Legend
    chart.legend.position = 'b'

    # Data
    chart.add_data(values, titles_from_data=True)
    chart.add_data(comparison_line, titles_from_data=True)

    # Axes
    chart.x_axis.title = "Date"
    chart.y_axis.title = y_axis_title

    chart.x_axis.number_format = "YYYY.MM.DD"
    chart.set_categories(dates)

    # Lines, chart design
    chart.series[0].graphicalProperties.line.solidFill = "7DCE82"
    chart.series[0].graphicalProperties.line.width = 27000
    chart.series[0].smooth = True
    chart.series[1].graphicalProperties.line.solidFill = "E3170A"
    chart.series[1].graphicalProperties.line.width = 27000
    props = GraphicalProperties(solidFill="2C302E")
    chart.plot_area.graphicalProperties = props

    return chart


def style_gain_loss(worksheet="", current=0, previous=0, cols=[], row=0):
    gain = Font(color="149911")
    loss = Font(color="B23A48")

    if current > previous:
        for col in cols:
            worksheet.cell(row, col).font = gain

    if current < previous:
        for col in cols:
            worksheet.cell(row, col).font = loss
