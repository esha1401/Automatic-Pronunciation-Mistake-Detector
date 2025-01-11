from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Label, Tk
import mysql.connector
import pyttsx3
import speech_recognition as sr
from PIL import ImageTk, Image  # Use Pillow to handle image formats like JPEG

# Database connection
mysqldb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='pronunciation'
)

if mysqldb.is_connected():
    print("Successfully connected to the database")
else:
    print("Not Connected")

mycursor = mysqldb.cursor()

# Global variables
logged_in = False

# Functions
def pythonlogin():
    global logged_in
    username = usernameEntry.get()
    password = password_entry.get()
    
    sql = 'SELECT * FROM data WHERE username = %s AND password = %s'
    mycursor.execute(sql, (username, password))
    result = mycursor.fetchall()
    
    if result:
        messagebox.showinfo("Automatic Pronunciation Mistake Detector", "Login Successful")
        logged_in = True
        system_window()
        return True
    else:
        messagebox.showwarning("Automatic Pronunciation Mistake Detector", "Please Check Your Input!")
        usernameEntry.delete(0, 'end')
        password_entry.delete(0, 'end')
        return False

def toggle_password_visibility():
    if password_entry["show"] == '*':
        password_entry.config(show='')
        show_password_button.config(text='Hide')
    else:
        password_entry.config(show='*')
        show_password_button.config(text='Show')

import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk

def register_user():
    try:
        username = username_entry.get()
        password = password_entry.get()
        first_name = firstname_entry.get()
        last_name = lastname_entry.get()
        email = email_entry.get()
        age = age_combobox.get()
        gender = var_gender.get()

        if not all([username, password, first_name, last_name, email, age, gender]):
            messagebox.showwarning("Registration", "All fields are required!")
            return
        
        sql = 'INSERT INTO data (username, password, first_name, last_name, email, age, gender) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        values = (username, password, first_name, last_name, email, age, gender)
        mycursor.execute(sql, values)
        mysqldb.commit()
        messagebox.showinfo("Registration", "Registration Successful!")
        register_window.destroy()
    except mysql.connector.Error as error:
        messagebox.showerror("Registration", f"Error Encountered: {error}")

def reg():
    global register_window, username_entry, password_entry, firstname_entry, lastname_entry, email_entry, age_combobox, var_gender
    
    register_window = Toplevel(root)  # Use Toplevel instead of Tk.Toplevel
    register_window.title("Registration Form")
    register_window.geometry("500x500")
    
    img = Image.open("form.png")
    img = img.resize((500, 500))
    bg_image = ImageTk.PhotoImage(img)
    
    canvas = Canvas(register_window, height=500, width=500)
    canvas.pack()
    canvas.create_image(0, 0, anchor=NW, image=bg_image)
    
    sign_in_label = Label(register_window, text="Sign Up", fg="black", font=("Comic Sans MS", 18, "bold"))
    sign_in_label.place(x=250, y=30, anchor="center")
    
    labels = ['Username', 'Password', 'First Name', 'Last Name', 'Email', 'Age', 'Gender']
    entries = []
    
    for i, label in enumerate(labels, 1):
        Label(register_window, text=label, fg="black", font=("Comic Sans MS", 12, "bold")).place(x=50, y=50 + 30 * i)
        entry = Entry(register_window, font=("Comic Sans MS", 12))
        entry.place(x=170, y=50 + 30 * i, width=170)
        entries.append(entry)
        
    # Unpack entries
    username_entry, password_entry, firstname_entry, lastname_entry, email_entry, age_combobox = entries[:6]
    
    var_gender = StringVar()
    Radiobutton(register_window, text="Male", variable=var_gender, value="Male").place(x=170, y=290)
    Radiobutton(register_window, text="Female", variable=var_gender, value="Female").place(x=230, y=290)

    # Add a Register button
    sign_up_button = Button(register_window, text="Register", command=register_user, bg="#00CDCD", fg="black", font=("Comic Sans MS", 12, "bold"))
    sign_up_button.place(x=250, y=450, anchor="center")

def check_pronunciation(target_word):
    attempts = 5
    for i in range(attempts):
        print(f"Attempt {i + 1}/{attempts}")
        speak(f"Please pronounce the word {target_word}")
        spoken_text = listen()
        if spoken_text.lower() == target_word:
            speak("You got a correct pronunciation!")
            return "Correct pronunciation!"
        else:
            speak("Incorrect pronunciation!")
            if i == attempts - 1:
                return "The attempts are over!"

