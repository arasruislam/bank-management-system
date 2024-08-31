from .user import User

class Bank:
    def __init__(self):
        self.users = {}
        self.total_loans = 0
        self.loan_feature_off = False
        self.next_account_number = 1000
        
    def create_user_account(self, name, email, address, account_type):
        account_number = self.generate_account_number()
        user = User(name, email, address, account_type, account_number)
        self.users[account_number]=user
        print(f"account created done. Account Number: {user.account_number}")
        
    def generate_account_number(self):
        account_number = self.next_account_number
        self.next_account_number +=1
        return account_number
    
    def get_user_by_account_number(self, account_number):
        return self.users.get(account_number, None)
    
    def total_balance(self):
        return sum(user.balance for user in self.users.values())
    
