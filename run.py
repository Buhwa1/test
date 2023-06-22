import tkinter as tk
from tkinter import messagebox
top = tk.Tk()


def helloCallBack():
    # messagebox.showinfo("Hello Python", "Hello World")
    # messagebox.showerror("Hello Python", "Hello World")
    # messagebox.showwarning("Hello Python", "Hello World")
    messagebox.askquestion("Hello Python", "Hello World")


B = tk.Button(top, text="Hello", command=helloCallBack,
              padx="10", pady="1", highlightcolor="gray")

B.pack()
top.mainloop()
