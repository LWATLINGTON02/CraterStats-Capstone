import tkinter as tk
import craterstats
import time
import os

class TkTemplate(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for Frames in (GetStartedPage, FormatPage, StatsPage):
            frame = Frames(container, self)
            self.frames[Frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GetStartedPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GetStartedPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#1F1F1E")
        self.controller = controller

        # Create and format the welcome label
        welcome_label = tk.Label(self, text="Welcome to CraterStats",
                                 font=("Nunito", 18),
                                 fg="#FFFFFF",
                                 bg="#1F1F1F")
        welcome_label.pack(pady=(10, 5))

        # Create and format the "Crater Graph Statistics Settings" label
        graph_stats_label = tk.Label(self,
                               text="Crater Graph Statistics Settings",
                                  font=("Nunito", 16),
                                  fg="#FFFFFF",
                                  bg="#1F1F1F")
        graph_stats_label.pack(anchor=tk.W, pady=(10, 0), padx=179)

        # Create the stats button and redirect to the graph statistics
        # settings page
        stats_button = tk.Button(self, width=20,
                                  text="Stats",
                                  font=("Nunito", 16),
                                  bg="#FFFFFF",
                                  fg="#1F1F1F",
                                  command=lambda: controller.
                                  show_frame(StatsPage))
        stats_button.pack(pady=(0, 10))

        # Create and format the "Graph Format Settings" label
        graph_format_label = tk.Label(self, text="Graph Format Settings",
                                       font=("Nunito", 16),
                                       fg="#FFFFFF",
                                       bg="#1F1F1F")
        graph_format_label.pack(anchor=tk.W, pady=(10, 0), padx=179)

        # Create the format button and redirect to the format page
        format_button = tk.Button(self, width=20,
                                 text="Format",
                                 font=("Nunito", 16),
                                 bg="#FFFFFF",
                                 fg="#1F1F1F",
                                 command=lambda: controller.
                                 show_frame(FormatPage))
        format_button.pack(pady=(0, 10))


class FormatPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#1F1F1F")
        self.controller = controller


class StatsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#1F1F1F")
        self.controller = controller

        PLOTS = [
                 (" cumulative ", "cumulativeCmd"),
                 ("differential", "differentialCmd"),
                 ("relative (R)", "relativeCmd"),
                 ("  Hartmann  ", "HartmannCmd"),
                 (" chronology ", "chronologyCmd")
                ]
        
        plotType = tk.StringVar()
        chronoVar = tk.StringVar()
        # set the chronoVar default variable
        chronoVar.set("Default")
        showTitle = tk.IntVar()

        # Create and format the crater_stats_label label
        crater_stats_label = tk.Label(self, text="Input Crater Stats",
                                      font=("Nunito", 18),
                                      fg="#FFFFFF",
                                      bg="#1F1F1F")
        crater_stats_label.pack(pady=(10, 5))

        # Create and format the plot_type_label
        plot_type_label = tk.Label(self, text="Plot Type:",
                                   font=("Nunito", 16),
                                   fg="#FFFFFF",
                                   bg="#1F1F1F")
        plot_type_label.pack(anchor=tk.W, pady=(10, 0), padx=191)

        # Loop to create and format the plot type radio buttons
        for text, cmd in PLOTS:
            tk.Radiobutton(self, text=text, variable=plotType,
                           value=cmd).pack()

        # Create and format the chronology_function_label
        chronology_function_label = tk.Label(self, text="Chronology Function:",
                                             font=("Nunito", 16),
                                             fg="#FFFFFF",
                                             bg="#1F1F1F")
        chronology_function_label.pack(pady=(10, 0))
        
        # Create and format the chornology function dropdown menu
        chronoDrop = tk.OptionMenu(self, chronoVar,
                                   "chrono1",
                                   "chrono2",
                                   "chrono3").pack()
        
        # Create and format the graph_title_label
        graph_title_label = tk.Label(self, text="Graph Title:",
                                     font=("Nunito", 16),
                                     fg="#FFFFFF",
                                     bg="#1F1F1F")
        graph_title_label.pack(pady=(10, 0))
        
        # Create and format the title display checkbox
        titleCheck = tk.Checkbutton(self, text="Display Title",
                                    variable=showTitle).pack()



app = TkTemplate()
app.title("TkTemplate")
app.geometry("600x800")
app.configure
app.mainloop()
