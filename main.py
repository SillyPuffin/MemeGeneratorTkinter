import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageDraw

root = tk.Tk()
root.geometry()


frame = tk.Frame(master=root,bg="#083212",height=200, width = 200)
ctk.CTkButton(master=frame,text="hello",corner_radius=20,fg_color="green").place(rely=0.5,relx=0.5,anchor="center")

frame.pack(fill=tk.BOTH,side=tk.TOP,expand=True)

root.mainloop()