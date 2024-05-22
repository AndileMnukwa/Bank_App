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
        self.current_balance = 0.0
        self.user_file = 'users.csv'
        self.create_user_file()

    def create_user_file(self):
        if not os.path.exists(self.user_file):
            with open(self.user_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'username', 'bank_pin', 'password', 'balance'])

    def generate_password(self):
        password_length = 4
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(password_length))

    def hash_password(self, password):
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
            if len(data) == 1:
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
        self.check_balance()
        new_balance = self.current_balance + amount
        self.update_user_balance(new_balance)
        self.current_balance = new_balance

    def withdraw(self, amount):
        self.check_balance()
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
        self.master.geometry("800x600")
        self.banking_app = BankingApplication()
        self.master.configure(bg='black')

        self.logo_image = tk.PhotoImage(file="logo.png")

        self.label = tk.Label(self.master, text="Binary Finance", font=('Helvetica', 20, 'bold'), bg='black', fg='gold')
        self.label.pack(pady=20)

        self.logo_label = tk.Label(self.master, image=self.logo_image, bg='black')
        self.logo_label.pack()

        self.register_button = tk.Button(self.master, text="Register", command=self.register, width=20, bg='gold', fg='black')
        self.register_button.pack(pady=10)

        self.login_button = tk.Button(self.master, text="Login", command=self.login, width=20, bg='gold', fg='black')
        self.login_button.pack(pady=10)

        self.forget_password_button = tk.Button(self.master, text="Forget Password", command=self.forgot_password, width=20, bg='gold', fg='black')
        self.forget_password_button.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.master.destroy, width=20, bg='gold', fg='black')
        self.exit_button.pack(pady=10)

    def register(self):
        self.master.withdraw()
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("500x400")
        register_window.configure(bg='black')

        self.logo_label = tk.Label(register_window, image=self.logo_image, bg='black')
        self.logo_label.pack()

        username_label = tk.Label(register_window, text="Enter a username:", font=("Arial", 12), fg='gold', bg='black')
        username_label.pack(pady=10)

        self.username_entry = tk.Entry(register_window, font=("Arial", 10))
        self.username_entry.pack(pady=10)

        pin_label = tk.Label(register_window, text="Enter a 4-digit bank PIN:", font=("Arial", 12), fg='gold', bg='black')
        pin_label.pack(pady=10)

        self.pin_entry = tk.Entry(register_window, show="*", font=("Arial", 10))
        self.pin_entry.pack(pady=10)
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
        self.master.deiconify()

    def login(self):
        self.master.withdraw()
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        login_window.geometry("500x400")
        login_window.configure(bg='black')

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
            self.ask_for_transaction()
        else:
            messagebox.showerror("Login Error", "Invalid credentials. Please try again.")

    def ask_for_transaction(self):
        response = messagebox.askyesno("Transaction", "Would you like to perform a transaction?")
        if response:
            self.main_menu()
        else:
            self.check_balance()

    def main_menu(self):
        main_menu_window = tk.Toplevel(self.master)
        main_menu_window.title("Main Menu")
        main_menu_window.geometry("500x400")
        main_menu_window.configure(bg='black')

        self.banking_app.check_balance()

        balance_label = tk.Label(main_menu_window, text=f"Balance: R{self.banking_app.current_balance}", font=('Helvetica', 14), bg='black', fg='gold')
        balance_label.pack(pady=10)

        deposit_button = tk.Button(main_menu_window, text="Deposit", command=self.deposit, width=20, bg='gold', fg='black')
        deposit_button.pack(pady=10)

        withdraw_button = tk.Button(main_menu_window, text="Withdraw", command=self.withdraw, width=20, bg='gold', fg='black')
        withdraw_button.pack(pady=10)

        change_password_button = tk.Button(main_menu_window, text="Change Password", command=self.change_password, width=20, bg='gold', fg='black')
        change_password_button.pack(pady=10)

        download_button = tk.Button(main_menu_window, text="Download Transaction History", command=self.download_transaction_history, width=20, bg='gold', fg='black')
        download_button.pack(pady=10)

        exit_button = tk.Button(main_menu_window, text="Logout", command=main_menu_window.destroy, width=20, bg='gold', fg='black')
        exit_button.pack(pady=10)

    def check_balance(self):
        balance = self.banking_app.current_balance
        messagebox.showinfo("Balance", f"Your current balance is: R{balance}")

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter the amount to deposit:")
        if amount is not None:
            self.banking_app.deposit(amount)
            self.banking_app.record_transaction("Deposit", amount)
            messagebox.showinfo("Deposit", f"Successfully deposited R{amount}")

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter the amount to withdraw:")
        if amount is not None:
            if amount <= self.banking_app.current_balance:
                self.banking_app.withdraw(amount)
                self.banking_app.record_transaction("Withdraw", amount)
                messagebox.showinfo("Withdraw", f"Successfully withdrew R{amount}")
            else:
                messagebox.showerror("Withdraw Error", "Insufficient balance.")

    def change_password(self):
        new_password = simpledialog.askstring("Change Password", "Enter a new password:", show="*")
        if new_password:
            username = self.banking_app.current_user
            self.banking_app.update_password(username, new_password)
            messagebox.showinfo("Change Password", "Password updated successfully.")

    def forgot_password(self):
        username = simpledialog.askstring("Forgot Password", "Enter your username:")
        if username:
            password = self.banking_app.forgot_password(username)
            if password:
                messagebox.showinfo("Forgot Password", f"Your password is: {password}")
            else:
                messagebox.showerror("Error", "Username not found.")

    def download_transaction_history(self):
        log_file_path = 'TransactionLog.txt'
        if not os.path.exists(log_file_path):
            messagebox.showerror("Error", "No transaction history found.")
            return
        
        download_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                                     filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if download_path:
            try:
                with open(log_file_path, 'r') as src, open(download_path, 'w') as dst:
                    dst.write(src.read())
                messagebox.showinfo("Download", "Transaction history downloaded successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download transaction history: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()