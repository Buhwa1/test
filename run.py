import tkinter as tk
from tkinter import messagebox
import mysql.connector
import bcrypt
import re


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid()
        self.login()

    def login(self):
        """login to account"""
        # Remove the register widgets
        # self.title.grid_forget()
        # self.email_label.grid_forget()
        # self.password_label.grid_forget()
        # self.email_input.grid_forget()
        # self.password_input.grid_forget()
        # self.register_button.grid_forget()
        # self.fname_label.grid_forget()
        # self.lname_label.grid_forget()
        # self.fname_input.grid_forget()
        # self.lname_input.grid_forget()
        self.login_frame = tk.Frame().grid()
        # labels
        title = tk.Label(self.login_frame, text="Log in",
                         font=("Arial", 15, "bold"))
        email_label = tk.Label(self.login_frame, text="Email")
        password_label = tk.Label(self.login_frame, text="Password")

        # textvariable
        current_email = tk.StringVar()
        current_password = tk.StringVar()

        # entries
        email_input = tk.Entry(self.login_frame, width=30, font=(
            "Arial", 10), textvariable=current_email)
        password_input = tk.Entry(self.login_frame,
                                  width=30, show="*", font=("Arial", 10, "bold"), textvariable=current_password)

        # buttons
        login_button = tk.Button(self.login_frame, text="login", command=lambda: self.authenticate(
            current_email.get(), current_password.get()))
        register_button = tk.Button(self.login_frame,
                                    text="Register", command=self.register)

        # positioning
        title.grid(row=0, column=0, columnspan=3)
        email_label.grid(row=1, column=0)
        password_label.grid(row=2, column=0)
        email_input.grid(row=1, column=1, columnspan=2, pady=3)
        password_input.grid(row=2, column=1, columnspan=2, pady=3)
        login_button.grid(row=3, column=1, pady=3)
        register_button.grid(row=3, column=2, pady=3)

    def register(self):
        """create an account"""
        # Remove the login widgets
        # self.title.grid_forget()
        # self.email_label.grid_forget()
        # self.password_label.grid_forget()
        # self.email_input.grid_forget()
        # self.password_input.grid_forget()
        # self.login_button.grid_forget()
        # self.register_button.grid_forget()
        self.register_frame = tk.Frame
        # labels
        title = tk.Label(self.register_frame, text="Register",
                         font=("Arial", 15, "bold"))
        email_label = tk.Label(self.register_frame, text="Email")
        fname_label = tk.Label(self.register_frame, text="First Name")
        lname_label = tk.Label(self.register_frame, text="Last Name")
        password_label = tk.Label(self.register_frame, text="Password")

        # textvariable
        current_email = tk.StringVar()
        current_password = tk.StringVar()
        current_fname = tk.StringVar()
        current_lname = tk.StringVar()

        # entries
        email_input = tk.Entry(self.register_frame, width=30, font=(
            "Arial", 10), textvariable=current_email)
        fname_input = tk.Entry(self.register_frame, width=30, font=(
            "Arial", 10), textvariable=current_fname)
        lname_input = tk.Entry(self.register_frame, width=30, font=(
            "Arial", 10), textvariable=current_lname)
        password_input = tk.Entry(self.register_frame, width=30, font=(
            "Arial", 10), textvariable=current_password)

        # buttons
        register_button = tk.Button(self.register_frame,
                                    text="Register", command=lambda: self.createAccount(current_fname.get(), current_lname.get(), current_email.get(), current_password.get()))

        # positioning
        title.grid(row=0, column=0, columnspan=2)
        fname_label.grid(row=1, column=0)
        lname_label.grid(row=2, column=0)
        email_label.grid(row=3, column=0)
        password_label.grid(row=4, column=0)

        fname_input.grid(row=1, column=1, pady=3)
        lname_input.grid(row=2, column=1, pady=3)
        email_input.grid(row=3, column=1, pady=3)
        password_input.grid(row=4, column=1, pady=3)

        register_button.grid(row=5, column=1)

    def createAccount(self, fname, lname, email, password):
        if not (fname and lname and email and password):
            messagebox.showinfo(
                "Missing Values", "Please fill in all necessary information!")
        else:
            if (self.checkEmail(email)):
                if (self.checkPassword(password)):
                    self.save(fname, lname, email, password)
                    self.login()

    def checkEmail(self, email):
        # check that email is valid
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            messagebox.showinfo(
                "Invalid Email", "Email entered is not valid! Please choose a valid email address")
            return False
        else:
            return True

    def checkPassword(self, password):
        # Check length of at least 8 characters
        if len(password) < 8:
            messagebox.showinfo(
                "Weak Password", "Password should have atleast 8 characters")
            return False

        # Check for at least one special character
        if not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\:;\"'<>,.?/~`]", password):
            messagebox.showinfo(
                "Weak Password", "Please include special characters in password")
            return False

         # Check for at least one lowercase letter, one uppercase letter, and one digit
        if not (re.search(r"[a-z]", password) and re.search(r"[A-Z]", password) and re.search(r"\d", password)):
            messagebox.showinfo(
                "Weak Password", "Password should include mixed case letters and digits")
            return False

        return True

    def save(self, fname, lname, email, password):
        """save data entered ehen creating account"""

        # hash password
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())

        # Connect to the MySQL server
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        print(db)

        # Create a database
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS project")

        # create tables
        cursor.execute("USE project")
        sql = """
            CREATE TABLE IF NOT EXISTS users(
                id int primary key auto_increment,
                first_name varchar(25) not null,
                last_name varchar(25) not null,
                email varchar(50) not null unique,
                password varchar(255) not null
            )"""
        cursor.execute(sql)

        # Connect to the newly created database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="project"
        )
        cursor = db.cursor()
        # check if email is  exists
        query = f"SELECT * FROM users WHERE email='{email}'"
        cursor.execute(query)
        row = cursor.fetchone()

        # if email exists
        if (row):
            messagebox.showinfo(
                "Email Taken", "Email is already taken! Please use another email")

        # email does not exist
        else:
            # insert data to users table
            sql = "INSERT INTO users(first_name, last_name,email, password) VALUES (%s, %s,%s, %s)"
            values = (fname, lname, email, hashed_password)
            cursor.execute(sql, values)

            # commit changes
            db.commit()

            # close cursor and database connection
            cursor.close()
            db.close()

    def authenticate(self, email, password):
        """authenticate a user"""
        if (self.checkEmail(email)):
            # Connect to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="project"
            )
            cursor = db.cursor()

            # check if email is  exists
            query = f"SELECT password FROM users WHERE email='{email}'"
            cursor.execute(query)
            row = cursor.fetchone()
            if not row:
                messagebox.showinfo(
                    "", "There is no account with the above Email!")
            else:
                if (bcrypt.checkpw(password.encode("utf-8"), row[0].encode("utf-8"))):
                    messagebox.showinfo(
                        "Login", "You have successfully logged in")
                else:
                    messagebox.showinfo(
                        "Login", "You entered an incorrect password!")

    def clear_widgets(self):
        """remove all widgets in the frame"""
        attributes = vars(self)
        for attr, value in attributes.items():
            print(f"{attr}: {value}")


root = tk.Tk()
root.title("Squints Detection Application")
root.geometry("400x200")
# Configure column and row to center
# root.columnconfigure((0, 1, 2), weight=1)
# root.rowconfigure((0, 1, 2), weight=1)
app = App(root)
app.mainloop()
