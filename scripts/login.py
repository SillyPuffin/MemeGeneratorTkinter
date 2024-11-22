import tkinter as tk
import customtkinter as ctk

from scripts import colours


class LoginScreen():
    def __init__(self, main):
        self.root = main.root
        self.showPass = False
        self.accountDatabasePaht = main.accountDatabasePath
        self.folderDatabasePath = main.folderNamePath
#gui creation
    def createLoginForm(self):
        #variables
        entryWidth = 500
        entryHeight = 50
        
        #login text boxes
        self.loginForm = ctk.CTkFrame(master = self.frame,border_width=2,border_color="black",corner_radius=6, fg_color=colours.backgroundHighlight)
        self.loginForm.place(rely=0.5,relx=0.5,anchor='center')

        #sign in subheading
        loginTypelabel = tk.Label(master=self.loginForm, text='Sign In', font=("Calibri",45), bg=colours.backgroundHighlight, fg=colours.Heading)
        loginTypelabel.grid(row=0, column=0, sticky='w',padx=20,pady=5)

        #divider line
        divider1 = tk.Frame(master=self.loginForm, bg=colours.backgroundShadow, height=2 ,width=entryWidth)
        divider1.grid(column=0,row=1,padx=5,pady=10)

        #entries
        self.user = ctk.CTkEntry(master=self.loginForm,font=("Microsoft YaHei UI light", 30), height=entryHeight, width=entryWidth )
        self.user.grid(row=2,column = 0, sticky="S",pady=5,padx=15)
        #refill with username when empty
        self.user.insert(0,'username')
        self.user.bind('<FocusOut>',self.OnExitUser)
        self.user.bind('<FocusIn>', self.OnEntryUser)

        #password entry and show password button frame########
        passwordFrame = tk.Frame(master=self.loginForm, background=colours.backgroundHighlight)

        TargetButtonWidth = 1 #single pixel will make it as big as it has to be to encompass text
        ButtonPadLeft=5
        #creating show pass button
        showPassButton = ctk.CTkButton(master=passwordFrame,text='show',height=entryHeight,width=TargetButtonWidth,command=self.ToggleShowPassword)
        showPassButton.grid(row=0,column=1,padx=(ButtonPadLeft,0))
        self.root.update()
        ActualButtonWidth = showPassButton.winfo_width()

        #creating password entry box
        self.password = ctk.CTkEntry(master=passwordFrame,font=("Microsoft YaHei UI light", 30), height=entryHeight, width=entryWidth-(ActualButtonWidth+ButtonPadLeft) )
        self.password.grid(row=0,column=0)
        
        passwordFrame.grid(row=3,column=0,pady=5)

        #refill password when empty
        self.password.insert(0,'password')
        self.password.bind("<FocusOut>",self.OnExitPass)
        self.password.bind("<FocusIn>",self.OnEntryPass)
        self.password.bind("<KeyPress>",self.OnPassLetterTyped)

        #second divider line
        divider2 = tk.Frame(master=self.loginForm, bg=colours.backgroundShadow, height=2 ,width=entryWidth)
        divider2.grid(column=0,row=4,padx=5,pady=10)

        #sign in button
        signIn = ctk.CTkButton(master=self.loginForm, width=entryWidth, height=50, fg_color=colours.button,hover_color=colours.buttonHover, corner_radius=8, text="Sign In",font=('Calibir',20))
        signIn.grid(row=5,column=0,pady=10)

        #switch to signup button and label
        switchToCreateFrame = tk.Frame(master=self.loginForm, background=colours.backgroundHighlight)
        switchToCreateFrame.grid(row=6,column=0,pady=10)

        dontHaveAccount = tk.Label(master=switchToCreateFrame, text="Don't have an Account?",bg=colours.backgroundHighlight, fg='white')
        dontHaveAccount.pack(side=tk.LEFT)

        signUp = ctk.CTkButton(master=switchToCreateFrame,text='Sign Up?', fg_color='transparent',text_color='#27bee8',width=1,height=1,command=self.SwitchToAccount)
        signUp.pack(side=tk.LEFT)
    
    def createAccountForm(self):
        pass#create account sign up form

    def createMainFrame(self):
        self.frame = tk.Frame(master=self.root,background=colours.backgroundColour)
        self.frame.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        #title
        title = tk.Label(master=self.frame,text="Meme Maker", font =('impact',80), fg=colours.Heading, bg = colours.backgroundColour, pady=15)
        title.pack(side=tk.TOP)       

    def DestroyMainFrame(self):
        self.frame.destroy()

    def SwitchToAccount(self):
        self.loginForm.destroy()
        self.createAccountForm()

    def SwitchToLogin(self):
        self.accountForm.destroy()
        self.createLoginForm()
#entrylogic
    def ToggleShowPassword(self):
        self.showPass = not self.showPass
        if not self.showPass:
            self.password.config(show='*')
        else:
            self.password.config(show='')

    def ReplaceDefaultText(self,text,entry):
        if entry.get() == '':
            entry.insert(0,text)
        
    def DeleteDefaultText(self,text,entry):
        if entry.get() == text:
            entry.delete(0,tk.END)

#placin and removing default text for username
    def OnExitUser(self,event):
        self.ReplaceDefaultText('username',self.user)

    def OnEntryUser(self,event):
        self.DeleteDefaultText('username',self.user)
    
#placing and removing defualt text for password
    def OnExitPass(self,event):
        self.ReplaceDefaultText('password',self.password)
    
    def OnEntryPass(self,event):
        self.DeleteDefaultText('password',self.password)