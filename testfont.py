import customtkinter as ctk
import tkinter as tk


root = tk.Tk()

ctk.FontManager.load_font('Fonts/impact.ttf')

label = ctk.CTkLabel(master=root, text='hello!', font=("Fonts/impact",20), text_color='black')
label.place(relx=0.5,rely=0.5,anchor='center')

root.mainloop()