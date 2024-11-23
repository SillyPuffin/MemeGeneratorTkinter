import tkinter as tk
import customtkinter as ctk
from time import sleep

from scripts import colours


class LoginScreen():
    def __init__(self, main):
        self.root = main.root
        self.showPass = False
        self.accountDatabasePaht = main.accountDatabasePath
        self.folderDatabasePath = main.folderNamePath

        self.entryWidth = 500
        self.entryHeight = 50

#gui creation
    def CreateEntryBoxes(self,masterFrame):
        """Creates the password and username boxes that you enter details into"""

        #divider line
        divider1 = tk.Frame(master=masterFrame, bg=colours.backgroundShadow, height=2 ,width=self.entryWidth)
        divider1.grid(column=0,row=1,padx=5,pady=10)

        #entries-----------------------------------------------------------------------------------------------

            #username#####
        self.user = ctk.CTkEntry(master=masterFrame,font=("Microsoft YaHei UI light", 30), height=self.entryHeight, width=self.entryWidth )
        self.user.grid(row=2,column = 0, sticky="S",pady=5,padx=15)

        #refill with username when empty
        self.user.insert(0,'username')
        self.user.bind('<FocusOut>',self.OnExitUser)
        self.user.bind('<FocusIn>', self.OnEntryUser)

            #password entry and show password button frame########
        passwordFrame = tk.Frame(master=masterFrame, background=colours.backgroundHighlight)

        TargetButtonWidth = 1 #single pixel will make it as big as it has to be to encompass text
        ButtonPadLeft=5
                #creating show pass button
        showPassButton = ctk.CTkButton(master=passwordFrame,text='show',height=self.entryHeight,width=TargetButtonWidth,command=self.ToggleShowPassword)
        showPassButton.grid(row=0,column=1,padx=(ButtonPadLeft,0))
        self.root.update()
        ActualButtonWidth = showPassButton.winfo_width()

                #creating password entry box
        self.password = ctk.CTkEntry(master=passwordFrame,font=("Microsoft YaHei UI light", 30), height=self.entryHeight, width=self.entryWidth-(ActualButtonWidth+ButtonPadLeft) )
        self.password.grid(row=0,column=0)

                #refill password when empty
        self.passString = ""
        self.password.insert(0,'password')
        self.password.bind("<FocusOut>",self.OnExitPass)
        self.password.bind("<FocusIn>",self.OnEntryPass)
        self.password.bind("<KeyPress>",self.GetTypedLetter)
        self.password.bind("<BackSpace>",self.DoBackspace)
        
        passwordFrame.grid(row=3,column=0,pady=5)

        #second divider line
        divider2 = tk.Frame(master=masterFrame, bg=colours.backgroundShadow, height=2 ,width=self.entryWidth)
        divider2.grid(column=0,row=4,padx=5,pady=10)

    def createLoginForm(self):
        '''Creates the form that appears in the middle of the screen to enter login details to access an account'''

        #login text boxes
        self.loginForm = ctk.CTkFrame(master = self.frame,border_width=2,border_color="black",corner_radius=6, fg_color=colours.backgroundHighlight)
        

        #sign in subheading
        loginTypelabel = tk.Label(master=self.loginForm, text='Sign In', font=("Calibri",45), bg=colours.backgroundHighlight, fg=colours.Heading)
        loginTypelabel.grid(row=0, column=0, sticky='w',padx=20,pady=5)

        self.CreateEntryBoxes(self.loginForm)

        #sign in button
        signIn = ctk.CTkButton(master=self.loginForm, width=self.entryWidth, height=50, fg_color=colours.button,hover_color=colours.buttonHover, corner_radius=8, text="Sign In",font=('Calibir',20))
        signIn.grid(row=5,column=0,pady=10)

        #switch to signup button and label
        switchToCreateFrame = tk.Frame(master=self.loginForm, background=colours.backgroundHighlight)
        switchToCreateFrame.grid(row=6,column=0,pady=10)

        dontHaveAccount = tk.Label(master=switchToCreateFrame, text="Don't have an Account?",bg=colours.backgroundHighlight, fg='white')
        dontHaveAccount.pack(side=tk.LEFT)

        signUp = ctk.CTkButton(master=switchToCreateFrame,text='Sign Up?', fg_color='transparent',text_color='#27bee8',width=1,height=1,command=self.SwitchToAccount)
        signUp.pack(side=tk.LEFT)

        self.loginForm.place(rely=0.5,relx=0.5,anchor='center')
    
    def createAccountForm(self):
        """Creates the box in the middle of the screen for entering details to create a new account"""
        #login text boxes
        self.accountForm = ctk.CTkFrame(master = self.frame,border_width=2,border_color="black",corner_radius=6, fg_color=colours.backgroundHighlight)

        #sign in subheading
        SignUpTypelabel = tk.Label(master=self.accountForm, text='Create Account', font=("Calibri",45), bg=colours.backgroundHighlight, fg=colours.Heading)
        SignUpTypelabel.grid(row=0, column=0, sticky='w',padx=20,pady=5)

        self.CreateEntryBoxes(self.accountForm)

        #sign in button
        signUp = ctk.CTkButton(master=self.accountForm, width=self.entryWidth, height=50, fg_color=colours.button,hover_color=colours.buttonHover, corner_radius=8, text="Sign Up",font=('Calibir',20))
        signUp.grid(row=5,column=0,pady=10)

        #switch to signin button and label
        switchToSignInFrame = tk.Frame(master=self.accountForm, background=colours.backgroundHighlight)
        switchToSignInFrame.grid(row=6,column=0,pady=10)

        HaveAccount = tk.Label(master=switchToSignInFrame, text="Already Have an account?",bg=colours.backgroundHighlight, fg='white')
        HaveAccount.pack(side=tk.LEFT)

        signIn = ctk.CTkButton(master=switchToSignInFrame,text='Sign In?', fg_color='transparent',text_color='#27bee8',width=1,height=1,command=self.SwitchToLogin)
        signIn.pack(side=tk.LEFT)

        self.accountForm.place(rely=0.5,relx=0.5,anchor='center')

    def createMainFrame(self):
        """creates the main frame used for the log in class"""
        self.frame = tk.Frame(master=self.root,background=colours.backgroundColour)
        self.frame.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

        #title
        title = tk.Label(master=self.frame,text="Meme Maker", font =('impact',80), fg=colours.Heading, bg = colours.backgroundColour, pady=15)
        title.pack(side=tk.TOP)       

    def DestroyMainFrame(self):
        """destroys the main frame"""
        self.frame.destroy()

    def SwitchToAccount(self):
        """destroys the login form and creates the account creation form"""
        self.loginForm.destroy()
        self.root.update()
        self.createAccountForm()

    def SwitchToLogin(self):
        """destroys the account creation form and switches to the login form"""
        self.accountForm.destroy()
        self.root.update()
        self.createLoginForm()
#entrylogic
    def ToggleShowPassword(self):
        """toggles the show password bool"""
        if self.passString!="":
            self.showPass = not self.showPass
        self.setShowCharacter()

    def setShowCharacter(self):
        """sets the password entry boxes' show character based on showPass"""
        if self.showPass:
            self.password.configure(show="")
        else:
            self.password.configure(show="*")

    def GetTypedLetter(self,event):
        """adds letters on to the offscreen password string"""
        self.passString += event.char
    
    def DoBackspace(self,event):
        '''removes letters from the passstring when backspace pressed'''
        self.passString = self.passString[0:-1]

    def ReplaceDefaultText(self,text,entry):
        """reenters password or username when the entery box is empty"""
        if entry.get() == '':
            entry.insert(0,text)
        
    def DeleteDefaultText(self,text,entry):
        """deletes the default text when you click on the text box"""
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
        if self.passString=="":
            self.showPass= True
            self.setShowCharacter()

    def OnEntryPass(self,event):
        if self.passString == "":
            self.DeleteDefaultText('password',self.password)
            self.showPass=False
            self.setShowCharacter()