"""This file runs the main program.
Current iteration accesses database to display user information, track added plants.
Also provides currency and streak functions.
Displays current weather."""

from tkinter import Tk, Entry, Label, Frame, Button, messagebox
from tkinter.ttk import Combobox
from tkinter.simpledialog import askstring
import re
try:  # Only runs if access granted
    from weather_module import temperature, humidity, weather
except ImportError:
    pass
from datetime import datetime, timedelta
from PIL import Image, ImageTk
import csv


class Windows(Tk):
    """Control frame to switch frames.
    Define show frame method and frame specific interactions."""
    # *args **kwargs in case other params passed in.

    def __init__(self, *args, **kwargs):
        """Create frame, attributes, dictionary for frame."""

        Tk.__init__(self, *args, **kwargs)
        self.wm_title('Blossom')
        container = Frame(self, height=690, width=462)
        container.grid(row=0, column=0)
        self.resizable(False, False)
        self.maxsize(462, 690)
        self.minsize(462, 690)
        # Create dictionary to select out frame variable to use
        self.frames = {}
        for i in (login_frame, home_frame, task_frame,
                  shop_frame, settings_frame, add_frame,
                  streak_frame, daily_frame, plant_info_frame,
                  loading_frame):
            frame = i(container, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky='nesw')

        self.show_frame(login_frame)

    def show_frame(self, control):
        """Raise selected frame to top level."""
        frame = self.frames[control]
        frame.tkraise()

        for row in range(690):
            frame.grid_rowconfigure(row, minsize=1, weight=1)

        # Frame interactions
        if str(frame) == '.!frame.!settings_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[settings_frame]
            hidden_email = []
            location = email.find('@')
            location -= 3
            if location < 0:
                location = 0
            for i in range(len(email) - location):
                hidden_email.append(email[location + i])
                self.display2 = ''.join(hidden_email)
            # Reconfigures email which appear on settings screen
            frame.email_label.config(text=f'Email: *****{self.display2}')

        elif str(frame) == '.!frame.!login_frame':
            frame.login_error.config(text='')

        elif str(frame) == '.!frame.!task_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email
            frame.retrieve_data()
            streak = frame.current_streak
            frame.streak_label.config(text=streak)
            frame.claim_button.config(
                text="          Claim Today's Daily Reward        ",
                state='active', relief='raised')
            frame.streak_info_label.config(text='')
            frame = self.frames[task_frame]

        elif str(frame) == '.!frame.!streak_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email
            frame.retrieve_data()
            streak = frame.current_streak
            frame.streak_label.config(text=streak)
            frame.claim_button.config(
                text="        Claim Today's Daily Reward        ",
                state='active', relief='raised')

        elif str(frame) == '.!frame.!shop_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email
            frame.retrieve_data()
            currency = frame.currency
            frame = self.frames[shop_frame]
            frame.currency_label.config(text=f'{currency} Leaves')

        elif str(frame) == '.!frame.!home_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email
            # In case sign up, reread csv.
            frame.read_csv_file()
            frame.retrieve_data()
            if frame.plant1 != '':
                control_plant1 = frame.plant1
            else:
                control_plant1 = ''
            if frame.plant2 != '':
                control_plant2 = frame.plant2
            else:
                control_plant2 = ''
            if frame.plant3 != '':
                control_plant3 = frame.plant3
            else:
                control_plant3 = ''
            frame = self.frames[daily_frame]
            frame.combo_plant1 = control_plant1
            frame.combo_plant2 = control_plant2
            frame.combo_plant3 = control_plant3
            control_list = frame.plant_list_combo
            frame.set_combo()
            frame = self.frames[home_frame]
            frame.plant1_h2 = control_plant1
            frame.plant2_h2 = control_plant2
            frame.plant3_h2 = control_plant3
            frame.home_list = control_list
            # Configures label
            frame.retrieve_data_home(frame.plant1_h2)

        elif str(frame) == '.!frame.!loading_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email
            # In case sign up, reread csv.
            frame.read_csv_file()
            frame.retrieve_data()
            if frame.plant1 != '':
                control_plant1 = frame.plant1
            else:
                control_plant1 = ''
            if frame.plant2 != '':
                control_plant2 = frame.plant2
            else:
                control_plant2 = ''
            if frame.plant3 != '':
                control_plant3 = frame.plant3
            else:
                control_plant3 = ''
            frame = self.frames[daily_frame]
            frame.combo_plant1 = control_plant1
            frame.combo_plant2 = control_plant2
            frame.combo_plant3 = control_plant3
            control_list = frame.plant_list_combo
            frame.set_combo()
            frame = self.frames[home_frame]
            frame.plant1_h2 = control_plant1
            frame.plant2_h2 = control_plant2
            frame.plant3_h2 = control_plant3
            frame.home_list = control_list
            # Configures label
            frame.retrieve_data_home(frame.plant1_h2)
            frame = self.frames[loading_frame]

        elif str(frame) == '.!frame.!daily_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email
            # In case sign up, reread csv.
            frame.read_csv_file()
            frame.retrieve_data()
            control_plant1 = frame.plant1
            control_plant2 = frame.plant2
            control_plant3 = frame.plant3
            frame = self.frames[daily_frame]
            frame.combo_plant1 = control_plant1
            frame.combo_plant2 = control_plant2
            frame.combo_plant3 = control_plant3
            frame.set_combo()

        elif str(frame) == '.!frame.!plant_info_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[add_frame]
            full_info_list = frame.found_full
            if frame.which_button_pressed == 1:
                selected_plant = frame.plant_id1
            elif frame.which_button_pressed == 2:
                selected_plant = frame.plant_id2
            elif frame.which_button_pressed == 3:
                selected_plant = frame.plant_id3
            elif frame.which_button_pressed == 4:
                selected_plant = frame.plant_id4
            else:
                return
            frame = self.frames[plant_info_frame]
            frame.plant_list = full_info_list
            # +1 to account for header row
            frame.plant_row = selected_plant
            frame.retrieve_plant()
            frame.row_value = email


