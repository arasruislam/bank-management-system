class User:
    def __init__(self, name, email, address, account_type, account_number):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = account_number

        self.balance = 0
        self.transaction_history = []
        self.load_count = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: {amount}")
            print(f"${amount} deposit done. Current balance: ${self.balance}")
        else:
            print("deposit amount must be grater then 0")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        elif amount <= 0:
            print("Withdrawal failed")
        else:
            self.balance -= amount
            self.transaction_history.append(f"withdrawn: ${amount}")

    def check_balance(self):
        print(f"Current Balance: ${self.balance}")

    def show_transaction_history(self):
        print("Transaction History: ")
        for transaction in self.transaction_history:
            print(transaction)

    def take_loan(self, amount, bank):
        if self.load_count >= 2:
            print("load limit cross already!")
            return
        if bank.load_feature_off:
            print("currently loan system off")
            return

        self.balance += amount
        self.load_count +=1
        self.transaction_history.append(f"Load Take: ${amount}")
        bank.total_loan += amount
        print(f"${amount} loan received. Current balance ${self.balance}")

    def transfer(self, amount, to_account, bank):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
            return
        recipient = bank.get_user_by_account_number(to_account)
        if not recipient:
            print("Account does not exist!")
            return
        if amount <=0:
            print("transfer amount is less then zero.")
            return
        self.balance -= amount
        recipient.balance += amount
        self.transaction_history.append(f"Transferred: ${amount} to {to_account}")
        recipient.transaction_history.append(
            f"Received: ${amount} from {self.account_number}"
        )
        
        print(f"${amount} transfer done to {to_account}. Current balance: ${self.balance}")
