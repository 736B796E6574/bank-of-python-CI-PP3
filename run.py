# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

new_user = []

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
    print('Deposit successfull!')



add_new_name()
print(new_user)