class loading_frame(Frame):
    """Configure account settings in between frames.
    Create launch button to move to home frame."""

    def __init__(self, parent, control_frame):
        """Create widgets."""

        Frame.__init__(self, parent)
        for col in range(100):
            self.grid_columnconfigure(col, minsize=1, weight=1)
        for row in range(300):
            self.grid_columnconfigure(row, minsize=1, weight=1)

        self.launch_button = Button(self, text='Launch', fg='white',
                                    bg='#9AB752', borderwidth=1,
                                    height=3, width=24,
                                    activebackground='#F0F0ED',
                                    activeforeground='#9AB752',
                                    command=lambda: control_frame.show_frame(home_frame)
                                    )
        self.launch_button.grid(row=270, column=80)


class login_frame(Frame):
    """Create login frame.
    Define login methods and sign up methods."""

    def __init__(self, parent, control_frame):
        """Create widgets."""

        Frame.__init__(self, parent)
        for col in range(100):
            self.grid_columnconfigure(col, minsize=5, weight=1)

        # Define logo object and resize
        logo_image = Image.open('logo.png')
        resize_logo  =  logo_image.resize((200,95))
        logo_photo  =  ImageTk.PhotoImage(resize_logo)
        
        title_label = Label(self, text='', image=logo_photo)
        title_label.image = logo_photo
        title_label.grid(row=95, column=18, rowspan=59, columnspan=20)
        self.user_label = Label(self, text='Email:')
        self.user_label.grid(row=250, column=28, rowspan=21, columnspan=6, sticky='w')
        self.user_entry = Entry(self, width=30)
        self.user_entry.grid(row=271, column=28, rowspan=21, columnspan=6, sticky='w')

        self.pass_label = Label(self, text='Password:')
        self.pass_label.grid(row=312, column=28, rowspan=21, columnspan=6, sticky='w')
        self.pass_entry = Entry(self, show='\u2022', width=30) # Show function hides inputs
        self.pass_entry.grid(row=333, column=28, rowspan=21, columnspan=6, sticky='w')

        self.toggle_pass = Button(self, text="Show", width=5, command=lambda: self.toggle_show())
        self.toggle_pass.grid(row=333, column=34, columnspan=3, rowspan=21)

        login_button = Button(self, text="Login", command=lambda: self.check_details(control_frame))
        login_button.grid(row=384, column=18, rowspan=21, columnspan=20)

        signup_button = Button(self, text='Don\'t Have an Account?', command=lambda: self.signup())
        signup_button.grid(row=441, column=18, rowspan=21, columnspan=20)

        self.login_error = Label(self, text='', fg='red')
        self.login_error.config(text='')
        self.login_error.grid(row=354, column=28, rowspan=21, columnspan=7, sticky='w')

    def signup(self):
        """Define regex and check if details match."""

        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        file = open('account_details.csv', 'r')
        new_email = askstring('Email', 'What is your email')
        for line in file:
            item = line.split(',')
            if new_email == item[0]:
                messagebox.showerror('Error', 'This e-mail has already been registered.')
                file.close()
                return
            # If matches regex of email
            elif (re.fullmatch(email_regex, new_email)):
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
        new_info = '\n' + new_email.lower() + ',' + new_password + ',100,,0,0,,,'
        # Write to new line in account detail csv
        file.write(new_info)
        messagebox.showinfo('Success!',
                            'Signed up successfully! Please restart to launch properly')
        file.close()

    def check_details(self, control_frame):
        """Check if login details match row in csv."""
        if self.user_entry.get() == '':
            self.login_error.config(text='Please enter an e-mail')
            return
        else:
            email = self.user_entry.get().lower()
        if self.pass_entry.get() == '':
            self.login_error.config(text='Please enter a password')
            return
        else:
            password = self.pass_entry.get()
        file = open('account_details.csv', 'r')
        next(file)  # Skip first line
        for line in file:
            item = line.split(',')
            if email == item[0].strip() and password == item[1].strip():
                control_frame.show_frame(loading_frame)
            else:
                self.login_error.config(text='Incorrect username or password')
    
    def toggle_show(self):
        """Create method for show/hide button."""
        # If password text is hidden, show
        if self.pass_entry.cget('show') == '\u2022':
            self.pass_entry.config(show='')
            self.toggle_pass.config(text='Hide')
        else:
            self.pass_entry.config(show='\u2022')  # Else, hide
            self.toggle_pass.config(text='Show')


