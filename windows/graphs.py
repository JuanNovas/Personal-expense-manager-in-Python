import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry
from datetime import datetime, timedelta
from windows.window_functionalities import Functionality
from extra.money_format import out_money

class GraphWindow(Functionality):
    def create_graph_view(self):
        # Declaring the frame
        self.frame = tk.Frame(self.master)
        # Declaring the last_week variable
        last_week = datetime.now() - timedelta(days=6)
        
        # Creating the frame
        self.back_grid = tk.Frame(self.frame)
        self.back_grid.columnconfigure(0, weight=1)
        self.back_grid.columnconfigure(1, weight=1)
        
        # Go back button
        self.back = tk.Button(self.back_grid, text="Back", command=lambda  : self.change_window("create_table_view"))
        self.back.grid(row=0,column=0, sticky="nw", pady=5,padx=5)
        self.back_grid.pack(side="top", fill="x")
        
        # Creating header frame
        self.header = tk.Frame(self.frame)

        # Headers labels
        self.inicial_label = tk.Label(self.header, text="From: ", font=("Verdana", 8))
        self.inicial_label.grid(row=0,column=0,padx=10)
        
        self.end_label = tk.Label(self.header, text="To: ", font=("Verdana", 8))
        self.end_label.grid(row=0,column=1,padx=10)
        
        self.type_label = tk.Label(self.header, text="Type: ", font=("Verdana", 8))
        self.type_label.grid(row=0,column=2,padx=10)
        
        
        # Header options
        ## Type of transaction
        self.type_options = ['all','clothing and accessories','education','entertainment','foods','gifts and donations','health and hygiene','housing',
        'insurance','investments','others','personal care','pets','taxes and fees','technology','transportation','travel']
        
        self.type_selected = tk.StringVar(self.master)
        self.type_selected.set(self.type_options[0])
        
        self.type_menu = tk.OptionMenu(self.header, self.type_selected, *self.type_options)
        self.type_menu.grid(row=1,column=2,padx=10)
        
        ## Inicial date
        self.inicial_date = DateEntry(self.header, date_pattern='yyyy-mm-dd')
        self.inicial_date.set_date(last_week)
        self.inicial_date.grid(row=1,column=0,padx=10)
        
        ## Final date
        self.final_date = DateEntry(self.header, date_pattern='yyyy-mm-dd')
        self.final_date.grid(row=1,column=1,padx=10)
        
        self.inicial_date.bind("<<DateEntrySelected>>", self.date_changed)
        self.final_date.bind("<<DateEntrySelected>>", self.date_changed)
        self.type_selected.trace_add('write', self.date_changed)
        
        self.header.pack(side="top")
        
        # Warn label
        self.warn_label = tk.Label(self.frame)
        self.warn_label.pack()
        
        # Graph
        fig = Figure(figsize=(5, 4), dpi=130)
        self.ax = fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(fig, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.update_graph()

        
        self.frame.pack()
        
    def update_graph(self):
        """
        Updates the graph information
        """
        self.ax.clear()
        
        x,y = self.graph_data()
        
        self.ax.plot(x, y)
    
        # Setting an Y axys limit
        max_y = max(y)
        if max_y > 0:
            self.ax.set_ylim(0, max_y + (max_y / 10))
        else:
            self.ax.set_ylim(0, 1)
        
        # Showing only some dates in the X axys to make the graph more clear
        n = 7  # Dates shown
        step = len(x) // n
        self.ax.set_xticks(range(0, len(x), step))
        self.ax.set_xticklabels([x[i] for i in range(0, len(x), step)])
            
            
        self.ax.plot(x,y)

        
        self.canvas.draw()
        
    def graph_data(self):
        """
        Gets the information from the database
        """
        
        # Getting data from the inputs
        inicial= self.inicial_date.get_date()
        final= self.final_date.get_date()
        category= self.type_selected.get()
        
        # Getting the data form the database
        if category == "all":
        
            self.cursor.execute(""" SELECT SUM("amount"),"date" FROM "transactions"
                                WHERE "date" BETWEEN (?) AND (?) 
                                GROUP BY "date" 
                                ORDER BY "date" ASC"""
                                ,(inicial,final))
        else:
            
            self.cursor.execute(""" SELECT SUM("amount"),"date" FROM "transactions"
                                WHERE "date" BETWEEN (?) AND (?) 
                                AND "type" = (?)
                                GROUP BY "date" 
                                ORDER BY "date" ASC"""
                                ,(inicial,final,category))
        
        
        data = self.cursor.fetchall()

        # Formating the data
        money_list = []
        dates_list = []
        
        temp_date = inicial
        i = 0
        
        while temp_date <= final:
            dates_list.append(temp_date.strftime("%d-%m"))
            
            try:
                if str(temp_date) == data[i][1]:
                    money_list.append(out_money(data[i][0]))
                    i += 1
                else:
                    money_list.append(0)
            except:
                money_list.append(0)
            
            temp_date += timedelta(days=1)
        

        return dates_list, money_list
        
        
    def date_changed(self,event,*args):
        """
        Checks if date is valid
        """
        inicial = self.inicial_date.get_date()
        final = self.final_date.get_date()
        
        if final > inicial:
        
            self.update_graph()
            self.set_warn("")
        else:
            self.set_warn("Invalid Date")
        