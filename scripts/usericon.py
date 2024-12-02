import tkinter as tk
import customtkinter as ctk

from tkinter import font
from scripts import colours

class UserIcon():
    def __init__(self,master, viewer, id, name, maxwidth) -> None:
        self.username = name
        self.frame = master
        self.id = id
        self.viewer = viewer
        self.pad = 5
        self.maxwidth = maxwidth

        self.createBox(self)

    def createBox(self):
        
        calibriFont = font.Font(family='calibri', size = 15)

        #get the string that fits on the image
        displayName = self.username
        while calibriFont.measure(displayName) > self.imagesize:
            displayName = displayName[0:-1]

        self.frame = ctk.CTkFrame(master = self.frame, fg_color=colours.backgroundColour, border_color=colours.backgroundAccent, border_width=2)

        self.label = tk.Label(master=self.frame, text = displayName, font = calibriFont,background=colours.backgroundColour,fg='white')
        self.label.pack(padx=self.pad,pady=self.pad)