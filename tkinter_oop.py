from functools import partial
from tkinter import *
from database_connection import *

class ATM:
    #constructor
    def __init__(self,username,password):
        self.username = username
        self.password = password
    
    #create new user
    def register (username,password):
        username_value = username.get()
        password_value = password.get()
        if len(password_value) <= 0:
            Label(window,text ="This field cannot be empty!")
            window.destroy()
            raise LenZero
        
        #call function from database_connection file    
        create_user = create_new_user(username_value,password_value)      
        #if exists    
        if create_user:
            #create "successfully" label
            label_username = Label(window, text = f"Welcome, {username_value}")
            label_username.grid()
            label_password = Label(window,text = "Successfully created. Please log in.")
            label_password.grid(row = 3,column = 1)
            
        else:
            label_wrong = Label(window,text = "Something went wrong. Try Again!")
            label_wrong.grid()
        return create_user
    

    #fetch account info
    def  account_status (validation):
        #get username
        label_username = Label(window,text =f"Username: {validation[0][1]}")
        label_username.grid() 
        
        #get password
        label_password = Label(window,text =f"Password: {validation[0][2]}")
        label_password.grid()
        
        #get balance
        label_balance = Label(window,text = f"Balance: {validation[0][3]}")
        label_balance.grid()

    #payment method
    def payment (validation,balance):
        balance_value = int(balance.get())
        old_balance = int(validation[0][3])
        
        #Cannont payment -100
        if balance_value < 0:
            Label(window,text = "Payment balacne cannot be less then zero!")
            window.destroy()
            raise LessThenZero
        else:
            #if field not empty
            if balance_value:
                new_balance = old_balance + balance_value
                update_balance = database_manipulation("update","users","amount",new_balance,"password",validation[0][2])
                
                if update_balance:
                    Label(window, text = f"Old ablance: {old_balance}").grid()
                    Label(window, text = f"Payment: {balance_value}").grid()
                    Label(window, text = f"New balance: {new_balance}").grid()
                else:
                    Label(window,text = "Something went wrong!").grid()
            else:
                    Label(window,text = "Something went wrong!").grid()
   
    
    #withdraw money
    def withdraw (validation,balance):
        balance_value = int(balance.get())
        old_balance = int(validation[0][3])
        
        #For Example - > You connot withdraw -100  
        if balance_value < 0:
            Label(window,text ="Amount connot be less then zero")
            window.destroy()
            raise LessThenZero
        else:
            # Amount cannot be greater then your currently balance
            if balance_value <= old_balance:
                new_balance = old_balance - balance_value
                update_balance = database_manipulation("update","users","amount",new_balance,"password",validation[0][2])
                if update_balance:
                    Label(window, text = f"Old ablance: {old_balance}").grid()
                    Label(window, text = f"Withdraw: {balance_value}").grid()
                    Label(window, text = f"New balance: {new_balance}").grid()
                else:
                    Label(window,text = "Something went wrong!").grid()
            else:
                Label(window,text = "You don`t have enough money!").grid()
                
    
    #change password
    def change_password(validation,new_password):
            currently_password = validation[0][2]
            new_password = int(new_password.get())
            if len(str(new_password)) <= 0:
                Label(window,text ="This field cannot be empty!")
                window.destroy()
                raise LenZero 
            
            # check if user with that (new) password already exists
            #if not...update
            query_select = database_manipulation("select","users","password",new_password)
            query_update = database_manipulation("update","users","password",new_password,"password",currently_password)
            if not query_select:
                if query_update:
                    Label(window,text ="Password Successfully changed!").grid()
                    
                else:
                    Label(window,text = "Something went wrong! Try Again").grid()
            else:
                Label(window,text = "User with this password already exists!\nClose aplication and try again!").grid()
                
    #user login
    def login_validation (username,password):
        username_value = username.get()
        password_value = password.get()
        
        #check validation
        validate_user = database_maipulation_login(username_value,password_value)
        if validate_user:
            label_username = Label(window,text = (f"Successfully Login.\nHi, {username_value}"))
            label_username.grid()
            
            #create account status button
            account_status = partial(ATM.account_status,validate_user)
            account_status_button = Button(window,text = "Account status",command = account_status)
            account_status_button.grid()
            
            #change password
            #password label 
            password_label = Label(window,text = f"Currently password: {password_value}")
            password_label.grid(row = 7)
            # new password label and entry field 
            password_label = Label(window,text = "New Password")
            password_label.grid(row = 8)
            new_password = StringVar()
            password_entry = Entry(window,textvariable=new_password)
            password_entry.grid(row = 9)
            password_change = partial(ATM.change_password,validate_user,new_password)
            password_button = Button(window, text ="Change password",command = password_change)
            password_button.grid(row = 10)
            
            #balance
            label_balance = Label(window,text = f"Balance: {validate_user[0][3]}")
            label_balance.grid()
            
            #withdraw money from your account
            #withdraw label and entry field
            withdraw_money = StringVar()
            account_label  = Label(window,text="Amount: ")
            account_label.grid()
            account_entry  = Entry(window,textvariable=withdraw_money)
            account_entry.grid()
            #account button 
            account_withdraw = partial(ATM.withdraw,validate_user,withdraw_money)
            account_button = Button(window,text = "Withdraw",command = account_withdraw)           
            account_button.grid()
            
            #put money on your account
            #label and entry field
            money = StringVar()
            money_label = Label(window,text = "Amount: ")
            money_label.grid()
            money_entry = Entry(window,textvariable=money)
            money_entry.grid()
            #payment button
            payment_method = partial(ATM.payment,validate_user,money)
            payment_button = Button(window,text ="Payment",command = payment_method)
            payment_button.grid()
            
            
        else:
            label_wrong = Label(window,text = "Incorrect username or password. Try Again!")
            label_wrong.grid()
            
        return validate_user
 
    

#window 
window = Tk()
window.title("BANKOMAT APP")
window.geometry("300x300")


#username label and entry field 
username_label = Label(window,text = "Username: ").grid(column = 0,row = 0)
username = StringVar()
username_entry = Entry(window,textvariable=username).grid(column = 1,row = 0)

#password label and entry field 
password_label = Label(window,text = "Password").grid(column = 0,row = 1)
password = StringVar()
password_entry = Entry(window,textvariable=password,show = "*").grid(column = 1,row = 1)

#login button
validate_login = partial(ATM.login_validation,username,password)

login_button = Button(window,text = "Login",command = validate_login).grid(column = 1,row = 2)

#register button
register = partial(ATM.register,username,password)
register_button = Button(window,text ="Register", command=register).grid(column = 2,row = 2)

#info label
info_label = Label(window,text = "Please refresh the screen after each action. The program is in refinement.")
info_label.grid()

#start project 
window.mainloop()



