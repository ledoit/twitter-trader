import pymongo
import json

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.gn2iv.mongodb.net/twitter_trader?retryWrites=true&w=majority")
        self.db = self.client.twitter_trader
        self.portfolio = self.db.portfolio
        self.profits = self.db.profits
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
    def updatePortfolio(self,portfolio_lst):
        self.portfolio.delete_many({})
        lst = []
        for co in portfolio_lst:
            doc = {"company": co, "price": co}
            lst.append(doc)
        self.portfolio.insert_many(lst)

    # takes in current profit and adds to DB
    def updateProfits(self,net_profit):
        pass



if __name__ == "__main__":
    mongo = Mongo()
    port = mongo.getPortfolio()
    example_dict = {"apple":100,"pear":200,"potato":50,"pineapple":99}
    print("Current port:\n", port)
    mongo.updatePortfolio(example_dict) 
    print("\n\nNew port:", mongo.getPortfolio())

    