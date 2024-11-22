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

        entryWidth = 500
        entryHeight = 50

        #title
        title = tk.Label(master=self.frame,text="Meme Maker", font =('impact',80), fg=colours.Heading, bg = colours.backgroundColour, pady=15)
        title.pack(side=tk.TOP)

        #login text boxes
        loginForm = ctk.CTkFrame(master = self.frame,border_width=2,border_color="black",corner_radius=6, fg_color=colours.backgroundHighlight)
        loginForm.place(rely=0.5,relx=0.5,anchor='center')

        #sign in subheading
        loginTypelabel = tk.Label(master=loginForm, text='Sign In', font=("Calibri",45), bg=colours.backgroundHighlight, fg=colours.Heading)
        loginTypelabel.grid(row=0, column=0, sticky='w',padx=10,pady=5)

        #divider line
        divider1 = tk.Frame(master=loginForm, bg=colours.backgroundShadow, height=2 ,width=entryWidth)
        divider1.grid(column=0,row=1,padx=5,pady=10)

        #entries
        user = ctk.CTkEntry(master=loginForm,font=("Microsoft YaHei UI light", 30), height=entryHeight, width=entryWidth )
        user.grid(row=2,column = 0, sticky="S",pady=5,padx=15)

        password = ctk.CTkEntry(master=loginForm,font=("Microsoft YaHei UI light", 30), height=entryHeight, width=entryWidth )
        password.grid(row=3,column = 0, sticky="N",pady=5,padx=15)

        #second divider line
        divider2 = tk.Frame(master=loginForm, bg=colours.backgroundShadow, height=2 ,width=entryWidth)
        divider2.grid(column=0,row=4,padx=5,pady=10)

        #sign in button
        signIn = ctk.CTkButton(master=loginForm, width=entryWidth, height=50, fg_color=colours.button,hover_color=colours.buttonHover, corner_radius=8, text="Sign In",font=('Calibir',20))
        signIn.grid(row=5,column=0,pady=10)

        #switch to signup button
        switchToCreateFrame = tk.Frame(master=loginForm, background=colours.backgroundHighlight)
        switchToCreateFrame.grid(row=6,column=0,pady=10)

        dontHaveAccount = tk.Label(master=switchToCreateFrame, text="Don't have an Account?",bg=colours.backgroundHighlight, fg='white')
        dontHaveAccount.pack(side=tk.LEFT)

        signUp = ctk.CTkButton(master=switchToCreateFrame,text='Sign Up?', fg_color='transparent',text_color='#27bee8',width=1,height=1)
        signUp.pack(side=tk.LEFT)

        self.frame.pack(fill=tk.BOTH,side=tk.TOP,expand=True)        

    def DestroyLoginScreen(self):
        self.frame.destroy()