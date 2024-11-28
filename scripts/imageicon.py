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
        print(self.imagesize)

        self.maxTextWidth = 20

        if len(name) > self.maxTextWidth:
            tempname = name[0:self.maxTextWidth]
            tempname += '-'
            self.displayName = tempname
        else:
            self.displayName = name

        self.createBox()
    
    def createBox(self):
        self.frame = ctk.CTkFrame(master= self.gallery.scrollGalleryFrame,fg_color=colours.backgroundHighlight,border_color=colours.backgroundAccent,border_width=3,corner_radius=4)

        image = tk.Label(master=self.frame, image=self.image,bg=colours.backgroundHighlight,width=self.imagesize,height=self.imagesize)
        image.bind("<Button-1>",self.openImageInViewer)

        testfont = font.Font(family='calibri',size=15)
        self.textLabel = tk.Label(master=self.frame, text=self.displayName, fg='white',bg=colours.backgroundHighlight, font=testfont)

        #calculate the max width of the box
        sizeString = 'A'
        sizeString *= self.maxTextWidth
        print(sizeString)
        self.width = max([self.imagesize+10,testfont.measure(sizeString)+10])
        print(testfont.measure(sizeString)+10)

        self.frame.configure(width=self.width)
        self.frame.pack_propagate(False)
        

        image.pack(pady=5,padx=5)
        self.textLabel.pack(pady=5,padx=5)

    def returnWidth(self):
        """returns the width of the frame of the icon"""
        return self.width

    def openImageInViewer(self,event):
        """executes the gallery function to open the depicted image in the viewer window"""
        self.gallery.openImageInViewer(self.fullname, self.index)