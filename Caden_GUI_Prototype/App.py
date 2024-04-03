import tkinter as tk
from tkinter import ttk
from Frames import Stats, Format, Plot

# -- Windows only configuration --
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass
# -- End Windows only configuration --


class Window(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set up for the window
        self.title('CraterStats')
        self.geometry('1048x768')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=0)  # Row 0 for menu bar
        self.rowconfigure(1, weight=1)  # Row 1 for notebook
        self.resizable(False, False)

        # Create menu container frame
        menu_container = ttk.Frame(self)
        menu_container.grid(row=0, column=0, sticky='ew')

        # Configure menu container frame
        menu_container.columnconfigure(0, weight=0)  # Make the column stretch

        # Create Menu Bar
        file = ttk.Menubutton(menu_container, text='File')
        plot = ttk.Menubutton(menu_container, text='Plot')
        export = ttk.Menubutton(menu_container, text='Export')
        utilities = ttk.Menubutton(menu_container, text='Utilities')
        about = ttk.Menubutton(menu_container, text='About')

        file.menu = tk.Menu(file, tearoff=0)
        plot.menu = tk.Menu(plot, tearoff=0)
        export.menu = tk.Menu(export, tearoff=0)
        utilities.menu = tk.Menu(utilities, tearoff=0)
        about.menu = tk.Menu(about, tearoff=0)
        file["menu"] = file.menu
        plot["menu"] = plot.menu
        export["menu"] = export.menu
        utilities["menu"] = utilities.menu
        about["menu"] = about.menu

        file.grid(row=0, column=0, sticky="w")
        plot.grid(row=0, column=1, sticky="w")
        export.grid(row=0, column=2, sticky="w")
        utilities.grid(row=0, column=3, sticky="w")
        about.grid(row=0, column=4, sticky="w")

        # File Menu Button options
        file.menu.add_checkbutton(label="Save")
        file.menu.add_checkbutton(label="Open")
        file.menu.add_checkbutton(label="Close")
        file.menu.add_checkbutton(label="Exit")

        # Plot Menu Button options
        plot.menu.add_checkbutton(label="New")
        plot.menu.add_checkbutton(label="Duplicate")
        plot.menu.add_checkbutton(label="Delete")

        # Export Menu Button options
        export.menu.add_checkbutton(label="Image")
        export.menu.add_checkbutton(label="Summary file")
        export.menu.add_checkbutton(label=".stat table")

        # Utilities menu button options
        utilities.menu.add_checkbutton(label="Sum .stat files")
        utilities.menu.add_checkbutton(label="Merge .diam files")
        utilities.menu.add_checkbutton(label="Randomness Analysis")

        # Create tabs
        container = ttk.Frame(self)
        # Make container stretch
        container.grid(row=1, column=0, sticky='nsew')

        container.columnconfigure(0, weight=1)  # Make the column stretch
        container.rowconfigure(0, weight=1)  # Make the row stretch

        tab_parent = ttk.Notebook(container)

        tab1 = Stats(tab_parent, self)
        tab2 = Format(tab_parent, self)
        tab3 = Plot(tab_parent, self)

        tab_parent.add(tab1, text='Statistics')
        tab_parent.add(tab2, text='Formatatting')
        tab_parent.add(tab3, text='Plot')

        tab_parent.grid(row=0, column=0, sticky="nsew")

        style = ttk.Style(self)
        print(style.theme_names())
        style.theme_use("alt")


app = Window()
app.mainloop()
