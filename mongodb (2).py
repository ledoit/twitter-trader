import pymongo
import json
from datetime import datetime as dt, timedelta as td
from twitter import get_new_50, compare
from prices import get_price


class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient(
            "mongodb+srv://user:user@cluster0.gn2iv.mongodb.net/twitter_trader?retryWrites=true&w=majority")
        self.db = self.client.twitter_trader
        self.portfolio = self.db.portfolio
        self.balance = self.db.balance
@@ -15,69 +18,89 @@ def __init__(self):
    def getPortfolio(self):
        cursor = self.portfolio.find()
        return list(cursor)

    # takes in lst of new portfolio and updates DB
    def setPortfolio(self, new_portfolio):
        # storing a lst:
        self.portfolio.delete_many([])
        self.portfolio.insert_one(new_portfolio)

        # # storing a dict:
        # self.portfolio.delete_many({})
        # lst = []
        # for co in new_portfolio:
        #     doc = {"company": co, "price": new_portfolio[co]}
        #     lst.append(doc)
        # self.portfolio.insert_many(lst)

    # calculates total value of portfolio as float
    def evalPortfolio(self, lst):
        total = 0.0
        for ticker in lst:
            total += get_price(ticker)
        return total

    # gets latest balance from DB as float
    def getLatestBalance(self):
        return self.balance.find().limit(1).sort([('$natural', -1)])

    # sets new balance in DB as float
    def setNewBalance(self, new_stock, new_cash):
        last_entry = self.getLatestBalance().next()
        last_time = last_entry['time']
        self.balance.insert_one({'time': last_time + 1, 'balance': new_stock, 'cash': new_cash})

    # # takes in dict of new portfolio and returns JSON
    # def JSONifyPortfolio(self,portfolio_dict):
    #     json.dumps(portfolio_dict)
    #
    # # takes in dict of new portfolio and returns tuple of what to buy and sell -- (to_buy, to_sell) tuple
    # def getTrades(self,new_portfolio):
    #     old_portfolio = self.getPortfolio()
    #     to_buy = []
    #     to_sell = []
    #     for co in old_portfolio:
    #         if not co in new_portfolio:
    #             to_sell.append(co)
    #     for co in new_portfolio:
    #         if not co in old_portfolio:
    #             to_buy.append(co)
    #     return (to_buy,to_sell)

    def initDatabases(self, lst):
        self.setPortfolio(lst)
        self.balance.delete_many({})
        self.balance.insert_one({'time': 0, 'stock': 0, 'cash': 0})

    def processBalance(self):
        old_50 = self.getPortfolio()
        new_50 = get_new_50()
        [hold, sell, buy] = compare(old_50, new_50)
        cash_in = self.evalPortfolio(sell)
        cash_out = self.evalPortfolio(buy)
        latest_cash = self.getLatestBalance()['cash'] + cash_in - cash_out
        latest_stock = self.evalPortfolio(hold) + cash_out
        self.setNewBalance(latest_stock, latest_cash)
        self.setPortfolio(hold + buy)


if __name__ == "__main__":
    # setting up mongo DB
    mongo = Mongo()
    port = mongo.getPortfolio()
    print("Current port:\n", port)
    print("\n\nNew port:", mongo.getPortfolio())

    # initializing DB
    mongo.initDatabases([])

    # first call to processBalance
    mongo.processBalance()
    start_time = dt.now()

    # infinite loop for fetching positivity ratings & prices, and updating the DB
    while True:
        # time buffer that lasts 1 day
        if dt.now() - start_time >= td(days = 1):
            start_time = dt.now()
        mongo.processBalance()