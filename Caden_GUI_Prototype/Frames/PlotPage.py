import tkinter as tk
from tkinter import ttk


class Plot(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        image = tk.PhotoImage(file="Caden_GUI_Prototype\Frames\moonpic.png")

        self.plot_picture = tk.Label(
            self,
            image=image
        )

        self.plot_picture.pack()
