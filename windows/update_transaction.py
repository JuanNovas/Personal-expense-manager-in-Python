from windows.window_functionalities import Functionality
from extra.money_format import in_money, out_money
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

class UpdateTransactionWindow(Functionality):
    def create_upate_transaction_menu(self):
        # Menu creation
        self.transaction_menu = tk.Toplevel(self.frame)
        self.transaction_menu.title("Update transaction")
        self.transaction_menu.geometry(self.menu_position())
        self.transaction_menu.grab_set() 
        
        # Getting the original transaction information
        self.cursor.execute("""SELECT * FROM "transactions" WHERE id = (?) """,(self.transaction_update_id,))
        self.pre_transaction = self.cursor.fetchall()[0]
        
        self.transaction_update = {
                "id" : self.pre_transaction[0],
                "name" : self.pre_transaction[1],
                "type" : self.pre_transaction[2],
                "amount" : out_money(self.pre_transaction[3]),
                "date" : self.pre_transaction[4]
            }
        
        # Menu frame
        self.transaction_frame = tk.Frame(self.transaction_menu)

        # Configure the grid to expand widgets
        self.transaction_frame.columnconfigure(0, weight=1)
        self.transaction_frame.columnconfigure(1, weight=1)

        # Title
        self.section_title_label = tk.Label(self.transaction_frame, text="Update Transaction")
        self.section_title_label.grid(row=0, column=1)
        
        
        # Name
        self.title_label = tk.Label(self.transaction_frame, text="Name: ")
        self.title_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.transaction_title = tk.Entry(self.transaction_frame)
        self.transaction_title.insert(0, self.transaction_update["name"])
        self.transaction_title.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        # Type
        self.type_label = tk.Label(self.transaction_frame, text="Type: ")
        self.type_label.grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.selected_value = tk.StringVar()
        self.transaction_type = ttk.Combobox(self.transaction_frame, textvariable=self.selected_value, values=self.type_options)
        self.transaction_type.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        self.transaction_type.set(self.type_options[self.type_options.index(self.transaction_update["type"])])
        self.transaction_type.bind('<KeyRelease>', self.update_options)
               
        # Amount
        self.amount_label = tk.Label(self.transaction_frame, text="Amount: ")
        self.amount_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        
        self.transaction_amount = tk.Entry(self.transaction_frame, validate="key", validatecommand=self.v_number)
        self.transaction_amount.insert(0,f"{'{:.2f}'.format(round(self.transaction_update['amount']),2)}")
        self.transaction_amount.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        # Date
        self.date_label = tk.Label(self.transaction_frame, text="Date")
        self.date_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        
        self.transaction_date = DateEntry(self.transaction_frame, date_pattern='yyyy-mm-dd')
        self.transaction_date.set_date(self.transaction_update["date"])
        self.transaction_date.grid(row=4, column=1, sticky="we", padx=5, pady=5)
        
        # Confirm button
        self.transaction_complete = tk.Button(self.transaction_frame, text="Confirm", height=2, width=12, command=lambda : self.confirm_transaction_update(self.transaction_title.get(),self.transaction_type.get(),self.transaction_amount.get(),self.transaction_date.get()))
        self.transaction_complete.grid(row=5, column=1, padx=5, pady=5)
        
        # Delete button
        self.delete = tk.Button(self.transaction_frame, text="Delete",command=self.delete_transaction)
        self.delete.grid(row=5,column=0, sticky="we")
        
        # Warn label
        self.warn_label = tk.Label(self.transaction_frame)
        self.warn_label.grid(row=6, column=1, pady=10)
    
    
        # Packing the frame
        self.transaction_frame.pack()
    
   
        
        
    def confirm_transaction_update(self, new_title, new_type, new_amount, new_date):
        """
        Checks if the new transaction data is valid, and saves it
        """
        
        if self.transaction_validation(new_title,new_type, new_amount, new_date):
            # Updateing balance
            self.balance += round((float(self.transaction_update["amount"]) - float(new_amount)),2)
            # Formating new date
            new_date_formated = self.format_input_date(new_date)
            # Updating transactions db
            self.cursor.execute(""" UPDATE  "transactions" set "title" = (?), "type" = (?), "amount" = (?), "date" = (?) WHERE "id" = (?) """,(new_title,new_type,in_money(new_amount),new_date_formated,self.transaction_update["id"]))
            self.conection.commit()
            # Changing window
            self.close_update_transaction_menu()
        
        
    def delete_transaction(self):
        """
        Deletes the transaction
        """
        # Ask for a confirmation
        answer = messagebox.askyesno("Delete transaction", "Are you sure you want to delete this transaction?")
        # Delets the transaction depending on the answer
        if answer:
            self.balance += self.transaction_update["amount"]
            self.cursor.execute(""" DELETE FROM "transactions" WHERE "id" = (?) """,(self.transaction_update["id"],))
            self.conection.commit()
            self.close_update_transaction_menu()
        else:
            return
        
        
    def close_update_transaction_menu(self):
        """
        Close method
        """
        self.transaction_menu.destroy()
        self.change_window("create_table_view")