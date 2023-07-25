from tkinter import Tk, Entry, Label, Frame, Button, messagebox
from tkinter.simpledialog import askstring
import re
try: # Only runs if access granted
    from weather_module import temperature, humidity, weather
except ImportError:
    pass
from datetime import datetime, timedelta
import csv

class windows(Tk):
    def __init__(self, *args, **kwargs): # *args **kwargs in case other params passed in.
        Tk.__init__(self, *args, **kwargs)
        self.wm_title('CBT')
        container = Frame(self, height = 690, width = 462)
        container.grid(row = 0, column = 0)
        self.resizable(False, False)
        self.maxsize(462, 690)
        self.minsize(462, 690)
        self.frames = {} # Create dictionary to select out frame variable to use
        for F in (login_frame, home_frame, task_frame, shop_frame, settings_frame, add_frame, streak_frame):
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = 'nesw')

        self.show_frame(login_frame)

    def show_frame(self, control): # Method to raise selected frame to top level
        frame = self.frames[control]
        frame.tkraise()

        for row in range(690):
            frame.grid_rowconfigure(row, minsize = 1, weight=1)

        if str(frame) == '.!frame.!settings_frame': # If going to settings frame
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
            frame.email_label.config(text = f'Email: *****{self.display2}')
        
        elif str(frame) == '.!frame.!login_frame': # If going to login frame
            frame.login_error.config(text = '')
        
        elif str(frame) == '.!frame.!streak_frame':
            frame = self.frames[login_frame]
            email = frame.user_entry.get()
            frame = self.frames[streak_frame]
            frame.row_value = email

class login_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)
        for col in range(100):
            self.grid_columnconfigure(col, minsize = 5, weight = 1)

        title_label = Label(self, text='App', font = ('Arial', 35))
        title_label.grid(row = 95, column = 18, rowspan = 59, columnspan = 20)
        self.user_label = Label(self, text = 'Email:')
        self.user_label.grid(row = 250, column = 28, rowspan = 21, columnspan = 6, sticky = 'w')
        self.user_entry = Entry(self, width = 30)
        self.user_entry.grid(row = 271, column = 28, rowspan = 21, columnspan = 6, sticky = 'w')

        self.pass_label = Label(self, text = 'Password:')
        self.pass_label.grid(row = 312, column = 28, rowspan = 21, columnspan = 6, sticky = 'w')
        self.pass_entry = Entry(self, show='\u2022', width = 30) # Show function hides inputs
        self.pass_entry.grid(row = 333, column = 28, rowspan = 21, columnspan = 6, sticky = 'w')

        toggle_pass = Button(self, text = "Icon", command = lambda: self.toggleShow())
        toggle_pass.grid(row = 333, column = 34, rowspan = 21)

        login_button = Button(self, text = "Login", command = lambda: self.check_details(control_frame))
        login_button.grid(row = 384, column = 18, rowspan = 21, columnspan = 20)

        signup_button = Button(self, text = 'Don\'t Have an Account?', command = lambda: self.signup())
        signup_button.grid(row = 441, column = 18, rowspan = 21, columnspan = 20)

        self.login_error = Label(self, text = '', fg='red')
        self.login_error.config(text = '')
        self.login_error.grid(row = 354, column = 28, rowspan = 21, columnspan = 7, sticky = 'w')
    
    def signup(self):
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
        new_info = '\n' + new_email.lower() + ',' + new_password + ',100,,0,,'
        file.write(new_info)
        file.close()

    def check_details(self, control_frame):
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
        next(file) # Skip first line
        for line in file:
            item = line.split(',')
            if email == item[0].strip() and password == item[1].strip():
                control_frame.show_frame(home_frame)
            else:
                self.login_error.config(text='Incorrect username or password')
    
    def toggleShow(self):
        if self.pass_entry.cget('show') == '\u2022': # If password text is hidden, show
            self.pass_entry.config(show = '')
        else:
            self.pass_entry.config(show = '\u2022') # Else, hide


