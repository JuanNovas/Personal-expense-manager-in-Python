import tkinter as tk
from windows.window_functionalities import Functionality
from extra.money_format import in_money, out_money

class BudgetWindow(Functionality):
    
    def create_budget_menu(self):
        # Menu creation
        self.budget = tk.Toplevel(self.frame)
        self.budget.title("Budget")
        self.budget.geometry(self.menu_position())
        self.budget.grab_set()
        
        # Frame
        self.budget_frame = tk.Frame(self.budget)
        
        # Configure the grid to expand widgets
        self.budget_frame.columnconfigure(0, weight=1)
        self.budget_frame.columnconfigure(1, weight=1)
        
        # Amount
        self.amount_label = tk.Label(self.budget_frame, text="Budget")
        self.amount_label.grid(row=0, column=0)
        
        self.set_budget_entry = tk.Entry(self.budget_frame, state="normal", validate="key", validatecommand=self.v_number)
        self.cursor.execute(""" SELECT "budget" FROM "user_data" """)
        budget = out_money(self.cursor.fetchone()[0])
        self.set_budget_entry.insert(0,'{:.2f}'.format(round(budget,2)))
        self.set_budget_entry.grid(row=1, column=0, sticky="e")
        
        # Period
        self.period_label = tk.Label(self.budget_frame, text="Period")
        self.period_label.grid(row=0,column=1)
        
        options = ["daily", "weekly", "monthly"]
        selected_option = tk.StringVar(self.budget_frame)
        self.cursor.execute(""" SELECT "period" FROM "user_data" """)
        selected_option.set(options[self.cursor.fetchone()[0] - 1])
        
        self.period_menu = tk.OptionMenu(self.budget_frame, selected_option, *options)
        self.period_menu.grid(row=1, column=1, sticky="we", padx=2, pady=1)
    
        # Confirm button
        self.confirm_button = tk.Button(self.budget_frame,text="Confirm",command=lambda selected_option=selected_option: self.confirm_budget(selected_option))
        self.confirm_button.grid(row=2, column=1, sticky="we", padx=4)
        
        self.budget_frame.pack()
    
    
    def close_budget_menu(self):
        """
        close method
        """
        self.budget.destroy()
        self.change_window("create_table_view")
    
        
        
    def confirm_budget(self, selected_option):
        """
        Loads the information into the database
        """
        
        match selected_option.get():
            case "daily" : 
                period_id = 1
            case "weekly" :
                period_id = 2
            case "monthly" :
                period_id = 3
                
        self.cursor.execute(""" UPDATE "user_data" SET "budget" = (?), "period" = (?)  """, (in_money(self.set_budget_entry.get()),period_id))
        self.conection.commit()

        self.close_budget_menu()
        
        