from tkinter import Tk, Entry, Label, Frame, Button
import csv

# Defining button functions to switch between frames

def goLogin():
    login_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    plant_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goAdd():
    add_frame.grid(row = 0, column = 0)
    login_frame.grid_forget()
    home_frame.grid_forget()
    task_frame.grid_forget()
    plant_frame.grid_forget()
    settings_frame.grid_forget()

def goHome():
    home_frame.grid(row = 0, column = 0)
    login_frame.grid_forget()
    task_frame.grid_forget()
    plant_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goTask():
    task_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    login_frame.grid_forget()
    plant_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goPlant():
    plant_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    login_frame.grid_forget()
    settings_frame.grid_forget()
    add_frame.grid_forget()

def goSettings():
    settings_frame.grid(row = 0, column = 0)
    home_frame.grid_forget()
    task_frame.grid_forget()
    plant_frame.grid_forget()
    login_frame.grid_forget()
    add_frame.grid_forget()

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
appwidth = int(screenwidth/2.77)
appheight = screenheight
colcount = int(appwidth/6)
rowcount = int(appheight/10)

root.maxsize(appwidth, screenheight)
root.minsize(appwidth, screenheight)
login_frame = Frame(root)
home_frame = Frame(root)
task_frame = Frame(root)
plant_frame = Frame(root)
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

user_label = Label(login_frame, text = '     Username:') # Spaces line up text with input box
user_label.grid(row = 25, column = 20, columnspan = 5)
user_entry = Entry(login_frame, width = 30)
user_entry.grid(row = 26, column = 23, columnspan = 5)

pass_label = Label(login_frame, text = '     Password:')
pass_label.grid(row = 30, column = 20, columnspan = 5)
pass_entry = Entry(login_frame, show='\u2022', width = 30) # Show function hides inputs
pass_entry.grid(row = 31, column = 23, columnspan = 5)

toggle_pass = Button(login_frame, text = "Icon", command = toggleShow)
toggle_pass.grid(row = 31, column = 28)

login_button = Button(login_frame, text = "Login", command = goHome)
login_button.grid(row = 41, column = 25)

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

topnav_plant = Button(home_frame, text = 'Plants', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goPlant)
topnav_plant.grid(row = 4, column = 2, columnspan=2, sticky = 'w')

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

left_button = Button(home_frame, text = '<', height = 5, command=print('Debug: Switch to left')) # Swaps sprite
left_button.grid(row = 25, column = 0, rowspan = 2)
right_button = Button(home_frame, text = '>', height = 5, command=print('Debug: Switch to right')) # Swaps sprite
right_button.grid(row = 25, column = 9, rowspan = 2)

# Add Frame

for col in range(colcount): # Configure grid size
    add_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    add_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(add_frame, text = 'Add', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white')

topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_plant = Button(add_frame, text = 'Plants', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goPlant)
topnav_plant.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(add_frame, text = 'Home', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goHome)
topnav_home.grid(row = 0, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(add_frame, text = 'Tasks', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goTask)
topnav_tasks.grid(row = 0, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(add_frame, text = 'Settings', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goSettings)
topnav_settings.grid(row = 0, column = 8, columnspan=2, sticky = 'w')

# Plant Frame

for col in range(colcount): # Configure grid size
    plant_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    plant_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(plant_frame, text = 'Add', width = 12, height = 1, 
                    fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goAdd)

topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_plant = Button(plant_frame, text = 'Plants', width = 12, height = 1, 
                     bg = '#9AB752', relief = 'sunken', state = 'disabled', disabledforeground = 'white')
topnav_plant.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

topnav_home = Button(plant_frame, text = 'Home', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goHome)
topnav_home.grid(row = 0, column = 4, columnspan = 2, sticky = 'w')

topnav_tasks = Button(plant_frame, text = 'Tasks', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goTask)
topnav_tasks.grid(row = 0, column = 6, columnspan=2, sticky = 'w')

topnav_settings = Button(plant_frame, text = 'Settings', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goSettings)
topnav_settings.grid(row = 0, column = 8, columnspan=2, sticky = 'w')

# Task Frame

for col in range(colcount): # Configure grid size
    task_frame.grid_columnconfigure(col, minsize=6, weight=1)

for row in range(rowcount):
    task_frame.grid_rowconfigure(row, minsize=10, weight=1)

topnav_add = Button(task_frame, text = 'Add', width = 12, height = 1, 
                    fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goAdd)
topnav_add.grid(row = 0, column = 0, columnspan=2, sticky='w')

topnav_plant = Button(task_frame, text = 'Plants', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goPlant)
topnav_plant.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

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

topnav_plant = Button(settings_frame, text = 'Plants', width = 12, height = 1,
                        fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', activeforeground = '#9AB752', command = goPlant)
topnav_plant.grid(row = 0, column = 2, columnspan=2, sticky = 'w')

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