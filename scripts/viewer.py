import tkinter as tk
import customtkinter as ctk

from PIL import ImageTk, Image

from scripts import database
from scripts import colours

class Viewer():
    def __init__(self, gallery) -> None:
        self.gallery = gallery
        self.index = None
        
        self.imagePad= 10
        self.buttonWidth = 20

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

    def createTopBar(self):
        """Creates the top UI bar where the title and buttons are located"""
        self.TopFrame = ctk.CTkFrame(master = self.frame, border_color=colours.backgroundHighlight, border_width=2,corner_radius=0)
        self.TopFrame.pack_propagate(False)
        self.TopFrame.pack(side='top',fill=tk.X)

        #backbutton
        backButton = ctk.CTkButton(master=self.TopFrame, text='back',font=("calibri",25),hover_color=colours.buttonHover,fg_color=colours.button,command=self.backToGallery)
        backButton.pack(side=tk.RIGHT,padx=10,pady=10,anchor='ne')

        #title in the center
        Title = ctk.CTkLabel(master=self.TopFrame, text_color=colours.Heading, font=('impact',50), text='Image Viewer')
        Title.place(relx=0.5,rely=0.5,anchor='center')

        self.gallery.root.update_idletasks()
        self.TopFrame.configure(height=Title.winfo_height()+10)

    def destroyImageFrame(self):
        if self.imagelabel != None:
            self.imagelabel.destroy()
            self.imagelabel = None

    def openImage(self,id,path,index):
        self.id = id
        self.packMainFrame()

        self.index = index
        
        windowHeight = self.gallery.main.screenSize[1]-self.TopFrame.winfo_height()
        windowWidth = self.gallery.main.screenSize[0]

        imageHeight = windowHeight - self.imagePad*2
        imageWidth = windowWidth - self.imagePad*4 - self.buttonWidth * 2

        prefix = database.getFolderPath(self.id, self.gallery.DatabasePath)
        
        fullpath= prefix+"/"+path
        meme = Image.open(fullpath)
        meme.thumbnail((imageWidth, imageHeight))
        self.meme = ImageTk.PhotoImage(meme)

        self.imagelabel = tk.Label(master=self.ImageDisplayFrame, bg=colours.backgroundHighlight, image=self.meme)
        self.imagelabel.place(relx=0.5,rely=0.5, anchor ='center')


    def openNextImage(self):
        pass

    def openPreviousImage(self):
        pass

    def backToGallery(self):
        self.frame.pack_forget()
        self.gallery.repackFrame()