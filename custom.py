import customtkinter as ctk
from tkinter import messagebox, StringVar
import mysql.connector
from tkinter import filedialog
from PIL import ImageTk, Image
import tensorflow as tf
import numpy as np
import bcrypt
import re
import cv2

# Modes: system (default), light, dark
ctk.set_appearance_mode("light")
# Themes: blue (default), dark-blue, green
ctk.set_default_color_theme("blue")


class MyFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    # add widgets onto the frame, for example:

    def login_view(self):

        legend = ctk.CTkLabel(self, text="Log In", font=(
            "Arial", 25), width=300, height=35, pady=10, text_color="black")
        email = ctk.CTkEntry(
            self, placeholder_text="Enter Email", width=300, height=35,  text_color="black", border_width=0, font=("Arial", 18), corner_radius=10)
        password = ctk.CTkEntry(
            self, placeholder_text="Enter Password", width=300, height=35,  text_color="black", border_width=0, font=("Arial", 18), corner_radius=10, show="*")
        button_frame = ctk.CTkFrame(
            self, width=300, height=40, border_width=0, bg_color="transparent")
        login_button = ctk.CTkButton(
            button_frame, text="login", text_color="black", width=100, height=30, font=("Arial", 18), corner_radius=8, border_width=0, command=lambda: self.login(email.get(), password.get()))
        register_button = ctk.CTkButton(
            button_frame, text="register", text_color="black", width=100, height=30, font=("Arial", 18), corner_radius=8, border_width=0, command=self.showRegister)

        legend.pack()
        email.pack(pady=10)
        password.pack(pady=10)
        button_frame.pack(pady=10)
        login_button.grid(pady=10, padx=10, row=0, column=0)
        register_button.grid(pady=10, padx=10, row=0, column=1)

    def showRegister(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.register_view()

    def register_view(self):

        legend = ctk.CTkLabel(self, text="Register", font=(
            "Arial", 25), width=300, height=35, pady=10, text_color="black")
        first_name = ctk.CTkEntry(
            self, placeholder_text="Enter First Name", width=300, height=35,  text_color="black", border_width=0, font=("Arial", 18), corner_radius=10)
        last_name = ctk.CTkEntry(
            self, placeholder_text="Enter Last Name", width=300, height=35,  text_color="black", border_width=0, font=("Arial", 18), corner_radius=10)
        email = ctk.CTkEntry(
            self, placeholder_text="Enter Email", width=300, height=35,  text_color="black", border_width=0, font=("Arial", 18), corner_radius=10)
        password = ctk.CTkEntry(
            self, placeholder_text="Enter Password", width=300, height=35,  text_color="black", border_width=0, font=("Arial", 18), corner_radius=10, show="*")
        register_button = ctk.CTkButton(
            self, text="register", text_color="black", width=100, height=30, font=("Arial", 18), corner_radius=8, border_width=0, command=lambda: self.register(first_name.get(), last_name.get(), email.get(), password.get()))

        legend.pack()
        first_name.pack(pady=10)
        last_name.pack(pady=10)
        email.pack(pady=10)
        password.pack(pady=10)
        register_button.pack(pady=10)

    def login(self, email, password):
        """authenticate a user"""
        if (email and password):
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
                        # messagebox.showinfo(
                        #     "Login", "You have successfully logged in")
                        self.home()

                    else:
                        messagebox.showinfo(
                            "Login", "You entered an incorrect password!")
        else:
            messagebox.showinfo("Missing Values", "Please fill in all fields!")

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

    def register(self, fname, lname, email, password):
        if not (fname and lname and email and password):
            messagebox.showinfo(
                "Missing Values", "Please fill in all necessary information!")
        else:
            if (self.checkEmail(email)):
                if (self.checkPassword(password)):
                    self.save(fname, lname, email, password)
                    for widget in self.winfo_children():
                        widget.destroy()
                    self.login_view()

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

    def open_image(self):
        # clear the frame
        for widget in self.winfo_children():
            widget.destroy()
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            # get and display image
            my_image = ctk.CTkImage(
                light_image=Image.open(file_path), size=(300, 300))
            image_label = ctk.CTkLabel(self, image=my_image, text="")
            image_label.pack(pady=20)

            # obtain prediction from model
            IMG_SIZE = 224
            image_array = cv2.imread(file_path)
            image_resized = cv2.resize(image_array, (IMG_SIZE, IMG_SIZE))
            model_path = "C:\\Users\\hp\\projects\\data_science\\squint_detection\\Models\\Squint_detector_20230520150447_model"
            model = tf.keras.models.load_model(model_path)
            yhat = model.predict(np.expand_dims(image_resized, axis=0))
            prediction = StringVar(value='Eyes are squinted' if (
                yhat > 0.5) else 'Eyes are not squinted')

            # display the prediction
            display_frame = ctk.CTkFrame(self, width=300, height=45)
            display_frame.pack()
            prediction_label = ctk.CTkEntry(
                display_frame, width=180, height=35, border_width=0, textvariable=prediction, corner_radius=10, state="disabled")
            prediction_label.grid(row=0, column=0, padx=10, pady=10)
            home_button = ctk.CTkButton(display_frame, text="Home", text_color="white", font=(
                "Arial", 18), border_width=0, corner_radius=8, width=80, command=self.home, height=35)
            home_button.grid(row=0, column=1, padx=10, pady=10)

    def home(self):
        # clear the frame
        for widget in self.winfo_children():
            widget.destroy()
        title_label = ctk.CTkLabel(
            self, text="Welcome...", font=("Arial", 30), width=300)
        title_label.pack(pady=20)
        select_image = ctk.CTkButton(self, text="Upload Image", width=100,
                                     height=30, corner_radius=8, border_width=0, command=self.open_image, font=("Arial", 18), text_color="white")
        select_image.pack(pady=10)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x500")
        self.title("Squinted Eyes Detection App")
        self.grid_rowconfigure(0, weight=1)  # configure grid system
        self.grid_columnconfigure(0, weight=1)

        my_frame = MyFrame(master=self)
        my_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        my_frame.login_view()


app = App()
app.mainloop()
