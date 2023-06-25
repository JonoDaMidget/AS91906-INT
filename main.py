from tkinter import Tk, Entry, Label, Frame, Button, messagebox
from tkinter.simpledialog import askstring
import csv

# Defining button functions to switch between frames

def goLogin():
    login_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    shop_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goAdd():
    add_frame.grid(row = 0, column = 0)
    login_frame.grid_forget()
    home_frame.grid_forget()
    task_frame.grid_forget()
    shop_frame.grid_forget()
    settings_frame.grid_forget()

def goHome():
    home_frame.grid(row = 0, column = 0)
    login_frame.grid_forget()
    task_frame.grid_forget()
    shop_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goTask():
    task_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    login_frame.grid_forget()
    shop_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goShop():
    shop_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    login_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goSettings():
    settings_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    shop_frame.grid_forget()
    login_frame.grid_forget()
    add_frame.grid_forget()

def toggleShow():
    if pass_entry.cget('show') == '\u2022': # If password text is hidden, show
        pass_entry.config(show = '')
    else:
        pass_entry.config(show = '\u2022') # Else, hide

# Login Functions

def checkDetails():
    if user_entry.get() == '':
        print('Please enter an e-mail')
        return
    else:
        email = user_entry.get()
    if pass_entry.get() == '':
        print('Please enter a password')
        return
    else:
        password = pass_entry.get()
    file = open('account_details.csv', 'r')
    next(file) # Skip first line
    for line in file:
        item = line.split(',')
        if email == item[0] and password == item[1]:
            goHome()
        else:
            print('Incorrect username or password')

def signup():
    file = open('account_details.csv', 'r')
    new_email = askstring('Email', 'What is your email')
    for line in file:
        item = line.split(',')
        if new_email == item[0]:
            messagebox.showerror('Error', 'This e-mail has already been registered.')
            file.close()
            return
    while True:
        new_password = askstring('Password', 'Please enter a password')
        if len(new_password) < 8:
            messagebox.showerror('Error', 'Please enter a password longer than 8 characters')
            continue
        else:
            break
    file = open('account_details.csv', 'a')
    new_info = '\n' + new_email + ',' + new_password
    file.write(new_info)
    file.close()

# Setting up window states and Frames
root = Tk()
root.title('CBT')
# Set geometry of window
screenheight = root.winfo_screenheight()
screenwidth = root.winfo_screenwidth()
appwidth = int(screenwidth/2.77)
appheight = screenheight
colcount = int(appwidth/6)
rowcount = int(appheight/10)

root.maxsize(appwidth, screenheight)
root.minsize(appwidth, screenheight)
login_frame = Frame(root)
home_frame = Frame(root)
task_frame = Frame(root)
shop_frame = Frame(root)
settings_frame = Frame(root)
add_frame = Frame(root)

# Login Frame
login_frame.grid(row = 0, column = 0) # Open login frame on launch

for col in range(colcount): # Configure grid size
    login_frame.grid_columnconfigure(col, minsize=6, weight=1) # Weight sets the grid cells to not change

for row in range(rowcount):
    login_frame.grid_rowconfigure(row, minsize=10, weight=1)


title_label = Label(login_frame, text='App', font = ('Arial', 35))
title_label.grid(row = 5, column = 17, columnspan=15, rowspan = 10)

user_label = Label(login_frame, text = 'Email:')
user_label.grid(row = 25, column = 20, columnspan = 5)
user_entry = Entry(login_frame, width = 30)
user_entry.grid(row = 26, column = 23, columnspan = 5)

pass_label = Label(login_frame, text = 'Password:')
pass_label.grid(row = 30, column = 20, columnspan = 5, sticky = 'E')
pass_entry = Entry(login_frame, show='\u2022', width = 30) # Show function hides inputs
pass_entry.grid(row = 31, column = 23, columnspan = 5)

toggle_pass = Button(login_frame, text = "Icon", command = toggleShow)
toggle_pass.grid(row = 31, column = 28)

login_button = Button(login_frame, text = "Login", command = checkDetails)
login_button.grid(row = 35, column = 25)

signup_button = Button(login_frame, text = 'Sign Up', command = signup)
signup_button.grid(row = 40, column = 25)

# Home Frame

for col in range(colcount): # Configure grid size
    home_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    home_frame.grid_rowconfigure(row, minsize=10, weight=1)

weather_label = Label(home_frame, text = 'Weather Placehold', font = 'Arial, 24') 
weather_label.grid(row = 0, column = 0, columnspan=71, rowspan=4, sticky='w')

