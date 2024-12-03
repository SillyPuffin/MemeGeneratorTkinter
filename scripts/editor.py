import tkinter as tk
import customtkinter as ctk

from scripts import colours

class Editor():
    def __init__(self,main) -> None:
        self.DatabasePath = main.DatabasePath
        self.templatePath = 'Templates/'

        self.root = main.root
        self.main = main

        self.createMainFrame()

    def openImage(self, path=None):
        """loads the image supplied in the path and opens the editor or opens an empty image"""
        self.currentAccount = self.main.currentAccount
        if path:
            self.loadImage(path)

        self.openMainFrame()

    def loadImage(self,path):
        pass

    def createMainFrame(self):
        self.frame = tk.Frame(master=self.main.root,background=colours.backgroundColour)

    def openMainFrame(self):
        self.frame.pack(fill=tk.BOTH,expand= True)

    def LoadTemplate(self,templateName):
        self.loadImage(self.templatePath + templateName)