class home_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)
        try:
            weather_label = Label(self, text = f'{weather}, {temperature}°C, {humidity}%', font = 'Arial, 24')
        except NameError:
            weather_label = Label(self, text = 'N/A', font = 'Arial, 24')
        weather_label.grid(row = 0, column = 0, columnspan=71, rowspan = 44, sticky = 'w')

        topnav_add = Button(self, text = 'Add', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', 
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row = 45, column = 0, columnspan=2, rowspan = 24, sticky = 'nw')

        topnav_shop = Button(self, text = 'Shop', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED', 
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row = 45, column = 2, columnspan=2, rowspan = 24, sticky = 'nw')

        topnav_home = Button(self, text = 'Home', width = 12, height = 1,
            bg = '#9AB752', relief = 'sunken', state = 'disabled', 
            disabledforeground = 'white') # Disabled because it is active frame

        topnav_home.grid(row = 45, column = 4, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_tasks = Button(self, text = 'Tasks', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row = 45, column = 6, columnspan=2, rowspan = 24, sticky = 'nw')

        topnav_settings = Button(self, text = 'Settings', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(settings_frame))

        topnav_settings.grid(row = 45, column = 8, columnspan=2, rowspan = 24, sticky = 'nw')

        main_sprite = Label(self, text = 'Image \nPlacehold', font = 'Arial, 45')
        main_sprite.grid(row = 202, column = 3, rowspan = 140, columnspan=5)

        left_button = Button(self, text = '<', height = 5) # Swaps sprite
        left_button.grid(row = 229, column = 0, rowspan = 86)
        right_button = Button(self, text = '>', height = 5) # Swaps sprite
        right_button.grid(row = 229, column = 9, rowspan = 86)

        plants_h1 = Label(self, text = 'Common Name', font = 'Arial, 20')
        plants_h1.grid(row = 110, column = 3, columnspan = 5, rowspan = 38)
        plants_h2 = Label(self, text = 'Scientific Name', fg = '#8a8a8a')
        plants_h2.grid(row = 148, column = 4, rowspan = 21)

        plants_button = Button(self, text = 'Owned Plants', height = 2)
        plants_button.grid(row = 432, column = 4)


class add_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)
        try:
            weather_label = Label(self, text = f'{weather}, {temperature}°C, {humidity}%', font = 'Arial, 24')
        except NameError:
            weather_label = Label(self, text = 'N/A', font = 'Arial, 24')
        weather_label.grid(row = 0, column = 0, columnspan=71, rowspan = 44, sticky = 'w')

        topnav_add = Button(self, text = 'Add', width = 12, height = 1, 
            bg = '#9AB752', relief = 'sunken', state = 'disabled',
            disabledforeground = 'white') # Move all buttons to function in iter 2

        topnav_add.grid(row = 45, column = 0, columnspan=2, sticky = 'nw')

        topnav_shop = Button(self, text = 'Shop', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row = 45, column = 2, columnspan=2, sticky = 'nw')

        topnav_home = Button(self, text = 'Home', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(home_frame))
        
        topnav_home.grid(row = 45, column = 4, columnspan = 2, sticky = 'nw')

        topnav_tasks = Button(self, text = 'Tasks', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row = 45, column = 6, columnspan=2, sticky = 'nw')

        topnav_settings = Button(self, text = 'Settings', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(settings_frame))

        topnav_settings.grid(row = 45, column = 8, columnspan=2, sticky = 'nw')

        self.search_entry = Entry(self, width = 36, bg = '#F0F0ED')
        self.search_entry.grid(row = 68, column = 3, columnspan = 4, sticky = 'W', rowspan = 21)
        search_button = Button(self, text = 'Search', command = lambda: self.match_search())
        search_button.grid(row = 68, column = 2, sticky = 'E', rowspan = 21)

        self.search_result_1 = Button(self, width = 15, height = 10, text = 'Placeholder 1')
        self.search_result_2 = Button(self, width = 15, height = 10, text = 'Placeholder 2')
        self.search_result_3 = Button(self, width = 15, height = 10, text = 'Placeholder 3')
        self.search_result_4 = Button(self, width = 15, height = 10, text = 'Placeholder 4')

        self.previous_add = Button(self, text = '<', height = 5, command = lambda: self.prev_search())
        self.next_add = Button(self, text = '>', height = 5, command = lambda: self.next_search())
    
    def match_search(self):
        self.page_number = 1 # Ensures only displays results in order from start
        self.found_results = []
        self.found = False # Used to check if any results were found
        file = open('plant_data.csv', 'r')
        next(file)
        search = self.search_entry.get()
        search = search.strip().lower()
        search = re.sub(r'[^\w]', '', search)
        for line in file: # Search for best matches first
            line = line.strip()
            item = line.split(', ')
            lower_list = [x.lower() for x in item] # List Comprehension to lower case
            regex_list = [re.sub(r'[^\w]', '', x) for x in lower_list] # List Comprehension to remove symbols
            s1_list = list(regex_list[::3]) # Only searches common names
            if any(search in a for a in s1_list):
                self.found_results.append(item[0])
                self.found = True
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
                self.found_results.append(item[0])
                self.found = True
                self.search_error.grid_forget()
        if self.found == False:
            self.search_error = Label(self,
                text = f'No results found for "{self.search_entry.get()}"\n If you cannot find your plant, please file a ticket!', 
                fg = 'red')
            self.search_error.grid(row = 90, column = 2, rowspan = 21, columnspan = 6)
        self.previous_add.grid(row = 262, column = 0, rowspan = 86)
        self.previous_add.config(text = '', state = 'disabled', relief = 'flat')
        self.next_add.grid(row = 262, column = 9, rowspan = 86)
        self.next_add.config(text = '', state = 'disabled', relief = 'flat')

        self.display_search()

    def display_search(self):
        active_button_num = 0 # Selects which button to config
        
        # Iter will be used to iterate through results without
        # resetting page number value
        self.page_iter = self.page_number
        
        try:
            self.found_results[self.page_number*4-1]
            self.next_add.config(text = '>', state='active', relief='raised')
        except IndexError:
            self.next_add.config(text = '', state='disabled', relief='flat')

        self.search_result_1.grid_forget() # Forgetting grid so will not show previous search results
        self.search_result_2.grid_forget() # if not enough results to fill
        self.search_result_3.grid_forget()
        self.search_result_4.grid_forget()

        while active_button_num < len(self.found_results) and self.page_iter > 0:
            if active_button_num%4 == 0:
                self.search_result_1.grid_forget()
                self.search_result_2.grid_forget()
                self.search_result_3.grid_forget()
                self.search_result_4.grid_forget()
                self.search_result_1.grid(row = 117, column = 2, rowspan = 161, columnspan = 3)
                self.search_result_1.config(text = f'{self.found_results[active_button_num]}')
                active_button_num += 1
                self.page_iter -= 1/4
            elif active_button_num%4 == 1:
                self.search_result_2.grid(row = 117, column = 5, rowspan = 161, columnspan = 3)
                self.search_result_2.config(text = f'{self.found_results[active_button_num]}')
                active_button_num += 1
                self.page_iter -= 1/4
            elif active_button_num%4 == 2:
                self.search_result_3.grid(row = 337, column = 2, rowspan = 161, columnspan = 3)
                self.search_result_3.config(text = f'{self.found_results[active_button_num]}')
                active_button_num += 1
                self.page_iter -= 1/4
            elif active_button_num%4 == 3:
                self.search_result_4.grid(row = 337, column = 5, rowspan = 161, columnspan = 3)
                self.search_result_4.config(text = f'{self.found_results[active_button_num]}')
                active_button_num += 1
                self.page_iter -= 1/4
            else:
                # Accounting for error
                messagebox.showerror('Error', 'Error Loading Results')

    def next_search(self):
        self.page_number += 1
        self.previous_add.config(text = '<', state='active', relief='raised')
        self.display_search()

    def prev_search(self):
        self.page_number -= 1
        self.next_add.config(text = '>', state='active', relief='raised')
        if self.page_number == 1:
            self.previous_add.config(text = '', state='disabled', relief='flat')
        self.display_search()


