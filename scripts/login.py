import tkinter as tk
import customtkinter as ctk

from scripts import colours


class LoginScreen():
    def __init__(self, main):
        self.root = main.root
        self.accountDatabasePaht = main.accountDatabasePath
        self.folderDatabasePath = main.folderNamePath
    
    def createLoginScreen(self):
        self.frame = tk.Frame(master=self.root,background=colours.backgroundColour)

        title = tk.Label(master=self.frame,text="Meme Maker", font =('TkMenuFont',80), fg=colours.Heading, bg = colours.backgroundColour, pady=15)
        title.pack(side=tk.TOP)

        loginForm = tk.Frame(master = self.frame,background=colours.backgroundHighlight,border=10,borderwidth=10,highlightcolor=colours.backgroundHighlight)
        loginForm.place(rely=0.5,relx=0.5,anchor='center')

        loginTypelabel = tk.Label(master=loginForm, text='Login', font=("Calibri",40), bg=colours.backgroundColour, fg=colours.Heading, pady=20)
        loginTypelabel.grid(row=0, column=0, sticky='w')

        user = ctk.CTkEntry(master=loginForm,font=("Microsoft YaHei UI light", 40), height=100, width=500, )
        user.grid(row=1,column = 0, sticky="w")

        self.frame.pack(fill=tk.BOTH,side=tk.TOP,expand=True)        

    def DestroyLoginScreen(self):
        self.frame.destroy()