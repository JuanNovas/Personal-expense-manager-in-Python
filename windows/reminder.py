import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from windows.window_functionalities import Functionality
from tkcalendar import DateEntry
from datetime import datetime, timedelta, date
from extra.money_format import in_money, out_money

class ReminderMenu(Functionality):
    def create_reminder_menu(self):
        # Menu creation
        self.reminder_menu = tk.Toplevel(self.frame)
        self.reminder_menu.title("Create Reminder")
        self.reminder_menu.geometry(self.menu_position())
        
        self.reminder_menu.grab_set()
        # Frame
        self.reminder_frame = tk.Frame(self.reminder_menu)
        
        # Configure the grid to expand widgets
        self.reminder_frame.columnconfigure(0, weight=1)
        self.reminder_frame.columnconfigure(1, weight=1)
        
        self.title_label = tk.Label(self.reminder_frame, text="New reminder")
        self.title_label.grid(row=0, column=1)
        
        # Name of the reminder
        self.name_label = tk.Label(self.reminder_frame, text="Reminder: ")
        self.name_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)
        
        self.name_entry = tk.Entry(self.reminder_frame)
        self.name_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        
        # Type of the reminder
        self.type_label = tk.Label(self.reminder_frame, text="Type: ")
        self.type_label.grid(row=2, column=0)
        
        self.selected_value = tk.StringVar()
        self.transaction_type = ttk.Combobox(self.reminder_frame, textvariable=self.selected_value, values=self.type_options)
        self.transaction_type.grid(row=2, column=1, sticky="we", padx=5, pady=5)
        self.transaction_type.bind('<KeyRelease>', self.update_options)
        
        # Amount of the reminder if any
        self.amount_label = tk.Label(self.reminder_frame, text="Amount: ")
        self.amount_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)
        
        self.amount_entry = tk.Entry(self.reminder_frame, validate="key", validatecommand=self.v_number)
        self.amount_entry.grid(row=3, column=1, sticky="we", padx=5, pady=5)
        
        # Date of the reminder
        self.date_label = tk.Label(self.reminder_frame, text="Date: ")
        self.date_label.grid(row=4, column=0, sticky="e", padx=5, pady=5)
        
        self.date_entry = DateEntry(self.reminder_frame, date_pattern='yyyy-mm-dd')
        self.date_entry.set_date(datetime.now() + timedelta(days=6))
        self.date_entry.grid(row=4, column=1, sticky="we", padx=5, pady=5)
        
        # Confirm button
        self.confirm_button = tk.Button(self.reminder_frame, text="Confirm", height=2, width=12, command=self.confirm_reminder)
        self.confirm_button.grid(row=5, column=1)
        
        # Warn label
        self.warn_label = tk.Label(self.reminder_frame)
        self.warn_label.grid(row=5, column=0)
        
        self.reminder_frame.pack()


    def create_reminder_list(self):
        # Creation of the menu
        self.reminder_list = tk.Toplevel(self.frame)
        self.reminder_list.title("Reminders")
        self.reminder_list.geometry(self.menu_position())
        
        self.reminder_list.grab_set()

        # Get the reminders data
        self.cursor.execute("""SELECT * FROM "reminder" ORDER BY "date" """)
        self.reminders = self.cursor.fetchall()
        
        # Defines the page
        self.page = 1
        
        self.create_page()
        
        
    def ask_delete_reminder(self, id, frame):
        """
        Adk to delete the reminder, and deletes it
        """
        
        answer = messagebox.askyesno("Delete reminder", "Are you sure you want to delete this reminder?")
        if answer:
            self.delete_reminder(id, frame)

            

    def delete_reminder(self, id, frame): 
        """
        Deletes the reminder
        """
    
        self.cursor.execute("""DELETE FROM "reminder" WHERE "id" = (?) """, (id,))
        self.conection.commit()
        
        self.cursor.execute("""SELECT * FROM "reminder" ORDER BY date """)
        reminders = self.cursor.fetchall()
        if not reminders:
            self.no_reminder()
        
        self.close_reminder_list()
        
    def load_reminder(self, id, frame):
        """
        Ask to loads the reminder as a transaction into the database
        """
        answer = messagebox.askyesno("Load transaction", "Are you sure you want to load this transaction?")
        if not answer:
            return
        self.cursor.execute("""SELECT * FROM "reminder" WHERE "id" = (?) """,(id,))
        reminder = self.cursor.fetchone()
        
        self.cursor.execute("""INSERT INTO "transactions" ("title","type","amount","date") VALUES ((?),(?),(?),(?))""",(reminder[1],reminder[2],reminder[3],reminder[4]))
        self.balance -= round(float(out_money(reminder[3])),2)
        self.conection.commit()
        
        self.delete_reminder(id, frame)



    def confirm_reminder(self):
        """
        Validates the reminder and loads it into the database
        """
        
        if self.transaction_validation(self.name_entry.get(),self.transaction_type.get(),self.amount_entry.get(),self.date_entry.get()):
            self.cursor.execute("""INSERT INTO "reminder" ("name","type","amount","date") VALUES ((?),(?),(?),(?))""",(self.name_entry.get(),self.transaction_type.get(),in_money(self.amount_entry.get()),self.date_entry.get()))
            self.conection.commit()
            self.reminder_menu.destroy()
            
            
    def no_reminder(self):
        """
        Creates a no reminder label
        """
        self.no_reminder_label = tk.Label(self.reminder_list, text="No reminders")
        self.no_reminder_label.pack()
        
        
    def close_reminder_list(self):
        """
        Close method
        """
        self.reminder_list.destroy()
        self.change_window("create_table_view")
        
    def create_page(self):
        """
        Creates a page of 2 reminders
        """
        # Frame
        self.page_frame = tk.Frame(self.reminder_list)
        self.page_frame.pack()
        # Try to create one or two reminders into the page
        try:
            self.pack_reminder(self.reminders[(self.page*2)-2])
            try:               
                self.pack_reminder(self.reminders[(self.page*2)-1])
            except:
                self.ghost_reminder()
        except:
            self.no_reminder()
            
        # Buttons frame
        self.button_page = tk.Frame(self.reminder_list)
        
        self.button_page.columnconfigure(0, weight=1)
        self.button_page.columnconfigure(1, weight=1)
        
        # Go back and further buttons
        if (self.page*2)-3 > 0:
            self.left_button = tk.Button(self.button_page, text="left", command=self.left_page, height=1, width=7)
            self.left_button.grid(row=0,column=0, sticky="w", padx=40, pady=20)
        try:
            self.reminders[(self.page*2)]
        except:
            pass
        else:
            self.right_button = tk.Button(self.button_page, text="right", command=self.right_page, height=1, width=7)
            self.right_button.grid(row=0,column=1, sticky="e", padx=40, pady=20)
            
        self.button_page.pack(side="bottom", fill="x")
            
        

    def pack_reminder(self, reminder):
        """
        Adds the reminder 
        """
        # Frame
        reminder_frame = tk.Frame(self.page_frame)
        reminder_frame.pack(pady=10)
        
        reminder_frame.columnconfigure(0, weight=1)
        reminder_frame.columnconfigure(1, weight=1)
        
        # Name
        self.reminder_name = tk.Label(reminder_frame, text=f"{reminder[1]}")
        self.reminder_name.grid(row=0, column=0)
        
        # Type
        self.reminder_type = tk.Label(reminder_frame, text=f"{reminder[2]}")
        self.reminder_type.grid(row=1, column=0)
        
        # Amount
        self.reminder_amount = tk.Label(reminder_frame, text=f"${'{:.2f}'.format(round(out_money(reminder[3]),2))}")
        self.reminder_amount.grid(row=0,column=1)
        
        # Date
        self.reminder_date = tk.Label(reminder_frame, text=f"{reminder[4]}")
        self.reminder_date.grid(row=1,column=1)
        date_to_compare = reminder[4].split("-")
        date_to_compare = date(int(date_to_compare[0]),int(date_to_compare[1]),int(date_to_compare[2]))
        if date_to_compare <= date.today():
            self.reminder_date.config(fg="red")
        
        # Delete button
        self.reminder_delete = tk.Button(reminder_frame, text="Delete", command=lambda id=reminder[0], frame=reminder_frame : self.ask_delete_reminder(id,frame))
        self.reminder_delete.grid(row=0,column=2)
        
        # Load button
        self.reminder_load = tk.Button(reminder_frame, text="Load", command=lambda id=reminder[0], frame=reminder_frame: self.load_reminder(id,frame))
        self.reminder_load.grid(row=1,column=2)
        
        
    def left_page(self):
        """
        go to the left page
        """
        self.page_frame.pack_forget()
        self.button_page.pack_forget()
        
        self.page -= 1
        
        self.create_page()


    
    def right_page(self):
        """
        Go to the right page
        """
        self.page_frame.pack_forget()
        self.button_page.pack_forget()
        
        self.page += 1
        
        self.create_page()
        
        
    def ghost_reminder(self):
        """
        Place holder to make the buttons stay in the same place
        """
        reminder_frame = tk.Frame(self.page_frame)
        reminder_frame.pack(pady=10)
        self.ghost = tk.Label(reminder_frame, text="")
        self.ghost.pack(pady=15)
            