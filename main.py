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
    

class Admin:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def create_account(self, bank, name, email, address, account_type):
        user = User(name, email, address, account_type)
        bank.users[user.account_number] = user
        print(f"Account created done. Account Number: {user.account_number}")

    def delete_account(self, bank, account_number):
        if account_number in bank.users:
            del bank.users[account_number]
            print(f"Account {account_number} delete done")
        else:
            print("Account could not found")

    def view_all_accounts(self, bank):
        print("All users list: ")
        for acc_num, user in bank.users.items():
            print(
                f"Account Number: {acc_num}, Name: {user.name}, Email: {user.email}, Balance: ${user.balance}"
            )

    def check_total_balance(self, bank):
        print(f"Total bank balance: {bank.total_balance()}")

    def check_total_loans(self, bank):
        print(f"Total loan: ${bank.total_loans}")

    def toggle_loan_feature(self, bank):
        bank.loan_feature_off = not bank.loan_feature_off
        status = "off" if bank.loan_feature_off else "on"
        print("Loan feature {status} now")

def main():
    bank = Bank()
    admin = Admin("Admin", "arasru01@gmail.com")

    while True:
        print("\n--- Bank Management System ---")
        print("1. User login")
        print("2. Admin login")
        print("3. Exit")
        choice = input("Please select your option: ")

        if choice == "1":
            account_number = input("Enter your account number: ")
            user = bank.get_user_by_account_number(account_number)

            if user:
                while True:
                    print(f"\n--- {user.name}'s menu ---")
                    print("1. Deposit")
                    print("2. Withdraw")
                    print("3. Check balance")
                    print("4. View Transaction History")
                    print("5. Take a Loan")
                    print("6. Transfer")
                    print("7. Logout")
                    user_choice = input("Please select your option: ")

                    if user_choice == "1":
                        amount = float(input("Enter the amount to deposit: "))
                        user.deposit(amount)
                    elif user_choice == "2":
                        amount = float(input("Enter the amount to withdrawal: "))
                        user.withdraw(amount)
                    elif user_choice == "3":
                        user.check_balance()
                    elif user_choice == "4":
                        user.show_transaction_history()
                    elif user_choice == "5":
                        if not bank.loan_feature_off:
                            amount = float(input("Enter the loan amount: "))
                            user.take_loan(amount, bank)
                        else:
                            print("The loan feature is currently disabled.")
                    elif user_choice == "6":
                        to_account = input("Enter the account number to transfer to: ")
                        amount = float(input("Enter the amount to transfer: "))
                        user.transfer(amount, to_account, bank)
                    elif user_choice == "7":
                        print("Logged out successfully")
                        break
                    else:
                        print("Invalid choice. Please try again")
            else:
                print("Account not found.")

        elif choice == "2":
            admin_email = input("Enter admin email: ")
            if admin_email == admin.email:
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Create User Account")
                    print("2. Delete User Account")
                    print("3. View All User Account")
                    print("4. Check Bank's Total Balance")
                    print("5. Check Total Loan Amount")
                    print("6. Toggle Loan Feature")
                    print("7. Logout")
                    admin_choice = input("Please select your option: ")

                    if admin_choice == "1":
                        name = input("Name: ")
                        email = input("Email: ")
                        address = input("Address: ")
                        account_type = input("Account Type: ")
                        admin.create_account(bank, name, email, address, account_type)
                    elif admin_choice == "2":
                        account_number = input("Enter the account number to delete: ")
                        admin.delete_account(bank, account_number)
                    elif admin_choice == "3":
                        admin.view_all_accounts(bank)
                    elif admin_choice == "4":
                        admin.check_total_balance(bank)
                    elif admin_choice == "5":
                        admin.check_total_loans(bank)
                    elif admin_choice == "6":
                        admin.toggle_loan_feature(bank)
                    elif admin_choice == "7":
                        print("Admin logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Incorrect email of password.")

        elif choice == "3":
            print("Exited successfully.")
            break

        else:
            print("Invalid choice. Please try again.")
