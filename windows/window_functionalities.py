# All view clases inherit from this
# Has all the methods any view needs
class Functionality:

    def create_window(self,str_method):
        """Creates a new view, not forgetting the frame
            just need to be called the first time a view is load
            because the next time the frame need to be forgiven

        Args:
            str_method (str): a method name
        """
        # Checks if the method is valid, calling it
        method = getattr(self, str_method, None)
        if method == None:
            print("Error while loading new window")
        else:  
            method()

    def change_window(self,str_method):
        """Creates a new view forgetting the actual frame
            to reset the view

        Args:
            str_method (str): A method name
        """
        # Checks if the method is valid, calling it
        method = getattr(self, str_method, None)
        if method == None:
            print("Error while loading new window")
        else:  
            self.frame.pack_forget()
            method()
            
    def create_menu(self,str_method):
        """Creates a top level window, not needing to 
            forget the frame because the menu has 
            his own window
            
        Args:
            str_method (str): A method name
        """
        # Checks if the method is valid, calling it
        method = getattr(self, str_method, None)
        if method == None:
            print("Error while loading new window")
        else:  
            method()
            
    def update_options(self, event):
        """
        Updates the options menu depending on the user input
        """
        # Filtering the transactions
        input_text = self.transaction_type.get()
        filtered_options = [option for option in self.type_options if option.lower().startswith(input_text.lower().strip())]

        # Updating the options
        self.transaction_type['values'] = filtered_options
        
    def menu_position(self):
        """
        Defines a standar size and start position (center) to all
        menus (topLevel)
        """
        # Gets the window sizes
        self.master.update_idletasks()
        root_width = self.master.winfo_width()
        root_height = self.master.winfo_height()
        
        # Defines the menu size and position
        window_width = 280
        window_height = 200
        window_x = (self.master.winfo_x() + root_width // 2) - (window_width // 2)
        window_y = (self.master.winfo_y() + root_height // 2) - (window_height // 2)
        
        return(f"{window_width}x{window_height}+{window_x}+{window_y}")