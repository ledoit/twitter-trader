import yfinance


def compare(old_50, new_50):
    hold = sell = buy = []
    for ticker in old_50:
        if ticker in new_50:
            hold += ticker
        else:
            sell += ticker
    for ticker in new_50:
        if ticker not in hold:
            buy += ticker
    return [hold, sell, buy]


def get_price(ticker):
    company_info = yfinance.Ticker(ticker)
    # print(ticker, "last close: ", company_info.info['previousClose'])
    return float(company_info.info['previousClose'])


# test code
get_price('TSLA')
