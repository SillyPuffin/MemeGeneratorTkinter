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

        self.cutName = name[0:-4]#removes the file type prefix

        self.createBox()
    
    def createBox(self):
        """create the elements of the meme icon and define the width and height"""
        pad = 5
        bordersize = 2
        
        self.width = self.imagesize + 2*pad + 2*bordersize

        calibriFont = font.Font(family='calibri', size = 15)

        #get the string that fits on the image
        displayName = self.cutName
        while calibriFont.measure(displayName) > self.imagesize:
            displayName = displayName[0:-1]
        
        self.height = self.imagesize + calibriFont.metrics('linespace') + pad*4 + bordersize * 2
    

        self.frame = ctk.CTkFrame(master = self.gallery.scrollGalleryFrame, width = self.width, height=self.height,corner_radius=4, border_width=bordersize, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent)
        self.frame.pack_propagate(False)

        imageLabel = tk.Label(master=self.frame, background=colours.backgroundColour, image=self.image, width=self.imagesize, height=self.imagesize)
        imageLabel.pack(padx=pad,pady=(pad,pad))
        imageLabel.bind("<Button-1>",self.openImageInViewer)

        imageLabel.bind("<Enter>",self.widenBorder)
        imageLabel.bind("<Leave>",self.shrinkBorder)

        nameLabel = tk.Label(master=self.frame, text=displayName, background=colours.backgroundHighlight, foreground='white',font=calibriFont)

        topLeftofLabel = bordersize + pad + self.imagesize + pad
        percentofHeight = topLeftofLabel/self.height

        nameLabel.place(x=bordersize+pad,y=topLeftofLabel, anchor='nw')

    def returnWidth(self):
        """returns the width of the frame of the icon + how much padding it should have"""
        return self.width + 20

    def openImageInViewer(self,event):
        """executes the gallery function to open the depicted image in the viewer window"""
        self.gallery.openImageInViewer(self.fullname, self.index)

    def widenBorder(self,event):
        """doubles the border size"""
        borderwidth = self.frame._border_width
        self.frame.configure(border_width=int(borderwidth*2))

    def shrinkBorder(self,event):
        """halfs the border size"""
        borderwidth = self.frame._border_width
        self.frame.configure(border_width=int(borderwidth/2))