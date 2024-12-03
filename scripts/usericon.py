import tkinter as tk
import customtkinter as ctk

from tkinter import font
from scripts import colours

class UserIcon():
    def __init__(self,master, sharer, id, name, maxwidth) -> None:
        self.username = name
        self.masterframe = master
        self.id = id
        self.sharer = sharer
        self.pad = 5
        self.border_width = 2
        self.maxwidth = maxwidth
        self.textmaxwidth = maxwidth - self.border_width * 2 - self.pad*2

        self.createBox()

    def createBox(self):
        """creates all the elements of each box"""
        calibriFont = font.Font(family='calibri', size = 20)

        #get the string that fits on the image
        displayName = self.username
        while calibriFont.measure(displayName) > self.textmaxwidth:
            displayName = displayName[0:-1]

        self.frame = ctk.CTkFrame(master = self.masterframe, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent, border_width=self.border_width, width = self.maxwidth, height=calibriFont.metrics('linespace')+self.pad*2)
        self.frame.pack_propagate(False)

        self.label = tk.Label(master=self.frame, text = displayName, font = calibriFont,background=colours.backgroundHighlight,fg='white')
        self.label.pack(side=tk.LEFT,padx=self.pad,pady=self.pad)

        self.label.bind('<Button-1>', self.confirmShare)
        self.label.bind("<Enter>",self.widenBorder)
        self.label.bind("<Leave>",self.shrinkBorder)
        
    def confirmShare(self,event):
        """executes the sharer's confirm share function passing the id of the dst account"""
        self.sharer.confirmShare(self.id)

    def widenBorder(self,event):
        """widen the border"""
        self.frame.configure(border_width= self.border_width*2)

    def shrinkBorder(self,event):
        """shrink the border"""
        self.frame.configure(border_width = self.border_width)
        