class Account():
    def __init__(self,name,balance=0):
        self.owner = name
        self.balance = balance
    def __str__(self):
        return f"{self.owner} has {self.balance} amount"
    def deposit(self,amount):
        self.balance+=amount
        print("Current available balalnce is {}".format(self.balance))
    def withdraw(self,amount):
        if amount>self.balance:
            print("You don't have enough amount to withdraw")
        else:
            self.balance-=amount
            print(f"Your current balance is {self.balance}")
acct1 = Account('Jose',100)
print(acct1)
print(acct1.owner)
print(acct1.balance)
acct1.deposit(50)
acct1.withdraw(75)
acct1.withdraw(500)
