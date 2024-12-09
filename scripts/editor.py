import tkinter as tk
import customtkinter as ctk

from tkinter import font, filedialog

from PIL import Image, ImageTk, ImageFont, ImageDraw

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

    def LoadTemplate(self):
        """load a template image from the template directory"""
        filename = filedialog.askopenfilename(initialdir=self.templatePath,title='open an image', filetypes=[('all files','*.png *.jpg'),('PNG file','*.png'),('JPEG file','*.jpg')])

        print(f"loading {filename}")

        self.loadImage(filename)

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

    def setDisplayImage(self):
        """udate and resize the display image based on the width parameters"""
        self.displayImage = self.image.copy()
        self.displayImage.thumbnail((self.imageWidth, self.imageHeight))
        self.displayImage = ImageTk.PhotoImage(self.displayImage)

    def updateImageLabel(self):
        """reset the image label to use the new display image"""
        self.imageLabel.place_forget()
        self.imageLabel = tk.Label(master= self.imageFrame, text='', image= self.displayImage, bg=colours.backgroundColour)
        self.imageLabel.place(relx=0.5,rely=0.5,anchor='center')

    def loadImage(self,path):
        """load the image into the right window"""
        self.root.update_idletasks()
        self.imageWidth = self.main.screenSize[0] - self.leftWindow.winfo_width() - 20
        self.imageHeight = self.main.screenSize[1] - self.topFrame.winfo_height() - 20

        self.size= 40
        self.baseImage = Image.open(path)
        self.updateImage()
        self.setDisplayImage()

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

        #reset the text boxes
        self.topText.textBox.delete(0,tk.END)
        self.topText.leaveBox()

        self.bottomText.textBox.delete(0,tk.END)
        self.bottomText.leaveBox()

        self.updateImageLabel()

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

    def createTopBar(self):
        """create the file bar and title bar along the top"""
        self.topFrame = ctk.CTkFrame(master=self.frame, fg_color=colours.backgroundHighlight, border_color=colours.backgroundAccent, border_width=2, corner_radius=0)
        self.topFrame.pack(side='top', fill=tk.X)

        self.title = tk.Label(master=self.topFrame, text='Editor',font=('impact',20),bg=colours.backgroundHighlight, fg=colours.Heading)

        saveButton = ctk.CTkButton(master=self.topFrame, text='Save', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.saveImage)
        saveButton.pack(side='left', anchor='w',pady=4, padx=(5,3))

        loadButton = ctk.CTkButton(master=self.topFrame, text='Load', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.openImageFromFile)
        loadButton.pack(side='left',anchor='w',padx=(0,3),pady=4)

        templatesButton = ctk.CTkButton(master=self.topFrame, text='Templates', font=('calibri',20),width=1,corner_radius=4 ,fg_color=colours.backgroundHighlight, hover_color=colours.backgroundAccent,command=self.LoadTemplate)
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
            self.ActiveFontName = list(self.fontList.keys())[0]
            self.uifont = (list(self.fontList.items())[0][1], 20)
        except:
            self.ActiveFontName = None
            self.uifont = ('Microsoft Yahei UI Light',20)

        fontnames = list(self.fontList.keys())
        fontsizeBoxWidth = 125
        pad = 10

        self.fontChangeBox = ctk.CTkOptionMenu(self.fontFrame,height=50, width=self.entryWidth - fontsizeBoxWidth - pad, bg_color=colours.backgroundHighlight,button_color=colours.textboxShadow, button_hover_color=colours.textboxHover,dropdown_hover_color=colours.dropDownHover, dropdown_fg_color=colours.textboxBackground,dropdown_text_color=colours.typeText, fg_color=colours.textboxBackground,dropdown_font=self.uifont, font=self.uifont, text_color=colours.typeText
        ,values=fontnames, command=self.switchFont)
        self.fontChangeBox.pack(side='left',padx=(0,10))

        self.fontsizeBox = ctk.CTkComboBox(self.fontFrame, width= fontsizeBoxWidth, height=50, bg_color=colours.backgroundHighlight, button_color=colours.textboxShadow, button_hover_color=colours.textboxHover, dropdown_hover_color=colours.dropDownHover, dropdown_fg_color=colours.textboxBackground, dropdown_text_color=colours.typeText, fg_color=colours.textboxBackground, dropdown_font=('calibri',20), font=('calibri',20),text_color=colours.typeText,
        values = [str(i) for i in range(40,81,2)], command=self.setFontSize)
        self.fontsizeBox.set(str(self.size)) 
        self.fontsizeBox.bind('<Return>',self.setFontSize)
        self.fontsizeBox.pack(side='left')

        #packing font seletcion grid
        self.fontFrame.grid(row= 2, column=0, pady=(10,5))

        self.topText = entrybox.EntryBox(self.textFrame, self.updateImage, self.entryWidth, 50, self.uifont,colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Top Text')
        self.topText.textBox.grid(row=3,column=0,pady=5)

        self.bottomText = entrybox.EntryBox(self.textFrame, self.updateImage, self.entryWidth, 50, self.uifont,colours.textboxBackground,colours.backgroundHighlight, colours.textboxShadow, colours.typeText, colours.defaultText, 'Bottom Text')
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
        self.size= 40

        pathwalk = list(walk('Fonts/'))

        if pathwalk != []:
            fontnames = pathwalk[0][2]

        self.fontList = {}

        for name in fontnames:
            #loading the font from the .ttf
            ctk.FontManager.load_font("Fonts/"+name)
            #getting the name of the family of the font because its different to the name of the font file
            familyName = ImageFont.truetype("Fonts/"+name).getname()[0]
            self.fontList[name[:-4]] = familyName
            
#image editing logic
    def switchFont(self,font):
        """switch the font"""
        self.uifont = (self.fontList[font], 20)
        self.ActiveFontName = font
        
        self.fontChangeBox.configure(font=self.uifont, dropdown_font=self.uifont)

        self.topText.setFont(self.uifont)

        self.bottomText.setFont(self.uifont)

        self.updateImage()

    def setFontSize(self, choice=None):
        """set the global font size for top and bottom text"""
        if type(choice)==str:
            self.size = int(choice)
        else:
            self.size = int(self.fontsizeBox.get())

        self.updateImage()

    def getWordWidth(self, new_font, word, draw)-> int:
        """return the width of the word in pixels"""
        font_ttf = new_font
        bounding = draw.textbbox(xy=(0,0), text=word, font=font_ttf)
        width = bounding[2] - bounding[0]

        return int(width)

    def wrapText(self, text, font, size, pad = 10)->list[str] | int:
        """returns a string seperated by new line characters for each wrapped line as well as the height of the bounding box of the whole textbox"""
        lines = []
        current_line = []

        #draw image for getting the text width
        draw = ImageDraw.Draw(self.image)
        maxWidth = self.image.width - pad*2 #max width in pixels
        words = text.split(" ")

        if font:#load the active font nmae
            font_ttf= ImageFont.truetype("Fonts/" + font + ".ttf", size = size)
        else:
            font_ttf = ImageFont.load_default()#if its not set load the default font

        for word in words:
            #get the width of the word
            width = self.getWordWidth(font_ttf, word, draw)

            if width > maxWidth:
                #add the word in individual letters until it is to big to fit
                if current_line:
                    lines.append(" ".join(current_line))
                    current_line = []
                temp_word = word

                while temp_word:
                    #finding the maximum amount of letters that will fit
                    breaked = False
                    for i in range(1, len(temp_word) + 1):
                        part = temp_word[:i]
                        partWidth = self.getWordWidth(font_ttf, part, draw)
                        if partWidth > maxWidth:
                            # If adding one more character exceeds max width add the last fitting letters
                            lines.append(temp_word[:i-1])
                            temp_word = temp_word[i-1:]  # Update remaining word
                            breaked= True
                            break
                        
                    #if the for loop ends and it hasn't appended the last part add it to a new line
                    if not breaked:
                        current_line.append(part)
                        temp_word = ''
            
            else:
                #check to see if the test line is larger than the max width
                testLine = " ".join(current_line + [word])
                width = self.getWordWidth(font_ttf, testLine, draw)
                
                if width <= maxWidth:
                    current_line.append(word)
                else:
                    #commit the current line and start a new one
                    lines.append(" ".join(current_line))
                    current_line = [word]
        
        #add the last line if there are any words in it
        if current_line:
            lines.append(" ".join(current_line))

        #find the height of a single line
        ascent, descent = font_ttf.getmetrics()#get the height of the highest letters like b and lowest like g form the baseline
        (width, baseline), (offset_x, offset_y) = font_ttf.font.getsize('A')

        height = (ascent) * len(lines)
        if len(lines) > 0:
            height += (len(lines) - 1) * 4

        return "\n".join(lines) , height
    
    def updateImage(self, event=None):
        """reset the image and update the text displayed on it"""
        if self.baseImage:
            self.image = self.baseImage.copy()

            self.updateText()

            self.setDisplayImage()
            self.updateImageLabel()

    def updateText(self):
        """update the text on the image"""
        
        padding = 10

        #toptext
        if self.topText.userTyped:
            lines, height = self.wrapText(self.topText.variable.get(), self.ActiveFontName, self.size, padding)
            self.drawCaptionText(lines, self.ActiveFontName, self.size, padding, height, 'top')

        #bottomtext
        if self.bottomText.userTyped:
            lines, height = self.wrapText(self.bottomText.variable.get(), self.ActiveFontName, self.size, padding)
            self.drawCaptionText(lines, self.ActiveFontName, self.size, padding, height, 'bottom')

    def drawCaptionText(self, text, font, size, padding, height, orientation):
        """draw the text on the top or bottom of the bed"""
        if font:#load the active font nmae
            font_ttf= ImageFont.truetype("Fonts/" + font + ".ttf", size = size)
        else:
            font_ttf = ImageFont.load_default()#if its not set load the default font

        draw = ImageDraw.Draw(self.image)

        if orientation == 'top':
            draw.multiline_text(xy=(padding, 0), text=text, font= font_ttf)
        if orientation == 'bottom':
            y = self.image.height - height
            draw.multiline_text(xy=(padding, y), text=text, font= font_ttf)
#open and close editor
    def openMainFrame(self):
        """pack the main frame"""
        self.frame.pack(fill=tk.BOTH,expand= True)

    def backToGallery(self):
        """go back to the gallery"""
        self.frame.pack_forget()
        self.baseImage = None
        self.image = None
        self.displayImage = None

        #readying the gallery to be displayed again
        self.main.gallery.createMemeIcons(database.getFolderPath(self.currentAccount, self.main.DatabasePath))
        self.main.gallery.packMemeIcons()
        #putting the gallery back on the screen
        self.main.gallery.repackFrame()

