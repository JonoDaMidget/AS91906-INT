from tkinter import Tk, Entry, Label, Frame, Button, messagebox
from tkinter.simpledialog import askstring
import re

# Defining button functions to switch between frames

def goLogin():
    login_frame.grid(row = 0, column = 0, height = 100)
    home_frame.grid_forget()
    task_frame.grid_forget()
    shop_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()
    login_error.config(text = '') # Resets error message upon returning to login screen

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

    # Hide Full E-mail, only display ending 3 characters + domain
    email = user_entry.get()
    hidden_email = []
    location = email.find('@')
    location -= 3
    if location < 0:
        location = 0

    for i in range(len(email) - location):
        hidden_email.append(email[location + i])

    display2 = ''.join(hidden_email)
    # Reconfigures email which appear on settings screen
    email_label.config(text = f'Email: *****{display2}') 

def toggleShow():
    if pass_entry.cget('show') == '\u2022': # If password text is hidden, show
        pass_entry.config(show = '')
    else:
        pass_entry.config(show = '\u2022') # Else, hide

# Login Functions

def checkDetails():
    if user_entry.get() == '':
        login_error.config(text='Please enter an e-mail')
        return
    else:
        email = user_entry.get()
    if pass_entry.get() == '':
        login_error.config(text='Please enter a password')
        return
    else:
        password = pass_entry.get()
    file = open('account_details.csv', 'r')
    next(file) # Skip first line
    for line in file:
        item = line.split(',')
        if email == item[0].strip() and password == item[1].strip():
            goHome()
        else:
            login_error.config(text='Incorrect username or password')

def signup():
    # Defining Regex
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    file = open('account_details.csv', 'r')
    new_email = askstring('Email', 'What is your email')
    for line in file:
        item = line.split(',')
        if new_email == item[0]:
            messagebox.showerror('Error', 'This e-mail has already been registered.')
            file.close()
            return
        elif (re.fullmatch(email_regex, new_email)): # If matches regex
            pass
        else:
            messagebox.showerror('Error', 'Please enter a valid e-mail.')
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

# Defining Search Function
def match_search():
    found_results = []
    found = False # Used to check if any results were found
    file = open('plant_data.csv', 'r')
    next(file)
    search = search_entry.get()
    search = search.strip().lower()
    search = re.sub(r'[^\w]', '', search)
    for line in file: # Search for best matches first
        line = line.strip()
        item = line.split(', ')
        lower_list = [x.lower() for x in item] # List Comprehension to lower case
        regex_list = [re.sub(r'[^\w]', '', x) for x in lower_list] # List Comprehension to remove symbols
        s1_list = list(regex_list[::3]) # Only searches common names
        if any(search in a for a in s1_list):
            found_results.append(item[0])
            found = True
    file.seek(0)
    for line in file: # Search for other names after
        line = line.strip()
        item = line.split(', ')
        lower_list = [x.lower() for x in item]
        regex_list = [re.sub(r'[^\w]', '', x) for x in lower_list]
        s1_list = list(regex_list[::3])
        s2_list = list(regex_list[1:3])
        # Don't include duplicate searches
        if any(search in b for b in s2_list) and not any(search in a for a in s1_list):
            found_results.append(item[0])
            found = True
    if found == False:
        print(f'No results found for "{search_entry.get()}", if you cannot find your plant, please file a ticket!')

    # Iterate through searches

    active_button_num = 0 # Selects which button to config
    page_number = 1 # Ensures only displays results in order from start

    search_result_1.grid_forget() # Forgetting grid so will not show previous search results
    search_result_2.grid_forget() # if not enough results to fill
    search_result_3.grid_forget()
    search_result_4.grid_forget()

    previous_add.grid(row = 23, column = 0, rowspan = 10)
    next_add.grid(row = 23, column = 9, rowspan = 10)

    while active_button_num < len(found_results) and page_number > 0:
        if active_button_num%4 == 0:
            search_result_1.grid(row = 15, column = 2, rowspan = 10, columnspan = 3)
            search_result_1.config(text = f'{found_results[active_button_num]}')
            active_button_num += 1
            page_number -= 1/4
        elif active_button_num%4 == 1:
            search_result_2.grid(row = 15, column = 5, rowspan = 10, columnspan = 3)
            search_result_2.config(text = f'{found_results[active_button_num]}')
            active_button_num += 1
            page_number -= 1/4
        elif active_button_num%4 == 2:
            search_result_3.grid(row = 30, column = 2, rowspan = 10, columnspan = 3)
            search_result_3.config(text = f'{found_results[active_button_num]}')
            active_button_num += 1
            page_number -= 1/4
        elif active_button_num%4 == 3:
            search_result_4.grid(row = 30, column = 5, rowspan = 10, columnspan = 3)
            search_result_4.config(text = f'{found_results[active_button_num]}')
            active_button_num += 1
            page_number -= 1/4
        else:
            messagebox.showerror('Error', 'Error Loading Results')
            # Accounting for error

