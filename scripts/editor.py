import tkinter as tk
import customtkinter as ctk

from scripts import colours

class Editor():
    def __init__(self,main) -> None:
        self.DatabasePath = main.DatabasePath
        self.templatePath = 'Templates/'

        self.root = main.root
        self.main = main

        self.templateIcons = []

        self.image = None
        self.displayImage = None

        self.createMainFrame()
        self.createTopBar()

    def openImage(self, path=None):
        """loads the image supplied in the path and opens the editor or opens an empty image"""
        self.currentAccount = self.main.currentAccount

        if path:
            self.loadImage(path)

        self.openMainFrame()

    def openImageFromFile(self):
        """open file dialog to open an image"""
        pass

    def LoadTemplate(self,templateName):
        """load a template image from the template directory"""
        self.loadImage(self.templatePath + templateName)

    def openTemplateList(self):
        """open the template selection list in the middle of the screen"""

    def saveImage(self):
        """save the current image to the users meme folder"""
        pass

    def loadImage(self,path):
        """load the image into the right image"""
        pass

    def createMainFrame(self):
        """create the main frame"""
        self.frame = tk.Frame(master=self.main.root,background=colours.backgroundColour)

    def createTemplateList(self):
        """create the frame and icons for the template list offscreen"""
        pass

    def createTemplatedisplay(self):
        """generate the frame and scroll bar elements in the template frame"""
        pass

    def createTemplateIcons(self):
        """create the template icons and pack them"""
        pass

    def createTopBar(self):
        """create the file bar and title bar along the top"""
        #create four buttons for save, load, load template and exit.
        # have a title in the middle top bar

        #saving will use the predetermined path from the user directory
        #loading will use the filedialog to open the user picked image
        #load template will open a selection list in the middle that allows the user to select a template by click on an icon with a label
        pass

    def createLeftWindow(self):
        """create the bottom left window that contains the entry boxes for top and bottom text"""
        pass

    def openMainFrame(self):
        """pack the main frame"""
        self.frame.pack(fill=tk.BOTH,expand= True)

    def backToGallery(self):
        self.frame.pack_forget()
        self.image = None
        self.displayImage = None
        self.main.gallery.repackFrame()