class shop_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)

        try:
            weather_label = Label(self, text = f'{weather}, {temperature}°C, {humidity}%', font = 'Arial, 24')
        except NameError:
            weather_label = Label(self, text = 'N/A', font = 'Arial, 24')
        weather_label.grid(row = 0, column = 0, columnspan=71, rowspan = 42, sticky = 'w')

        topnav_add = Button(self, text = 'Add', width = 12, height = 1, 
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row = 43, column = 0, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_shop = Button(self, text = 'Shop', width = 12, height = 1, 
            bg = '#9AB752', relief = 'sunken', state = 'disabled',
            disabledforeground = 'white')

        topnav_shop.grid(row = 43, column = 2, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_home = Button(self, text = 'Home', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(home_frame))

        topnav_home.grid(row = 43, column = 4, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_tasks = Button(self, text = 'Tasks', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row = 43, column = 6, columnspan=2, rowspan = 24, sticky = 'nw')

        topnav_settings = Button(self, text = 'Settings', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(settings_frame))
        
        topnav_settings.grid(row = 43, column = 8, columnspan=2, rowspan = 24, sticky = 'nw')

        currency_label = Button(self, text = 'Money\nPlacehold')
        currency_label.grid(row = 70, column = 8, rowspan = 41, sticky  = 'E')

        pots_button = Button(self, text = 'Pot Designs', bg = '#9AB752', fg = 'white',
                            activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')
        pots_button.grid(row = 190, column = 0, columnspan = 10, rowspan = 68, sticky = 'n')

        furniture_button = Button(self, text = 'Furniture Sets', bg = '#9AB752', fg = 'white',
                            activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')
        furniture_button.grid(row = 400, column = 0, columnspan = 10, rowspan = 68, sticky = 'n')


class task_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)
        try:
            weather_label = Label(self, text = f'{weather}, {temperature}°C, {humidity}%', font = 'Arial, 24')
        except NameError:
            weather_label = Label(self, text = 'N/A', font = 'Arial, 24')
        weather_label.grid(row = 0, column = 0, columnspan=71, rowspan = 42, sticky = 'w')

        topnav_add = Button(self, text = 'Add', width = 12, height = 1, 
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row = 43, column = 0, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_shop = Button(self, text = 'Shop', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row = 43, column = 2, columnspan=2, rowspan = 24, sticky = 'nw')

        topnav_home = Button(self, text = 'Home', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(home_frame))

        topnav_home.grid(row = 43, column = 4, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_tasks = Button(self, text = 'Tasks', width = 12, height = 1, 
            bg = '#9AB752', relief = 'sunken', state = 'disabled',
            disabledforeground = 'white')

        topnav_tasks.grid(row = 43, column = 6, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_settings = Button(self, text = 'Settings', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(settings_frame))

        topnav_settings.grid(row = 43, column = 8, columnspan = 2, rowspan = 24, sticky = 'nw')

        tasks_button = Button(self, text = 'Daily Tasks', bg = '#9AB752', fg = 'white',
            activebackground = '#9AB752', activeforeground = 'white', width = 24, height = 3, font = 'Arial, 12')

        tasks_button.grid(row = 190, column = 0, columnspan = 10, rowspan = 68, sticky = 'n')

        streak_button = Button(self, text = 'Login Rewards', bg = '#9AB752', fg = 'white',
            activebackground = '#9AB752', activeforeground = 'white',
            width = 24, height = 3, font = 'Arial, 12', command = lambda: control_frame.show_frame(streak_frame))

        streak_button.grid(row = 400, column = 0, columnspan = 10, rowspan = 68, sticky = 'n')

class streak_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)
        self.data = [] # Stores list of lists of csv file
        self.read_csv_file() # Appends to dataframe
        self.row_value = None

        back_button = Button(self, text = 'Back', command = lambda: control_frame.show_frame(task_frame))
        back_button.grid(column = 0, row = 0, rowspan = 26)

        claim_button = Button(self, text = 'Claim Daily Reward', command = lambda: self.calc_streak())
        claim_button.grid(column = 8, row = 260)


    def read_csv_file(self):
        self.data = []
        with open('account_details.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                self.data.append(row)
        return self.data

    def write_csv_file(self, data):
        with open('account_details.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_file.truncate()
            csv_writer.writerows(data)

    def edit_row_column(self, row_index, column_index, value):
        self.data = self.read_csv_file()
        if row_index < len(self.data) and column_index < len(self.data[row_index]):
            self.data[row_index][column_index] = value
            self.write_csv_file(self.data)
            print("Data updated successfully.")
        else:
            print("Invalid row or column index.")

    def calc_streak(self):
        for sublist in self.data:
            try:
                sublist.index(self.row_value)
                row_num = self.data.index(sublist)
                current_streak = (self.data[row_num][4])
                current_streak = int(current_streak)
                lastlogin = datetime.strptime(self.data[row_num][3], '%Y-%m-%d')
                current_date = datetime.strptime(str(datetime.now().date()), '%Y-%m-%d')
                delta = current_date - lastlogin
                if delta == timedelta(days = 1):
                    current_streak += 1
                elif delta > timedelta(days = 1):
                    current_streak = 0
                elif delta == timedelta(days = 0):
                    pass

                self.edit_row_column(row_num, 3, str(datetime.now().date()))
                self.edit_row_column(row_num, 4, current_streak)
                return

            except ValueError:
                pass # Ignores other sublists

class settings_frame(Frame):
    def __init__(self, parent, control_frame):
        Frame.__init__(self, parent)

        try:
            weather_label = Label(self, text = f'{weather}, {temperature}°C, {humidity}%', font = 'Arial, 24')
        except NameError:
            weather_label = Label(self, text = 'N/A', font = 'Arial, 24')
        weather_label.grid(row = 0, column = 0, columnspan = 71, rowspan = 42, sticky = 'w')

        topnav_add = Button(self, text = 'Add', width = 12, height = 1, 
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(add_frame))

        topnav_add.grid(row = 43, column = 0, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_shop = Button(self, text = 'Shop', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(shop_frame))

        topnav_shop.grid(row = 43, column = 2, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_home = Button(self, text = 'Home', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(home_frame))

        topnav_home.grid(row = 43, column = 4, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_tasks = Button(self, text = 'Tasks', width = 12, height = 1,
            fg = '#9AB752', borderwidth = 1, activebackground = '#F0F0ED',
            activeforeground = '#9AB752', command = lambda: control_frame.show_frame(task_frame))

        topnav_tasks.grid(row = 43, column = 6, columnspan = 2, rowspan = 24, sticky = 'nw')

        topnav_settings = Button(self, text = 'Settings', width = 12, height = 1, 
            bg = '#9AB752', relief = 'sunken', state = 'disabled',
            disabledforeground = 'white')

        topnav_settings.grid(row = 43, column = 8, columnspan = 2, rowspan = 24, sticky = 'nw')

        pfp_placehold = Button(self, text = 'Profile Picture', height = 8, width = 16)
        pfp_placehold.grid(row = 90, column = 1, rowspan = 131, columnspan = 4)

        self.email_label = Label(self, text = 'Error: E-mail not found')
        self.email_label.grid(row = 95, column = 5, columnspan = 3, rowspan = 21, sticky = 'w')

        pass_label = Label(self, text = 'Password: ' + '\u2022' * 8)
        pass_label.grid(row = 116, column = 5, columnspan = 3, rowspan = 21, sticky = 'w')

        change_pass = Button(self, text = 'Edit')
        change_pass.grid(row = 116, column = 8, rowspan = 21, sticky = 'w')

        logout_button  = Button(self, text = 'Logout', bg = 'red',
            fg = 'white', width = 20, font = 'Arial, 10', command = lambda: control_frame.show_frame(login_frame))

        logout_button.grid(row = 500, column = 3, columnspan = 4, rowspan = 28)

if __name__ == '__main__':
    application = windows()
    application.mainloop()
