import tkinter as tk
from tkinter import filedialog
from scripts import *

class Main():
    def __init__(self):
        #setting core variables
        self.currentAccount = None
        self.root = tk.Tk()
        self.root.title("Meme Maker")

        #database variables
        self.DatabasePath = "databases/userdata.db"
        
        #creating window
        screenSize = self.GetScreenSize()
        self.root.geometry(f"{screenSize[0]}x{screenSize[1]}")

        #go to login screen
        self.login = LoginScreen(self)  
        self.login.createMainFrame()
        self.login.createLoginForm()

        #create gallery class

    
    def GetScreenSize(self):
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        return (width,height)


if __name__ == "__main__":
    app = Main()
    app.root.mainloop()
