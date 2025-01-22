import pandas as pd
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkfont
from PIL import Image, ImageTk

def main_window():
    # Function to load the CSV file into a DataFrame
    def load_movie_data():
        try:
            # Load the CSV data into a pandas DataFrame
            df = pd.read_csv('imdb_top_1000.csv')  # Path to your CSV file
            return df
        except Exception as e:
            messagebox.showerror("File Error", f"Error loading the CSV file: {e}")
            return None

    # Function to fetch recommended movies based on user input
    def get_recommendations():
        genre = genre_entry.get().strip()
        director = director_entry.get().strip()
        actor = actor_entry.get().strip()

        if not genre and not director and not actor:
            messagebox.showwarning("Input Error", "Please enter at least one search criteria.")
            return

        # Load the movie data from the CSV file
        df = load_movie_data()
        if df is None:
            return  # Return if there's an issue loading the data

        # Filtering the dataframe based on user input
        filtered_df = df

        if genre:
            filtered_df = filtered_df[filtered_df['Genre'].str.contains(genre, case=False, na=False)]
        if director:
            filtered_df = filtered_df[filtered_df['Director'].str.contains(director, case=False, na=False)]
        if actor:
            filtered_df = filtered_df[filtered_df['Star1'].str.contains(actor, case=False, na=False)]

        # Check if any movies match the criteria
        if not filtered_df.empty:
            display_recommendations(filtered_df.head())
        else:
            messagebox.showinfo("No Results", "No movies found based on the given criteria.")

    # Function to display recommended movies in the GUI
    def display_recommendations(df):
        result_text.delete(1.0, tk.END)  # Clear previous results
        for index, row in df.iterrows():
            result_text.insert(tk.END, f"Title: {row['Series_Title']}\n")
            result_text.insert(tk.END, f"Genre: {row['Genre']}\n")
            result_text.insert(tk.END, f"Director: {row['Director']}\n")
            result_text.insert(tk.END, f"Year: {row['Released_Year']}\n")
            result_text.insert(tk.END, f"Actor: {row['Star1']}\n")
            result_text.insert(tk.END, "-" * 40 + "\n")

    # Create the GUI
    root = tk.Tk()
    root.title("Movie Recommendation System")
    root.geometry("800x600")  # Set the window size

    # Load background image
    bg_image = Image.open("background.jfif")  # Path to your background image
    bg_image = bg_image.resize((800, 600))  # Resize to fit window
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a canvas to display the background image
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)

    # Set the background image
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Add a custom font
    custom_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

    # Labels and Entry Widgets for user inputs with styling
    tk.Label(root, text="Enter Genre:", font=custom_font, bg="#ffffff").place(x=50, y=50)
    genre_entry = tk.Entry(root, font=custom_font, width=40)
    genre_entry.place(x=200, y=50)

    tk.Label(root, text="Enter Director:", font=custom_font, bg="#ffffff").place(x=50, y=100)
    director_entry = tk.Entry(root, font=custom_font, width=40)
    director_entry.place(x=200, y=100)

    tk.Label(root, text="Enter Actor:", font=custom_font, bg="#ffffff").place(x=50, y=150)
    actor_entry = tk.Entry(root, font=custom_font, width=40)
    actor_entry.place(x=200, y=150)

    # Button to trigger recommendations with styling
    recommend_button = tk.Button(root, text="Get Recommendations", command=get_recommendations, font=custom_font, bg="#4CAF50", fg="white", activebackground="#45a049")
    recommend_button.place(x=200, y=200, width=200, height=40)

    # Text widget to display recommendations with styling
    result_text = tk.Text(root, font=custom_font, width=60, height=15, bg="white", fg="black", bd=2, relief="solid")
    result_text.place(x=50, y=250)

    # Run the GUI
    root.mainloop()