class home_frame(Frame):
    """Create home frame.
    Create method to display image
    Create method to retrieve user data
    Create method to swap between plants."""

    def __init__(self, parent, control_frame):
        """Create widgets."""

        Frame.__init__(self, parent)
        try:
            weather_label = Label(self, text=f'{weather}, {temperature}°C, {humidity}%', font='Arial, 24')
        except NameError:
            weather_label = Label(self, text='Service not connected', font='Arial, 24')
        weather_label.grid(row=0, column=0, columnspan=71, rowspan=44, sticky='w')

        topnav_add = Button(self, text='Add', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED', 
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row=45, column=0, columnspan=2, rowspan=24, sticky='nw')

        topnav_shop = Button(self, text='Shop', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED', 
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row=45, column=2, columnspan=2, rowspan=24, sticky='nw')

        topnav_home = Button(self, text='Home', width=12, height=1,
            bg='#9AB752', relief='sunken', state='disabled', 
            disabledforeground='white') # Disabled because it is active frame

        topnav_home.grid(row=45, column=4, columnspan=2, rowspan=24, sticky='nw')

        topnav_tasks = Button(self, text='Tasks', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row=45, column=6, columnspan=2, rowspan=24, sticky='nw')

        topnav_settings = Button(self, text='Settings', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(settings_frame))

        topnav_settings.grid(row=45, column=8, columnspan=2, rowspan=24, sticky='nw')

        self.main_sprite = Label(self, text='Image \nPlacehold', font='Arial, 45')
        self.main_sprite.grid(row=240, column=2, rowspan=312, columnspan=6, sticky  =  'E')

        self.left_button = Button(self, text='<', height=5, command=lambda: self.left_home()) # Swaps sprite
        self.left_button.grid(row=309, column=0, rowspan=86)
        self.right_button = Button(self, text='>', height=5, command=lambda: self.right_home()) # Swaps sprite
        self.right_button.grid(row=309, column=9, rowspan=86)

        self.plant1_h1 = None
        self.plant1_h2 = None
        self.plant2_h1 = None
        self.plant2_h2 = None
        self.plant3_h1 = None
        self.plant3_h2 = None

        self.home_list = []

        self.plant_num = 1 # Page number of home sprite

        self.plants_h1 = Label(self, text='Common Name', font='Arial, 20')
        self.plants_h1.grid(row=110, column=3, columnspan=10, rowspan=38)
        self.plants_h2 = Label(self, text='Scientific Name', fg='#8a8a8a')
        self.plants_h2.grid(row=148, column=3, rowspan=21, columnspan=5)

    def retrieve_data_home(self, plant_num):
        if self.plant1_h2 != '':
            for sublist in self.home_list:
                try:
                    sublist.index(plant_num)
                    # Finds row index of email to edit further on
                    self.row_num = self.home_list.index(sublist)

                    # Data for daily task frame:
                    self.plant1_h1 = (self.home_list[self.row_num][0])
                    # Spaces to center
                    self.plants_h1.config(text=f'{self.plant1_h1}                ')
                    self.plants_h2.config(text=f'{plant_num}              ')
                    plant_type  =  self.home_list[self.row_num][2]
                    if plant_type == 'Flower' or plant_type == 'Foliage':
                        plant_image = Image.open('plant.png')
                        resize_image = plant_image.resize((216, 312))
                        plant_photo  =  ImageTk.PhotoImage(resize_image)
                    else:
                        plant_image = Image.open('cactus.png')
                        resize_image = plant_image.resize((216, 312))
                        plant_photo  =  ImageTk.PhotoImage(resize_image)
                    self.main_sprite.config(text='', image=plant_photo)
                    self.main_sprite.image = plant_photo

                except ValueError:
                    pass # Ignores other sublists

                    self.left_button.config(text='<', relief='raised', state='active')
                    self.right_button.config(text='>', relief='raised', state='active')
        else:
            self.plants_h1.config(text='Please add a plant first            ')
            self.plants_h2.config(text='')
            self.left_button.config(text='', relief='flat', state='disabled')
            self.right_button.config(text='', relief='flat', state= 'disabled')
            self.main_sprite.config(text='', image = '')
        
    def left_home(self):
        """Move to previous plant."""

        if self.plant_num == 1 and self.plant3_h2 != '':
            self.retrieve_data_home(self.plant3_h2)
            self.plant_num = 3
            return
        elif self.plant_num == 1 and self.plant2_h2 != '':
            self.retrieve_data_home(self.plant2_h2)
            self.plant_num = 2
            return
        elif self.plant_num == 3:
            self.retrieve_data_home(self.plant2_h2)
            self.plant_num = 2
            return
        elif self.plant_num == 2:
            self.retrieve_data_home(self.plant1_h2)
            self.plant_num = 1
            return
        else:
            return

    def right_home(self):
        """Move to next plant."""

        if self.plant_num == 1 and self.plant2_h2 != '':
            self.retrieve_data_home(self.plant2_h2)
            self.plant_num = 2
            return
        elif self.plant_num == 2 and self.plant3_h2 != '':
            self.retrieve_data_home(self.plant3_h2)
            self.plant_num = 3
            return
        elif self.plant_num == 2 and self.plant3_h2 == '':
            self.retrieve_data_home(self.plant1_h2)
            self.plant_num = 1
            return
        elif self.plant_num == 3:
            self.retrieve_data_home(self.plant1_h2)
            self.plant_num = 1
            return
        else:
            return


