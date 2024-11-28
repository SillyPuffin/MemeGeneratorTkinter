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

        cutName = name[0:-4]

        if len(name) > self.maxTextWidth:
            tempname = cutName[0:self.maxTextWidth]
            tempname += '-'
            self.displayName = tempname
        else:
            self.displayName = cutName

        self.createBox()
    
    def createBox(self):
        """create the elements of the meme icon and define the width and height"""
        pad = 5
        bordersize = 2
        
        self.width = self.imagesize + 2*pad + 2*bordersize

        calibriFont = font.Font(family='calibri', size = 15)
        
        self.height = self.imagesize + calibriFont.metrics('linespace') + pad*4 + bordersize * 2
    

        self.frame = ctk.CTkFrame(master = self.gallery.frame, width = self.width, height=self.height,corner_radius=4, border_width=bordersize, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent)
        self.frame.pack_propagate(False)
        imageLabel = tk.Label(master=self.frame, background=colours.backgroundHighlight, image=self.image, width=self.imagesize, height=self.imagesize)
        imageLabel.pack(padx=pad,pady=(pad,pad))
        nameLabel = tk.Label(master=self.frame, text=self.displayName, background=colours.backgroundHighlight, foreground='white',font=calibriFont)

        nameLabel.pack(anchor='w',padx=pad,pady=(pad,pad))

    def returnWidth(self):
        """returns the width of the frame of the icon"""
        return self.width

    def openImageInViewer(self,event):
        """executes the gallery function to open the depicted image in the viewer window"""
        self.gallery.openImageInViewer(self.fullname, self.index)