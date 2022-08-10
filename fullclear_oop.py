from database_connection import *


class ATM:
    def __init__(self,username,password):
        print("Welcome to ATM System!")
        self.username = username 
        self.password = password
        
    def register(self,username,password):
        create_user = create_new_user(username,password)
        return create_user
    
    def login(self):
        validate_user = database_manipulation("select","users","password",f"{self.password}")
        print(validate_user)
        return validate_user
    
    #fetch account info
    def  account_status (self,validation):
        print("Username: ",validation[0][1])
        print("Balacne:",validation[0][3])
        print("Password:",validation[0][2])
        print("*"*18)
        user_option = int(input("Select option: 1)Money payment 2)Money payout 3)Change Password  4) Exit: "))
        if user_option == 1:
            self.money_payment(validation=validation)
        elif user_option == 2:
            self.money_payout(validation=validation)
        elif user_option == 3:
            ATM.change_password(validation=validation)
        else:
            exit()
    
    #deposit money into your account
    def money_payment(self,validation):
        print("Money payment!")
        print("Balance:",validation[0][3])
        self.amount = int(input("Amount: "))
        if self.amount < 0:
            raise LessThenZero()
        
        currently_balacne = int(validation[0][3]) + self.amount
        update = database_manipulation("update","users","amount",f"{currently_balacne}","password",f"{self.password}")
        print("New balance:",currently_balacne)
        print("*"*18)
        
        if update:
            user_option = int(input("Select option: 1)Money_payment 2)Money_payout 3)Change Password  4) Exit: "))
            if user_option == 1:
                self.money_payment(validation=validation)
            elif user_option == 2:
                self.money_payout(validation=validation)
            elif user_option == 3:
                ATM.change_password(validation=validation)
            else:
                exit()
                
        else:
            print("Something went wrong, try again or exit!")
            user_option = int(input("Select: 1)Try again   2)Exit   "))            
            if user_option == 1: 
             self.money_payment(validation = validation)
            else: 
                exit()
    
            
        
    # withdraw money 
    def money_payout(self,validation):
        print("Money payout!")
        print("Balance:",validation[0][3])
        self.amount = int(input("Amount: "))
        if self.amount < 0:
            raise LessThenZero()
            
        currently_balacne = int(validation[0][3]) - self.amount
        update = database_manipulation("update","users","amount",f"{currently_balacne}","password",f"{self.password}")
        print("New balance:",currently_balacne)
        print("*"*18)
        if update:
            user_option = int(input("Select option: 1)Money_payment 2)Money_payout 3)Change Password  4) Exit: "))
            if user_option == 1:
                self.money_payment(validation=validation)
            elif user_option == 2:
                self.money_payout(validation=validation)
            elif user_option == 3:
                ATM.change_password(validation=validation)
            else:
                exit()
        else:
            print("Something went wrong, try again or exit!")
            user_option = int(input("Select: 1)Try again   2)Exit   "))            
            if user_option == 1: 
             self.money_payment(validation = validation)
            else: 
                exit()

    
    #change password
    def change_password(self,validation):
        print("Change password!")
        print("password:",validation[0][2])
        old_password = validation[0][2]
        self.new_password = int(input("New password: "))
        update = database_manipulation("update","users","password",self.new_password,"password",old_password)
        print("New Password:",self.new_password)
        print("*"*18)
        if update:
            user_option = int(input("Select option: 1)Status 2)Money_payment 3)Money_payout  4) Exit: "))
            if user_option == 1:
                self.account_status(validation = validation)
            elif user_option == 2:
                self.money_payment(validation=validation)
            elif user_option == 3:
                self.money_payout(validation=validation)
            else:
                exit()
        else:
            print("Something went wrong, try again or exit!")
            user_option = int(input("Select: 1)Try again   2)Exit   "))            
            if user_option == 1: 
             self.money_payment(validation = validation)
            else: 
                exit()
       


#user option
def choose(user_select,validation):
    if user_select == 1:
        atm.account_status(validation)
    elif user_select == 2:
        atm.money_payment(validation)
    elif user_select == 3:
        atm.money_payout(validation)
    elif user_select == 4:
        atm.change_password(validation)

while True:
    #user info
    username = input("Username: ")
    password = input("Password: ")

    #object 
    atm = ATM(username,password)

    validation = atm.login()
    if len(validation) > 0:
        user_select = int(input("Select option: "))
        choose(user_select,validation)
    else: 
        print("You don`t have account?")
        user_option = int(input("1)Create account or exit"))
        if user_option == 1:
           username = input("Username: ")
           password = input("Password: ")
           atm.register(username,password)
            

        
        