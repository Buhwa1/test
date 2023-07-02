import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image
import sqlite3
import bcrypt
from io import BytesIO
import tensorflow as tf
import numpy as np
from datetime import datetime
import re

class LoginForm(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Login Form")
        self.width=400
        self.height=420
        
        # welcome label
        self.label1=ctk.CTkLabel(
            self, text="WELCOME BACK", font=("Lucida", 15, "bold"), text_color="gray")
        # login label
        self.label2=ctk.CTkLabel(
            self, text="Log into your account", font=("Lucida", 20, "bold"), text_color="white")
        # email label
        self.email_label=ctk.CTkLabel(
            self, text="Email", font=("Lucida", 15), text_color="white")
        # email field
        self.email_field=ctk.CTkEntry(
            self, placeholder_text="Enter your email", width=300, height=35, corner_radius=5, border_width=0)
        # password label
        self.password_label= ctk.CTkLabel(
            self, text="Password", font=("Lucida", 15), text_color="white")
        # password field
        self.password_field = ctk.CTkEntry(
            self, placeholder_text="Enter your password", width=300, height=35, corner_radius=5, border_width=0, show="*")
        # show password checkbox
        self.showPassword = ctk.CTkCheckBox(
            self, text="Show Password", hover=False, border_width=2, width=3, height=3, corner_radius=5, command=lambda: self.togglePasswordVisibility([self.password_field], self.showPassword))
        # submit button
        self.submit_button = ctk.CTkButton(
            self, text="login", width=300, height=35, corner_radius=5, border_width=0, font=("Lucida", 15, "bold"), command=lambda: self.login(self.email_field.get(), self.password_field.get(), master))
        # register text
        self.label3=ctk.CTkLabel(
            self, text="Not registered yet?", font=("Lucida", 12), text_color="gray", anchor="e")
        # register link
        self.link1=ctk.CTkButton(
            self, text="Register", text_color="white", command=lambda: self.switchForm(master), hover=False, anchor="w", fg_color="transparent")
        

        self.label1.grid(row=0, column=0, sticky="nsew",
                           columnspan=2, pady=(30, 0))
        self.label2.grid(row=1, column=0, sticky="nsew",
                         columnspan=2, pady=(0, 20))
        self.email_label.grid(row=2, column=0, sticky="w", padx=30, columnspan=2)
        self.email_field.grid(row=3, column=0, sticky="W",
                         padx=30, columnspan=2, pady=(0, 10))
        self.password_label.grid(row=4, column=0, sticky="w", padx=30)
        self.password_field.grid(row=5, column=0, sticky="W", padx=30, columnspan=2)
        self.showPassword.grid(row=6, column=0, padx=(20, 0), pady=(10, 0))
        self.submit_button.grid(row=7, column=0,  padx=30,
                           columnspan=2, sticky="nwse", pady=(10, 0))
        self.label3.grid(row=8, column=0,
                            pady=(0, 30), padx=(30, 0))
        self.link1.grid(row=8, column=1, pady=(0, 30),
                             padx=(0, 0), sticky="w")
        

    def switchForm(self, master):
        self.destroy()
        register=RegisterForm(master)
        register.grid(row=0, column=0, padx=10, pady=10)


    def login(self, email, password, master):
        if self.formValidation(email, password):
            with sqlite3.connect("project.db") as conn:
                c=conn.cursor()
                # check if email exists
                query = "SELECT * FROM users WHERE email=:email"
                c.execute(query, {'email': email})
                row = c.fetchone()
                if not row:
                    messagebox.showinfo(
                    "Account not created", f"There is no account the the email {email}.\n Please register account.")
                    return 
                else:
                    if bcrypt.checkpw(password.encode("utf-8"), row[2]):
                        self.destroy()
                        currentUser.userid=row[0]
                        currentUser.email=row[1]
                        home=Home(master)
                        panel=LeftPanel(master)
                        home.grid(row=0, column=1)
                        panel.grid(row=0, column=0)
                        master.grid_columnconfigure(0, weight=1)
                        master.grid_columnconfigure(1, weight=5)


                    else:
                        messagebox.showinfo(
                    "Incorrect password", "Password entered is incorrect")
                    return 

    def togglePasswordVisibility(self, widgets, checkbox):
        if checkbox.get():
            for widget in widgets:
                widget.configure(show="")
        else:
            for widget in widgets:
                widget.configure(show="*")


    def formValidation(self, email, password):
        if email:
            # check that email is valid
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email):
                messagebox.showinfo(
                    "invalid email", "Email entered is not valid! Please enter a valid email address")
                return False
            else:
                if password:
                    return True
                else:
                    messagebox.showinfo("Empty Fields", "Please enter value for password field")
                    return False
        else:
            messagebox.showinfo("Empty Fields", "Please enter value for email field")
            return False

