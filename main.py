class User:
    def __init__(self, name, email, address, account_type, account_number):
        self.name = name
        self.email = email
        self.address = address
        self.account_type = account_type
        self.account_number = account_number

        self.balance = 0
        self.transaction_history = []
        self.loan_count = 0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.transaction_history.append(f"Deposited: ${amount}")
            print(f"${amount} deposit done. Current balance: ${self.balance}")
        else:
            print("Deposit amount must be greater than 0.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Withdrawal amount exceeded.")
        elif amount <= 0:
            print("Withdrawal amount must be greater than 0.")
        else:
            self.balance -= amount
            self.transaction_history.append(f"Withdrawn: ${amount}")
            print(f"${amount} withdrawn successfully. Current balance: ${self.balance}")

    def check_balance(self):
        print(f"Current Balance: ${self.balance}")

    def show_transaction_history(self):
        print("Transaction History:")
        if not self.transaction_history:
            print("No transactions yet.")
        else:
            for transaction in self.transaction_history:
                print(transaction)

    def take_loan(self, amount, bank):
        if self.loan_count >= 2:
            print("Loan limit exceeded!")
            return
        if bank.loan_feature_off:
            print("Currently, the loan system is disabled.")
            return

        self.balance += amount
        self.loan_count += 1
        self.transaction_history.append(f"Loan Taken: ${amount}")
        bank.total_loans += amount
        print(f"${amount} loan received. Current balance: ${self.balance}")

    def transfer(self, amount, to_account, bank):
        if amount > self.balance:
            print("Transfer amount exceeded current balance.")
            return

        recipient = bank.get_user_by_account_number(int(to_account))
        if not recipient:
            print("Account does not exist!")
            return

        if amount <= 0:
            print("Transfer amount must be greater than 0.")
            return

        self.balance -= amount
        recipient.balance += amount
        self.transaction_history.append(f"Transferred: ${amount} to {to_account}")
        recipient.transaction_history.append(f"Received: ${amount} from {self.account_number}")

        print(f"${amount} transferred to {to_account}. Current balance: ${self.balance}")


class Bank:
    def __init__(self):
        self.users = {}
        self.total_loans = 0
        self.loan_feature_off = False
        self.next_account_number = 1000

    def create_user_account(self, name, email, address, account_type):
        account_number = self.generate_account_number()
        user = User(name, email, address, account_type, account_number)
        self.users[account_number] = user
        print(f"Account created successfully. Account Number: {user.account_number}")

    def generate_account_number(self):
        account_number = self.next_account_number
        self.next_account_number += 1
        return account_number

    def get_user_by_account_number(self, account_number):
        return self.users.get(account_number)

    def total_balance(self):
        return sum(user.balance for user in self.users.values())


class Admin:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def create_account(self, bank, name, email, address, account_type):
        bank.create_user_account(name, email, address, account_type)

    def delete_account(self, bank, account_number):
        account_number = int(account_number)
        if account_number in bank.users:
            del bank.users[account_number]
            print(f"Account {account_number} deleted successfully.")
        else:
            print("Account not found.")

    def view_all_accounts(self, bank):
        print("All Users List:")
        if not bank.users:
            print("No accounts available.")
        else:
            for acc_num, user in bank.users.items():
                print(
                    f"Account Number: {acc_num}, Name: {user.name}, Email: {user.email}, Balance: ${user.balance}"
                )

    def check_total_balance(self, bank):
        print(f"Total bank balance: ${bank.total_balance()}")

    def check_total_loans(self, bank):
        print(f"Total loans: ${bank.total_loans}")

    def toggle_loan_feature(self, bank):
        bank.loan_feature_off = not bank.loan_feature_off
        status = "off" if bank.loan_feature_off else "on"
        print(f"Loan feature is now {status}.")


def main():
    bank = Bank()
    admin = Admin("Admin", "arasru01@gmail.com")

    while True:
        print("\n--- Bank Management System ---")
        print("1. User Login")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Please select your option: ")

        if choice == "1":
            try:
                account_number = int(input("Enter your account number: "))
                user = bank.get_user_by_account_number(account_number)

                if user:
                    while True:
                        print(f"\n--- {user.name}'s Menu ---")
                        print("1. Deposit")
                        print("2. Withdraw")
                        print("3. Check Balance")
                        print("4. View Transaction History")
                        print("5. Take a Loan")
                        print("6. Transfer")
                        print("7. Logout")
                        user_choice = input("Please select your option: ")

                        if user_choice == "1":
                            amount = float(input("Enter the amount to deposit: "))
                            user.deposit(amount)
                        elif user_choice == "2":
                            amount = float(input("Enter the amount to withdraw: "))
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
                            print("Logged out successfully.")
                            break
                        else:
                            print("Invalid choice. Please try again.")
                else:
                    print("Account not found.")

            except ValueError:
                print("Invalid account number format.")

        elif choice == "2":
            admin_email = input("Enter admin email: ")
            if admin_email == admin.email:
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Create User Account")
                    print("2. Delete User Account")
                    print("3. View All User Accounts")
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
                        admin.check_total_loans(bank
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
