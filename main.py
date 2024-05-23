import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
from datetime import datetime
import random
import string
import csv
import hashlib
import os

class BankingApplication:
    def __init__(self):
        self.current_user = None
        self.current_balance = 4
        self.user_file = 'users.csv'
        self.create_user_file()

    def create_user_file(self):
        # Create the users CSV file if it doesn't exist
        if not os.path.exists(self.user_file):
            with open(self.user_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'username', 'bank_pin', 'password', 'balance'])

    def generate_password(self):
        password_length = 4
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(password_length))

    def hash_password(self, password):
        # Hash the password using a secure hashing algorithm like SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username, bank_pin, password):
        user_id = self.generate_user_id()
        with open(self.user_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_id, username, bank_pin, password, 0.0])

    def generate_user_id(self):
        with open(self.user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
            if len(data) == 1:  # Only header row present
                return 1
            else:
                return int(data[-1][0]) + 1

    def login(self, username, bank_pin, password):
        with open(self.user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username and row[2] == bank_pin and row[3] == password:
                    self.current_user = username
                    self.current_balance = float(row[4])
                    return True
            return False

    def check_balance(self):
        with open(self.user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == self.current_user:
                    self.current_balance = float(row[4])
                    break

    def update_user_balance(self, new_balance):
        rows = []
        with open(self.user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == self.current_user:
                    row[4] = new_balance
                rows.append(row)
        with open(self.user_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def deposit(self, amount):
        self.check_balance()  # Update current balance from CSV
        new_balance = self.current_balance + amount
        self.update_user_balance(new_balance)
        self.current_balance = new_balance

    def withdraw(self, amount):
        self.check_balance()  # Update current balance from CSV
        if self.current_balance >= amount:
            new_balance = self.current_balance - amount
            self.update_user_balance(new_balance)
            self.current_balance = new_balance

    def record_transaction(self, transaction_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open('TransactionLog.txt', 'a') as file:
            file.write(f"{timestamp} - {self.current_user} - {transaction_type} - Amount: R{amount}\n")

    def update_password(self, username, new_password):
        rows = []
        with open(self.user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username:
                    row[3] = new_password
                rows.append(row)
        with open(self.user_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def forgot_password(self, username):
        with open(self.user_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == username:
                    return row[3]
            return None


class BankingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking Application")
        self.master.geometry("800x600")  # Set the size of the main window
        self.banking_app = BankingApplication()
        self.master.configure(bg='black')

        self.logo_image = tk.PhotoImage(file="logo.png")  # Change "logo.png" to your image file

        # Create widgets inside the main window
        self.label = tk.Label(self.master, text="Binary Finance", font=('Helvetica', 20, 'bold'), bg='black', fg='gold')
        self.label.pack(pady=20)

        # Display the logo
        self.logo_label = tk.Label(self.master, image=self.logo_image, bg='black')
        self.logo_label.pack()

        self.register_button = tk.Button(self.master, text="Register", command=self.register, width=20, bg='gold', fg='black')
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.master, text="Login", command=self.login, width=20, bg='gold', fg='black')
        self.login_button.pack(pady=10)

        self.forgot_password_button = tk.Button(self.master, text="Forget Password", command=self.forgot_password, width=20, bg='gold', fg='black')
        self.forgot_password_button.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, width=20, bg='gold', fg='black')
        self.exit_button.pack(pady=10)

    def register(self):
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("500x400")  # Set the size of the register window
        register_window.configure(bg='black') # Corrected the method name

        self.logo_label = tk.Label(register_window, image=self.logo_image, bg='black')
        self.logo_label.pack()

        # Username
        username_label = tk.Label(register_window, text="Enter a username:", font=("Arial", 12), fg='gold', bg='black')
        username_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.username_entry = tk.Entry(register_window, font=("Arial", 10))
        self.username_entry.pack(pady=10)  # Added padding in the y-direction for spacing

        # PIN
        pin_label = tk.Label(register_window, text="Enter a 4-digit bank PIN:", font=("Arial", 12), fg='gold', bg='black')
        pin_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.pin_entry = tk.Entry(register_window, show="*", font=("Arial", 10))
        self.pin_entry.pack(pady=10)  # Added padding in the y-direction for spacing
        register_button = tk.Button(register_window, text="Register", command=self.perform_registration, width=15, bg='gold', fg='black')
        register_button.pack(pady=10)

    def perform_registration(self):
        username = self.username_entry.get()
        bank_pin = self.pin_entry.get()

        if not bank_pin.isdigit() or len(bank_pin) != 4:
            messagebox.showerror("Registration Error", "Invalid PIN. Please enter a 4-digit number.")
            return

        if not username:
            messagebox.showerror("Registration Error", "Please enter a username.")
            return

        password = self.banking_app.generate_password()
        self.banking_app.register(username, bank_pin, password)
        messagebox.showinfo("Registration", f"Registration successful!\nYour password is: {password}")
        self.master.deiconify()  # Show main window

    def login(self):
        self.master.withdraw()  # Hide main window
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.geometry("500x400")  # Set the size of the login window
        login_window.configure(bg='black')

        # Display the logo
        self.logo_label = tk.Label(login_window, image=self.logo_image, bg='black')
        self.logo_label.pack(pady=10)

        username_label = tk.Label(login_window, text="Username:", font=("Arial", 10), fg='gold', bg='black')
        username_label.pack(pady=10)

        self.username_entry = tk.Entry(login_window, font=("Arial", 12))
        self.username_entry.pack(pady=10)

        pin_label = tk.Label(login_window, text="Bank PIN:", font=("Arial", 10), fg='gold', bg='black')
        pin_label.pack(pady=10)

        self.pin_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
        self.pin_entry.pack(pady=10)

        password_label = tk.Label(login_window, text="Password:", font=("Arial", 10), fg='gold', bg='black')
        password_label.pack(pady=10)

        self.password_entry = tk.Entry(login_window, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=10)

        login_button = tk.Button(login_window, text="Login", command=self.perform_login, width=15, bg='gold', fg='black')
        login_button.pack(pady=10)

    def perform_login(self):
        username = self.username_entry.get()
        bank_pin = self.pin_entry.get()
        password = self.password_entry.get()
        if self.banking_app.login(username, bank_pin, password):
            messagebox.showinfo("Login", "Login successful!")
            self.show_transaction_options()
        else:
            messagebox.showerror("Login Error", "Invalid username, bank pin, or password.")
            self.master.deiconify()  # Show main window

    def show_transaction_options(self):
        self.master.withdraw()  # Hide main window
        transaction_window = tk.Toplevel(self.master)
        transaction_window.title("Transactions")
        transaction_window.geometry("500x400")  # Set the size of the transaction window
        transaction_window.configure(bg='black')

        # Display the logo
        self.logo_label = tk.Label(transaction_window, image=self.logo_image, bg='black')
        self.logo_label.pack()

        # Display balance label
        self.balance_label = tk.Label(transaction_window, text="", bg='black', fg='gold', font=("Helvetica", 15))
        self.balance_label.pack(pady=10)

        make_transaction = messagebox.askyesno("Transaction", "Would you like to make a transaction?")
        if make_transaction:
            transaction_type = messagebox.askyesno("Transaction Type", "Would you like to make a deposit/withdraw?")
            if transaction_type:
                self.display_transaction_buttons(transaction_window)
            else:
                self.display_transaction_buttons(transaction_window)



        # Add download transaction log button
        download_button = tk.Button(transaction_window, text="Download Transaction Log", command=self.download_transaction_log, width=20, bg='gold', fg='black')
        download_button.pack(pady=10)

        # Update the balance label with the current balance
        self.update_balance_label()

        exit_button = tk.Button(transaction_window, text="Exit", command=self.master.destroy, width=10)
        exit_button.pack(pady=10)
        exit_button.configure(bg='gold')

    def display_transaction_buttons(self, transaction_window):
        deposit_button = tk.Button(transaction_window, text="Deposit", command=self.open_deposit_window, width=10, fg='black')
        deposit_button.pack(pady=10)
        deposit_button.configure(bg='gold')

        withdraw_button = tk.Button(transaction_window, text="Withdraw", command=self.open_withdraw_window, width=10, fg='black')
        withdraw_button.pack(pady=10)
        withdraw_button.configure(bg='gold')

    def update_balance_label(self):
        self.banking_app.check_balance()
        self.balance_label.config(text=f"Your current balance is: R{self.banking_app.current_balance}")

    def check_balance(self):
        self.banking_app.check_balance()
        messagebox.showinfo("Balance", f"Your current balance is: R{self.banking_app.current_balance}")
        self.update_balance_label()

    def open_deposit_window(self):
        deposit_window = tk.Toplevel(self.master)
        deposit_window.title("Deposit")
        deposit_window.geometry("500x400")  # Set the size of the transaction window
        deposit_window.configure(bg='black')

        self.logo_label = tk.Label(deposit_window, image=self.logo_image, bg='black')
        self.logo_label.pack()

        # Display balance label
        self.balance_label = tk.Label(deposit_window, text="", bg='black', fg='gold', font=("Helvetica", 15))
        self.balance_label.pack(pady=10)

        # Create labels with font
        amount_label = tk.Label(deposit_window, text="How much would you like to deposit? R", font=("Helvetica", 12),
                                fg='gold', bg='black')
        amount_label.pack(pady=10)

        # Create an entry for the user to input the amount
        amount_entry = tk.Entry(deposit_window, font=("Arial", 12))
        amount_entry.pack(pady=10)

        # Create a button to submit the deposit
        deposit_button = tk.Button(deposit_window, text="Deposit", command=lambda: self.perform_deposit(amount_entry),
                                   width=15)
        deposit_button.pack(pady=10)
        deposit_button.configure(bg='gold')

        # Add download transaction log button
        download_button = tk.Button(deposit_window, text="Download Transaction Log",
                                    command=self.download_transaction_log, width=20, bg='gold', fg='black')
        download_button.pack(pady=10)

        # Update the balance label with the current balance
        self.update_balance_label()

    def perform_deposit(self, amount_entry):
        amount_str = amount_entry.get()
        try:
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Invalid deposit amount.")
                return

            self.banking_app.deposit(amount)
            self.banking_app.record_transaction("Deposit", amount)
            self.check_balance()
            messagebox.showinfo("Deposit", f"Deposited R{amount}. Current Balance: R{self.banking_app.current_balance}")

            # Clear the deposit text box after successful deposit
            amount_entry.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def open_withdraw_window(self):
        withdraw_window = tk.Toplevel(self.master)
        withdraw_window.title("Withdraw")
        withdraw_window.geometry("500x400")  # Set the size of the transaction window
        withdraw_window.configure(bg='black')

        # Display the logo
        self.logo_label = tk.Label(withdraw_window, image=self.logo_image, bg='black')
        self.logo_label.pack()

        # Display balance label
        self.balance_label = tk.Label(withdraw_window, text="", bg='black', fg='gold', font=("Helvetica", 15))
        self.balance_label.pack(pady=10)

        # Create labels with font
        amount_label = tk.Label(withdraw_window, text="How much would you like to withdraw? R", font=("Helvetica", 12), fg='gold', bg='black')
        amount_label.pack(pady=10)

        # Create an entry for the user to input the amount
        amount_entry = tk.Entry(withdraw_window, font=("Arial", 12))
        amount_entry.pack(pady=10)

        # Create a button to submit the withdrawal
        withdraw_button = tk.Button(withdraw_window, text="Withdraw", command=lambda: self.perform_withdraw(amount_entry.get()), width=15)
        withdraw_button.pack(pady=10)
        withdraw_button.configure(bg='gold')

        # Add download transaction log button
        download_button = tk.Button(withdraw_window, text="Download Transaction Log", command=self.download_transaction_log, width=20, bg='gold', fg='black')
        download_button.pack(pady=10)

        # Update the balance label with the current balance
        self.update_balance_label()

    def perform_withdraw(self, amount_str):
        try:
            amount = float(amount_str)
            if amount < 10 or amount % 1 != 0:
                messagebox.showerror("Error", "Invalid withdrawal amount. Please enter a whole number greater than or equal to R10.")
                return

            if amount > self.banking_app.current_balance:
                messagebox.showerror("Error", "Withdrawal amount exceeds the current balance. Please enter another amount.")
                return

            self.banking_app.withdraw(amount)
            self.banking_app.record_transaction("Withdrawal", amount)
            self.check_balance()
            messagebox.showinfo("Withdraw", f"Withdrew R{int(amount)}. Current Balance: R{self.banking_app.current_balance}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def forgot_password(self):
        username = simpledialog.askstring("Forgot Password", "Enter your username:")
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        result = self.banking_app.forgot_password(username)
        if result:
            messagebox.showinfo("Password Reset", f"Your new password is: {result}")
        else:
            messagebox.showerror("Error", "Username not found.")

    def download_transaction_log(self):
        log_file = 'TransactionLog.txt'
        if os.path.exists(log_file):
            with open(log_file, 'r') as file:
                log_content = file.read()
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
            if save_path:
                with open(save_path, 'w') as file:
                    file.write(log_content)
                messagebox.showinfo("Download", "Transaction log downloaded successfully!")
        else:
            messagebox.showerror("Error", "Transaction log file not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()
