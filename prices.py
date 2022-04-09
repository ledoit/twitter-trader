import yfinance


def get_price(ticker):
    company_info = yfinance.Ticker(ticker)
    # print(ticker, "last close: ", company_info.info['previousClose'])
    return float(company_info.info['previousClose'])


# test code
get_price('TSLA')
