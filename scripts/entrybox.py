import tkinter as tk
import customtkinter as ctk

from scripts import colours

class EntryBox():
    def __init__(self, master, command=None, width :int=200, height : int = 20,font=None ,fg:str=None, bg : str=None, border_colour: str=None, text_colour:str=None, default_colour:str=None, default_text:str=None):
        self.master= master
        self.default = default_text
        self.command = command

        self.font = font
        self.default_font = ('Microsoft Yahei UI Light',font[1])

        self.bg = bg
        self.fg=fg
        self.border_colour = border_colour
        self.text_colour = text_colour
        self.default_colour = default_colour

        self.width=width
        self.height = height

        self.userTyped = False

        self.createBox()

    def createBox(self):
        """creates the entry box and gets all variables ready"""
        self.variable = tk.StringVar()
        #self.variable.trace_add('write', self.executeCommand)
        self.textBox = ctk.CTkEntry(master=self.master, font=self.default_font, width=self.width, height = self.height, bg_color=self.bg,fg_color=self.fg,border_color=self.border_colour,border_width=2, text_color=self.default_colour, textvariable=self.variable)
        self.textBox.insert(0, self.default)

        self.textBox.bind("<KeyRelease>", self.executeCommand)
        self.textBox.bind('<KeyPress>',self.setUserTyped, add=True)
        self.textBox.bind('<FocusIn>', self.enterBox)
        self.textBox.bind('<FocusOut>', self.leaveBox)
        
    def setUserTyped(self,event):
        """set the user typed variable to true when the user types"""
        self.userTyped = True

    def leaveBox(self,event=None):
        """trigger when the user clicks of the box"""
        if self.textBox.get() == '':
            self.userTyped = False
            self.textBox.insert(0, self.default)
            self.textBox.configure(font=self.default_font)
            self.textBox.configure(text_color = self.default_colour)

    def enterBox(self, event):
        """trigger when the user clicks on the box"""
        if self.textBox.get() == self.default and self.userTyped == False:
            self.textBox.delete(0,tk.END)
            self.textBox.configure(font=self.font)
            self.textBox.configure(text_color = self.text_colour)

    def setFont(self,font):
        """change the font of the text box to something new"""
        self.font = font
        
        if self.userTyped or (not self.userTyped and self.textBox.get()==''):
            self.textBox.configure(font=self.font)

    def executeCommand(self,*event):
        if self.command:
            self.command()