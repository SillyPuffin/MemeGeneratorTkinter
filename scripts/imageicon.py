import tkinter as tk
from tkinter import font
import customtkinter as ctk

from scripts import colours

class ImageIcon():
    def __init__(self, gallery, image,imagesize, index, name) -> None:
        self.image = image
        self.gallery = gallery
        self.index = index
        self.fullname = name
        self.imagesize = imagesize

        self.maxTextWidth = 20
        self.width = imagesize + 20

        if len(name) > self.maxTextWidth:
            tempname = name[0:self.maxTextWidth]
            tempname += '-'
            self.displayName = tempname
        else:
            self.displayName = name

        self.createBox()
    
    def createBox(self):
        """create the elements of the meme icon"""
        self.frame = ctk.CTkFrame(master= self.gallery.scrollGalleryFrame,fg_color=colours.backgroundHighlight,border_color=colours.backgroundAccent,border_width=3,corner_radius=4)

        image = tk.Label(master=self.frame, image=self.image,bg=colours.backgroundHighlight,width=self.imagesize,height=self.imagesize)
        image.bind("<Button-1>",self.openImageInViewer)

        testfont = font.Font(family='calibri',size=15)
        textframe=tk.Frame(master=self.frame, width=self.imagesize, background=colours.backgroundHighlight, height=testfont.metrics('linespace'))
        textframe.pack_propagate(False)

        self.textLabel = tk.Label(master=textframe, text=self.displayName, fg='white',bg=colours.backgroundHighlight, font=testfont)

        image.pack(pady=(5,0),padx=(10,10))

        self.textLabel.pack(side=tk.LEFT,anchor='nw')

        textframe.pack(pady=(0,5),padx=(10,10))

    def returnWidth(self):
        """returns the width of the frame of the icon"""
        return self.width

    def openImageInViewer(self,event):
        """executes the gallery function to open the depicted image in the viewer window"""
        self.gallery.openImageInViewer(self.fullname, self.index)