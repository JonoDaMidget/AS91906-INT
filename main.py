from tkinter import Tk, Entry, Label, Frame, Button
import csv

# Defining button functions to switch between frames

def goLogin():
    login_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    streak_frame.grid_forget()
    settings_frame.grid_forget()

def goHome():
    home_frame.grid(row = 0, column = 0)
    login_frame.grid_forget()
    task_frame.grid_forget()
    streak_frame.grid_forget()
    settings_frame.grid_forget()

def goTask():
    task_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    login_frame.grid_forget()
    streak_frame.grid_forget()
    settings_frame.grid_forget()

def goStreak():
    streak_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    login_frame.grid_forget()
    settings_frame.grid_forget()

def goSettings():
    settings_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    streak_frame.grid_forget()
    login_frame.grid_forget()

def toggleShow():
    if pass_entry.cget('show') == '\u2022': # If password text is hidden, show
        pass_entry.config(show = '')
    else:
        pass_entry.config(show = '\u2022') # Else, hide


# Setting up window states and Frames
root = Tk()
root.title('CBT')
# Set geometry of window
screenheight = root.winfo_screenheight()
screenwidth = root.winfo_screenwidth()
appwidth = int(screenwidth/3)
appheight = screenheight
colcount = int(appwidth/6)
rowcount = int(appheight/10)

root.geometry(f'{appwidth}x{screenheight}+{int(screenwidth/2-appwidth/2)}+{0}') # Launch app centered
root.maxsize(appwidth, screenheight)
root.minsize(appwidth, screenheight)
login_frame = Frame(root)
home_frame = Frame(root)
task_frame = Frame(root)
streak_frame = Frame(root)
settings_frame = Frame(root)

# Login Frame
login_frame.grid(row = 0, column = 0) # Open login frame on launch

for col in range(colcount): # Configure grid size
    login_frame.grid_columnconfigure(col, minsize=6, weight=1) # Weight sets the grid cells to not change

for row in range(rowcount):
    login_frame.grid_rowconfigure(row, minsize=10, weight=1)


title_label = Label(login_frame, text='App', font = ('Arial', 35))
title_label.grid(row = 5, column = 13, columnspan=15, rowspan = 10)

user_label = Label(login_frame, text = 'Username:')
user_label.grid(row = 25, column = 16, columnspan = 5)
user_entry = Entry(login_frame, width = 30)
user_entry.grid(row = 26, column = 19, columnspan = 5)

pass_label = Label(login_frame, text = 'Password:')
pass_label.grid(row = 30, column = 16, columnspan = 5)
pass_entry = Entry(login_frame, show='\u2022', width = 30) # Show function hides inputs
pass_entry.grid(row = 31, column = 19, columnspan = 5)

toggle_pass = Button(login_frame, text = "Icon", command = toggleShow)
toggle_pass.grid(row = 31, column = 24)

login_button = Button(login_frame, text = "Login", command = goHome)
login_button.grid(row = 41, column = 21)


root.mainloop()