import tkinter as tk
import customtkinter as ctk

from tkinter import font, filedialog

from PIL import Image, ImageTk, ImageFont

from time import sleep

from os import walk

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

        self.createRightWindow()

##image load/save logic
    def openImage(self, path=None):
        """loads the image supplied in the path and opens the editor or opens an empty image"""
        self.currentAccount = self.main.currentAccount

        self.openMainFrame()

        if path:
            self.loadImage(path)
        else:
            self.title.configure(text='Editor')

    def openImageFromFile(self):
        """open file dialog to open an image"""
        filename = filedialog.askopenfilename(title='open an image', filetypes=[('all files','*.png *.jpg'),('PNG file','*.png'),('JPEG file','*.jpg')])

        print(f"loading {filename}")

        self.loadImage(filename)

    def LoadTemplate(self,templateName):
        """load a template image from the template directory"""
        self.loadImage(self.templatePath + templateName)

    def openTemplateList(self):
        """open the template selection list in the middle of the screen"""

    def saveImage(self):
        """save the current image to the users meme folder"""

        if self.imageNameBox.userTyped and self.imageNameBox.textBox.get() != '':
            self.imageName = self.imageNameBox.textBox.get()

            savePath = database.getFolderPath(self.currentAccount, self.DatabasePath)

            database.saveImage(self.image, self.imageName +'.png', savePath)

            successSavelabel = tk.Label(master=self.saveFrame, text='Saving Successful', font=('calibri',20), fg=colours.successText,bg=colours.backgroundHighlight)
            successSavelabel.grid(row=4, column=0, sticky='w')
            self.root.update()
            sleep(1.5)
            successSavelabel.grid_forget()
        else:
            print('The image has no Name')
            failSavelabel = tk.Label(master=self.saveFrame, text='Image has No Name', font=('calibri',12), fg=colours.alertText,bg=colours.backgroundHighlight)
            failSavelabel.grid(row=4, column=0, sticky='w')
            self.root.update()
            sleep(0.75)
            failSavelabel.grid_forget()

    def loadImage(self,path):
        """load the image into the right window"""
        self.root.update_idletasks()
        self.imageWidth = self.main.screenSize[0] - self.leftWindow.winfo_width() - 20
        self.imageHeight = self.main.screenSize[1] - self.topFrame.winfo_height() - 20

        self.baseImage = Image.open(path)
        self.image = self.baseImage.copy()

        self.displayImage = self.image.copy()
        self.displayImage.thumbnail((self.imageWidth, self.imageHeight))
        self.displayImage = ImageTk.PhotoImage(self.displayImage)


        #showing the name of the file loaded on the editor title
        count = 1
        while path[-count] != '/':
            count+=1

        self.imageName = path[-(count-1):-4]

        self.title.configure(text=f'Editor - {self.imageName}')
        #putting in the meme name box the loaded image name
        self.imageNameBox.textBox.configure(text_color=colours.typeText)
        self.imageNameBox.textBox.delete(0,tk.END)
        self.imageNameBox.textBox.insert(0, self.imageName)
        self.imageNameBox.userTyped = True

        self.imageLabel.place_forget()
        self.imageLabel = tk.Label(master= self.imageFrame, text='', image= self.displayImage, bg=colours.backgroundColour)
        self.imageLabel.place(relx=0.5,rely=0.5,anchor='center')

    def saveNotification(self):
        """little notifcation box pop-up to tell the user that they have saved the image"""
        self.notiFrame = ctk.CTkFrame(master=self.frame, corner_radius=0,border_width=2, border_color=colours.backgroundAccent, fg_color=colours.backgroundHighlight)
        notification = ctk.CTkLabel(master=self.notiFrame, text='Saving...',text_color=colours.successText, font = ('calibri',30))
        notification.pack(padx=10,pady=7)
        self.notiFrame.place(relx=0.5,rely=0.5,anchor='center')
        self.root.update()
        sleep(1)
        self.notiFrame.destroy()
