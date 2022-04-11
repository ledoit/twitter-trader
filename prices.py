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


def get_price_dict(ticker_lst):
    price_dict = {}
    for ticker in ticker_lst:
        print("ticker: ", ticker)
        price_dict[ticker] = get_price(ticker)
    return price_dict
