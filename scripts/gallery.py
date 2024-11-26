import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image
from os import walk

from scripts import colours
from scripts import database


class Gallery():
    def __init__(self,main) -> None:
        self.currentAccount = main.currentAccount
        self.DatabasePath = main.DatabasePath
        self.id = None

        self.main = main
        self.root = main.root

    def createGalleryScreen(self,id):
        """create the gallery classes, instanciate the main frame and the scroll window for viewing your memes"""
        self.createMainFrame()
        self.buildGallery(id)

    def createMainFrame(self):
        """create the main frame all the gallery elements are contatined inside"""
        self.frame = tk.Frame(self.root,bg=colours.backgroundColour)
        self.frame.pack(fill=tk.BOTH, expand= True)

    def buildGallery(self,id):
        """create all the elements in the main screen"""
        self.id = id

        self.createTopBar()

        self.createGalleryScroll()

    def createTopBar(self):
        """Creates the top UI bar where the title and buttons are located"""
        self.TopFrame = ctk.CTkFrame(master = self.frame, border_color=colours.backgroundHighlight, border_width=2,corner_radius=0)
        self.TopFrame.pack_propagate(False)
        self.TopFrame.pack(side='top',fill=tk.X)

        #button for new
        #does nothing at the moment because they dont exist
        createNew = ctk.CTkButton(master= self.TopFrame, text='Create Meme', font=('calibri',25),fg_color=colours.button,hover_color=colours.buttonHover,command=self.openEmptyImage)
        createNew.pack(side=tk.LEFT, anchor='n' ,padx=10,pady=10)

        #button for close
        CloseApp = ctk.CTkButton(master= self.TopFrame, text='Exit', font=('calibri',25),fg_color=colours.button,hover_color=colours.buttonHover,command=self.main.closeApp)
        CloseApp.pack(side=tk.RIGHT, anchor='n' ,padx=10,pady=10)

        #button for logout
        logOut = ctk.CTkButton(master= self.TopFrame, text='Logout', font=('calibri',25),fg_color=colours.button,hover_color=colours.buttonHover, command=self.switchToLogIn)
        logOut.pack(side=tk.RIGHT, anchor='n', pady=10)

        #title in the center
        Title = ctk.CTkLabel(master=self.TopFrame, text_color=colours.Heading, font=('impact',70), text='Gallery')
        Title.place(relx=0.5,rely=0.5,anchor='center')

        self.root.update_idletasks()
        self.TopFrame.configure(height=Title.winfo_height()+10)

    def createGalleryScroll(self):
        """create and pack all elements for the viewing scroll bar area"""
        self.scrollGalleryFrame = ctk.CTkScrollableFrame(master=self.frame,fg_color=colours.backgroundColour)
        self.scrollGalleryFrame.pack(side=tk.TOP,expand = True, fill=tk.BOTH)

        memeFolderPath = database.getFolderPath(self.id, self.DatabasePath)

        if memeFolderPath:
            self.LoadMemeIcons(memeFolderPath)
    
    def LoadMemeIcons(self,Path):
        """Load all images in the path and pack them to the scroll area"""
        filenames = list(walk(Path))
        if filenames != []:
            filenames = filenames[2]
        
        #list to store all the image data
        images = []

        for item in filenames:
            newimage = ImageTk.Image(Image.open(".."+Path))
    

    ##logic
    def DestroyMainFrame(self):
        "destroy the main frame"
        self.frame.destroy()

    def switchToLogIn(self):
        """destroy the gallery frame and reopen the login screen"""
        self.main.currentAccount = None
        self.DestroyMainFrame()
        self.main.login.setupLoginScreen()

    def openEmptyImage(self):
        self.frame.destroy()
        self.main.editor.loadImage()