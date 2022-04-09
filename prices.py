import yfinance


def get_price(ticker):
    company_info = yfinance.Ticker(ticker)
    # print(ticker, "last close: ", company_info.info['previousClose'])
    return float(company_info.info['previousClose'])


# test code
get_price('TSLA')

def get_prices(ticker_lst):
    prices = []
    for ticker in ticker_lst:
        prices.append(get_price(ticker))
    return prices

