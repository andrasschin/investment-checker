from yahooquery import Ticker

class Stock:
    def __init__(self, stock_data):
        self.ticker = stock_data[0]
        self.name = stock_data[1]
        self.quantity = int(stock_data[2])
        self.buying_price = float(stock_data[3])
        self.market_value = float(stock_data[4])
        self.currency_symbol = stock_data[5]
        self.currency = stock_data[6]
        self.date_bought = stock_data[7]

    def get_stock_data(self):
        ticker = Ticker(self.ticker)
        data = ticker.price[self.ticker]
        self.current_price = data["regularMarketPrice"]
        self.price_difference = round(float(self.current_price) - float(self.buying_price), 2)
        self.current_market_value = round(float(self.quantity) * float(self.current_price), 2)
        self.market_value_difference = round(float(self.current_market_value) - float(self.market_value), 2)

        return [self.ticker, self.name, self.quantity, self.buying_price, self.current_price, self.price_difference, self.market_value, self.current_market_value, self.market_value_difference, self.currency, self.date_bought]