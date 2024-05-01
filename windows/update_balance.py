import tkinter as tk
from windows.window_functionalities import Functionality

class UpdateBalanceWindow(Functionality):
    
    def core_balance_menu(self):
        # Creates the core menu
        self.balance_menu = tk.Toplevel(self.frame)
        self.balance_menu.title("Balance")
        self.balance_menu.geometry(self.menu_position())
        self.balance_menu.grab_set()
        
        # Title
        self.title = tk.Label(self.balance_menu, text="--")
        self.title.pack()
        
        
        # Status information
        self.status_frame = tk.Frame(self.balance_menu)
        self.status_frame.pack()
        
        ## Actual and new balance labels
        self.actual_label = tk.Label(self.status_frame, text="Actual Balance")
        self.actual_label.grid(row=0, column=0)
          
        self.new_label = tk.Label(self.status_frame, text="New Balance")
        self.new_label.grid(row=0, column=2)
        
        ## Amount labels
        self.actual_label_n = tk.Label(self.status_frame, text=f"${'{:.2f}'.format(round(self.balance,2))}")
        self.actual_label_n.grid(row=1, column=0)
        
        self.arrow = tk.Label(self.status_frame, text="=>")
        self.arrow.grid(row=1, column=1)
        
        self.new_label_n = tk.Label(self.status_frame, text=f"${'{:.2f}'.format(round(self.balance,2))}")
        self.new_label_n.grid(row=1, column=2)
        
        ## Entry and accept button
        self.balance_entry = tk.Entry(self.status_frame, state="normal", validate="key", validatecommand=self.v_number)
        self.balance_entry.grid(row=2, column=0, columnspan=2)
        self.balance_entry.bind("<KeyRelease>", self.update_balance_label)
        
        ## Accept button
        self.accept_button = tk.Button(self.status_frame, text="Acept", command=self.confirm_update)
        self.accept_button.grid(row=2, column=2)
    
    def create_add_balance_menu(self):
        """
        Creates the balance menu with the add functionality
        """
        
        self.core_balance_menu()
        
        self.transaction_type = "add"
    
        self.title.config(text="Add balance")
        
    def create_reduce_balance_menu(self):
        """
        Creates the balance menu with the reduce functionality
        """
        self.core_balance_menu()
        
        self.transaction_type = "reduce"
    
        self.title.config(text="Reduce balance")
        
    def create_set_balance_menu(self):
        """
        Creates the balance menu with the set functionality
        """
        self.core_balance_menu()
        
        self.transaction_type = "set"
    
        self.title.config(text="Set balance")
    
    
    def update_balance_label(self,event):
        """
        Updates the new amount label depending on the type of update
        """
        if self.transaction_type == "add":
            try:
                self.new_label_n.config(text=f"${'{:.2f}'.format(round((self.balance + float(self.balance_entry.get())),2))}")
            except:
                self.new_label_n.config(text=f"${'{:.2f}'.format(round(self.balance,2))}")
                
        if self.transaction_type == "reduce":
            try:
                self.new_label_n.config(text=f"${'{:.2f}'.format(round((self.balance - float(self.balance_entry.get())),2))}")
            except:
                self.new_label_n.config(text=f"${'{:.2f}'.format(round(self.balance,2))}")
                
                
        if self.transaction_type == "set":
            try:
                self.new_label_n.config(text=f"${'{:.2f}'.format(round((float(self.balance_entry.get())),2))}")
            except:
                self.new_label_n.config(text=f"${'{:.2f}'.format(round(self.balance,2))}")



        
    def confirm_update(self):
        """
        Updates the balance and close the menu
        """

        if self.transaction_type == None:
            pass
        
        elif self.transaction_type == "add":
            self.balance += round(float(self.balance_entry.get()),2)
            
        elif self.transaction_type == "reduce":
            self.balance -= round(float(self.balance_entry.get()),2)
            
        elif self.transaction_type == "set":
            self.balance = round(float(self.balance_entry.get()),2)
            
        self.close_balance_menu()
        
    def close_balance_menu(self):
        """
        Close menu method
        """
        self.balance_menu.destroy()
        self.change_window("create_table_view")