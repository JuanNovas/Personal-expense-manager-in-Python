import app
import tkinter as tk

# Declaring the main function
def main(): 
    
    # Creating the root parameters (Title, size and icon)
    root = tk.Tk()
    root.title("Manager")
    root.geometry("900x430")
    icon_image = tk.PhotoImage(file="icono.png")
    root.iconphoto(True, icon_image)
    
    # Creating the window object 
    application = app.Window(root)
    
    # Declaring the method to be executed before closing the app to ensure to close de database connection and save the data
    root.protocol("WM_DELETE_WINDOW", application.close_app)
    
    # Starting the mainloop
    root.mainloop()

if __name__ == "__main__":
    main()
