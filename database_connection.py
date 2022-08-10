import mysql.connector

#database
my_database = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "bankomat"
)

        

#cursor
my_cursor = my_database.cursor()


#login management function
def database_maipulation_login(username,password):
    sql = f"select * from bankomat.users where username = '{username}' and password = '{password}' limit 1"
    my_cursor.execute(sql)
    my_result = my_cursor.fetchall()
    return  my_result

#database management content
def database_manipulation(type,table,column,column_value,key_update_field = None,value_update_field=None):
    
    #read data
    if type.lower().strip() == "select".lower().strip():
        sql = f"{type} * from bankomat.{table} where {column} = '{column_value}'"
        my_cursor.execute(sql)
        my_result = my_cursor.fetchall()
        return my_result
    
    #update data
    if type.lower().strip() == "update".lower().strip():
        if int(value_update_field) >= 0:
                
            sql = f"{type} {table} SET {column} = '{column_value}' where {key_update_field} = '{value_update_field}'"
            my_cursor.execute(sql)
            my_database.commit()
            return True
    

#create new user
def create_new_user(username,password):
   sql = f"SELECT * FROM users WHERE password = {password}"
   my_cursor.execute(sql)
   result = my_cursor.fetchall()
   
   if not result:
        if len(result) > 0:
            print("User with that password already exists!")
        else: 
            sql = f"INSERT INTO users(username,password,amount) VALUES ('{username}',{password},0)"
            my_cursor.execute(sql)
            my_database.commit()
            return True      
            
     
#excetion raised class
class LessThenZero(Exception):
    """ Error raised for errors in input amount (If integer is less then zero)
    Attributes: 
        message: -> explanation of the error
    
    """
    
    def __init__(self,message ="The amount is less then zero "):
        self.message = message
        super().__init__(message)

class LenZero(Exception):
    """ Error raised for errorrs in inputs (If len <= 0)
    Attributes:
        message: -> explanation of the error 
    
    """
    
    def __init__(self,message ="Len is less then zero"):
        self.message = message 
        super().__init__(message)