class User:
    def __init__(self):
        self.userid=None
        self.email=None


currentUser=User()
model_cache={}

class RegisterForm(LoginForm):
    def __init__(self, master):
        super().__init__(master)
        master.title("Register Form")
        self.label1.destroy()
        self.label2.destroy()
        self.submit_button.configure(text="register", command=lambda: self.register(self.email_field.get(), self.password_field.get(), self.confirmPassword_field.get(), master))
        self.label3.configure(text="Already have an account?")
        self.link1.configure(text="Login", command=lambda: self.switchForm(master))
        self.showPassword.configure(command=lambda: self.togglePasswordVisibility([self.password_field, self.confirmPassword_field], self.showPassword))
        # confirm password label
        self.confirmPassword_label=ctk.CTkLabel(self, text="Confirm password", font=("Lucida", 15), text_color="white")
        # confirm password field
        self.confirmPassword_field = ctk.CTkEntry(
            self, placeholder_text="Enter password again", width=300, height=35, corner_radius=5, border_width=0, show="*")
        # register label
        self.label1=ctk.CTkLabel(
            self, text="Create account", font=("Lucida", 20, "bold"), text_color="white")
        

        self.label1.grid(row=0, column=0, sticky="nsew",
                            columnspan=2, pady=(30, 20))
        self.email_label.grid(row=1, column=0, sticky="w", padx=30, columnspan=2)
        self.email_field.grid(row=2, column=0, sticky="W",
                         padx=30, columnspan=2, pady=(0, 10))
        self.password_label.grid(row=3, column=0, sticky="w", padx=30)
        self.password_field.grid(row=4, column=0, sticky="W",
                            padx=30, columnspan=2, pady=(0, 10))
        self.confirmPassword_label.grid(row=5, column=0, sticky="w", padx=30)
        self.confirmPassword_field.grid(row=6, column=0, sticky="W",
                                   padx=30, columnspan=2, pady=(0, 10))
        self.showPassword.grid(row=7, column=0, padx=(
            30, 0), pady=(0, 10), columnspan=2, sticky='w')
        self.submit_button.grid(row=8, column=0,  padx=30,
                           columnspan=2, sticky="nwse", pady=(0, 0))
        self.label3.grid(row=9, column=0,
                            pady=(0, 30), padx=(30, 0))
        self.link1.grid(row=9, column=1, pady=(0, 30),
                             padx=(0, 0), sticky="w")
        

    def switchForm(self, master):
        self.destroy()
        login=LoginForm(master)
        login.grid(row=0, column=0, padx=10, pady=10)


    def register(self, email, password, confirmPassword, master):
        if self.formValidation(email, password, confirmPassword):
            try:
                response=self.createAccount(email, password)
            except Exception as e:
                messagebox.showinfo(
                    "Registration Error", e)
                return False
            else:
                if response:
                    self.destroy()
                    login=LoginForm(master)
                    login.grid(row=0, column=0, padx=10, pady=10)

                    
                


    def createAccount(self, email, password):
        with sqlite3.connect("project.db") as conn:
            c = conn.cursor()
            password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt())
            # check that email does not already exist
            query = "SELECT * FROM users WHERE email=:email"
            c.execute(query, {'email': email})
            row = c.fetchone()
            if row:
                raise Exception(
                    f"An account already exists with that email address {email}.\nChoose another email")
            else:
                sql = "INSERT INTO users(email, password) VALUES (:email, :password)"
                c.execute(sql, {'email': email, 'password': password})
                if c.rowcount > 0:
                    return 1
                else:
                    raise Exception("An error occurred when creating account.")



    def formValidation(self, email, password, confirmPassword):
        if email:
            # check that email is valid
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if not re.match(pattern, email):
                messagebox.showinfo(
                    "invalid email", "Email entered is not valid! Please enter a valid email address")
                return False
            else:
                if password:
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
                    
                    if confirmPassword:
                        # check that passwords are the same
                        if password != confirmPassword:
                            messagebox.showinfo(
                                "passwords not matching", "Please enter the same password for 'Confirm password' and 'password' fields.")
                            return False
                        else:
                            return True
                    else:
                        messagebox.showinfo("Empty Fields", "Please enter value for confirm password field")
                        return False

       
                else:
                    messagebox.showinfo("Empty Fields", "Please enter value for password field")
                    return False

        else:
            messagebox.showinfo("Empty Fields", "Please enter value for email field")
            return False

        

