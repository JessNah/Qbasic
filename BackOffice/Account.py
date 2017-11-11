

class Account:

    def __init__(self, num, balance, name):
        self.accountName = name
        self.accountNum = num
        self.balance = balance

    def getAccountNum(self):
        return self.accountNum

    def getAccountName(self):
        return self.accountName

    def getAccountBalance(self):
        return self.balance
