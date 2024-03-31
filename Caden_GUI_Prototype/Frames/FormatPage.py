import tkinter as tk
from tkinter import ttk


class Format(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.title_box = tk.IntVar(value=0)
        self.subtitle_box = tk.IntVar(value=0)
        self.plot_title = tk.StringVar()
        self.plot_subtitle = tk.StringVar()
        self.print_scale = tk.StringVar()
        self.text_point = tk.StringVar()

        # Plot Title/Size
        self.plot_title_checkbox = ttk.Checkbutton(
            self,
            text="Title",
            variable=self.title_box
        )
        self.plot_title_entry = ttk.Entry(
            self,
            textvariable=self.plot_title
        )
        self.plot_subtitle_checkbox = ttk.Checkbutton(
            self,
            text="Subtitle",
            variable=self.subtitle_box
        )
        self.plot_subtitle_entry = ttk.Entry(
            self,
            textvariable=self.plot_subtitle
        )



