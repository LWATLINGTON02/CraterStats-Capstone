import tkinter as tk
from tkinter import ttk


class Stats(ttk.Frame):
    def __init__(self,  parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)  # Row 0 will take any extra space
        self.grid_rowconfigure(1, weight=0)  # Row 1 will take minimum space
        self.grid_columnconfigure(1, weight=0)  # Set weight of column=1 to 0

        plot_types = ttk.Frame(self)
        plot_types.grid(row=0, column=0, sticky='nw')

        func_drop_down = ttk.Frame(self)
        func_drop_down.grid(row=1, column=0, sticky='nw')

        axes_boxes = ttk.Frame(self)
        axes_boxes.grid(row=0, column=1, rowspan=2, sticky='ne')

        iso_text = ttk.Frame(self)
        iso_text.grid(row=2, column=0, sticky='sw')

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.plot_type = tk.StringVar(value='1')

        self.controller = controller
        self.cumulativeR = ttk.Radiobutton(
            plot_types,
            text='cumulative',
            variable=self.plot_type,
            value='cum')
        self.differentialR = ttk.Radiobutton(
            plot_types,
            text='differential',
            variable=self.plot_type,
            value='dif')
        self.relativeR = ttk.Radiobutton(
            plot_types,
            text='relative (R)',
            variable=self.plot_type,
            value='rel')
        self.hartmannR = ttk.Radiobutton(
            plot_types,
            text='Hartmann',
            variable=self.plot_type,
            value='har')
        self.chronologyR = ttk.Radiobutton(
            plot_types,
            text='chronology',
            variable=self.plot_type,
            value='chr')

        self.cumulativeR.grid(row=0, column=0, sticky='w')
        self.differentialR.grid(row=0, column=1, sticky='w')
        self.relativeR.grid(row=0, column=2, sticky='w')
        self.hartmannR.grid(row=0, column=3, sticky='w')
        self.chronologyR.grid(row=0, column=4, sticky='w')

        selected_chron_func = tk.StringVar()

        self.chron_func = ttk.Combobox(
            func_drop_down,
            textvariable=selected_chron_func,
            width=50)
        self.chron_func_label = ttk.Label(
            func_drop_down,
            text='Chronology Function')

        self.chron_func['values'] = ('func1', 'func2', 'func3')
        self.chron_func['state'] = 'readonly'
        self.chron_func.grid(row=2, column=0, sticky='w', padx=5)
        self.chron_func_label.grid(row=2, column=1, sticky='ew', padx=5)

        selected_prod_func = tk.StringVar()

        self.prod_func = ttk.Combobox(
            func_drop_down,
            textvariable=selected_chron_func,
            width=50)
        self.prod_func_label = ttk.Label(
            func_drop_down,
            text='Production Function')

        self.prod_func['values'] = ('func1', 'func2', 'func3')
        self.prod_func['state'] = 'readonly'
        self.prod_func.grid(row=3, column=0, sticky='w', padx=5)
        self.prod_func_label.grid(row=3, column=1, sticky='ew', padx=5)

        selected_equil_func = tk.StringVar()

        self.equil_func = ttk.Combobox(
            func_drop_down,
            textvariable=selected_equil_func,
            width=50
        )
        self.equil_func_label = ttk.Label(
            func_drop_down,
            text='Equilibrium Function'
        )

        self.equil_func['values'] = ('func1', 'func2', 'func3')
        self.equil_func['state'] = 'readonly'
        self.equil_func.grid(row=4, column=0, sticky='w', padx=5)
        self.equil_func_label.grid(row=4, column=1, sticky='ew', padx=5)

        # Data Legend Area

        self.data_check_box_var = tk.IntVar(value=0)
        self.fit_check_box_var = tk.IntVar(value=0)
        self.func_check_box_var = tk.IntVar(value=0)
        self.picto_check_box_var = tk.IntVar(value=0)
        self.rand_check_box_var = tk.IntVar(value=0)

        self.display_data_legend_data = ttk.Checkbutton(
            axes_boxes,
            text='Data',
            variable=self.data_check_box_var)
        self.display_data_legend_fit = ttk.Checkbutton(
            axes_boxes,
            text='Fit',
            variable=self.fit_check_box_var)
        self.display_data_legend_funcs = ttk.Checkbutton(
            axes_boxes,
            text='Functions',
            variable=self.func_check_box_var)
        self.display_data_legend_picto = ttk.Checkbutton(
            axes_boxes,
            text='Pictogram',
            variable=self.picto_check_box_var)
        self.display_data_legend_rand = ttk.Checkbutton(
            axes_boxes,
            text='Randomness',
            variable=self.rand_check_box_var)

        self.display_data_legend_data.grid(row=2, column=2, sticky='nw')
        self.display_data_legend_fit.grid(row=3, column=2, sticky='nw')
        self.display_data_legend_funcs.grid(row=4, column=2, sticky='nw')
        self.display_data_legend_picto.grid(row=5, column=2, sticky='nw')
        self.display_data_legend_rand.grid(row=6, column=2, sticky='nw')

        self.display_data_legend_data['state'] = 'normal'
        self.display_data_legend_fit['state'] = 'normal'
        self.display_data_legend_funcs['state'] = 'normal'
        self.display_data_legend_picto['state'] = 'normal'
        self.display_data_legend_rand['state'] = 'noraml'

        # Isochron Area
        iso_var = tk.StringVar()

        self.iso_entry_box = ttk.Entry(
            iso_text,
            width=10,
            textvariable=iso_var)

        self.iso_label = ttk.Label(
            iso_text,
            text='Isochrons, Ga'
        )

        self.iso_entry_box.grid(row=0, column=0, sticky='w')
        self.iso_label.grid(row=0, column=1, sticky='w')

        # Axes
        log_d_var = tk.StringVar()
        log_y_var = tk.StringVar()

        self.axes_label_start = ttk.Label(
            iso_text,
            text='Axes, log D:'
        )
        self.axes_label_log_y = ttk.Label(
            iso_text,
            text=' log y:'
        )
        self.log_d_entry = ttk.Entry(
            iso_text,
            width=10,
            textvariable=log_d_var
        )
        self.log_y_entry = ttk.Entry(
            iso_text,
            width=10,
            textvariable=log_y_var
        )
        self.auto_button = ttk.Button(
            iso_text,
            text='Auto',
            width=10
        )

        self.axes_label_start.grid(row=1, column=0, sticky='sw')
        self.log_d_entry.grid(row=1, column=1, sticky='sw')
        self.axes_label_log_y.grid(row=1, column=2, sticky='sw')
        self.log_y_entry.grid(row=1, column=3, sticky='sw')
        self.auto_button.grid(row=1, column=4, sticky='sw')

        # Style Buttons
        self.style_choice = tk.StringVar()

        self.style_label = ttk.Label(
            iso_text,
            text="Style:"
        )
        self.decadel_button = ttk.Radiobutton(
            iso_text,
            text='decadel',
            variable=self.style_choice,
            value='decadel'
        )
        self.root_2_button = ttk.Radiobutton(
            iso_text,
            text='root-2',
            variable=self.style_choice,
            value='root-2'
        )

        self.style_label.grid(row=2, column=0, sticky='sw')
        self.decadel_button.grid(row=2, column=1, sticky='sw')
        self.root_2_button.grid(row=2, column=2, sticky='sw')
