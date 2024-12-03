import tkinter as tk
import customtkinter as ctk

from scripts import colours

class Editor():
    def __init__(self,main) -> None:
        self.DatabasePath = main.DatabasePath
        self.templatePath = 'Templates/'
        self.savelocation = None

        self.root = main.root
        self.main = main

        self.image = None
        self.displayImage = None

        self.createMainFrame()
        self.createTopBar()

    def openImage(self, path=None):
        """loads the image supplied in the path and opens the editor or opens an empty image"""
        self.currentAccount = self.main.currentAccount
        self.savelocation = None

        if path:
            self.loadImage(path)

        self.openMainFrame()

    def LoadTemplate(self,templateName):
        """load a template image from the template directory"""
        self.loadImage(self.templatePath + templateName)

    def loadImage(self,path):
        """load the image into the right image"""
        pass

    def createMainFrame(self):
        """create the main frame"""
        self.frame = tk.Frame(master=self.main.root,background=colours.backgroundColour)

    def createTopBar(self):
        """create the file bar and title bar along the top"""
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

