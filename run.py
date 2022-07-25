# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

from re import match
import gspread
import os
import time
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
account_number = 1
accounts_data = accounts.col_values(1)
account_current_number = len(accounts_data)

def clear_screen(seconds):
    """
    Pauses the program for a specified number of seconds and then clears the text from the terminal.
    """
    time.sleep(seconds)
    os.system('cls' if os.name == 'nt' else 'clear')

def home_screen():
    """
    Offers the main menu options to the user. Takes a number input from the user and calls the function to offer the selected menu option.
    """
    print('\nWelcome to the Bank of Python\n')
    try:
        option_choice = int(input('Please select from the following options by entering the corresponding number.\n1. Create a new account.\n2. Change your pin.\n3. Make a withdrawal.\n4. Exit program.\n\nEnter your selection number then press enter: '))
    except ValueError as e:
        print('You did not enter a selection! Please try again.')
        clear_screen(2)
        home_screen()

    if option_choice == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        add_new_name()
    elif option_choice == 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        change_pin_security()
        os.system('cls' if os.name == 'nt' else 'clear')
    elif option_choice == 3:
        withdrawal_security()
    elif option_choice == 4:
        quit()
    else:
        print('Invalid selection!')
        clear_screen(2)
        home_screen()


def add_new_name():
    """
    Receives the users name, validates it, and adds it to an array which will be later pushed to the spreadsheet.
    """
    global new_user
    print('Welcome to account creation.\n')
    
    try:
        new_account_name = input('Please enter your full name and press enter: \n')
        if not new_account_name:
            raise ValueError()
    except ValueError as e:
        print('You did not enter a selection! Please try again.')
        clear_screen(2)
        add_new_name()
    
    print(f'Opening account for "{new_account_name}"…\n')
    time.sleep(2)
    new_user.append(new_account_name)
    print('Account created successfully!\n')
    clear_screen(2)
    add_new_pin()

def add_new_pin():
    """
    Receives the users PIN input, validates it, and pushes it to the new_user array 
    """
    try:
        new_account_pin = int(input('Please enter a 4 digit numerical pin\n'))
        if new_account_pin < 9999 and len(str(new_account_pin)) == 4:
            print('Saving PIN…')
            time.sleep(2)
            new_user.append(new_account_pin)
            print('PIN Saved!\n')
            clear_screen(2)
            add_new_balance()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Invalid entry!')
            clear_screen(2)
            add_new_pin()
    except:
        print('Invalid entry. Please try again.')
        clear_screen(2)
        add_new_pin()

def add_new_balance():
    """
    Receives the users deposit amount when opening the account. This is the last input required to open the account so the function pushes the new_user array to the spreadsheet to complete the account creations process.
    """
    global account_current_number
    global accounts_data
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        new_deposit = int(input('Please enter your deposit amount, without commas: \n'))
    except ValueError as e:
        print('You did not enter a number! Please try again.')
        clear_screen(2)
        add_new_balance()

    print(f'You entered {new_deposit}. Updating your account...\n')
    time.sleep(2)
    new_user.append(new_deposit)
    print('Deposit successful!\n')
    clear_screen(2)
    accounts.append_row(new_user)
    print('Your account creation was successful!\n')
    accounts_data = accounts.col_values(1)
    account_current_number = len(accounts_data)
    print(f'Your account number is {account_current_number}. Don\'t forget to write it down!\n')
    print('THANK YOU, COME AGAIN!')
    clear_screen(5)
    home_screen()

def change_pin_security():
    """
    Takes the users account number and pin. Checks that the data matches the data stored in the spread sheet. If security is passed then change_pin() is called. 
    """
    global account_number
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        account_number = int(input('Please enter your account number: \n'))
    except ValueError as e:
        print('Invalid entry!')
        clear_screen(2)
        change_pin_security()

    if account_number < 1 or account_number > account_current_number:
        print('Invalid entry!')
        clear_screen(2)
        change_pin_security()

    old_pin = accounts.cell(account_number, 2).value
    current_pin = input('Please enter your current pin and press enter: \n')
    if old_pin == current_pin:
        os.system('cls' if os.name == 'nt' else 'clear')
        customer_name = accounts.cell(account_number, 1).value
        print(f'Welcome back {customer_name}\n')
        time.sleep(2)
        change_pin()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Your information is incorrect! Please check and try again.\n')
        time.sleep(2)
        change_pin_security()
    
def change_pin():
    """
    Asks for the new pin 2 times and they must match each other. It is the last function in this option.
    """
    global account_number
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        first_attempt = int(input('Please enter your new PIN and press enter: \n'))
        second_attempt = int(input('Please enter your new PIN again and press enter: \n'))
    except ValueError as e:
        print('You did not enter a number. Please start again.')
        clear_screen(2)
        change_pin()

    if new_account_pin < 9999 and len(str(new_account_pin)) == 4:
        if first_attempt == second_attempt:
            accounts.update_cell(account_number, 2, second_attempt)
            print(f'PIN change successful! Your new PIN is {second_attempt}.\n')
            print('THANK YOU, COME AGAIN!')
            clear_screen(5)
            home_screen()
        else:
            print('Your PIN did not match! Please try again.')
            time.sleep(2)
            change_pin()
    else:
        print('Invalid input. PIN must be 4 digits.')



def withdrawal_security():
    global account_number
    global balance
    global account_current_number
    global accounts_data
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        account_number = int(input('Please enter your account number: \n'))
    except ValueError as e:
        print('Invalid input.')
        clear_screen(2)
        withdrawal_security()
    
    if account_number < 1 or account_number > account_current_number:
        print('Invalid entry!')
        clear_screen(2)
        withdrawal_security()
    
    old_pin = int(accounts.cell(account_number, 2).value)
    try:
        current_pin = int(input('Please enter your current pin and press enter: \n'))
    except ValueError as e:
        print('Invalid input.')
        clear_screen(2)
        withdrawal_security()
    

    if old_pin == current_pin and current_pin < 9999 and len(str(current_pin)) == 4:
        os.system('cls' if os.name == 'nt' else 'clear')
        customer_name = accounts.cell(account_number, 1).value
        print(f'Welcome back {customer_name}\n')
        balance = int(accounts.cell(account_number, 3).value) 
        print(f'You current balance is ${balance}.\n')
        print('---------------------------')
        time.sleep(3)
        withdraw_money()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Your information is incorrect! Please check and try again.\n')
        time.sleep(2)
        withdrawal_security()
        
def withdraw_money():
    global balance  
    os.system('cls' if os.name == 'nt' else 'clear')   
    
    try:
        withdrawal_amount = int(input('Your withdrawal must be a multiple of 10. \nPlease enter your withdrawal amount and press enter: '))
    except ValueError as e:
        print('Invalid input!')
        clear_screen(2)
        withdraw_money()
    if withdrawal_amount % 10 > 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Invalid amount! Please enter a multiple of 10.\n')
        time.sleep(2)
        withdraw_money()
    elif balance < withdrawal_amount:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Insufficient funds! Please enter a lesser amount.\n')
        time.sleep(2)
        withdraw_money()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Withdrawal successful! Please collect your ${withdrawal_amount} from the disk drive.')
        new_balance = balance - withdrawal_amount
        print(f'Your new balance is ${new_balance}')
        accounts.update_cell(account_number, 3, new_balance)
        print('THANK YOU, COME AGAIN!')
        clear_screen(5)
        home_screen()
    
home_screen()


