import pymongo
import json
from twitter import get_new_50
from prices import get_price

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.gn2iv.mongodb.net/twitter_trader?retryWrites=true&w=majority")
        self.db = self.client.twitter_trader
        self.portfolio = self.db.portfolio
        self.balance = self.db.balance
        # print(self.db.command("serverStatus"))

    # returns portfolio from DB as lst
    def getPortfolio(self):
        cursor = self.portfolio.find()
        return list(cursor)
        
    # takes in dict of new portfolio and returns JSON
    def JSONifyPortfolio(self,portfolio_dict):
        json.dumps(portfolio_dict)
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
    def setPortfolio(self,portfolio_lst):
        self.portfolio.delete_many({})
        lst = []
        for co in portfolio_lst:
            doc = {"company": co, "price": co}
            lst.append(doc)
        self.portfolio.insert_many(lst)

    # sets balance in DB as float
    def setBalance(self,new_balance):  # not sponsored
        last_entry = self.getLatestProfit().next()
        last_time = last_entry['time']
        last_profit = last_entry['profit']
        self.profits.insert_one({'time': last_time + 1, 'profit': 0})
        return last_profit + new_balance

    # returns portfolio from DB as lst
    def getBalance(self):
        return self.balance.find()


if __name__ == "__main__":
    mongo = Mongo()
    port = mongo.getPortfolio()
    example_lst = ["apple","pear","potato","pineapple"]
    print("Current port:\n", port)
    mongo.setPortfolio(example_lst)
    print("\n\nNew port:", mongo.getPortfolio())

    