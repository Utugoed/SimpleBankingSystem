import random
import sqlite3

def luhn(number):
    sum = 0
    for i in range(15):
        if i % 2 == 0:
            k = int(number[i]) * 2
            if k > 9:
                k -= 9
            sum += k
        else:
            sum += int(number[i])
    sum = (10 - sum % 10) % 10
    return str(sum)

def create_acc():
    number = '400000' + str(random.randint(100000000, 999999999))
    number += luhn(number)
    pin = str(random.randint(0, 9999)).zfill(4)
    balance = 0
    cur.execute('''SELECT number FROM card WHERE number={}'''.format(number))
    if (cur.fetchone() == None):
        cur.execute('''INSERT INTO card(number,pin,balance)
                        VALUES ({},{},{})'''.format(number, pin, balance))
        conn.commit()
        print('''Your card has been created
Your card number:
{}
Your card PIN:
{}'''.format(number, pin))
    else:
        return create_acc()

def log_in():
    print('Enter your card number:')
    global number
    number = input()
    print('Enter your PIN:')
    pin = str(input())
    cur.execute('''SELECT
                    number,
                    pin
                    FROM
                    card
                    WHERE
                    number = {}'''.format(number))
    temp = str(cur.fetchone())
    if (temp == 'None'):
        print('Wrong card number or PIN!')
        return False
    temp = temp.replace('(', '')
    temp = temp.replace(')', '')
    temp = temp.replace("'", '')
    temp = temp.replace(',', '')
    tab_pin = temp.split()[1]
    if (tab_pin == pin):
        return True
    print('Wrong card number or PIN!')
    return False
#4000002070779259
#8761
def balance():
    global number
    cur.execute('''SELECT balance
                    FROM card
                    WHERE number = {}'''.format(number))
    balance = str(cur.fetchone())[1:-2]
    print('Balance: {}'.format(balance))

def add_income():
    global number
    print('Enter income:')
    income = int(input())
    cur.execute('''UPDATE card 
                    SET balance = balance + {} 
                    WHERE number = {}'''.format(income, number))
    conn.commit()
    print('Income was added!')

def transfer():
    global number
    print('Enter card number:')
    number_to = input()
    if (number_to == number):
        print("You can't transfer money to the same account!")
        return False
    if (number_to[-1] != luhn(number_to[0:-1])):
        print("Probably you made a mistake in the card number. Please try again!")
        return False
    cur.execute('SELECT number FROM card WHERE number = {}'.format(number_to))
    if (cur.fetchone() == None):
        print('Such a card does not exist.')
        return False
    print('Enter how much money you want to transfer:')
    sum = int(input())
    cur.execute('SELECT balance FROM card WHERE number = {}'.format(number))
    if (sum > int(str(cur.fetchone())[1:-2])):
        print('Not enough money!')
        return False
    cur.execute('''UPDATE card
                    SET balance = balance - {}
                    WHERE number = {}'''.format(sum, number))
    cur.execute('''UPDATE card
                    SET balance = balance + {}
                    WHERE number = {}'''.format(sum, number_to))
    conn.commit()
    return True

def close():
    global number
    cur.execute('DELETE FROM card WHERE number = {}'.format(number))
    conn.commit()


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS card(
            id INTEGER PRIMARY KEY,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT (0))''')
conn.commit()
exit = True
number = 0
while exit:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    act = int(input())
    if act == 1:
        create_acc()
    if act == 2:
        if log_in():
            print('You have successfully logged in!')
            exit2 = True
            while exit2:
                print('1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
                act_2 = int(input())
                if (act_2 == 1):
                    balance()
                if (act_2 == 2):
                    add_income()
                if (act_2 == 3):
                    if transfer():
                        print('Success!')
                if (act_2 == 4):
                    close()
                    exit2 = False
                if (act_2 == 5):
                    exit2 = False
                if (act_2 == 0):
                    print('Bye!')
                    exit2 = False
                    exit = False
    if (act == 0):
        print('Bye!')
        exit = False


