import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class Plot(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # Plot image
        self.image = Image.open("Caden_GUI_Prototype/Frames/moonpic.png")

        self.resized_image = self.image.resize((510, 510))
        self.new_image = ImageTk.PhotoImage(self.resized_image)

        self.plot_picture = tk.Canvas(
            self,
            bg='#FFF',
            width=510,
            height=510,
        )

        self.plot_picture.create_image(
            250, 0, anchor='n', image=self.new_image)

        self.plot_picture.place(relx=0.5, rely=0.5, anchor="center")

        # Command line text
        self.command_line_text = ttk.Label(
            self,
            text="craterstats -cs neukumivanov -ep mars -ef standard -p source=%sample%/Pickering.scc -p type=poisson,range=[2,5],offset_age=[2,-2] -p range=[.2,.7]",
            background="#000",
            foreground="#fff",
            padding=(5, 7.5),
            font=('Courier', 11)
        )
        # self.command_line_text['state'] = 'disabled'

        self.command_line_text.place(
            x=0, y=287.5, relx=0.5, rely=0.5, anchor='center')

        self.diameter = tk.StringVar()
        self.y = tk.StringVar()
        self.age = tk.StringVar()
        self.n_value = tk.StringVar()
        self.a0 = tk.StringVar()

        # Info Bar
        self.diam_label = ttk.Label(
            self,
            text="Diameter"
        )
        self.diam_entry = ttk.Entry(
            self,
            textvariable=self.diameter,
            width=7
        )

        self.bin_label = ttk.Label(
            self,
            text="Bin"
        )
        self.bin_text_box = ttk.Entry(
            self,
            width=7
        )

        self.n_label = ttk.Label(
            self,
            text="n"
        )
        self.n_text_box = ttk.Entry(
            self,
            width=7
        )

        self.y_label = ttk.Label(
            self,
            text="y"
        )
        self.y_text_box = ttk.Entry(
            self,
            textvariable=self.y,
            width=7
        )

        self.age_label = ttk.Label(
            self,
            text="Age"
        )
        self.age_text_box = ttk.Entry(
            self,
            textvariable=self.age,
            width=7
        )

        self.n_value_label = ttk.Label(
            self,
            text="n(T)"
        )
        self.n_value_text_box = ttk.Entry(
            self,
            textvariable=self.n_value,
            width=7
        )

        self.a0_label = ttk.Label(
            self,
            text="a0"
        )
        self.a0_text_box = ttk.Entry(
            self,
            textvariable=self.a0,
            width=7
        )

        self.diam_label.place(x=-225, y=-300, relx=0.5,
                              rely=0.5, anchor='center')
        self.diam_entry.place(x=-225, y=-280, relx=0.5,
                              rely=0.5, anchor='center')

        self.bin_label.place(x=-150, y=-300, relx=0.5,
                             rely=0.5, anchor='center')
        self.bin_text_box.place(x=-150, y=-280, relx=0.5,
                                rely=0.5, anchor='center')
        self.bin_text_box['state'] = 'disabled'

        self.n_label.place(x=-75, y=-300, relx=0.5, rely=0.5, anchor='center')
        self.n_text_box.place(x=-75, y=-280, relx=0.5,
                              rely=0.5, anchor='center')
        self.n_text_box['state'] = 'disabled'

        self.y_label.place(x=0, y=-300, relx=0.5, rely=0.5, anchor='center')
        self.y_text_box.place(x=0, y=-280, relx=0.5,
                              rely=0.5, anchor='center')

        self.age_label.place(x=75, y=-300, relx=0.5, rely=0.5, anchor='center')
        self.age_text_box.place(x=75, y=-280, relx=0.5,
                                rely=0.5, anchor='center')

        self.n_value_label.place(
            x=150, y=-300, relx=0.5, rely=0.5, anchor='center')
        self.n_value_text_box.place(
            x=150, y=-280, relx=0.5, rely=0.5, anchor='center')

        self.a0_label.place(x=225, y=-300, relx=0.5, rely=0.5, anchor='center')
        self.a0_text_box.place(x=225, y=-280, relx=0.5,
                               rely=0.5, anchor='center')
