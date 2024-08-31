from .bank import Bank
from .admin import Admin


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