def next_search():
    page_number += 1

def prev_search():
    page_number -= 1

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


title_label = Label(login_frame, text='App Logo', font = ('Arial', 35))
title_label.grid(row = 5, column = 17, columnspan=15, rowspan = 4)

user_label = Label(login_frame, text = 'Email:')
user_label.grid(row = 25, column = 23, columnspan = 5, sticky = 'W')
user_entry = Entry(login_frame, width = 30)
user_entry.grid(row = 26, column = 23, columnspan = 5)

pass_label = Label(login_frame, text = 'Password:')
pass_label.grid(row = 30, column = 23, columnspan = 5, sticky = 'W')
pass_entry = Entry(login_frame, show='\u2022', width = 30) # Show function hides inputs
pass_entry.grid(row = 31, column = 23, columnspan = 5)

toggle_pass = Button(login_frame, text = "Icon", command = toggleShow)
toggle_pass.grid(row = 31, column = 28)

login_button = Button(login_frame, text = "Login", command = checkDetails)
login_button.grid(row = 35, column = 25)

signup_button = Button(login_frame, text = 'Don\'t Have an Account?', command = signup)
signup_button.grid(row = 40, column = 25)

login_error = Label(login_frame, text = '', fg='red')
login_error.grid(row = 32, column = 23, columnspan = 7, sticky = 'W')

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

plants_h1 = Label(home_frame, text = 'Common Name', font = 'Arial, 20')
plants_h1.grid(row = 10, column = 3, columnspan = 5, rowspan = 2)
plants_h2 = Label(home_frame, text = 'Scientific Name', fg = '#8a8a8a')
plants_h2.grid(row = 12, column = 4)

plants_button = Button(home_frame, text = 'Owned Plants', height = 2)
plants_button.grid(row = 40, column = 4)

# Add Frame

for col in range(colcount): # Configure grid size
    add_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    add_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(add_frame, text = 'Add', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white') # Move all buttons to function in iter 2

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

search_entry = Entry(add_frame, width = 36, bg = '#F0F0ED')
search_entry.grid(row = 7, column = 3, columnspan = 4, sticky = 'W')
search_button = Button(add_frame, text = 'Search', command = match_search)
search_button.grid(row = 7, column = 2, sticky = 'E')

search_result_1 = Button(add_frame, width = 15, height = 10, text = 'Placeholder 1')
search_result_2 = Button(add_frame, width = 15, height = 10, text = 'Placeholder 2')
search_result_3 = Button(add_frame, width = 15, height = 10, text = 'Placeholder 3')
search_result_4 = Button(add_frame, width = 15, height = 10, text = 'Placeholder 4')

previous_add = Button(add_frame, text = '<', height = 5, command = prev_search)
next_add = Button(add_frame, text = '>', height = 5, command = next_search)

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

tasks_button = Button(task_frame, text = 'Daily Tasks', bg = '#9AB752', fg = 'white',
                     activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')
tasks_button.grid(row = 20, column = 0, columnspan = 10, rowspan = 5)

streak_button = Button(task_frame, text = 'Login Rewards', bg = '#9AB752', fg = 'white',
                     activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')
streak_button.grid(row = 40, column = 0, columnspan = 10, rowspan = 5)

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

pfp_placehold = Button(settings_frame, text = 'Profile Picture', height = 8, width = 16)
pfp_placehold.grid(row = 4, column = 1, rowspan = 15, columnspan = 4)

email_label = Label(settings_frame, text = 'Error: E-mail not found')
email_label.grid(row = 7, column = 5, columnspan = 3, sticky = 'w')

pass_label = Label(settings_frame, text = 'Password: ' + '\u2022' * 8)
pass_label.grid(row = 9, column = 5, columnspan = 3, sticky = 'w')

change_pass = Button(settings_frame, text = 'Edit')
change_pass.grid(row = 9, column = 8, sticky = 'w')

logout_button  = Button(settings_frame, text = 'Logout', bg = 'red', fg = 'white', width = 20, font = 'Arial, 10', command = goLogin)
logout_button.grid(row = 60, column = 3, columnspan = 4, rowspan = 2)

root.mainloop()