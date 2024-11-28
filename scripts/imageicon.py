import tkinter as tk
import customtkinter as ctk

from scripts import colours

class ImageIcon():
    def __init__(self, gallery, image, index, name) -> None:
        self.image = image
        self.gallery = gallery
        self.index = index
        self.fullname = name

        if len(name) > 25:
            tempname = name[0][25]
            tempname += '-'
            self.displayName = tempname
        else:
            self.displayName = name

        self.createBox()
    
    def createBox(self):
        self.frame = ctk.CTkFrame(master= self.gallery.scrollGalleryFrame,fg_color=colours.backgroundHighlight,border_color=colours.backgroundAccent,border_width=3,corner_radius=4)
        tk.Label(master=self.frame, image=self.image,bg=colours.backgroundHighlight,width=100,height=100).pack(pady=5)
        tk.Label(master=self.frame, text=self.displayName, fg='white',bg=colours.backgroundHighlight, font=('calibri',15)).pack(padx=5,pady=5)

        self.frame.bind("<Button-1>",self.openImageInViewer)
        
    def returnWidth(self):
        """returns the width of the frame of the icon"""
        return self.frame.winfo_width()

    def openImageInViewer(self,event):
        """executes the gallery function to open the depicted image in the viewer window"""
        print('skibbids')
        self.gallery.openImageInViewer(self.fullname, self.index)