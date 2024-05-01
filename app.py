import datetime
import os
import sqlite3
from tkinter import Menu
from extra.money_format import in_money,out_money
# Importing all the windows
import windows.window_collector as w

# Inherits for a class that has all the functionalityes of all of the other clases
class Window(w.All):
    def __init__(self, master):
        # Declaring atributes that will be called repetedly
        self.transactions = []
        self.master = master
        # If there is not database, one is created
        if not os.path.exists(os.path.join(os.getcwd(), "transactions.db")):
             
            # Creation of database and the "cursor"
            self.conection = sqlite3.connect(os.path.join(os.getcwd(), "transactions.db"))
            self.cursor = self.conection.cursor()
            # Creating the tables and default values
            self.cursor.execute("""
CREATE TABLE "transactions" (
    "id" INTEGER PRIMARY KEY,
    "title" TEXT NOT NULL,
    "type" TEXT CHECK("type" IN ('clothing and accessories','education','entertainment','foods','gifts and donations','health and hygiene','housing',
    'insurance','investments','others','personal care','pets','taxes and fees','technology','transportation','travel')),
    "amount" INTEGER NOT NULL,
    "date" DATE NOT NULL
); """)
            self.cursor.execute("""
CREATE TABLE "user_data" (
    "balance" INTEGER,
    "budget" INTEGER,
    "period" INTEGER -- 1 = daily, 2 = weekly, 3 = monthly
); """)
            self.cursor.execute("""
CREATE TABLE "reminder" (
    "id" INTEGER PRIMARY KEY,
    "name" TEXT NOT NULL,
    "type" TEXT CHECK("type" IN ('clothing and accessories','education','entertainment','foods','gifts and donations','health and hygiene','housing',
    'insurance','investments','others','personal care','pets','taxes and fees','technology','transportation','travel')),
    "amount" INTEGER,
    "date" TEXT NOT NULL
); """)
            self.cursor.execute("""
INSERT INTO "user_data" ("balance","budget","period") VALUES (0,0,3); 
                                """)
        # If there is a database connects to it and declare the cursor
        else:
            self.conection = sqlite3.connect("transactions.db")
            self.cursor = self.conection.cursor()    
            
        # Query to get the balance and formatting it
        self.cursor.execute(""" SELECT "balance" FROM "user_data" """)
        self.balance = out_money(self.cursor.fetchone()[0])      
        # Declaring the type_options value          
        self.type_options = ['clothing and accessories','education','entertainment','foods','gifts and donations','health and hygiene','housing',
        'insurance','investments','others','personal care','pets','taxes and fees','technology','transportation','travel']
        
        # VALIDATIONS
        ## Declaring the number validation process
        self.v_number = (self.master.register(self.valid_number), '%P')
        
        # NAVBAR
        ## Creating the menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)
        
        ## Creating the menu elements
        
        ### Balance menu
        self.balance_menu = Menu(self.menu, tearoff=0)
        self.balance_menu.add_command(label="Add", command=lambda : self.create_menu("create_add_balance_menu"))
        self.balance_menu.add_command(label="Reduce", command=lambda : self.create_menu("create_reduce_balance_menu"))
        self.balance_menu.add_command(label="Set", command=lambda : self.create_menu("create_set_balance_menu"))
        self.balance_menu.add_separator()
        self.balance_menu.add_command(label="Set Budget", command=lambda  : self.create_menu("create_budget_menu"))
        self.menu.add_cascade(label="Balance", menu=self.balance_menu)
        
        ### Transactions menu
        self.transactions_menu = Menu(self.menu, tearoff=0)
        self.transactions_menu.add_command(label="Create", command=lambda  : self.create_menu("create_transaction_menu"))
        self.transactions_menu.add_command(label="Visualize", command=lambda  : self.change_window("create_graph_view"))
        self.menu.add_cascade(label="Transactions", menu=self.transactions_menu)
        
        ### Reminders menu
        self.reminders_menu = Menu(self.menu, tearoff=0)
        self.reminders_menu.add_command(label="Create", command=lambda  : self.create_menu("create_reminder_menu"))
        self.reminders_menu.add_command(label="List", command=lambda  : self.create_menu("create_reminder_list"))
        self.menu.add_cascade(label="Reminders", menu=self.reminders_menu)

        
        # Calling the create menu to display the view
        self.create_window("create_table_view")

        
    def set_warn(self,text):
        """
        Displays a warn into the form
        """
        self.warn_label.config(text=text)
        
    def transaction_validation(self,title,type,amount,date):
        """Checks if a transactions values are valid or not

        Args:
            title (str): The transaction name
            type (str): The transaction type
            amount (str): The amount 
            date (str): Date in iso format

        Returns:
            bool: True or False
        """
        # Checking the values
        ## title, must be between 1 and 30 characters
        if title == "":
            self.set_warn("Name requiered")
            return False
        if len(title) > 30:
            self.set_warn("Name is too long")
            return False
        ## type, must be in the list
        if type not in self.type_options:
            self.set_warn("Type not allowed")
            return False
        ## amount, must be a number
        if amount == "":
            self.set_warn("Amount requiered")
            return False
        try:
            amount = float(amount)
        except:
            self.set_warn("Amount must be a number")
            return False
        
        ## Date, must be a iso formated date
        try:
            # gives and exeptions if the date format is not iso
            self.format_input_date(date)
        except:
            self.set_warn("Date format not supported")
            return False
        
        
        return True
    
    def format_input_date(self,date):
        """Validation of iso format date

        Args:
            date (str): A date in iso format

        Returns:
            object: a datetime object
        """
        new_date_div = date.split("-")
        return datetime.date(int(new_date_div[0]),int(new_date_div[1]),int(new_date_div[2]))
    
    # Close app method
    def close_app(self):
        # Updates the balance
        self.cursor.execute(""" UPDATE "user_data" SET "balance" = (?)  """, (in_money(self.balance),))
        self.conection.commit()
        # Close the connection
        self.conection.close()
        # Destroy the window
        self.master.destroy()
        
    # Method call in the number validation
    def valid_number(self, new_input):
        """Validate if the number given could be
           convert into a float

        Args:
            new_input (str): A number

        Returns:
            Bool: True if it could be convert into a float, False if not
        """
        if new_input == "":
            return True

        try:
            float(new_input)
            return True
        except ValueError:
            return False
