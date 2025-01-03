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
        self.bordersize = 2
        pad = 4
        
        self.width = self.imagesize + 4*self.bordersize

        calibriFont = font.Font(family='calibri', size = 15, weight='bold')

        #get the string that fits on the image
        displayName = self.cutName.title()
        while calibriFont.measure(displayName) > self.imagesize:
            displayName = displayName[0:-1]
        
        self.height = self.imagesize + 2 + calibriFont.metrics('linespace') + pad*2 + self.bordersize*4

        self.frame = ctk.CTkFrame(master = self.gallery.scrollGalleryFrame, width = self.width, height=self.height,corner_radius=4, border_width=self.bordersize, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent)
        self.frame.pack_propagate(False)

        imageLabel = tk.Label(master=self.frame, background=colours.backgroundColour, image=self.image, width=self.imagesize, height=self.imagesize)
        imageLabel.pack(padx=2*self.bordersize,pady=(2*self.bordersize,0))
        imageLabel.bind("<Button-1>",self.openImageInViewer)

        self.div1 = tk.Frame(master=self.frame, background=colours.backgroundAccent,height=2,width=self.width-self.bordersize*2)
        self.div1.pack(pady=(0,pad))

        imageLabel.bind("<Enter>",self.widenBorder)
        imageLabel.bind("<Leave>",self.shrinkBorder)

        nameLabel = tk.Label(master=self.frame, text=displayName, background=colours.backgroundHighlight, foreground='white',font=calibriFont)
        nameLabel.pack(pady=(0,pad+self.bordersize))

    def returnWidth(self):
        """returns the width of the frame of the icon + how much padding it should have"""
        return self.width + 20

    def openImageInViewer(self,event):
        """executes the gallery function to open the depicted image in the viewer window"""
        self.gallery.openImageInViewer(self.fullname, self.index)
        self.shrinkBorder

    def widenBorder(self,event):
        """doubles the border size"""
        if not self.gallery.pause:
            self.frame.configure(border_width=int(self.bordersize*2))

    def shrinkBorder(self,event):
        """halfs the border size"""
        if not self.gallery.pause:
            borderwidth = self.frame._border_width
            self.frame.configure(border_width=int(self.bordersize))