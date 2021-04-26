class Account:    
    def __init__(self, amount):
        self.balance = amount

    def setBalance(self, amount):
        self.balance = amount    

    def currentBalance(self):
        return self.balance

    def deposit(self, amount):
        self.balance = self.balance + amount

    def withdraw(self, amount):
        self.balance = self.balance - amount
        if(self.balance < 0):
            self.balance = 0