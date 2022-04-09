import pymongo

class Mongo:
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://user:user@cluster0.gn2iv.mongodb.net/twitter_trader?retryWrites=true&w=majority")
        self.db = self.client.twitter_trader
        self.portfolio = self.db.portfolio
        self.profits = self.db.profits
        print(self.db.command("serverStatus"))

# returns portfolio from DB as dict
def getPortfolio():
    pass
# takes in dict of new portfolio and returns JSON
def JSONifyPortfolio(portfolio_dict):
    pass
# takes in dict of new portfolio and returns tuple of what to buy and sell
def getTrades(portfolio_dict):
    pass
# takes in JSON of new portfolio and updates DB
def updatePortfolio(portfolio_json):
    pass
# takes in current profit and adds to DB
def updateProfits(net_profit):
    pass



if __name__ == "__main__":
    mongo = Mongo()
    print(mongo.portfolio.insert_one({
        "company": "$APL",
        "price": "1002"
        }))