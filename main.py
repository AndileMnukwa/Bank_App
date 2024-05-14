import tkinter as tk
from tkinter import messagebox
import random
import string

class BankingApplication:
    pass  # Placeholder for the Banking Application class

class BankingGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Banking Application")
        self.master.geometry("800x600")  # Set the size of the main window
        self.banking_app = BankingApplication()  # Create an instance of BankingApplication
        self.master.configure(bg='#3498db')

        # Create a LabelFrame for better organization
        self.label_frame = tk.LabelFrame(self.master, text="Welcome to Binary Brains \n "" \n Bank App", font=('broadway', 20, 'bold'), padx=70, pady=70)
        self.label_frame.pack(padx=70, pady=70)

        # Create widgets inside the LabelFrame
        self.label = tk.Label(self.label_frame, text="Select an option:", font=('broadway', 12))
        self.label.pack(pady=10)

        self.register_button = tk.Button(self.label_frame, text="Register", command=self.register, width=20)
        self.register_button.pack(pady=10)
        self.register_button.configure(bg='light blue')

        self.login_button = tk.Button(self.label_frame, text="Login", command=self.login, width=20)
        self.login_button.pack(pady=10)
        self.login_button.configure(bg='light blue')

        self.forgot_password_button = tk.Button(self.label_frame, text="Forgot Password", command=self.forgot_password, width=20)
        self.forgot_password_button.pack(pady=10)
        self.forgot_password_button.configure(bg='light blue')

        self.exit_button = tk.Button(self.label_frame, text="Exit", command=self.master.destroy, width=20)
        self.exit_button.pack(pady=10)
        self.exit_button.configure(bg='light blue')

    def register(self):
        self.master.withdraw()  # Hide the main window
        register_window = tk.Toplevel(self.master)
        register_window.title("Register")
        register_window.geometry("500x400")  # Set the size of the register window
        register_window.configure(bg='light blue')  # Corrected the method name

        # Username
        username_label = tk.Label(register_window, text="Enter a username:", font=("Arial", 12))
        username_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.username_entry = tk.Entry(register_window, font=("Arial", 10))
        self.username_entry.pack(pady=10)  # Added padding in the y-direction for spacing

        # PIN
        pin_label = tk.Label(register_window, text="Enter a 4-digit bank PIN:", font=("Arial", 12))
        pin_label.pack(pady=10)  # Added padding in the y-direction for spacing

        self.pin_entry = tk.Entry(register_window, show="*", font=("Arial", 10))
        self.pin_entry.pack(pady=10)  # Added padding in the y-direction for spacing
        register_button = tk.Button(register_window, text="Register", command=self.register, width=15)
        register_button.pack(pady=10)

    def login(self):
        pass  # Placeholder for the login method

    def forgot_password(self):
        pass  # Placeholder for the forgot_password method

def main():
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