class add_frame(Frame):
    """Create Add Frame
    Create methods to add new plants, display search results, swap between pages."""
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)
        try:
            weather_label = Label(self, text=f'{weather}, {temperature}°C, {humidity}%', font='Arial, 24')
        except NameError:
            weather_label = Label(self, text='Service not connected', font='Arial, 24')
        weather_label.grid(row=0, column=0, columnspan=71, rowspan=44, sticky='w')

        topnav_add = Button(self, text='Add', width=12, height=1, 
            bg='#9AB752', relief='sunken', state='disabled',
            disabledforeground='white') # Move all buttons to function in iter 2

        topnav_add.grid(row=45, column=0, columnspan=2, sticky='nw')

        topnav_shop = Button(self, text='Shop', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row=45, column=2, columnspan=2, sticky='nw')

        topnav_home = Button(self, text='Home', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(home_frame))
        
        topnav_home.grid(row=45, column=4, columnspan=2, sticky='nw')

        topnav_tasks = Button(self, text='Tasks', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row=45, column=6, columnspan=2, sticky='nw')

        topnav_settings = Button(self, text='Settings', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(settings_frame))

        topnav_settings.grid(row=45, column=8, columnspan=2, sticky='nw')

        self.search_entry = Entry(self, width=36, bg='#F0F0ED')
        self.search_entry.grid(row=68, column=3, columnspan=4, sticky='W', rowspan=21)
        search_button = Button(self, text='Search', command=lambda: self.match_search())
        search_button.grid(row=68, column=2, sticky='E', rowspan=21)

        self.search_error = Label(self,
            text='', fg='red')
        self.search_error.grid(row=90, column=2, rowspan=21, columnspan=6)
        # Four buttons for four search results
        self.search_result_1 = Button(self, width=15, height=10, text='Placeholder 1',
                                      command=lambda: self.search1_press(control_frame))
        self.search_result_2 = Button(self, width=15, height=10, text='Placeholder 2',
                                      command=lambda: self.search2_press(control_frame))
        self.search_result_3 = Button(self, width=15, height=10, text='Placeholder 3',
                                      command=lambda: self.search3_press(control_frame))
        self.search_result_4 = Button(self, width=15, height=10, text='Placeholder 4',
                                      command=lambda: self.search4_press(control_frame))

        self.previous_add = Button(self, text='<', height=5, command=lambda: self.prev_search())
        self.next_add = Button(self, text='>', height=5, command=lambda: self.next_search())

        # Below setting up for plant info frame
        self.found_full = []
        self.plant_id1 = None
        self.plant_id2 = None
        self.plant_id3 = None
        self.plant_id4 = None
        self.which_button_pressed = 1
    
    # Separate functions to display each different plant
    def search1_press(self, control_frame):
        self.which_button_pressed = 1
        control_frame.show_frame(plant_info_frame)

    def search2_press(self, control_frame):
        self.which_button_pressed = 2
        control_frame.show_frame(plant_info_frame)

    def search3_press(self, control_frame):
        self.which_button_pressed = 3
        control_frame.show_frame(plant_info_frame)

    def search4_press(self, control_frame):
        self.which_button_pressed = 4
        control_frame.show_frame(plant_info_frame)

    # Match search results with csv.
    def match_search(self):
        # Ensure only displays results from page 1
        self.page_number = 1
        self.found_results = []
        self.found_full = []  # Appends all details
        # Used to check if any results were found
        self.found = False
        file = open('plant_data.csv', 'r')
        next(file)
        search = self.search_entry.get()
        search = search.strip().lower()
        search = re.sub(r'[^\w]', '', search)
        for line in file: # Search for best matches first
            line = line.strip()
            item = line.split(',')
            # List Comprehension to lower case
            lower_list = [x.lower() for x in item]
            # List Comprehension to remove symbols
            regex_list = [re.sub(r'[^\w]', '', x) for x in lower_list]
            s1_list = list(regex_list[::3])  # Only searches common names
            if any(search in a for a in s1_list):
                self.found_results.append(item[0])
                self.found_full.append(item)
                self.found = True
        file.seek(0)
        for line in file:  # Search for scientific names after
            line = line.strip()
            item = line.split(',')
            lower_list = [x.lower() for x in item]
            # For each value, substitute symbols to blank via list comprehension
            # Substitute in order to match searches without correct punctuation.
            regex_list = [re.sub(r'[^\w]', '', x) for x in lower_list]
            s1_list = list(regex_list[::3])
            s2_list = list(regex_list[1:3])
            # Don't include duplicate searches
            if any(search in b for b in s2_list) and not any(search in a for a in s1_list):
                self.found_results.append(item[0])
                self.found_full.append(item)
                self.found = True
                self.search_error.config(text='')
        if self.found == False:
            self.search_error.config(
                text=f'No results found for "{self.search_entry.get()}"\n If you cannot find your plant, please file a ticket!', 
                fg='red')
        self.previous_add.grid(row=262, column=0, rowspan=86)
        self.previous_add.config(text='', state='disabled', relief='flat')
        self.next_add.grid(row=262, column=9, rowspan=86)
        self.next_add.config(text='', state='disabled', relief='flat')

        self.display_search()

    def display_search(self):
        active_button_num = 0  # Selects which button to config
        
        # Iterate through results without
        # resetting page number value
        self.page_iter = self.page_number
        
        try:
            self.found_results[self.page_number*4]
            self.next_add.config(text='>', state='active', relief='raised')
        except IndexError:
            self.next_add.config(text='', state='disabled', relief='flat')
        # Forgetting grid so will not show previous search results
        self.search_result_1.grid_forget()  # if not enough results to fill
        self.search_result_2.grid_forget()
        self.search_result_3.grid_forget()
        self.search_result_4.grid_forget()

        while active_button_num < len(self.found_results) and self.page_iter > 0:
        # Continue if there are still search results found
            if active_button_num%4 == 0:
                self.search_result_1.grid_forget()
                self.search_result_2.grid_forget()
                self.search_result_3.grid_forget()
                self.search_result_4.grid_forget()
                self.search_result_1.grid(row=117, column=2, rowspan=161, columnspan=3)
                self.search_result_1.config(text=f'{self.found_results[active_button_num]}', wraplength = 90)
                active_button_num += 1
                self.page_iter -= 1/4
                self.plant_id1 = self.page_number*4-4
            elif active_button_num%4 == 1:
                self.search_result_2.grid(row=117, column=5, rowspan=161, columnspan=3)
                self.search_result_2.config(text=f'{self.found_results[active_button_num]}', wraplength = 90)
                active_button_num += 1
                self.page_iter -= 1/4
                self.plant_id2 = self.page_number*4-3
            elif active_button_num%4 == 2:
                self.search_result_3.grid(row=337, column=2, rowspan=161, columnspan=3)
                self.search_result_3.config(text=f'{self.found_results[active_button_num]}', wraplength = 90)
                active_button_num += 1
                self.page_iter -= 1/4
                self.plant_id3 = self.page_number*4-2
            elif active_button_num%4 == 3:
                self.search_result_4.grid(row=337, column=5, rowspan=161, columnspan=3)
                self.search_result_4.config(text=f'{self.found_results[active_button_num]}', wraplength = 90)
                active_button_num += 1
                self.page_iter -= 1/4
                self.plant_id4 = self.page_number*4-1
            else:
                # Accounting for error
                messagebox.showerror('Error', 'Error Loading Results')

    def next_search(self):
        """Move to next page."""

        self.page_number += 1
        self.previous_add.config(text='<', state='active', relief='raised')
        self.display_search()

    def prev_search(self):
        """Move to previous page."""

        self.page_number -= 1
        self.next_add.config(text='>', state='active', relief='raised')
        if self.page_number == 1:
            self.previous_add.config(text='', state='disabled', relief='flat')
        self.display_search()


