import datetime
from tkcalendar import DateEntry
from windows.window_functionalities import Functionality
from extra.money_format import in_money
import tkinter as tk
from tkinter import ttk

class TransactionWindow(Functionality):
    
    def create_transaction_menu(self):
        # Creating the menu
        self.transaction_menu = tk.Toplevel(self.frame)
        self.transaction_menu.title("New transaction")
        self.transaction_menu.geometry(self.menu_position())
        self.transaction_menu.grab_set()
        
        self.transaction_frame = tk.Frame(self.transaction_menu)
        
        # Configure the grid to expand widgets
        self.transaction_frame.columnconfigure(0, weight=1)
        self.transaction_frame.columnconfigure(1, weight=1)

        # Title
        self.section_title_label = tk.Label(self.transaction_frame, text="New Transaction")
        self.section_title_label.grid(row=0, column=1)
        
        
        # Name
        self.title_label = tk.Label(self.transaction_frame, text="Name: ")
        self.title_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.transaction_title = tk.Entry(self.transaction_frame)
        self.transaction_title.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        # Type
        self.type_label = tk.Label(self.transaction_frame, text="Type: ")
        self.type_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.selected_value = tk.StringVar()
        self.transaction_type = ttk.Combobox(self.transaction_frame, textvariable=self.selected_value, values=self.type_options)
        self.transaction_type.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        self.transaction_type.bind('<KeyRelease>', self.update_options)
               
        # Amount
        self.amount_label = tk.Label(self.transaction_frame, text="Amount: ")
        self.amount_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        
        self.transaction_amount = tk.Entry(self.transaction_frame, validate="key", validatecommand=self.v_number)
        self.transaction_amount.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        # Date
        self.date_label = tk.Label(self.transaction_frame, text="Date")
        self.date_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        
        self.transaction_date = DateEntry(self.transaction_frame, date_pattern='yyyy-mm-dd')
        self.transaction_date.set_date(datetime.datetime.now())
        self.transaction_date.grid(row=4, column=1, sticky="we", padx=5, pady=5)
        
        # Confirm button
        self.transaction_complete = tk.Button(self.transaction_frame, text="Confirm", height=2, width=12, command=lambda : self.create_transaction(self.transaction_title.get(),self.transaction_type.get(),self.transaction_amount.get(),self.transaction_date.get()))
        self.transaction_complete.grid(row=5, column=1, padx=5, pady=5)
        
        # Warn label
        self.warn_label = tk.Label(self.transaction_frame)
        self.warn_label.grid(row=5, column=0, pady=10)
    
    
    
        self.transaction_frame.pack()
        
    def create_transaction(self,title,type,amount,date):
        """
        Checks if the transaction data is valid and load it
        """
        if self.transaction_validation(title,type,amount,date):

            amount_todb = in_money(amount)
            self.cursor.execute("""INSERT INTO "transactions" ("title","type","amount","date") VALUES ((?),(?),(?),(?))""",(title,type,amount_todb,date))
            self.balance -= round(float(amount),2)
            self.conection.commit()
            self.close_transaction_menu()
            
            
    def update_options(self, event):
        """
        Updates the options to pair the characters given
        """
        input_text = self.transaction_type.get()
        filtered_options = [option for option in self.type_options if option.lower().startswith(input_text.lower().strip())]


        self.transaction_type['values'] = filtered_options
        
        
    def close_transaction_menu(self):
        """
        Close menu method
        """
        self.transaction_menu.destroy()
        self.change_window("create_table_view")
        