class LeftPanel(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.fg_color="#3d3d3e"
        self.corner_radius=0
        userImage = ctk.CTkImage(
            dark_image=Image.open("images/user.png"), size=(20, 20))
        self.user_label = ctk.CTkLabel(self, text_color="white",
                                  fg_color="transparent", text=" "+currentUser.email, font=("Lucida", 15, "bold"), image=userImage, compound="left")
        self.user_label.grid(row=0, column=0, padx=(
            10, 0), pady=(10, 5), sticky="ew")

        homeImage = ctk.CTkImage(
            light_image=Image.open("images/home.png"), size=(20, 20))
        self.home_label = ctk.CTkButton(self, text_color="white",
                                   fg_color="gray", text=" Home", font=("Lucida", 15), corner_radius=5, hover_color="gray", anchor="w", image=homeImage, compound="left", height=35)
        self.home_label.grid(row=1, column=0, padx=(
            10, 0), pady=(5, 0), sticky="ew")

        clockImage = ctk.CTkImage(
            light_image=Image.open("images/clock.png"), size=(20, 20))
        self.history_label = ctk.CTkButton(self, text_color="white",
                                      fg_color="transparent", text=" History", font=("Lucida", 15), corner_radius=5, hover_color="gray", anchor="w", image=clockImage, compound="left", height=35)
        self.history_label.grid(row=2, column=0, padx=(
            10, 0), pady=(0, 0), sticky="ew")
        
        # def 
        

class Home(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        master.title("Home")
        text = "Upload eye images here"
        self.intro_label = ctk.CTkLabel(
            self, text=text, font=("Lucida", 20, "bold"), fg_color="transparent", text_color="white")
        self.intro_label.grid(row=0, column=0, padx=10,
                         pady=(30, 35), sticky="nsew")

        uploadImage = ctk.CTkImage(
            light_image=Image.open("images/upload.png"), size=(30, 30))
        self.upload_button = ctk.CTkButton(self, fg_color="gray",
                                      corner_radius=8, border_width=0, text="", image=uploadImage, command=self.upload, hover=None)
        self.upload_button.grid(row=0, column=1, padx=(
            10), pady=(0, 0))



    def upload(self):
        filepath = filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        image = Image.open(filepath)
        ctk_image = ctk.CTkImage(light_image=image, size=(300, 300))
        image_label = ctk.CTkLabel(self, text="", image=ctk_image)
        image_label.grid(row=1, column=0, rowspan=2, padx=(20, 0))

        model = self.loadModel()
        image = image.resize((224, 224), Image.LANCZOS)
        yhat = model.predict(np.expand_dims(image, axis=0))

        prediction = 1 if (yhat > 0.5) else 0
        prediction_label = ctk.CTkLabel(self, text="Positive" if (prediction == 1) else "Negative", width=100,
                                        height=35, fg_color="transparent", corner_radius=5, text_color="white", font=("Lucida", 20, "bold"))
        prediction_label.grid(padx=20, row=1, column=1, sticky="s")

        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_label = ctk.CTkLabel(self, text=time, text_color="white",
                                  fg_color="transparent", font=("Lucida", 20, "bold"))
        # time_label.grid(row=2, column=1, padx=20, sticky="n")

        image_bytes = BytesIO()
        image.save(image_bytes, format='JPEG')
        image_data = image_bytes.getvalue()
        image = sqlite3.Binary(image_data)

        self.saveUserHistory(image, prediction, time)


    def saveUserHistory(self, image, prediction, time_recorded):
         """save user history"""
         with sqlite3.connect("project.db") as conn:
            c=conn.cursor()
            sql = "INSERT INTO history(image, prediction, time_recorded, userid) VALUES (:image, :prediction, :time_recorded, :userid)"
            c.execute(sql, {'image': image, 'prediction': prediction,
                        "time_recorded": time_recorded, "userid": currentUser.userid})




    def loadModel(self):
        if model_cache.get("model"):
            return model_cache["model"]
        else:
            model_path = "Squint_detector_20230520151755_model"
            model = tf.keras.models.load_model(model_path)
            model_cache["model"] = model
            return model


class History(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)
        master.title("History")
    def showHistory(self):
        rows = self.getHistory()
        if rows:
            for i, row in enumerate(rows):
                inner = ctk.CTkFrame(self)
                inner.grid(row=i, column=0, padx=(20, 0),
                           pady=(20, 20), sticky="nwse")
                image = ctk.CTkImage(light_image=Image.open(
                    BytesIO(row[1])), size=(300, 300))
                image_label = ctk.CTkLabel(inner, text="", image=image)
                image_label.grid(row=0, column=0, rowspan=2)

                prediction = 1 if (row[2] > 0.5) else 0
                prediction_label = ctk.CTkLabel(inner, text="Positive" if (prediction == 1) else "Negative", width=100,
                                                height=35, fg_color="transparent", corner_radius=5, text_color="white", font=("Lucida", 20, "bold"))
                prediction_label.grid(padx=20, row=0, column=1, sticky="s")
                time = row[3]
                time_label = ctk.CTkLabel(
                    inner, text=time, text_color="white", fg_color="transparent", font=("Lucida", 20, "bold"))
                # time_label.grid(row=1, column=1, padx=20, sticky="n")
                remove_button = ctk.CTkButton(
                    inner, text="delete", corner_radius=5, width=150, height=35, font=("Lucida", 18), command=lambda: self.remove(row[3]))
                remove_button.grid(row=1, column=1, padx=20,
                                   sticky="n", pady=(20, 0))

        else:
            label = ctk.CTkLabel(self, text="No history available", font=(
                "Lucida", 30, "bold"), text_color="white", fg_color="transparent")
            label.grid(row=0, column=0, sticky="nwse",
                       padx=(200, 0), pady=(30, 0))
            

    def getHistory(self):
        """get a users history"""
        with sqlite3.connect("project.db") as conn:
            c=conn.cursor()
            query = "SELECT * FROM history WHERE userid=:userid ORDER BY time_recorded DESC"
            c.execute(query, {'userid': currentUser.userid})
            rows = c.fetchall()
            return rows



class App(ctk.CTk):        

    def createDatabase(self):
        conn=sqlite3.connect("project.db")
        c = conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS users(
            id integer primary key,
            email text not null,
            password text not null 
        )"""
        c.execute(sql)

        conn.execute('PRAGMA foreign_keys = ON')
        sql = """CREATE TABLE IF NOT EXISTS history(
            userid integer not null,
            image blob not null,
            prediction integer not null,
            time_recorded datetime not null,
            primary key(userid, time_recorded),
            foreign key(userid) references users(id)
        )"""
        c.execute(sql)

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")
app=App()
app.geometry("500x550")
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)
app.createDatabase()
login=LoginForm(app)
login.grid(row=0, column=0, padx=10, pady=10)


app.mainloop()

