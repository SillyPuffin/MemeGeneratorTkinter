import tkinter as tk
import customtkinter as ctk

from scripts import usericon
from scripts import colours
from scripts import database
from scripts import confirmbox


class Sharer():
    def __init__(self, viewer)->None:
        self.viewer = viewer
        self.masterFrame = viewer.frame
        self.DatabasePath = self.viewer.gallery.DatabasePath
        self.icons = []

        self.id = None

        self.createMainFrame()

    def set_id(self, id):
        """sets the id and then updates the shareable accounts acorrdingly"""
        self.id = id
        self.clearIcons()
        self.createIcons()
        self.packIcons()


    def createMainFrame(self):
        """create the main frame"""
        self.frame = ctk.CTkScrollableFrame(master=self.masterFrame, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent,border_width=2,corner_radius=0, height=600)
        self.frame.pack_propagate(False)
    
    def openSharer(self):
        self.frame.place(relx=0.5,rely=0.5,anchor='center')
        self.viewer.Pause()

    def closeSharer(self):
        self.frame.pack_forget()
    
    def exitSharer(self):
        self.frame.pack_forget()
        self.viewer.unpause()

    def clearIcons(self):
        """delete all the icons"""
        for icon in self.icons:
            icon.frame.destroy()
        self.icons = []

    def createIcons(self):
        """create the user icons"""
        accounts = database.getAllAccounts(self.id, self.DatabasePath)
        if accounts:

            for account in accounts:
                newIcon = usericon.UserIcon(self.frame,self.viewer, account[0], account[1])
                self.icons.append(newIcon)

    def packIcons(self):
        """pack all of sharers user icons"""
        for icon in self.icons:
            icon.frame.pack(pady=7,padx=7, side=tk.TOP)

    def copyImage(self):
        """copy the image from the current account to the dst account"""
        pass


    def confirmSharer(self):
        """create the confirm box for sharing the image"""
        confirm = confirmbox.ConfirmBox('Do you want to copy This?', self.masterFrame, self.copyImage, self.openSharer)