def on_submit():
    target_word = entry.get()
    result = check_pronunciation(target_word)
    result_label.config(text=result)

def system_window():
    if not logged_in:
        messagebox.showwarning("Automatic Pronunciation Mistake Detector", "Please log in first!")
        return 

    global entry, result_label
    
    window = Toplevel(root)
    window.title("Automatic Pronunciation Mistake Detector")
    window.geometry("700x400")
    
    bg_image = ImageTk.PhotoImage(Image.open("Mic.jpg"))
    background_label = Label(window, image=bg_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    label = Label(window, text="Enter a word to check pronunciation", font=("Arial", 18), bg="darkred")
    label.place(x=100, y=100)
    
    entry = Entry(window, width=30, font=("Arial", 15))
    entry.place(x=140, y=165)
    
    submit_button = Button(window, text="Submit", command=on_submit, bg="darkred", fg="white", font=("Arial", 16))
    submit_button.place(x=300, y=250)
    
    result_label = Label(window, text="", font=("Arial", 25), bg="blue")
    result_label.place(x=200, y=400)

    window.mainloop()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return ""

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

# Main GUI Setup
root = Tk()
root.title("Log In")
root.geometry("1080x720")
root.config(bg="white")

# Add image/icon (ensure the image paths are correct)
image_icon = Image.open("UserIcon.jpeg")
image_icon = ImageTk.PhotoImage(image_icon)  # Use ImageTk for Pillow-loaded images
root.iconphoto(False, image_icon)

profile_image = Image.open("Kemee.png")
profile_image = ImageTk.PhotoImage(profile_image)  # Use ImageTk for Pillow-loaded images

# Align the profile image and the form using 'place' method
Label(root, image=profile_image, bg="white").place(x=50, y=50, height=700, width=500)
  # Adjust the x and y values to position the image
  
# Create a frame to act as a border
border_frame = Frame(root, bg="white", highlightbackground="blue", highlightthickness=2)
border_frame.place(x=50, y=50, height=600, width=500)

# Place the label inside the frame
Label(border_frame, image=profile_image, bg="white").pack(fill="both", expand=True)  

# Create a frame for the login form and align it
frame = Frame(root, width=350, height=350, bg="#2a9df4")
frame.place(x=600, y=180)  # Adjust the x and y values to position the form next to the image

label = Label(frame, text="Log In", fg='black', bg='#2a9df4', font=('Comic Sans MS', 13))
label.place(x=150, y=30, height=50, width=50)

# Username Entry
usernameEntry = Entry(frame, width=25, fg="black", bg="#FF8303", font=('Comic Sans MS', 13))
usernameEntry.place(x=30, y=90)

# Password Entry
password_entry = Entry(frame, width=20, fg="black", bg="#FF8303", font=('Comic Sans MS', 10), show='*')
password_entry.place(x=30, y=120)

password_entry.bind('<FocusIn>', lambda e: password_entry.delete(0, 'end'))

# Show/Hide Password Button
show_password_button = Button(frame, text='Show', bg='#FFE761', fg='black', command=toggle_password_visibility)
show_password_button.place(x=200, y=120, height=25, width=85)

# Log In Button
Button(frame, text='Log In', bg='#FFE761', command=pythonlogin).place(x=88, y=185, width=200)

label = Label(frame, text="Not have an account?", fg='black', bg='#2a9df4', font=('Comic Sans MS', 11))
label.place(x=40, y=150)

# Sign Up Button
Button(frame, text='Sign Up', command=reg, width=6, bg='#FFE761').place(x=200, y=153, width=85)

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)  # Insert placeholder text by default
    entry.config(fg='black')  # Set the initial text color to grey to indicate placeholder

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")  # Clear the placeholder text
            entry.config(fg='black')  # Change text color to black

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder_text)  # Restore the placeholder text if the field is empty
            entry.config(fg='black')  # Set color back to black

    # Bind the events to the entry widget
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Create the Entry widget
usernameEntry = Entry(frame, width=25, fg="black", bg="#FF8303", font=('Comic Sans MS', 12))
usernameEntry.place(x=30, y=90)

# Add the placeholder functionality
add_placeholder(usernameEntry, "Enter your username")

# Create the password Entry widget
password_entry = Entry(frame, width=20, fg="black", bg="#FF8303", font=('Comic Sans MS', 10), show='*')
password_entry.place(x=30, y=120)

# Add the placeholder functionality for password
add_placeholder(password_entry, "Enter your password")

root.mainloop()

