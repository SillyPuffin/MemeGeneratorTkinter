import tkinter as tk
import customtkinter as ctk

from PIL import Image

from time import sleep

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

        self.imagetoshare = None
        self.id = None


    def set_id(self, id):
        """sets the id and then updates the shareable accounts acorrdingly"""
        self.id = id
        self.clearIcons()
        self.createIcons()
        self.packIcons()

    def set_image_name(self,name):
        """sets the path of the image that will be shared"""
        self.imagetoshare = name

    def createMainFrame(self):
        """create the main frame"""
        self.pad = 5
        borderwidth = 2
        self.boxmaxwidth = 200
        self.screenmaxwidth = self.boxmaxwidth + borderwidth*2  + self.pad*2
        height = 350

        self.frame = ctk.CTkFrame(master=self.masterFrame, fg_color=colours.backgroundColour, border_color=colours.backgroundAccent,border_width=borderwidth,corner_radius=0, height=height,width=self.screenmaxwidth)
        self.frame.pack_propagate(False)

        self.viewer.gallery.root.bind("<Escape>", self.exitSharer,add= '+')

        self.topframe = ctk.CTkFrame(master=self.frame,fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent,border_width=borderwidth,corner_radius=0,width=self.screenmaxwidth)

        self.exitIcon = ctk.CTkImage(Image.open('Graphics/cross.png'),None,(24,24))

        self.backButton = ctk.CTkButton(master=self.topframe, fg_color=colours.backgroundHighlight, hover_color=colours.darkbutton,text='', image=self.exitIcon, width=1, command=self.exitSharer)
        self.backButton.pack(side=tk.RIGHT, padx=self.pad,pady=self.pad)

        self.sharetitle = tk.Label(master=self.topframe, font=('calibri',18),fg='white', text='Share To?',bg=colours.backgroundHighlight)
        self.sharetitle.pack(side=tk.LEFT,padx=(self.pad,self.pad))

        self.topframe.pack(side=tk.TOP,fill = tk.X)

        self.scrollFrame = ctk.CTkScrollableFrame(master=self.frame, fg_color=colours.backgroundColour, corner_radius=0)
        self.scrollFrame.pack(fill=tk.Y,expand=True,padx=borderwidth,pady=(0,borderwidth))
        
    
    def openSharer(self):
        """packs the sharer frame and pauses menus"""
        self.frame.place(relx=0.5,rely=0.5,anchor='center')
        self.viewer.Pause()

    def closeSharer(self):
        """un packs the sharer"""
        self.frame.place_forget()
    
    def exitSharer(self,event=None):
        "unpacks and unpauses the menus"
        self.closeSharer()
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
                newIcon = usericon.UserIcon(self.scrollFrame,self, account[0], account[1],self.boxmaxwidth)
                self.icons.append(newIcon)

    def packIcons(self):
        """pack all of sharers user icons"""
        for icon in self.icons:
            icon.frame.pack(pady=self.pad,padx=self.pad)

    def copyImage(self):
        """copy the image from the current account to the dst account"""
        #copy notification
        filename = self.imagetoshare
        folderpath = database.getFolderPath(self.id, self.DatabasePath) + '/' + filename
        dst_folderpath = database.getFolderPath(self.id_dst, self.DatabasePath)

        database.copyFile(filename, folderpath, dst_folderpath)

        self.shareNotification()
        self.viewer.unpause()

    def confirmShare(self,id_destination):
        """create the confirm box for sharing the image"""
        self.closeSharer()
        self.id_dst = id_destination
        self.confirm = confirmbox.ConfirmBox('Do you want to copy This?', self.masterFrame, self.copyImage, self.openSharer)

    def shareNotification(self):
        """little popup box to show that the image has been shared"""
        self.notiFrame = ctk.CTkFrame(master=self.viewer.frame, corner_radius=0,border_width=2, border_color=colours.backgroundAccent, fg_color=colours.backgroundHighlight)
        notification = ctk.CTkLabel(master=self.notiFrame, text='Sharing...',text_color=colours.successText, font = ('calibri',25))
        notification.pack(padx=10,pady=7)
        self.notiFrame.place(relx=0.5,rely=0.5,anchor='center')
        self.viewer.gallery.root.update()
        sleep(1)
        self.notiFrame.destroy()