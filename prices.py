import yfinance


def get_price(ticker):
    company_info = yfinance.Ticker(ticker)
    print(ticker, "last close: ", company_info.info['previousClose'])


get_price('TSLA')  # test code
