import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from PIL import ImageTk, Image

from os import walk, path, mkdir

from time import sleep

from scripts import database
from scripts import viewer
from scripts import imageicon
from scripts import colours
from scripts import confirmbox


class Gallery():
    def __init__(self,main) -> None:
        self.currentAccount = main.currentAccount
        self.DatabasePath = main.DatabasePath
        self.memeIcons = []
        self.id = None

        self.pause = False

        self.main = main
        self.root = main.root

        self.Viewer = viewer.Viewer(self)
    #creation of elements
    def openImageInViewer(self,name,index):
        """open the meme larger in a proper viewer"""
        if not self.pause:
            self.frame.pack_forget()
            self.Viewer.openImage(self.id, name, index) #loadtheimage in viewer

    def repackFrame(self):
        """repacks the forgotten main frame"""
        self.frame.pack(fill=tk.BOTH,expand=True)

    def createGalleryScreen(self,id):
        """create the gallery classes, instanciate the main frame and the scroll window for viewing your memes"""
        self.createMainFrame()
        self.buildGallery(id)

    def createMainFrame(self):
        """create the main frame all the gallery elements are contatined inside"""
        self.frame = tk.Frame(self.root,bg=colours.backgroundColour)

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
        createNew = ctk.CTkButton(master= self.TopFrame, text='Create Meme', font=('calibri',25),corner_radius=8, fg_color=colours.button,hover_color=colours.buttonHover,command=self.openEmptyImage)
        createNew.pack(side=tk.LEFT, anchor='n' ,padx=10,pady=10)

        #sigmamaaaaaaaaaaaamustardddddddddd
        loadimageButton = ctk.CTkButton(master=self.TopFrame, text='Load Image', font=('calibri',25),fg_color=colours.button, hover_color=colours.buttonHover, command=self.openImageFromFile)
        loadimageButton.pack(side=tk.LEFT , anchor = 'nw', padx=10,pady=10)

        #delete all images
        deleteAll = ctk.CTkButton(master=self.TopFrame, text='Delete All', font=('calibri',25), fg_color=colours.redButton, hover_color=colours.redButtonHover, command=self.deleteAll)
        deleteAll.pack(side=tk.LEFT, anchor='n',padx=10,pady=10)

        #button for close
        CloseApp = ctk.CTkButton(master= self.TopFrame, text='Exit', font=('calibri',25),fg_color=colours.button,hover_color=colours.buttonHover,command=self.main.closeApp)
        CloseApp.pack(side=tk.RIGHT, anchor='n' ,padx=10,pady=10)

        #button for logout
        logOut = ctk.CTkButton(master= self.TopFrame, text='Logout', font=('calibri',25),fg_color=colours.button,hover_color=colours.buttonHover, command=self.switchToLogIn)
        logOut.pack(side=tk.RIGHT, anchor='n', pady=10)

        #deleteaccount
        deleteaccount = ctk.CTkButton(master=self.TopFrame, text='Delete Account', font=('calibri',25),fg_color=colours.redButton, hover_color=colours.redButtonHover,command=self.tryDeleteAccount)
        deleteaccount.pack(side=tk.RIGHT, anchor='n',pady=10,padx=10)

        #title in the center
        Title = ctk.CTkLabel(master=self.TopFrame, text_color=colours.Heading, font=('impact',45), text='Gallery')
        Title.place(relx=0.5,rely=0.5,anchor='center')

        self.root.update_idletasks()
        maxbuttonHeight= createNew.winfo_height() + 20
        titleHeight = Title.winfo_height() + 10
        
        if titleHeight > maxbuttonHeight:
            self.TopFrame.configure(height=Title.winfo_height()+10)
        else:
            self.TopFrame.configure(height=maxbuttonHeight)

    def createGalleryScroll(self):
        """create and pack all elements for the viewing scroll bar area"""
        self.scrollGalleryFrame = ctk.CTkScrollableFrame(master=self.frame,fg_color=colours.backgroundColour)
        self.scrollGalleryFrame.pack(side=tk.TOP,expand = True, fill=tk.BOTH)

        memeFolderPath = database.getFolderPath(self.id, self.DatabasePath)

        if memeFolderPath:
            self.createMemeIcons(memeFolderPath)
            if self.memeIcons:
                self.packMemeIcons()
    
    def createMemeIcons(self,Path):
        """Load all images in the users meme directory"""
        iconSize = 250

        if not path.exists(Path):
            mkdir(Path)

        filenames = list(walk(Path))
        if filenames != []:
            filenames = filenames[0][2]

        if len(filenames) != len(self.memeIcons):
            #add the new icons if its changed
            self.clearMemeIcons()
            for index, item in enumerate(filenames):
                if item[-4:] == ".png" or item[-4:] == ".jpg":
                    image = Image.open(f"{Path}/{item}")
                    #resize the image to fit within the icon size
                    image.thumbnail((iconSize,iconSize))
                    image = ImageTk.PhotoImage(image)

                    newIcon = imageicon.ImageIcon(self,image,iconSize,index,item)
                    self.memeIcons.append(newIcon)
            
    def packMemeIcons(self):
        """pack all the meme thumbnails to the scroll area"""
        maxWidth = max([icon.returnWidth() for icon in self.memeIcons])
        maxColumns = (self.main.screenSize[0]-20) // maxWidth
    
        finished = False
        r = 0
        while not finished:
            for col in range(maxColumns):
                index = r*(maxColumns) + col
                self.memeIcons[index].frame.grid(padx=(10,10),pady=10,row=r,column=col)
                self.root.update()

                if index + 1 == len(self.memeIcons):
                    finished = True
                    break
            r+=1

    #deleting things
    def clearMemeIcons(self):
        """clears all meme icons from the display and empties the list"""
        for item in self.memeIcons:
            item.frame.destroy()
        self.memeIcons = []

    def tryDeleteAccount(self):
        if not self.pause:
            self.pause = True
            confirm = confirmbox.ConfirmBox('Are you Sure?', self.frame, self.deleteAccount, self.unPause)

    def deleteAccount(self):
        "deletes the account currently active"
        database.deleteAllImages(database.getFolderPath(self.id, self.DatabasePath))
        database.deleteAccount(self.id, self.DatabasePath)
        self.deleteNotification()
        self.switchToLogIn()
        self.pause = False

    def deleteAll(self):
        """opens the diaglog box to confirm deleteAll and pauses the menus"""
        if not self.pause:
            self.pause = True
            confirm = confirmbox.ConfirmBox('Are you sure?',self.frame,self.removeFiles,self.unPause)
        
    def unPause(self):
        """unpauses if confirmbox is cancelled"""
        self.pause= False
    
    def removeFiles(self):
        """removes all files in the accounts image folder"""
        database.deleteAllImages(database.getFolderPath(self.id, self.DatabasePath))
        self.deleteNotification()
        self.clearMemeIcons()        
        self.pause = False
    
    def deleteNotification(self):
        """little notifcation box pop-up to tell the user that they have deleted all their files"""
        self.notiFrame = ctk.CTkFrame(master=self.frame, corner_radius=0,border_width=2, border_color=colours.backgroundAccent, fg_color=colours.backgroundHighlight)
        notification = ctk.CTkLabel(master=self.notiFrame, text='Deleting...',text_color=colours.alertText, font = ('calibri',25))
        notification.pack(padx=10,pady=7)
        self.notiFrame.place(relx=0.5,rely=0.5,anchor='center')
        self.root.update()
        sleep(1)
        self.notiFrame.destroy()
    
    ##logic
    def DestroyMainFrame(self):
        "destroy the main frame"
        self.frame.destroy()

    def switchToLogIn(self):
        """destroy the gallery frame and reopen the login screen"""
        self.main.currentAccount = None
        self.DestroyMainFrame()
        self.memeIcons = []
        self.main.login.setupLoginScreen()

    def openEmptyImage(self):
        """open the editor with nothing loaded"""
        if not self.pause:
            self.frame.pack_forget()
            self.main.editor.openImage()

    def openImageFromFile(self):
        """opens a filedialog box to get an image location to load into the editor"""
        filename = filedialog.askopenfilename(initialdir=database.getFolderPath(self.id, self.DatabasePath),title='open an image', filetypes=[('all files','*.png *.jpg'),('PNG file','*.png'),('JPEG file','*.jpg')])

        if filename != '':
            self.frame.pack_forget()
            print(f'loading {filename}')
            self.main.editor.openImage(filename)
