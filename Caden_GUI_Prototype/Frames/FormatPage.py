import tkinter as tk
from tkinter import ttk


class Format(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        # self.grid_rowconfigure(1, weight=1)
        # self.grid_rowconfigure(2, weight=1)
        # self.grid_rowconfigure(3, weight=1)
        # self.grid_rowconfigure(4, weight=1)
        # self.grid_rowconfigure(5, weight=1)
        # self.grid_rowconfigure(6, weight=1)

        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure(2, weight=1)
        # self.grid_columnconfigure(3, weight=1)
        # self.grid_columnconfigure(4, weight=1)

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
        self.plot_print_scale_label = ttk.Label(
            self,
            text="Print scale. cm/decade (or plot width x height.cm):"
        )
        self.plot_print_scale_entry = ttk.Entry(
            self,
            textvariable=self.print_scale,
            width=5
        )
        self.plot_text_size_label = ttk.Label(
            self,
            text="Text size.pt:"
        )
        self.plot_text_size_entry = ttk.Entry(
            self,
            textvariable=self.text_point,
            width=5
        )

        # Add Title and size
        self.plot_title_entry.grid(row=1, column=0, sticky='w')
        self.plot_title_checkbox.grid(row=1, column=1, sticky='w')
        self.plot_subtitle_entry.grid(row=2, column=0, sticky='w')
        self.plot_subtitle_checkbox.grid(row=2, column=1, sticky='w')
        self.plot_print_scale_label.grid(row=1, column=3, sticky='e')
        self.plot_print_scale_entry.grid(row=1, column=4, sticky='e')
        self.plot_text_size_label.grid(row=2, column=3, sticky='e')
        self.plot_text_size_entry.grid(row=2, column=4, sticky='e')

        plot_list_options = ("data", "age fit", "resurfacing fit")

        plot_option = tk.StringVar(value=plot_list_options)

        # Plot List settings
        self.plot_list_settings = tk.Listbox(
            self,
            listvariable=plot_option,
            height=3
        )
        self.plot_list_new_button = ttk.Button(
            self,
            text="New",
            width=9
        )
        self.plot_list_duplicate_button = ttk.Button(
            self,
            text="Duplicate",
            width=9
        )
        self.plot_list_delete_button = ttk.Button(
            self,
            text="Delete",
            width=9
        )
        self.plot_list_up_button = ttk.Button(
            self,
            text="Up",
            width=9
        )
        self.plot_list_down_button = ttk.Button(
            self,
            text="Down",
            width=9
        )

        self.plot_list_settings.grid(row=3, column=0, rowspan=2, sticky='w')
        self.plot_list_new_button.grid(row=3, column=1, sticky='w')
        self.plot_list_duplicate_button.grid(row=3, column=2, sticky='w')
        self.plot_list_delete_button.grid(row=3, column=3, sticky='w')
        self.plot_list_up_button.grid(row=4, column=1, sticky='w')
        self.plot_list_down_button.grid(row=4, column=2, sticky='w')

        # Source File
        self.source_file_label = ttk.Label(
            self,
            text="Soruce File"
        )
        self.source_file_text = tk.Text(
            self,
            width=20,
            height=1
        )
        self.source_browse_button = ttk.Button(
            self,
            text="Browse...",
            width=9
        )

        self.source_file_label.grid(row=5, column=0, sticky='w')
        self.source_file_text.grid(row=5, column=1, columnspan=3, sticky='w')
        self.source_browse_button.grid(row=5, column=3, sticky='w')
        self.source_file_text['state'] = 'disabled'

        # Diameter Range and Binning
        diam_range = tk.StringVar()
        selected_binning = tk.StringVar()

        self.diam_range_label = ttk.Label(
            self,
            text="Diameter range:"
        )
        self.diam_range_entry = ttk.Entry(
            self,
            textvariable=diam_range,
            width=7
        )
        self.binning_label = ttk.Label(
            self,
            text="Binning"
        )
        self.binning_dropdown = ttk.Combobox(
            self,
            textvariable=selected_binning,
            width=10
        )

        self.diam_range_label.grid(row=6, column=0, sticky='w')
        self.diam_range_entry.grid(row=6, column=1, sticky='w')
        self.binning_label.grid(row=6, column=2, sticky='w')
        self.binning_dropdown.grid(row=6, column=3, sticky='w')
