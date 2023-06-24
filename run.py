import customtkinter as ctk
from tkinter import ttk
import threading
import time


def long_running_task():
    # Simulating a long-running task
    time.sleep(5)  # Replace this with your actual task

    # After the task is complete, update the GUI
    app.event_generate("<<TaskComplete>>")  # Generate a custom event


def start_task():
    # Disable the button to prevent multiple clicks
    start_button.config(state="disabled")

    # Show the progress bar
    progress_bar.start()

    # Start the long-running task in a separate thread
    thread = threading.Thread(target=long_running_task)
    thread.start()


def handle_task_complete(event):
    # Enable the button and stop the progress bar
    start_button.config(state="normal")
    progress_bar.stop()


# Create the Tkinter app
app = ctk.CTk()

# Create a button to start the task
start_button = ctk.CTkButton(app, text="Start Task", command=start_task)
start_button.pack()

# Create a progress bar (indeterminate mode)
progress_bar = ctk.CTkProgressBar(app, mode="indeterminate")
progress_bar.pack(pady=10)

# Bind the custom event to a function
app.bind("<<TaskComplete>>", handle_task_complete)

# Run the Tkinter main loop
app.mainloop()
