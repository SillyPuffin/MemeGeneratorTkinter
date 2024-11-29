import customtkinter as ctk
import tkinter as tk

from scripts import colours

class ConfirmBox():
    def __init__(self,text, master, conf_command, canc_command):
        self.text = text
        self.command = conf_command
        self.canc_command = canc_command
        self.master = master

        self.createElements()

    def createElements(self):
        borderwidth = 4
        pad = 8

        self.frame = ctk.CTkFrame(master = self.master, border_width=borderwidth,corner_radius=0, border_color=colours.backgroundAccent, fg_color=colours.backgroundHighlight)
        self.frame.place(relx=0.5,rely=0.5, anchor = 'center')

        label = tk.Label(master=self.frame,fg='white', text=self.text, font=('calibri',20),background=colours.backgroundHighlight)
        label.pack(padx=pad+borderwidth,pady=(pad+borderwidth,pad))

        #buttons
        tempframe = tk.Frame(master=self.frame, background=colours.backgroundHighlight)
        confirm = ctk.CTkButton(master = tempframe, text='Confirm',font=('calibri',20),fg_color=colours.button,hover_color=colours.buttonHover, command=self.executeCommand)
        confirm.pack(side=tk.LEFT,padx=(0,pad))

        cancel = ctk.CTkButton(master = tempframe, text='Cancel',font=('calibri',20),fg_color=colours.redButton,hover_color=colours.redButtonHover, command=self.cancelCommand)
        cancel.pack(side=tk.LEFT,padx=(5,0))
        tempframe.pack(padx=pad+borderwidth,pady=(pad,pad+borderwidth))

    def cancelCommand(self):
        self.frame.destroy()
        self.canc_command()

    def executeCommand(self):
        self.frame.destroy()
        self.command()
