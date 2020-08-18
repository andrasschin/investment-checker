class Stock:
    def __init__(self, ticker, name, price, curr, curr_symbol):
        self.ticker = ticker
        self.name = name
        self.price = price
        self.currency = curr
        self.currency_symbol = curr_symbol


class MyStock:
    def __init__(self, stock_data):
        self.ticker = stock_data[0]
        self.name = stock_data[1]
        self.quantity = stock_data[2]
        self.buying_price = stock_data[3]
        self.market_value = stock_data[4]
        self.currency_symbol = stock_data[5]
        self.currency = stock_data[6]
        self.date_bought = stock_data[7]