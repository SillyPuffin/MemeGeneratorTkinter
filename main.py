import tkinter as tk
from tkinter import filedialog
from scripts import *

class Main():
    def __init__(self):
        #setting core variables
        self.currentAccount = None
        self.root = tk.Tk()

        #database variables
        self.accountDatabasePath = "databases/accounts.db"
        self.folderNamePath = "databases/folderNames.db"

        #creating window
        screenSize = self.GetScreenSize()
        self.root.geometry(f"{screenSize[0]}x{screenSize[1]}")

        #go to login screen
        login = LoginScreen(self)

    
    def GetScreenSize(self):
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        return (width,height)


if __name__ == "__main__":
    app = Main()
    app.root.mainloop()
