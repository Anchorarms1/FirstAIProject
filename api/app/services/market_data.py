import robin_stocks.robinhood as r
import os

class MarketDataService:
    def __init__(self):
        self.is_logged_in = False
    def login(self):
        username = os.getenv("ROBINHOOD_USERNAME")
        password = os.getenv("ROBINHOOD_PASSWORD")
        if username and password:
            r.login(username, password)
            self.is_logged_in = True
    def get_stock_price(self, symbol):
        if not self.is_logged_in: self.login()
        quote = r.get_latest_price(symbol)
        return float(quote[0]) if quote else None
    def get_historical_data(self, symbol, interval='hour', span='week'):
        if not self.is_logged_in: self.login()
        return r.stocks.get_stock_historicals(symbol, interval=interval, span=span)
