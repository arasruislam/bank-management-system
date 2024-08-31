from .user import User


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
