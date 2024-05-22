import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import filedialog
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

    def __init__(self):
        self.current_balance = 0.0

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

        self.login_button = tk.Button(self.master, text="Forget Password", command=self.forgot_password, width=20, bg='gold', fg='black')
        self.login_button.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, width=20, bg='gold',fg='black')
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
        register_button = tk.Button(register_window, text="Register", command=self.perform_registration, width=15, bg='gold',
                                 fg='black')
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
            messagebox.showerror("Login Error", "Invalid username, PIN, or password.")
            self.master.deiconify()  # Show main window

    def forgot_password(self):
        self.master.withdraw()  # Hide main window
        forgot_password_window = tk.Toplevel(self.master)
        forgot_password_window.title("Forgot Password")
        forgot_password_window.geometry("500x400")  # Set the size of the forgot password window
        forgot_password_window.configure(bg='black')

        self.logo_label = tk.Label(forgot_password_window, image=self.logo_image, bg='black')
        self.logo_label.pack()

        username_label = tk.Label(forgot_password_window, text="Enter your username:", font=("Arial", 12), fg='gold', bg='black')
        username_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.username_entry = tk.Entry(forgot_password_window, font=("Arial", 12))
        self.username_entry.pack(pady=10)  # Added padding in the y-direction for spacing

        submit_button = tk.Button(forgot_password_window, text="Submit", command=self.perform_forgot_password, width=15, bg='gold', fg='black')
        submit_button.pack(pady=10)

    def perform_forgot_password(self):
        username = self.username_entry.get()
        password = self.banking_app.forgot_password(username)
        if password:
            messagebox.showinfo("Forgot Password", f"Your password is: {password}")
            self.master.deiconify()  # Show main window
        else:
            messagebox.showerror("Error", "Username not found.")
            self.master.deiconify()  # Show main window

    def show_transaction_options(self):
        self.master.withdraw()  # Hide main window
        transaction_window = tk.Toplevel(self.master)
        transaction_window.title("Transaction Options")
        transaction_window.geometry("500x400")  # Set the size of the transaction options window
        transaction_window.configure(bg='black')

        self.logo_label = tk.Label(transaction_window, image=self.logo_image, bg='black')
        self.logo_label.pack(pady=10)

        balance_button = tk.Button(transaction_window, text="Check Balance", command=self.show_balance, width=20, bg='gold', fg='black')
        balance_button.pack(pady=10)

        deposit_button = tk.Button(transaction_window, text="Deposit", command=self.deposit, width=20, bg='gold', fg='black')
        deposit_button.pack(pady=10)

        withdraw_button = tk.Button(transaction_window, text="Withdraw", command=self.withdraw, width=20, bg='gold', fg='black')
        withdraw_button.pack(pady=10)

        download_button = tk.Button(transaction_window, text="Download Transactions", command=self.download_transactions, width=20, bg='gold', fg='black')
        download_button.pack(pady=10)

        logout_button = tk.Button(transaction_window, text="Logout", command=self.logout, width=20, bg='gold', fg='black')
        logout_button.pack(pady=10)

    def show_balance(self):
        self.banking_app.check_balance()
        messagebox.showinfo("Balance", f"Your current balance is: R{self.banking_app.current_balance:.2f}")

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount and amount > 0:
            self.banking_app.deposit(amount)
            self.banking_app.record_transaction("Deposit", amount)
            messagebox.showinfo("Deposit", f"Deposit successful! Amount: R{amount:.2f}")
        else:
            messagebox.showerror("Deposit Error", "Invalid amount entered.")

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount and amount > 0:
            if self.banking_app.current_balance >= amount:
                self.banking_app.withdraw(amount)
                self.banking_app.record_transaction("Withdraw", amount)
                messagebox.showinfo("Withdraw", f"Withdrawal successful! Amount: R{amount:.2f}")
            else:
                messagebox.showerror("Withdraw Error", "Insufficient balance.")
        else:
            messagebox.showerror("Withdraw Error", "Invalid amount entered.")

    def download_transactions(self):
        transaction_file = 'TransactionLog.txt'
        if os.path.exists(transaction_file):
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if save_path:
                with open(transaction_file, 'r') as file:
                    content = file.readlines()
                user_transactions = [line for line in content if f"- {self.banking_app.current_user} -" in line]
                with open(save_path, 'w') as file:
                    file.writelines(user_transactions)
                messagebox.showinfo("Download", "Transaction log downloaded successfully.")
        else:
            messagebox.showerror("Download Error", "Transaction log file not found.")

    def logout(self):
        self.master.deiconify()  # Show main window

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()