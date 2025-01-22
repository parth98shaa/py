import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import mysql.connector
import project
from PIL import Image, ImageTk

# Function to initialize the database
def init_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='2830412',
        database='movie_users'
    )
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to handle registration
def register():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='2830412',
                database='movie_users'
            )
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            messagebox.showinfo("Registration", "Registration Successful")
        except mysql.connector.IntegrityError:
            messagebox.showerror("Registration", "Username already exists")
        finally:
            conn.close()
    else:
        messagebox.showwarning("Registration", "Please fill in all fields")

# Function to handle login
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='2830412',
        database='movie_users'
    )
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login", "Login Successful")
        root.destroy()  # Close the login window
        project.main_window()  # Assuming 'project.main_window()' is defined in your project
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Initialize the database
init_db()

# Create the main window with gradient background
root = tk.Tk()
root.title("Login and Registration Form")
root.geometry("1250x700")
root.config(bg="#f4f4f9")

# Setting up the icon image
#icon_image = ImageTk.PhotoImage(file='icon_image1.jpg')  # Ensure the file path is correct
#root.iconphoto(False, icon_image)

# Gradient background setup
canvas = tk.Canvas(root, width=1250, height=700, highlightthickness=0, bg="#f4f4f9")
canvas.pack(fill="both", expand=True)

# Create a card-style frame for the form
card_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="solid", highlightbackground="#ddd", highlightcolor="#ddd")
canvas.create_window(620, 320, window=card_frame, width=600, height=320)

# Styling variables
font_label = ("Segoe UI", 18, "bold")
font_entry = ("Segoe UI", 16)
font_button = ("Segoe UI", 14, "bold")

# Create and place labels and entries with custom styling
tk.Label(card_frame, text="Username", font=font_label, bg="white", fg="#2c3e50").grid(row=0, column=0, padx=15, pady=(30, 10), sticky="w")
entry_username = ttk.Entry(card_frame, font=font_entry, width=25)
entry_username.grid(row=0, column=1, padx=15, pady=(30, 10))

tk.Label(card_frame, text="Password", font=font_label, bg="white", fg="#2c3e50").grid(row=1, column=0, padx=15, pady=10, sticky="w")
entry_password = ttk.Entry(card_frame, show="*", font=font_entry, width=25)
entry_password.grid(row=1, column=1, padx=15, pady=10)

# Button styles
def on_enter(btn):
    btn.config(bg="#0056b3", fg="white")

def on_leave(btn):
    btn.config(bg="#007bff", fg="white")

btn_register = tk.Button(card_frame, text="Register", font=font_button, bg="#28a745", fg="white", bd=0, relief="flat", command=register, width=20, height=2)
btn_register.grid(row=3, column=1, padx=20, pady=(20, 20))
btn_register.bind("<Enter>", lambda e: on_enter(btn_register))
btn_register.bind("<Leave>", lambda e: on_leave(btn_register))

btn_login = tk.Button(card_frame, text="Login", font=font_button, bg="#007bff", fg="white", bd=0, relief="flat", command=login, width=20, height=2)
btn_login.grid(row=2, column=1, padx=20, pady=(15, 10))
btn_login.bind("<Enter>", lambda e: on_enter(btn_login))
btn_login.bind("<Leave>", lambda e: on_leave(btn_login))

# Center alignment of widgets within card frame
card_frame.grid_columnconfigure(0, weight=1)
card_frame.grid_columnconfigure(1, weight=1)

# Run the main event loop
root.mainloop()