##generating gui     
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

        self.title = tk.Label(master=self.topFrame, text='Editor',font=('impact',20),bg=colours.backgroundHighlight, fg=colours.Heading)

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
        titleHeight = self.title.winfo_reqheight() + 8

        if titleHeight > maxButtonHeight:
            self.topFrame.pack_propagate(False)
            self.topFrame.configure(height = titleHeight)
            self.title.place(relx=0.5,rely=0.5,anchor='center')
        else:
            self.title.place(relx=0.5,rely=0.5,anchor='center')

    def createLeftWindow(self):
        """create the bottom left window that contains the entry boxes for top and bottom text"""
        self.entryWidth = 350
        padx = 10
        borderWidth = 2
        framewidth = self.entryWidth+2*padx + 2*borderWidth

        self.leftWindow = ctk.CTkFrame(master=self.frame, width=framewidth, fg_color = colours.backgroundHighlight,border_color=colours.backgroundAccent, border_width=borderWidth, bg_color=colours.backgroundColour)
        self.leftWindow.pack(side=tk.LEFT, fill=tk.Y)
        self.leftWindow.pack_propagate(False)

        #####SAVING NAME
        self.saveFrame = tk.Frame(master=self.leftWindow, background=colours.backgroundHighlight)
        self.saveFrame.pack(side='top', anchor='n', pady=borderWidth)

        saveTitle = tk.Label(master=self.saveFrame, text='Save Name', font = ('calibri',45), fg=colours.Heading, background=colours.backgroundHighlight)
        saveTitle.grid(row=0, column=0, sticky='w', padx=0)

        topsaveDiv = tk.Frame(self.saveFrame, width=self.entryWidth, height = 2, background=colours.dividerColour)
        topsaveDiv.grid(row=1,column=0)

        self.imageNameBox = entrybox.EntryBox(self.saveFrame, None, self.entryWidth, 50, ('Microsoft Yahei UI Light',20),colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Meme Name')
        self.imageNameBox.textBox.grid(row=2, column = 0,pady=10)

        bottomsaveDiv = tk.Frame(self.saveFrame, width=self.entryWidth, height=2 , background=colours.dividerColour)
        bottomsaveDiv.grid(row=3, column=0)

        #######TOP AND BOTTOM TEXT

        self.textFrame = tk.Frame(master=self.leftWindow, background=colours.backgroundHighlight)
        self.textFrame.pack(side='top')

        textTitle = tk.Label(master=self.textFrame, text='Text', font = ('calibri',45), fg=colours.Heading, background=colours.backgroundHighlight)
        textTitle.grid(row=0, column=0, sticky='w')

        topTextDiv = tk.Frame(self.textFrame, width=self.entryWidth, height = 2, background=colours.dividerColour)
        topTextDiv.grid(row=1,column=0)
        #font selection
        self.fontFrame = tk.Frame(master=self.textFrame, bg=colours.backgroundHighlight)
        
        try:
            self.ActiveFontName = list(self.fontList.items())[0][1]
            self.uifont = (list(self.fontList.items())[0][1], 20)
        except:
            self.ActiveFontName = None
            self.uifont = ('Microsoft Yahei UI Light',20)

        fontnames = list(self.fontList.keys())
        fontsizeBoxWidth = 100
        pad = 10

        print(self.uifont)

        self.fontChangeBox = ctk.CTkOptionMenu(self.fontFrame,height=50, width=self.entryWidth - fontsizeBoxWidth - pad, bg_color=colours.backgroundHighlight,button_color=colours.textboxShadow, button_hover_color=colours.textboxHover,dropdown_hover_color=colours.dropDownHover, dropdown_fg_color=colours.textboxBackground,dropdown_text_color=colours.typeText, fg_color=colours.textboxBackground,dropdown_font=self.uifont, font=self.uifont, text_color=colours.typeText
        ,values=fontnames, command=self.switchFont)
        self.fontChangeBox.pack(side='left',padx=(0,10))

        self.fontsizeBox = ctk.CTkComboBox(self.fontFrame, width= fontsizeBoxWidth, height=50, bg_color=colours.backgroundHighlight, button_color=colours.textboxShadow, button_hover_color=colours.textboxHover, dropdown_hover_color=colours.dropDownHover, dropdown_fg_color=colours.textboxBackground, dropdown_text_color=colours.typeText, fg_color=colours.textboxBackground, dropdown_font=('calibri',20), font=('calibri',20),text_color=colours.typeText,
        values = [str(i) for i in range(2,47,2)], command=self.setFontSize)
        self.fontsizeBox.set(str(self.size)) 
        self.fontsizeBox.bind('<Return>',self.setFontSize)
        self.fontsizeBox.pack(side='left')

        #packing font seletcion grid
        self.fontFrame.grid(row= 2, column=0, pady=(10,5))

        self.topText = entrybox.EntryBox(self.textFrame, self.updateText, self.entryWidth, 50, self.uifont,colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Top Text')
        self.topText.textBox.grid(row=3,column=0,pady=5)

        self.bottomText = entrybox.EntryBox(self.textFrame, self.updateText, self.entryWidth, 50, self.uifont,colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Bottom Text')
        self.bottomText.textBox.grid(row=4,column=0,pady=(5,10))

        bottomTextDiv = tk.Frame(self.textFrame, width=self.entryWidth, height = 2, background=colours.dividerColour)
        bottomTextDiv.grid(row=5, column=0)

        ###Borders


        ###resizing

    def createRightWindow(self):
        """generates the right window label for the image but keeps it empty"""
        self.imageFrame = tk.Frame(master=self.frame, bg=colours.backgroundColour)
        self.imageFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.imageLabel = tk.Label(master=self.imageFrame, text='', bg=colours.backgroundColour)
        self.imageLabel.place(relx=0.5,rely=0.5, anchor='center')

    def createFontList(self):
        """generate a dictionary full of all the font types"""
        self.size= 20

        pathwalk = list(walk('Fonts/'))

        if pathwalk != []:
            fontnames = pathwalk[0][2]

        self.fontList = {}

        for name in fontnames:
            ctk.FontManager.load_font("Fonts/"+name)
            familyName = ImageFont.truetype("Fonts/"+name).getname()[0]
            self.fontList[name[:-4]] = familyName
            

        print(self.fontList)

#image editing logic
    def switchFont(self,font):
        """switch the font"""
        self.uifont = (self.fontList[font], 20)
        
        self.fontChangeBox.configure(font=self.uifont, dropdown_font=self.uifont)

        self.topText.setFont(self.uifont)

        self.bottomText.setFont(self.uifont)

    def setFontSize(self, choice=None):
        """set the global font size for top and bottom text"""
        if type(choice)==str:
            self.size = int(choice)
        else:
            self.size = int(self.fontsizeBox.get())

    def updateText(self):
        """update the text on the image and change the display image to match"""
        pass

    def drawText(self, text, y):
        """draw the text on the top or bottom of the bed"""
        pass
#open and lcose editor
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

