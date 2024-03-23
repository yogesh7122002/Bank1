import sqlite3
from colorama import Fore
con = sqlite3.connect("bankdb.db")
cursor = con.cursor()
account_no = 100000

# Creating the table Bank
cursor.execute('''CREATE TABLE IF NOT EXISTS bank (
                    name TEXT,
                    Account_No INTEGER PRIMARY KEY,
                    DOB text,
                    contact_no TEXT,
                    Opening_bal NUMERIC
                  )''')
# creating the Table Account to show the account details
cursor.execute(''' CREATE TABLE IF NOT EXISTS ammount(name text,Account_No text,Balance NUMERIC)''')

def open_Acc():
    cursor.execute("SELECT MAX(Account_No) FROM bank")
    max_account_no = cursor.fetchone()[0]
    if max_account_no is not None:
        print("IF")
        print("Max Account Number is : ",max_account_no)
        curr_acc_no = max_account_no+1

        name = input("Please Enter Your Name :")
        DOB =input("Please Enter your Date Of birth :")
        contact_no = input("Please Enter Your Contact Number:")
        opening_Bal = int(input("PLease Enter your accout opening balance :"))

        cursor.execute("insert into bank(name,Account_No,DOB,contact_no,Opening_bal) values(?,?,?,?,?)",(name,curr_acc_no,DOB,contact_no,opening_Bal))

        cursor.execute("insert into ammount(name,Account_No,Balance) values(?,?,?)",(name,curr_acc_no,opening_Bal))
        con.commit()
    # cursor.execute("SELECT MAX(Account_No) FROM bank")
    # latest_account_no = cursor.fetchone()[0]
    # account_no = latest_account_no if latest_account_no is not None else account_no
    else :
        print("Else")
         
        name = input("Please Enter Your Name :")
        DOB =input("Please Enter your Date Of birth :")
        contact_no = input("Please Enter Your Contact Number:")
        opening_Bal = int(input("PLease Enter your accout opening balance :"))
        cursor.execute("insert into bank(name,Account_No,DOB,contact_no,Opening_bal) values(?,?,?,?,?)",(name,account_no,DOB,contact_no,opening_Bal))
        cursor.execute("insert into ammount(name,Account_No,Balance) values(?,?,?)",(name,account_no,opening_Bal))
        con.commit()


def show_Details():
    acc_no = input("Please Enter your Account Number: ")
    cursor.execute("SELECT * FROM ammount WHERE Account_No = ?", (acc_no,))
    # cursor.execute("SELECT * FROM ammount where ")
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Account not Found")
    else:
        print("\n\n")
        print("Name\t\tAcc_Number\tBalance")
        for row in rows:
            print("{}\t\t{}\t\t{}".format(row[0], row[1], row[2]))
        print("\n\n")

def Add_Ammount():
    acc_no  = int(input("Please Enter your Account number:"))
    cursor.execute("SELECT * FROM ammount WHERE Account_No = ?", (acc_no,))
    row = cursor.fetchone()
    if row is None:
        print(Fore.RED + "Account not found.")
        return
    else :
        balance = row[2]
        ammount = int(input("Please Enter the Ammount to be added into your account :"))
        balance = balance + ammount 
        print(balance)
        print(Fore.GREEN + "Account updated successfully")
        cursor.execute("UPDATE ammount SET Balance = ? where Account_No = ? ", (balance,acc_no,))
        cursor.execute("UPDATE bank SET Opening_bal = ? where Account_No = ? ", (balance,acc_no,))
        con.commit()

    
def withdraw_Money():
    acc_no  = int(input("Please Enter your Account number:"))
    cursor.execute("SELECT * FROM ammount WHERE Account_No = ?", (acc_no,))
    row = cursor.fetchone()
    if row is None:
        print(Fore.RED + "Account not found.")
        return
    balance = row[2]
    print(balance)
    with_ammount = int(input("Please Enter the Amount you want to withdraw:"))
    if with_ammount > balance:
        print(Fore.RED + "Insufficient Balance")
    else:
        print(Fore.GREEN + "Account updated successfully")
        rem = balance -with_ammount 
        cursor.execute("UPDATE ammount SET Balance = ? where Account_No = ? ", (rem,acc_no,))
        cursor.execute("UPDATE bank SET Opening_bal = ? where Account_No = ? ", (rem,acc_no,))
        con.commit()
        # exit()


def balance_Inquiry():
    acc_no  = int(input("Please Enter your Account number:"))
    cursor.execute("SELECT * FROM ammount WHERE Account_No = ?", (acc_no,))
    row = cursor.fetchone()
    
    if row is None:
        print(Fore.RED + "Account not found.")
        return
    else:
        balance = row[2]
        print("Your Account Balance is ",balance)


def delete():
    # cursor.execute("DROP TABLE IF EXISTS account")
    # cursor.execute("DROP TABLE IF EXISTS bank")
    cursor.execute("DELETE FROM ammount")
    cursor.execute("DELETE FROM bank")
    con.commit()

def show_all():
    #  acc_no = input("Please Enter your Account Number: ")
    cursor.execute("SELECT * FROM ammount")
    # cursor.execute("SELECT * FROM ammount where ")
    rows = cursor.fetchall()
    if len(rows) == 0:
        print("Account not Found")
    else:
        print("\n\n")
        print("Name\t\tAcc_Number\tBalance")
        for row in rows:
            print("{}\t\t{}\t\t{}".format(row[0], row[1], row[2]))
        print("\n\n")

while True :
    print(Fore.WHITE+"1. Open New Account ")
    print("2. Deposite Ammount ")
    print("3. Winthdraw Money")
    print("4. Balance Enquiry ")
    print("5. Show Customer Details")
    print("6. Delete all records")
    print("7. show All records")
    choice = int(input("Enter Your Choice From the above list :"))

    match choice:
        case 1:
            # account_no = account_no+1
            # print(account_no)
            open_Acc()
        case 2:
            Add_Ammount()
        case 3:
            withdraw_Money()
        case 4:
            balance_Inquiry()
        case 5: 
            show_Details()
        case 6:
            delete()
        case 7:
            show_all()
        case _:
            print("Please Enter the valid Chlice")

    