topnav_add = Button(home_frame, text = 'Add', width = 12, height = 1, 
                    fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goAdd)

topnav_add.grid(row = 4, column = 0, columnspan=2, sticky='w')

topnav_shop = Button(home_frame, text = 'Shop', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goShop)
topnav_shop.grid(row = 4, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(home_frame, text = 'Home', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white') # Disabled because it is active frame
topnav_home.grid(row = 4, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(home_frame, text = 'Tasks', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goTask)
topnav_tasks.grid(row = 4, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(home_frame, text = 'Settings', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goSettings)
topnav_settings.grid(row = 4, column = 8, columnspan=2, sticky = 'w')

main_sprite = Label(home_frame, text = 'Image \nPlacehold', font = 'Arial, 45')
main_sprite.grid(row = 25, column = 3, rowspan = 2, columnspan=5)

left_button = Button(home_frame, text = '<', height = 5) # Swaps sprite
left_button.grid(row = 25, column = 0, rowspan = 2)
right_button = Button(home_frame, text = '>', height = 5) # Swaps sprite
right_button.grid(row = 25, column = 9, rowspan = 2)

# Add Frame

for col in range(colcount): # Configure grid size
    add_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    add_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(add_frame, text = 'Add', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white')

topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_shop = Button(add_frame, text = 'Shop', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goShop)
topnav_shop.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(add_frame, text = 'Home', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goHome)
topnav_home.grid(row = 0, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(add_frame, text = 'Tasks', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goTask)
topnav_tasks.grid(row = 0, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(add_frame, text = 'Settings', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goSettings)
topnav_settings.grid(row = 0, column = 8, columnspan=2, sticky = 'w')

# Shop Frame

for col in range(colcount): # Configure grid size
    shop_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    shop_frame.grid_rowconfigure(row, minsize=10, weight=1)


topnav_add = Button(shop_frame, text = 'Add', width = 12, height = 1, 
                    fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goAdd)

topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_shop = Button(shop_frame, text = 'Shop', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white')
topnav_shop.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(shop_frame, text = 'Home', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goHome)
topnav_home.grid(row = 0, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(shop_frame, text = 'Tasks', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goTask)
topnav_tasks.grid(row = 0, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(shop_frame, text = 'Settings', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goSettings)
topnav_settings.grid(row = 0, column = 8, columnspan=2, sticky = 'w')

currency_label = Button(shop_frame, text = 'Money\nPlacehold')
currency_label.grid(row = 2, column = 8, rowspan = 2, sticky  = 'E')

pots_button = Button(shop_frame, text = 'Pot Designs', bg = '#9AB752', fg = 'white',
                     activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')
pots_button.grid(row = 20, column = 0, columnspan = 10, rowspan = 5)

furniture_button = Button(shop_frame, text = 'Furniture Sets', bg = '#9AB752', fg = 'white',
                     activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')
furniture_button.grid(row = 40, column = 0, columnspan = 10, rowspan = 5)


# Task Frame

for col in range(colcount): # Configure grid size
    task_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    task_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(task_frame, text = 'Add', width = 12, height = 1, 
                    fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goAdd)
topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_shop = Button(task_frame, text = 'Shop', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goShop)
topnav_shop.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(task_frame, text = 'Home', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goHome)
topnav_home.grid(row = 0, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(task_frame, text = 'Tasks', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white')
topnav_tasks.grid(row = 0, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(task_frame, text = 'Settings', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goSettings)
topnav_settings.grid(row = 0, column = 8, columnspan=2, sticky = 'w')

# Settings Frame

for col in range(colcount): # Configure grid size
    settings_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    settings_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(settings_frame, text = 'Add', width = 12, height = 1, 
                    fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goAdd)

topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_shop = Button(settings_frame, text = 'Shop', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goShop)
topnav_shop.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(settings_frame, text = 'Home', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goHome)
topnav_home.grid(row = 0, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(settings_frame, text = 'Tasks', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goTask)
topnav_tasks.grid(row = 0, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(settings_frame, text = 'Settings', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white')
topnav_settings.grid(row = 0, column = 8, columnspan=2, sticky = 'w')

logout_button  = Button(settings_frame, text = 'Logout', bg = 'red', fg = 'white', width = 20, font = 'Arial, 10', command = goLogin)
logout_button.grid(row = 60, column = 3, columnspan = 4, rowspan = 2)

root.mainloop()