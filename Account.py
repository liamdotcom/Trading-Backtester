class Account:
    def __init__(self):
        self.money = 1000
        self.profit = 0

    def buy_shares(self, price):
        bid = self.money * 0.05
        self.money = self.money - bid
        num_shares = bid / price
        print("\nBought: " + str(num_shares) + " shares\nat " + str(price) + " per share+\n"
                                                                             "Account Balance: " + str(self.money))
        self.profit = self.profit - bid

    def sell_shares(self, price, shares):
        if self.shares > 0:
            ask = shares * price
            self.money = self.money + ask
            self.profit = self.profit + ask
            print("\nSold: "+str(shares)+" shares\nat "+str(price)+" per share")
            print("Profit/Loss:"+str(self.profit)+"\nAccount Balance: "+str(self.money))
