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
        # print(self.db.command("serverStatus"))

    # returns portfolio from DB as dict
    def getPortfolio(self):
        cursor = self.portfolio.find()
        dict = {}
        for doc in cursor:
            dict[doc['company']] = doc['price']
        return dict
        
    # takes in dict of new portfolio and returns tuple of what to buy and sell -- (to_buy, to_sell) tuple
    def getTrades(self,new_portfolio):
        old_portfolio = self.getPortfolio()
        to_buy = []
        to_sell = []
        for co in old_portfolio:
            if not co in new_portfolio:
                to_sell.append(co)
        for co in new_portfolio:
            if not co in old_portfolio:
                to_buy.append(co)
        return (to_buy,to_sell)
    # takes in dict of new portfolio and updates DB
    def setPortfolio(self,new_portfolio):
        self.portfolio.delete_many({})
        lst = []
        for co in new_portfolio:
            doc = {"company": co, "price": new_portfolio[co]}
            lst.append(doc)
        self.portfolio.insert_many(lst)

    # sets balance in DB as float
    def setNewBalance(self,new_balance,new_cash):  # not sponsored by NB
        last_entry = self.getLatestBalance().next()
        last_time = last_entry['time']
        last_balance = last_entry['balance']
        self.balance.insert_one({'time': last_time + 1, 'balance': new_balance, 'cash': new_cash})
        return last_balance + new_balance

    # gets latest balance from DB as cursor
    def getLatestBalance(self):
        return self.balance.find().limit(1).sort([('$natural', -1)]).next()

    # sets new balance in DB as float
    def setNewBalance(self, new_stock, new_cash):
        last_entry = self.getLatestBalance().next()
        last_time = last_entry['time']
        self.balance.insert_one({'time': last_time + 1, 'stock': new_stock, 'cash': new_cash})

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

    def initDatabases(self,company_dict):
        self.setPortfolio(company_dict)
        self.balance.delete_many({})
        self.balance.insert_one({'time': 0, 'balance': 0, 'cash': 0})

    # processes new balance AND updates portfolio DB
    def processBalance(self):
        print("updating balance")
        old_portfolio = self.getPortfolio()
        new_50 = get_new_50()
        new_portfolio = get_price_dict(new_50)
        old_total = 0.0
        new_total = 0.0
        new_total = sum(list(new_portfolio.values()))
        for ticker in old_portfolio:
            old_total += get_price(ticker)
        # for ticker in new_50:
        #     new_total += get_price(ticker)
        latest_balance_entry = self.getLatestBalance().next()
        latest_balance = latest_balance_entry['balance'] - old_total + new_total
        latest_cash = latest_balance_entry['cash']
        print("new balance: ", latest_balance)
        print("new cash: ", latest_cash)
        self.setNewBalance(latest_balance, latest_cash)
        self.setPortfolio(new_portfolio)




if __name__ == "__main__":
    # setting up mongo DB
    mongo = Mongo()
    port = mongo.getPortfolio()
    example_lst = ['ABMD', 'ABBV', 'ATVI', 'AMD', 'ACN']
    example_dict = {'ABMD': 1, 'ABBV': 10, 'ACN': 100}
    example_dict2 = {'ABMD': 2, 'ABBV': 10, 'ACN': 100}
    print("Current port:\n", port)
    # new_50 = get_new_50()
    # print(new_50)
    # new_portfolio = get_price_dict(example_lst)
    # mongo.initDatabases(example_dict)
    mongo.processBalance()
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
