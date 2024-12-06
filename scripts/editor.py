import tkinter as tk
import customtkinter as ctk

from tkinter import font

from scripts import colours
from scripts import database
from scripts import entrybox

class Editor():
    def __init__(self,main) -> None:
        self.DatabasePath = main.DatabasePath
        self.templatePath = 'Templates/'

        self.root = main.root
        self.main = main

        self.templateIcons = []

        self.baseImage = None
        self.image = None
        self.displayImage = None

        self.createMainFrame()
        self.createTopBar()
        self.createFontList()
        self.createLeftWindow()

    def openImage(self, path=None):
        """loads the image supplied in the path and opens the editor or opens an empty image"""
        self.currentAccount = self.main.currentAccount

        if path:
            self.loadImage(path)

        self.openMainFrame()

    def openImageFromFile(self):
        """open file dialog to open an image"""
        pass

    def LoadTemplate(self,templateName):
        """load a template image from the template directory"""
        self.loadImage(self.templatePath + templateName)

    def openTemplateList(self):
        """open the template selection list in the middle of the screen"""

    def saveImage(self):
        """save the current image to the users meme folder"""
        pass

    def loadImage(self,path):
        """load the image into the right window"""
        pass

    def createMainFrame(self):
        """create the main frame"""
        self.frame = tk.Frame(master=self.main.root,background=colours.backgroundColour)

    def createTemplateList(self):
        """create the frame and icons for the template list offscreen"""
        self.createTemplatedisplay()
        self.createTemplateIcons()

    def createTemplatedisplay(self):
        """generate the frame and scroll bar elements in the template frame"""
        pass

    def createTemplateIcons(self):
        """create the template icons and pack them"""
        pass

    def createTopBar(self):
        """create the file bar and title bar along the top"""
        self.topFrame = ctk.CTkFrame(master=self.frame, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent, border_width=2, corner_radius=0)
        self.topFrame.pack(side='top', fill=tk.X)

        title = tk.Label(master=self.topFrame, text='Editor',font=('impact',18),bg=colours.backgroundHighlight, fg=colours.Heading)

        saveButton = ctk.CTkButton(master=self.topFrame, text='Save', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.saveImage)
        saveButton.pack(side='left', anchor='w',pady=4, padx=(5,3))

        loadButton = ctk.CTkButton(master=self.topFrame, text='Load', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.openImageFromFile)
        loadButton.pack(side='left',anchor='w',padx=(0,3),pady=4)

        templatesButton = ctk.CTkButton(master=self.topFrame, text='Templates', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.openTemplateList)
        templatesButton.pack(side='left',anchor='w',pady=4)

        exitButton = ctk.CTkButton(master=self.topFrame, text='Exit', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.backToGallery)
        exitButton.pack(side='right',anchor='e',pady=4,padx=(0,4))

        #setting the frame height
        maxButtonHeight = templatesButton.winfo_reqheight() + 8
        titleHeight = title.winfo_reqheight() + 8

        if titleHeight > maxButtonHeight:
            self.topFrame.pack_propagate(False)
            self.topFrame.configure(height = titleHeight)
            title.place(relx=0.5,rely=0.5,anchor='center')


    def createLeftWindow(self):
        """create the bottom left window that contains the entry boxes for top and bottom text"""
        self.entryWidth = 400
        padx = 10
        borderWidth = 2
        framewidth = self.entryWidth+2*padx + 2*borderWidth

        self.leftWindow = ctk.CTkFrame(master=self.frame, width=framewidth, fg_color = colours.backgroundHighlight,border_color=colours.backgroundAccent, border_width=borderWidth, bg_color=colours.backgroundColour)
        self.leftWindow.pack(side=tk.LEFT, fill=tk.Y)

        self.centerFrame = tk.Frame(master=self.leftWindow, background=colours.backgroundHighlight)
        self.centerFrame.place(relx=0.5,rely=0.5,anchor='center')
        
        self.font = self.fontList['Impact']
        fontnames = list(self.fontList.keys())

        self.fontChangeBox = ctk.CTkOptionMenu(self.centerFrame,height=50, width=self.entryWidth, bg_color=colours.backgroundHighlight,button_color=colours.textboxShadow, button_hover_color=colours.textboxHover, dropdown_fg_color=colours.textboxBackground,dropdown_text_color=colours.typeText, fg_color=colours.textboxBackground,dropdown_font=self.font, font=self.font, text_color=colours.typeText
        ,values=fontnames, command=self.switchFont)
        self.fontChangeBox.pack(padx=10,pady=10)

        self.topText = entrybox.EntryBox(self.centerFrame, self.updateText, self.entryWidth, 50, self.font,colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Top Text')
        self.topText.textBox.pack(padx=10,pady=10)

        self.bottomText = entrybox.EntryBox(self.centerFrame, self.updateText, self.entryWidth, 50, self.font,colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Bottom Text')
        self.bottomText.textBox.pack(padx=10,pady=10)

    def createFontList(self):
        """generate a dictionary full of all the font types"""
        size = 20
        self.fontList = {
            'Impact':('Impact',size),
            'Calibri':('Calibri',size)
        }

    def switchFont(self,font):
        """switch the font"""
        self.font = self.fontList[font]

        self.fontChangeBox.configure(font=self.font, dropdown_font=self.font)

        self.topText.setFont(self.font)

        self.bottomText.setFont(self.font)

    def updateText(self):
        """update the text on the image and change the display image to match"""
        pass

    def drawText(self, text, y):
        """draw the text on the top or bottom of the bed"""
        pass

    def openMainFrame(self):
        """pack the main frame"""
        self.frame.pack(fill=tk.BOTH,expand= True)

    def backToGallery(self):
        """go back to the gallery"""
        self.frame.pack_forget()
        self.image = None
        self.displayImage = None

        #readying the gallery to be displayed again
        self.main.gallery.createMemeIcons(database.getFolderPath(self.currentAccount, self.main.DatabasePath))
        self.main.gallery.packMemeIcons()
        #putting the gallery back on the screen
        self.main.gallery.repackFrame()

