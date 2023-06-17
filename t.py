import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import filedialog


class Application(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Image Uploader")
        self.geometry("400x300")
        
        # Create a sidebar frame
        self.sidebar_frame = tk.Frame(self, width=250, bg="gray")
        
        # Create buttons for sidebar
        home_button = tk.Button(self.sidebar_frame, text="Home", command=self.show_home)
        home_button.pack(pady=10)
        
        upload_button = tk.Button(self.sidebar_frame, text="Upload Image", command=self.upload_image)
        upload_button.pack(pady=10)
        
        # Create a content frame
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Show the login page initially
        self.show_login()
    
    def show_login(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Create login widgets
        username_label = tk.Label(self.content_frame, text="Username:")
        username_label.pack()
        
        self.username_entry = tk.Entry(self.content_frame)
        self.username_entry.pack(pady=5)
        
        password_label = tk.Label(self.content_frame, text="Password:")
        password_label.pack()
        
        self.password_entry = tk.Entry(self.content_frame, show="*")
        self.password_entry.pack(pady=5)
        
        login_button = tk.Button(self.content_frame, text="Login", command=self.login)
        login_button.pack(pady=10)
    
    def login(self):
        # Connect to MySQL database
        try:
            cnx = mysql.connector.connect(
                host="localhost",
            user="root",
            password="",
            database="squint"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to connect to MySQL: {err}")
            return
        
        # Get username and password
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Verify login credentials
        cursor = cnx.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        values = (username, password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        
        if result:
            # Login successful
            messagebox.showinfo("Success", "Login successful!")
            self.show_home()
            self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            # Login failed
            messagebox.showerror("Error", "Invalid username or password!")
        
        # Close database connection
        cursor.close()
        cnx.close()
    
    def show_home(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Add content to the home page
        label = tk.Label(self.content_frame, text="Welcome to the Homepage!", font=("Arial", 20))
        label1 = tk.Label(self.content_frame, 
                          text="Instructions on how to use the application.../n 1.Click on upload image", 
                          font=("Arial", 20))
        
        label.pack(pady=50)
        label1.pack(pady=50)
        
    
    def upload_image(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Add button to upload image
        upload_button = tk.Button(self.content_frame, text="Upload Image", command=self.select_image)
        upload_button.pack(pady=50)
        
        
        # Add button to remove image
        remove_button = tk.Button(self.content_frame, text="Remove Image", command=self.remove_image)
        remove_button.pack(pady=10)
    
    def select_image(self):
        # Open a file dialog to choose an image file
        filename = filedialog.askopenfilename(initialdir="/", title="Select an image file",
                                          filetypes=(("Image files", "*.jpg *.png"), ("All files", "*.*")))

        # Display the selected image
        image_label = tk.Label(self.content_frame)
        image_label.pack(pady=10)

        image = Image.open(filename)
        image.thumbnail((224, 224))  # Resize image to match the input size expected by ResNet50
        image = image.convert("RGB")  # Convert image to RGB mode if it's in a different mode

       
        
    def remove_image(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Remove the uploaded image
        # Additional logic here, if needed
        
        # Display a message
        message_label = tk.Label(self.content_frame, text="Image removed!")
        message_label.pack(pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