class plant_info_frame(Frame):
    """Display information about selected plant from add frame.
    Create widgets to add plant to user account."""

    def __init__(self, parent, control_frame):
        """Create and define all required widgets."""

        Frame.__init__(self, parent)

        for col in range(456):
            self.grid_columnconfigure(col, minsize=1, weight=1)

        # Define variables which are used from control frame
        self.plant_list = []
        self.data = []
        self.read_csv_file_plant()
        self.row_value = None
        self.row_num = None
        self.plant_scientific = None
        self.plant1 = None
        self.plant2 = None
        self.plant3 = None

        plant_back_button = Button(self, text='Back', command=lambda: control_frame.show_frame(add_frame))
        plant_back_button.grid(column=0, row=0, rowspan=26, columnspan=36, sticky='W')

        self.plant_info_h1 = Label(self, text='The One', font='Arial, 20')
        self.plant_info_h1.grid(row=111, column=105, rowspan=38, columnspan=150, sticky='W')
        self.plant_info_h2 = Label(self, text='Plant Scientific', fg='#8A8A8A')
        self.plant_info_h2.grid(row=90, column=105, rowspan=21, columnspan=84, sticky='W')
        self.plant_info_h3 = Label(self, text='', font='Arial, 8')
        self.plant_info_h3.grid(row=149, column=105, rowspan=12, columnspan=84, sticky='W')

        self.water_freq_label = Label(self, text=f'Water every: 1-2 Weeks')
        self.water_freq_label.grid(row=250, column=90, columnspan=81, rowspan=21, sticky='W')
        self.difficulty_label = Label(self, text=f'Difficulty: Easy-Moderate')
        self.difficulty_label.grid(row=250, column=160, columnspan=139, rowspan=21, sticky='W')
        self.plant_type_label = Label(self, text='Type: Succulent')
        self.plant_type_label.grid(row=300, column=90, columnspan=81, rowspan=21, sticky='W')

        self.plant_row=0

        add_button = Button(self, text='Add', width=12, height=2, command=lambda: self.append_plant())
        add_button.grid(row=500, column=125, rowspan=41, columnspan=94, sticky='W')

    def retrieve_plant(self):
        """Find location of plant in csv
        Add plant to user account in csv."""

        # Plant names for add frame
        plant_name = self.plant_list[self.plant_row][0]
        self.plant_scientific = self.plant_list[self.plant_row][1]
        difficulty = self.plant_list[self.plant_row][4]
        water_freq = self.plant_list[self.plant_row][5]
        plant_type = self.plant_list[self.plant_row][2]

        # If matches, get data
        if self.plant_list[self.plant_row][3] == '':
            self.plant_info_h3.config(text='')
        else:
            plant_alt = (self.plant_list[self.plant_row][3])
            self.plant_info_h3.config(text=plant_alt)

        self.plant_info_h1.config(text=plant_name)
        self.plant_info_h2.config(text=self.plant_scientific)
        self.difficulty_label.config(text=f'Difficulty: {difficulty}')
        self.water_freq_label.config(text=f'Water: {water_freq}')
        self.plant_type_label.config(text=f'Type: {plant_type}')
    
    def read_csv_file_plant(self):
        """Reads csv file to nested lists."""

        self.data = []  # Clearing previous contents
        with open('account_details.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.data.append(row)
        return self.data

    def write_csv_file_plant(self, data):
        """Writes new information to csv."""

        with open('account_details.csv', 'w', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_file.truncate() # Removes all csv file data once stored within dataframe
            csv_writer.writerows(data)

    def edit_cell_plant(self, row_index, column_index, value):
        """Edits row and column value within nested list."""

        self.data = self.read_csv_file_plant()
        if row_index < len(self.data) and column_index < len(self.data[row_index]):
            self.data[row_index][column_index] = value
            self.write_csv_file_plant(self.data)
        else:
            pass

    def retrieve_data_plant(self):
        """Find index of owned plants of user account."""

        for sublist in self.data:
            try:
                # Finds row index of email to edit further on
                sublist.index(self.row_value)
                self.row_num = self.data.index(sublist)

                # Data for daily task frame:
                self.plant1 = (self.data[self.row_num][6])
                self.plant2 = (self.data[self.row_num][7])
                self.plant3 = (self.data[self.row_num][8])

            except ValueError:
                pass # Ignores other sublists
    
    def append_plant(self):
        """Add plant to users account."""

        # Call function to get information about current plant selected
        self.retrieve_data_plant()

        # Create conditions if user is first time sign up
        if self.plant1 == None:
            self.plant1 = ''
    
        if self.plant2 == None:
            self.plant2 = ''

        if self.plant3 == None:
            self.plant3 = ''
        try:
            if self.plant1 == '':  # Checks which column to edit first
                self.edit_cell_plant(self.row_num, 6, self.plant_scientific)
                messagebox.showinfo('Success!', 'You have added your plant successfully!')
            elif self.plant2 == '':
                self.edit_cell_plant(self.row_num, 7, self.plant_scientific)
                messagebox.showinfo('Success!', 'You have added your plant successfully!')
            elif self.plant3 == '':
                self.edit_cell_plant(self.row_num, 8, self.plant_scientific)
                messagebox.showinfo('Success!', 'You have added your plant successfully!')
            else:
                messagebox.showerror('Error', 'You are limited to owning 3 plants at this time.')

        # Except function to ignore when information does not match.
        except TypeError:
            self.row_num = len(self.data)-1
            if self.plant1 == '':  # Checks which column to edit first
                self.edit_cell_plant(self.row_num, 6, self.plant_scientific)
                messagebox.showinfo('Success!', 'You have added your plant successfully!')
            elif self.plant2 == '':
                self.edit_cell_plant(self.row_num, 7, self.plant_scientific)
                messagebox.showinfo('Success!', 'You have added your plant successfully!')
            elif self.plant3 == '':
                self.edit_cell_plant(self.row_num, 8, self.plant_scientific)
                messagebox.showinfo('Success!', 'You have added your plant successfully!')
            else:
                messagebox.showerror('Error', 'You are limited to owning 3 plants at this time.')


class shop_frame(Frame):
    """Class for shop frame.
    Get information about user currency and display in top right
    Create buttons to link to shops."""

    def __init__(self, parent, control_frame):
        """Create and grid widgets."""

        Frame.__init__(self, parent)

        # Create top navigation widgets
        try:
            weather_label = Label(self, text=f'{weather}, {temperature}°C, {humidity}%', font='Arial, 24')
        except NameError:
            weather_label = Label(self, text='Service not connected', font='Arial, 24')
        weather_label.grid(row=0, column=0, columnspan=71, rowspan=42, sticky='w')

        topnav_add = Button(self, text='Add', width=12, height=1, 
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row=43, column=0, columnspan=2, rowspan=24, sticky='nw')

        topnav_shop = Button(self, text='Shop', width=12, height=1, 
            bg='#9AB752', relief='sunken', state='disabled',
            disabledforeground='white')

        topnav_shop.grid(row=43, column=2, columnspan=2, rowspan=24, sticky='nw')

        topnav_home = Button(self, text='Home', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(home_frame))

        topnav_home.grid(row=43, column=4, columnspan=2, rowspan=24, sticky='nw')

        topnav_tasks = Button(self, text='Tasks', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row=43, column=6, columnspan=2, rowspan=24, sticky='nw')

        topnav_settings = Button(self, text='Settings', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(settings_frame))
        
        topnav_settings.grid(row=43, column=8, columnspan=2, rowspan=24, sticky='nw')

        self.currency_label = Button(self, text='Money\nPlacehold')
        self.currency_label.grid(row=70, column=8, rowspan=41, sticky  = 'E')

        # Create shop buttons

        pots_button = Button(self, text='Pot Designs', bg='#9AB752', fg='white',
                            activebackground='#9AB752', activeforeground='white', width=24, height=3, font='Arial, 12',
                            command=lambda: messagebox.showerror('Error', 'Shop Functionalities will come in a later patch.'))
        pots_button.grid(row=190, column=0, columnspan=10, rowspan=68, sticky='n')

        power_button = Button(self, text='Power-Ups', bg='#9AB752', fg='white',
                            activebackground='#9AB752', activeforeground='white', width=24, height=3, font='Arial, 12',
                            command=lambda: messagebox.showerror('Error', 'Shop Functionalities will come in a later patch.'))
        power_button.grid(row=400, column=0, columnspan=10, rowspan=68, sticky='n')


class task_frame(Frame):
    """Create task frame
    Create widgets to link to tasks and daily logins."""

    def __init__(self, parent, control_frame):
        """Define and grid widgets."""

        Frame.__init__(self, parent)
        try:
            weather_label = Label(self, text=f'{weather}, {temperature}°C, {humidity}%', font='Arial, 24')
        except NameError:
            weather_label = Label(self, text='Service not connected', font='Arial, 24')
        weather_label.grid(row=0, column=0, columnspan=71, rowspan=42, sticky='w')

        topnav_add = Button(self, text='Add', width=12, height=1, 
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row=43, column=0, columnspan=2, rowspan=24, sticky='nw')

        topnav_shop = Button(self, text='Shop', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row=43, column=2, columnspan=2, rowspan=24, sticky='nw')

        topnav_home = Button(self, text='Home', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(home_frame))

        topnav_home.grid(row=43, column=4, columnspan=2, rowspan=24, sticky='nw')

        topnav_tasks = Button(self, text='Tasks', width=12, height=1, 
            bg='#9AB752', relief='sunken', state='disabled',
            disabledforeground='white')

        topnav_tasks.grid(row=43, column=6, columnspan=2, rowspan=24, sticky='nw')

        topnav_settings = Button(self, text='Settings', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(settings_frame))

        topnav_settings.grid(row=43, column=8, columnspan=2, rowspan=24, sticky='nw')

        # Links to task frame
        tasks_button = Button(self, text='Daily Tasks', bg='#9AB752', fg='white',
            activebackground='#9AB752', activeforeground='white', width=24, height=3, font='Arial, 12',
            command=lambda: control_frame.show_frame(daily_frame))

        tasks_button.grid(row=190, column=0, columnspan=10, rowspan=68, sticky='n')

        # Links to streak frame
        streak_button = Button(self, text='Login Rewards', bg='#9AB752', fg='white',
            activebackground='#9AB752', activeforeground='white',
            width=24, height=3, font='Arial, 12', command=lambda: control_frame.show_frame(streak_frame))

        streak_button.grid(row=400, column=0, columnspan=10, rowspan=68, sticky='n')


class daily_frame(Frame):
    """Display daily frame
    Display tasks based on weather information and plant."""

    def __init__(self, parent, control_frame):
        """Define and grid widgets."""

        Frame.__init__(self, parent)

        self.plant_list_combo = []

        for col in range(456):
            self.grid_columnconfigure(col, minsize=1, weight=1)

        task_back_button = Button(self, text='Back', command=lambda: control_frame.show_frame(task_frame))
        task_back_button.grid(column=0, row=0, rowspan=26, columnspan=36, sticky='W')
        
        # Define combobox values
        self.combo_plant1 = 'Plant 1'
        self.combo_plant2 = 'Plant 2'
        self.combo_plant3 = 'Plant 3'

        # Set combobox field as non-editable.
        self.plants_combo = Combobox(self, state='readonly')
        
        # Hide all task texts
        self.task1 = Label(self, text='')
        self.task2 = Label(self, text='')
        self.task3 = Label(self, text='')
        self.task4 = Label(self, text='')

    def set_combo(self):
        """Bind command to selecting combobox value
        On select, display plant information."""

        self.plants_combo.bind("<<ComboboxSelected>>", self.display_plant_tasks) # On selection

        self.plant_list_combo = [] # Append all lines in file, resets whenever run
        with open('plant_data.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.plant_list_combo.append(row)
        if self.combo_plant1 != '':
            # Search for row for plant 1
            for sublist in self.plant_list_combo:
                try:
                    sublist.index(self.combo_plant1)
                    self.row_num = self.plant_list_combo.index(sublist) # Finds row index of plant
                    self.combo_plant1 = self.plant_list_combo[self.row_num][0]
                except ValueError:
                    pass # Ignores other sublists
            
            # Search for row for plant 2
            for sublist in self.plant_list_combo:
                try:
                    sublist.index(self.combo_plant2)
                    self.row_num = self.plant_list_combo.index(sublist) # Finds row index of plant
                    self.combo_plant2 = self.plant_list_combo[self.row_num][0]
                except ValueError:
                    pass # Ignores other sublists
            
            for sublist in self.plant_list_combo:
                try:
                    sublist.index(self.combo_plant3)
                    self.row_num = self.plant_list_combo.index(sublist) # Finds row index of plant
                    self.combo_plant3 = self.plant_list_combo[self.row_num][0]
                except ValueError:
                    pass # Ignores other sublists

        if self.combo_plant1 == '':
            self.plants_combo.set("Please add a plant first!")
            self.plants_combo.config(state='disabled')
        elif self.combo_plant2 == '':
            self.plants_combo['values'] = (self.combo_plant1)
            self.plants_combo.set(self.combo_plant1)
            self.plants_combo.config(state='readonly')
        elif self.combo_plant3 == '':
            self.plants_combo['values'] = (self.combo_plant1, self.combo_plant2)
            self.plants_combo.set(self.combo_plant1)
            self.plants_combo.config(state='readonly')
        else:
            self.plants_combo['values'] = (self.combo_plant1, self.combo_plant2, self.combo_plant3)
            self.plants_combo.set(self.combo_plant1)
            self.plants_combo.config(state='readonly')

        self.plants_combo.grid(row=150, column=80, rowspan=21, columnspan=143)

    def display_plant_tasks(self, event):
        """Set tasks based on weather"""

        try:
            if temperature > 20 or weather == 'Clear' or weather == 'Clouds':
                self.task1.config(text='Ensure plant does not burn')
                self.task2.config(text='Check soil moisture')
                self.task3.config(text='If soil is dry, water!')
                self.task4.config(text='Prune dead leaves')
                self.task1.grid(row=180, column=102, rowspan=21, columnspan=150, sticky='W')
                self.task2.grid(row=205, column=102, rowspan=21, columnspan=150, sticky='W')
                self.task3.grid(row=230, column=102, rowspan=21, columnspan=150, sticky='W')
                self.task4.grid(row=255, column=102, rowspan=21, columnspan=150, sticky='W')
            
            if weather == 'Rain' or weather == 'Drizzle' or weather == 'Thunderstorm':
                self.task1.config(text='Ensure plant does not drown')
                self.task2.config(text='Move out of rain if needed')
                self.task3.config(text = '')
                self.task4.config(text = '')
                self.task1.grid(row=180, column=102, rowspan=21, columnspan=150, sticky='W')
                self.task2.grid(row=205, column=102, rowspan=21, columnspan=150, sticky='W')

            else:
                self.task1.config(text='Check soil moisture')
                self.task2.config(text='If soil is dry, water as required!')
                self.task3.config(text='Prune dead leaves')
                self.task4.config(text = '')
                self.task1.grid(row=180, column=102, rowspan=21, columnspan=150, sticky='W')
                self.task2.grid(row=205, column=102, rowspan=21, columnspan=150, sticky='W')
                self.task3.grid(row=230, column=102, rowspan=21, columnspan=150, sticky='W')

        except NameError:
            # Except function incase cannot reach weather variables
            self.task1.config(text='Please enable location services to access tasks')
            self.task1.grid(row=301, column=72, rowspan=21, columnspan=247, sticky='W')


class streak_frame(Frame):
    """Used to claim daily reward each day
    Reward will scale with streak.
    Define claim method"""

    def __init__(self, parent, control_frame):
        """Create and manage widgets,"""

        Frame.__init__(self, parent)

        for col in range(456):
            self.grid_columnconfigure(col, minsize=1, weight=1)

        self.data = [] # Stores list of lists of csv file
        self.read_csv_file() # Appends to dataframe
        self.row_value = None

        streak_back_button = Button(self, text='Back',
                                    command=lambda: control_frame.show_frame(task_frame)
                                    )
        streak_back_button.grid(column=0, row=0, rowspan=26, columnspan=36, sticky='W')

        self.claim_button = Button(self,
                                   text="        Claim Today's Daily Reward        ", 
                                   command=lambda: self.calc_streak()
                                   )
        self.claim_button.grid(column=95, row=456, rowspan=26, columnspan=153, sticky='W')

        self.streak_label = Label(self, text='0', font='Arial, 100')
        self.streak_label.grid(column=131, row=172, rowspan=155, columnspan=80, sticky='W')

        self.streak_info_label = Label(self, text='')

        self.streak_title_label = Label(self, text='Streak:', font='Arial, 24')
        self.streak_title_label.grid(column=123, row=130, rowspan=42, columnspan=106, sticky='W')

    def read_csv_file(self):
        """Append csv info to list,"""

        # Clearing previous contents
        self.data = []
        with open('account_details.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.data.append(row)
        return self.data

    def write_csv_file(self, data):
        """Write new data to csv,"""

        with open('account_details.csv', 'w', newline = '') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Remove all csv file data once stored within dataframe
            csv_file.truncate()
            csv_writer.writerows(data)

    def edit_cell(self, row_index, column_index, value):
        """Edits specific row and cell,"""

        self.data = self.read_csv_file()
        if row_index < len(self.data) and column_index < len(self.data[row_index]):
            self.data[row_index][column_index] = value
            self.write_csv_file(self.data)
        else:
            pass

    def retrieve_data(self):
        """Get data from csv file.
        Place into nested list."""

        for sublist in self.data:
            try:
                sublist.index(self.row_value)
                # Finds row index of email to edit further on
                self.row_num = self.data.index(sublist)

                # Data for daily task frame:
                self.plant1 = (self.data[self.row_num][6])
                self.plant2 = (self.data[self.row_num][7])
                self.plant3 = (self.data[self.row_num][8])

                # Streak data.
                self.current_streak = (self.data[self.row_num][4])
                self.current_streak = int(self.current_streak)
                self.currency = self.data[self.row_num][2]
                self.currency = int(self.currency)
                # If no date assigned yet, set as yesterday.
                if self.data[self.row_num][3] == '':
                    self.lastlogin = datetime.now().date() - timedelta(days = 1)
                    self.lastlogin = datetime.strptime(str(self.lastlogin), '%Y-%m-%d')
                else:
                    self.lastlogin = datetime.strptime(self.data[self.row_num][3], '%Y-%m-%d')
                self.current_date = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
                self.delta = self.current_date - self.lastlogin
                if self.delta == timedelta(days = 0):
                    self.claim_button.config(text='Login reward already claimed today!', state='disabled', relief='sunken')
                return self.lastlogin, self.current_date
            except ValueError:
                pass  # Ignores other sublists

    def calc_streak(self):
        """Check how to increment streak."""

        self.retrieve_data()

        # Check whether to change streak or not
        # If logged in yesterday, increase, else reset
        if self.delta == timedelta(days = 1):
            self.current_streak += 1
            self.currency += (self.current_streak + 1)*5
            self.streak_label.config(text=self.current_streak)
            self.streak_info_label.config(
                text=f'Your streak has increased to {self.current_streak}.\n You have gained {(self.current_streak+1)*5} Leaves!'
                )
        elif self.delta > timedelta(days = 1):
            self.current_streak = 1
            self.lastlogin = str(self.lastlogin)
            self.streak_info_label.config(
                text=f'You last claimed your login rewards on {self.lastlogin[:-9]}\n so your streak has reset.\n You have gained 5 leaves!'
                )
            self.streak_label.config(text=self.current_streak)
        elif self.delta == timedelta(days = 0):
            pass

        self.claim_button.config(text='Login reward already claimed today!', state='disabled', relief='sunken')

        self.streak_info_label.grid(column=15, row=300, rowspan=63, columnspan=272, sticky='nesw')

        self.edit_cell(self.row_num, 3, str(datetime.now().date()))
        self.edit_cell(self.row_num, 4, self.current_streak)
        self.edit_cell(self.row_num, 2, self.currency)
        return


class settings_frame(Frame):
    """Create settings frame.
    Define logout function and change password method."""

    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)

        try:
            weather_label = Label(self, text=f'{weather}, {temperature}°C, {humidity}%', font='Arial, 24')
        except NameError:
            weather_label = Label(self, text='Service not connected', font='Arial, 24')
        weather_label.grid(row=0, column=0, columnspan=71, rowspan=42, sticky='w')

        topnav_add = Button(self, text='Add', width=12, height=1, 
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row=43, column=0, columnspan=2, rowspan=24, sticky='nw')

        topnav_shop = Button(self, text='Shop', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row=43, column=2, columnspan=2, rowspan=24, sticky='nw')

        topnav_home = Button(self, text='Home', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(home_frame))

        topnav_home.grid(row=43, column=4, columnspan=2, rowspan=24, sticky='nw')

        topnav_tasks = Button(self, text='Tasks', width=12, height=1,
            fg='#9AB752', borderwidth=1, activebackground='#F0F0ED',
            activeforeground='#9AB752', command=lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row=43, column=6, columnspan=2, rowspan=24, sticky='nw')

        topnav_settings = Button(self, text='Settings', width=12, height=1, 
            bg='#9AB752', relief='sunken', state='disabled',
            disabledforeground='white')

        topnav_settings.grid(row=43, column=8, columnspan=2, rowspan=24, sticky='nw')

        # Grid profile information widgets.
        pfp_placehold = Button(self, text='Profile Picture', height=8, width=16)
        pfp_placehold.grid(row=90, column=1, rowspan=131, columnspan=4)

        self.email_label = Label(self, text='Error: E-mail not found')
        self.email_label.grid(row=95, column=5, columnspan=3, rowspan=21, sticky='w')

        pass_label = Label(self, text='Password: ' + '\u2022' * 8)
        pass_label.grid(row=116, column=5, columnspan=3, rowspan=21, sticky='w')

        logout_button  = Button(self, text='Logout', bg='red',
            fg='white', width=20, font='Arial, 10', command=lambda: control_frame.show_frame(login_frame))

        logout_button.grid(row=500, column=3, columnspan=4, rowspan=28)


if __name__ == '__main__':
    # If launched from main file.
    application = Windows()
    application.lift()  # Launches on top
    # Launch as topmost window
    application.attributes('-topmost',True)
    application.after_idle(application.attributes,'-topmost',False)
    # Toggle off topmost so user can tab out
    application.mainloop()
