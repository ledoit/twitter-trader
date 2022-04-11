from datetime import datetime as dt, timedelta as td
from twitter import get_new_50
import yfinance


# returns list that contains the list of companies to hold, sell, and buy respectively
def compare(old_50, new_50):
    hold, sell, buy = [], [], []
    for ticker in old_50:
        if ticker in new_50:
            hold.append(ticker)
        else:
            sell.append(ticker)
    for ticker in new_50:
        if ticker not in hold:
            buy.append(ticker)
    return [hold, sell, buy]


# calculates total value of portfolio as float
def eval_portfolio(lst):
    total = 0.0
    for ticker in lst:
        total += round(float(yfinance.Ticker(ticker).info['previousClose']), 2)
    return total


def process_balance(p, c):
    [hold, sell, buy] = compare(p, get_new_50())
    print(f"hold: {hold}, sell: {sell}, buy: {buy}")
    cash_in = eval_portfolio(sell)
    cash_out = eval_portfolio(buy)
    c += cash_in - cash_out
    s = eval_portfolio(hold) + cash_out
    print(f"portfolio: {hold + buy}, stock: {s}, cash: {c}")
    return hold + buy, s, c


if __name__ == "__main__":

    # first call to process_balance
    time_period, logs = 0, []
    portfolio, stock, cash = process_balance([], 0.0)
    logs.append([time_period, stock + cash])
    print(f"time period: {logs[-1][0]}, net balance is: {logs[-1][1]}")
    start_time = dt.now()

    # infinite loop for fetching positivity ratings & prices, and updating the DB
    while True:
        # time buffer that lasts 1 day
        # if dt.now() - start_time >= td(days=1):
        #     start_time = dt.now()
        portfolio, stock, cash = process_balance(portfolio, cash)
        time_period += 1
        logs.append([time_period, stock + cash])
        print(f"time period: {logs[-1][0]}, net balance is: {logs[-1][1]}")
