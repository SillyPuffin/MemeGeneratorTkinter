import tkinter as tk
import customtkinter as ctk
from os import remove
import os.path

from PIL import ImageTk, Image

from scripts import database
from scripts import colours
from scripts import confirmbox

class Viewer():
    def __init__(self, gallery) -> None:
        self.gallery = gallery
        self.pause= False
        self.index = None
        
        self.imagePad= 10
        self.buttonWidth = 20
        self.topHeight = 0

        self.imagelabel = None

        self.createMainFrame()
        self.createViewer()

    def createMainFrame(self):
        self.frame= tk.Frame(master=self.gallery.root, background=colours.backgroundColour)
       
    def packMainFrame(self):
        self.destroyImageFrame()
        self.frame.pack(expand=True,fill=tk.BOTH)

    def createViewer(self):
        self.createTopBar()
        self.createImageDisplay()

    def createImageDisplay(self):
        self.ImageDisplayFrame = tk.Frame(master=self.frame, background=colours.backgroundColour)
        self.ImageDisplayFrame.pack(fill=tk.BOTH, expand=True)

        height = 100
        
        self.left = ctk.CTkButton(master=self.ImageDisplayFrame, text='Prev',width=self.buttonWidth,height=height, fg_color=colours.darkbutton, hover_color=colours.darkbuttonHover, command=self.openPreviousImage)
        self.left.pack(side=tk.LEFT, anchor='w',padx=self.imagePad)

        self.right = ctk.CTkButton(master=self.ImageDisplayFrame, text='Next',width=self.buttonWidth,height=height, fg_color=colours.darkbutton, hover_color=colours.darkbuttonHover, command=self.openPreviousImage)
        self.right.pack(side=tk.RIGHT, anchor='e',padx=self.imagePad)

        #arrow buttons for left and right image showing

    def createTopBar(self):
        """Creates the top UI bar where the title and buttons are located"""
        self.TopFrame = ctk.CTkFrame(master = self.frame, border_color=colours.backgroundHighlight, border_width=2,corner_radius=0)
        self.TopFrame.pack_propagate(False)
        self.TopFrame.pack(side='top',fill=tk.X)

        #backbutton
        backButton = ctk.CTkButton(master=self.TopFrame, text='back',font=("calibri",25),hover_color=colours.buttonHover,fg_color=colours.button,command=self.backToGallery)
        backButton.pack(side=tk.RIGHT,padx=10,pady=10,anchor='ne')

        #delete
        deleteButton = ctk.CTkButton(master=self.TopFrame, text='Delete', font=('calibri',25),command=self.deleteImage,fg_color=colours.redButton,hover_color=colours.redButtonHover)
        deleteButton.pack(side=tk.LEFT, padx=10,pady=10, anchor='nw')

        #share

        self.TopFrame.update()
        self.topHeight = backButton.winfo_reqheight() + 10*2 #used to calculate the height of the top bar

        #title in the center
        Title = ctk.CTkLabel(master=self.TopFrame, text_color=colours.Heading, font=('impact',50), text='Image Viewer')
        Title.place(relx=0.5,rely=0.5,anchor='center')

        self.gallery.root.update_idletasks()
        self.TopFrame.configure(height=Title.winfo_height()+10)

        newHeight = Title.winfo_height()+10
        if newHeight > self.topHeight:
            self.topHeight = newHeight #if the height of the title +padding is bigger than the buttons + padding then use title

    def destroyImageFrame(self):
        if self.imagelabel != None:
            self.imagelabel.destroy()
            self.imagelabel = None

    def openImage(self,id,path,index):
        self.id = id
        self.packMainFrame()

        self.index = index
        
        windowHeight = self.gallery.main.screenSize[1]-self.topHeight #get the height of the image dispaly area for correct sizing
        windowWidth = self.gallery.main.screenSize[0]

        #print(f'{windowWidth},{windowHeight}')

        self.imageHeight = windowHeight - self.imagePad*2
        self.imageWidth = windowWidth - self.imagePad*4 - self.buttonWidth * 2

        prefix = database.getFolderPath(self.id, self.gallery.DatabasePath)
        
        fullpath= prefix+"/"+path
        meme = Image.open(fullpath)
        meme.thumbnail((self.imageWidth, self.imageHeight))
        self.meme = ImageTk.PhotoImage(meme)

        self.imagelabel = tk.Label(master=self.ImageDisplayFrame, bg=colours.backgroundHighlight, image=self.meme)
        self.imagelabel.place(relx=0.5,rely=0.5, anchor ='center')
        self.imagelabel.bind("<Button-1>",self.openNextImage)
        self.imagelabel.bind("<Button-3>", self.openPreviousImage)

    def openNextImage(self, event=None):
        if not self.pause:
            self.index += 1

            if self.index == len(self.gallery.memeIcons):
                self.index = 0

            self.setNewImage()

    def openPreviousImage(self,event=None):
        if not self.pause:
            self.index -= 1

            if self.index < 0:
                self.index = len(self.gallery.memeIcons)-1
                if self.index < 0:
                    self.index = 0
                
            self.setNewImage()

    def setNewImage(self):
        newPath = self.gallery.memeIcons[self.index].fullname
        prefix = database.getFolderPath(self.id, self.gallery.DatabasePath)
        fullPath = prefix + "/" + newPath

        meme = Image.open(fullPath)
        meme.thumbnail((self.imageWidth,self.imageHeight))
        self.meme = ImageTk.PhotoImage(meme)

        self.imagelabel.configure(image=self.meme)

    def removeImageFile(self):
        name = self.gallery.memeIcons[self.index].fullname
        prefix = database.getFolderPath(self.id, self.gallery.DatabasePath)
        remove(os.path.join(prefix,name))

        self.gallery.createMemeIcons(database.getFolderPath(self.id,self.gallery.DatabasePath))
        if self.gallery.memeIcons:
            self.gallery.packMemeIcons()
        self.pause = False

    def failDelete(self):
        self.pause = False

    def deleteImage(self):
        confirm = confirmbox.ConfirmBox('Are you sure?',self.frame,self.removeImageFile,self.failDelete)
        self.pause = True

    def backToGallery(self):
        if not self.pause:
            self.frame.pack_forget()
            self.gallery.repackFrame()