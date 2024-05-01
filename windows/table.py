import tkinter as tk
from windows.window_functionalities import Functionality
from extra.money_format import out_money
from tkinter import ttk
import datetime

class TableWindow(Functionality):
    def create_table_view(self):
        # Frame
        self.frame = tk.Frame(self.master)

        # Creating the Header
        self.header_frame = tk.Frame(self.frame)
        
        self.header_frame.columnconfigure(0, weight=1)
        self.header_frame.columnconfigure(1, weight=1)
        
        ## Budget frame
        self.budget_label = tk.Label(self.header_frame, text="--", font=("Verdana", 12))
        self.budget_label.grid(row=1,column=0, sticky="nw")
        self.set_budget_label()
        
        ## Balance label
        self.balance_label = tk.Label(self.header_frame, text=f"Balance: ${'{:.2f}'.format(round(self.balance,2))}", font=("Verdana", 12))
        self.balance_label.grid(row=0, column=0, sticky="nw")
        

        
        ## Edit Button

        self.edit_button = tk.Button(self.header_frame, text="Edit", command=self.edit_transaccion, font=("Verdana", 10))
        self.edit_button.grid(row=0, column=1, sticky="ne")
        
        ## Reminder Label
        
        self.reminder_label = tk.Label(self.header_frame, font=("Verdana", 12))
        self.reminder_label.grid(row=1, column=1, sticky="ne")
        self.set_reminder_label()
        
        self.header_frame.pack(side="top", fill="x")

        # Creating list of transactions
        self.transactions_table = ttk.Treeview(self.frame, columns=("Name", "Type", "Amount", "Date"), show="headings")
        
        # Configurating the headers
        self.transactions_table.heading("Name", text="Name")
        self.transactions_table.heading("Type", text="Type")
        self.transactions_table.heading("Amount", text="Amount")
        self.transactions_table.heading("Date", text="Date")
        
        self.transactions_table.column("Name", anchor="center") 
        self.transactions_table.column("Type", anchor="center")
        self.transactions_table.column("Amount", anchor="center")
        self.transactions_table.column("Date", anchor="center")
        
        # Adding the transactions
        self.cursor.execute("""SELECT * FROM "transactions" ORDER BY date ASC""")
        pre_transactions = self.cursor.fetchall()
        self.transactions = []
        for pre_transaction in pre_transactions:
            self.transactions.insert(0,{
                "id" : pre_transaction[0],
                "name" : pre_transaction[1],
                "type" : pre_transaction[2],
                "amount" : out_money(pre_transaction[3]),
                "date" : pre_transaction[4]
            })
        for transaction in self.transactions:
            self.transactions_table.insert("", "end", values=(transaction["name"], transaction["type"], "$" + str("{:.2f}".format(transaction["amount"])), transaction["date"]), tags=(transaction["id"],))
        
        self.transactions_table.pack(pady=40)

    
        self.frame.pack(pady=10)

        
    def set_budget_label(self):
        """
        Gets the data from the db and update the budget label
        """
        # Gets budget and period from the db
        self.cursor.execute(""" SELECT "budget" FROM "user_data" """)
        budget = out_money(self.cursor.fetchone()[0])
        
        self.cursor.execute(""" SELECT "period" FROM "user_data" """)
        
        # Defines the period variable
        today = datetime.datetime.now()
        match self.cursor.fetchone()[0]:
            case 1:
                period = today
            case 2:
                period = today - datetime.timedelta(days=today.weekday())
            case 3:
                period = datetime.datetime(today.year, today.month, 1)

        # Checks how much was spent in the specific period of time
        self.cursor.execute(f""" SELECT SUM("amount") FROM "transactions" WHERE "date" >= DATE(?);""",(period,))
        amount_spent = self.cursor.fetchone()[0]
        if not amount_spent:
            amount_spent = 0
        total = budget - (out_money(amount_spent))
        
        # Defines the color of the text
        if total > 0:
            fg = "black"
        else:
            fg = "red"
        
        # Updates the label
        self.budget_label.config(fg=fg,text=f"Budget:  ${'{:.2f}'.format(round(total,2))}/{'{:.2f}'.format(round(budget,2))}")
        
    def set_reminder_label(self):
        """
        Checks if there is a reminder overdue and show the reminder
        """
        self.cursor.execute("""SELECT * FROM "reminder" WHERE "date" <= (?) """, (datetime.datetime.now(),))
        reminders = self.cursor.fetchall()
        if reminders:
            self.reminder_label.config(text="!!!Overdue Reminder", fg="red")
    
    def edit_transaccion(self):
        """
        Checks if there is a transaction selected and creates the transaction menu
        """
        try:
            selected_item = self.transactions_table.focus()
            self.transaction_update_id = self.transactions_table.item(selected_item, "tags")[0]
            self.create_menu("create_upate_transaction_menu")
        except IndexError:
            pass