import tkinter as tk
import customtkinter as ctk

from scripts import colours

class Editor():
    def __init__(self,main) -> None:
        self.DatabasePath = main.DatabasePath
        self.templatePath = 'Templates/'

        self.root = main.root
        self.main = main

    def loadImage(self, path=None):
        self.currentAccount = self.main.currentAccount
        self.createMainFrame()

    def createMainFrame(self):
        self.frame = tk.Frame(master=self.main.root,background=colours.backgroundColour)
        self.frame.pack(fill=tk.BOTH,expand= True)

    def LoadTemplate(self,templateName):
        self.loadImage(self.templatePath + templateName)

