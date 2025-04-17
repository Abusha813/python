from tkinter import *
from tkinter import messagebox
import sqlite3

class LoginScreen:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Pharmacy Management System Login")
        self.root.geometry("400x300")

        self.login_screen()

    def login_screen(self):
        self.login_frame = Frame(self.root, bg='indigo')
        self.login_frame.pack(fill=BOTH, expand=True)

        title_label = Label(self.login_frame, text="Login to Pharmacy Management System", font=("Arial", 16, "bold"), bg='lightblue', fg='darkblue')
        title_label.pack(pady=20)

        self.username_label = Label(self.login_frame, text="Username:", font=("Arial", 12, "bold"), fg="darkblue", bg="lightblue")
        self.username_label.pack(pady=10)
        self.username_entry = Entry(self.login_frame, font=("Arial", 12))
        self.username_entry.pack(pady=10)

        self.password_label = Label(self.login_frame, text="Password:", font=("Arial", 12, "bold"), fg="darkblue", bg="lightblue")
        self.password_label.pack(pady=10)
        self.password_entry = Entry(self.login_frame, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=10)

        self.login_button = Button(self.login_frame, text="Login", font=("Arial", 12, "bold"), bg="#4CAF50", fg='white', command=self.check_login)
        self.login_button.pack(pady=20)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "a" and password == "a":
            self.login_frame.destroy()  # Destroy login screen
            self.on_login_success()  # Proceed to the main application
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")
