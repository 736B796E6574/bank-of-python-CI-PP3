# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Bank_of_Python')
accounts = SHEET.worksheet('Accounts')
new_user = []

def home_screen():
    print('\nWelcome to the Bank of Python\n')
    option_choice = int(input('Please select from the following options by entering the corresponding number.\n1. Create a new account.\n2. Change your pin.\n3. Make a withdrawal.\n\nEnter your selection number then press enter: '))
    if option_choice == 1:
        add_new_name()
    elif option_choice == 2:
        change_pin()
    else:
        print('Invalid selection!')
        home_screen()



def add_new_name():
    global new_user
    new_account_name = input('Please enter your full name:')
    print(f'Opening account for {new_account_name}…\n')
    new_user.append(new_account_name)
    print('Account created successfully!\n')
    add_new_pin()

def add_new_pin():
    new_account_pin = int(input('Please enter a 4 digit numerical pin\n'))
    if new_account_pin < 9999:
        print('Saving PIN…')
        new_user.append(new_account_pin)
        print('PIN Saved!\n')
        add_new_balance()
    else:
        print('Invalid entry!')
        add_new_pin()

def add_new_balance():
    new_deposit = int(input('Please enter your deposit amount, without commas: \n'))
    print(f'You entered {new_deposit}. Updating your account...\n')
    new_user.append(new_deposit)
    print('Deposit successfull!\n')
    accounts.append_row(new_user)
    print('Your account creation was successful!\n')



home_screen()


