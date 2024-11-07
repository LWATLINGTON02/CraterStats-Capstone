from argparse import Namespace

import concurrent.futures

import flet as ft
from craterstats import cli, Craterplot, Craterplotset, constants
from flet import FilePickerResultEvent, ControlEvent
import shutil

from Globals import *
from gm.file import file_exists, read_textstructure, read_textfile, filename
from helperFunctions import *
import Globals
import platform

import traceback

"""
IGNORE DEPRECATED WARNINGS
"""
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

# GM Folder from CraterstatsIII
# Also from craterstats
PATH = os.path.dirname(os.path.abspath(__file__))


# Custom component for plot chips
class PlotChip(ft.Chip):

    def __init__(self, label, selected, selected_color, show_checkmark, on_click):
        super().__init__(label)
        self.data = [
            {"source": ""},
            {
                "name": "",
                "range": [0, 100],
                "type": "data",
                "error_bars": 1,
                "hide": 0,
                "colour": 0,
                "psym": "1",
                "binning": "pseudo-log",
                "age_left": 0,
                "display_age": 1,
                "resurf": 0,
                "resurf_showall": 0,
                "offset_age": [0, 0],
            },
        ]
        self.label = label
        self.selected = selected
        self.selected_colour = selected_color
        self.show_checkmark = show_checkmark
        self.on_click = on_click


"""Main Function - EVERYTHING FLET IS INSIDE THIS FUNCTION"""


def main(page: ft.Page):

    def close_app():
        page.update()
        delete_temp_plots(PATH + "/assets/plots/", ["png", "jpg", "pdf", "svg", "tif"])
        delete_temp_plots(PATH + "/../demo/", None)
        page.window.destroy()

    def handle_window_event(e):
        if e.data == "close":
            close_app()

    def change_subplot_name(e):
        selected_chip = next(
            (chip for chip in plot_lists.controls if chip.selected), None
        )

        if selected_chip:
            selected_chip.label = ft.Text(e.control.value)
            selected_chip.data[0]["name"] = e.control.value
            update_config_dict()
            page.update()

    def chip_on_click(e):

        if len(plot_lists.controls) > 1:
            for chip in plot_lists.controls:
                if chip.selected:
                    chip.selected = False
            e.control.selected = True

        set_plot_info(e)

        page.update()

    def create_plot_lists():
        """Creates a dictionary of plots.

        A global dictionary of plots is filled out based off of the information
        in the file that is uploaded to make different subplots

        Args:
            none

        Returns:
            none
        """
        content_list = []

        plot_name = ""

        if Globals.template_dict:

            try:
                plot_name = Globals.template_dict["plot"][1]["name"]
            except IndexError:
                plot_name = "Default"

            content_list.append(
                PlotChip(
                    label=ft.Text(plot_name),
                    selected=True,
                    selected_color=ft.colors.BLUE,
                    show_checkmark=True,
                    on_click=lambda e: (chip_on_click(e), update_config_dict()),
                )
            )

        plot_lists.controls = content_list

        page.update()

    def demo_view(demo_dict):
        carousel_images = list(demo_dict.keys())
        setattr(
            Globals, "demo_cmd_str", demo_dict[carousel_images[Globals.image_index]]
        )

        def update_image():
            # Update the image based on the current index
            setattr(
                Globals, "demo_cmd_str", demo_dict[carousel_images[Globals.image_index]]
            )
            cmd_str.value = Globals.demo_cmd_str
            demo_image.src = f"{PATH}/../demo/{carousel_images[Globals.image_index]}"
            plot_num.value = f"Plot {Globals.image_index + 1} of {len(carousel_images)}"
            plot_num.update()
            demo_image.update()
            page.update()

        # Function to go to the next image
        def next_image(e):
            setattr(Globals, "image_index", Globals.image_index + 1)
            if Globals.image_index >= 24:
                # Loop back to the first image
                setattr(Globals, "image_index", 0)
            update_image()

        # Function to go to the previous image
        def prev_image(e):
            setattr(Globals, "image_index", Globals.image_index - 1)
            if Globals.image_index < 0:
                # Loop back to the last image
                setattr(Globals, "image_index", len(carousel_images) - 1)
            update_image()

        demo_image = ft.Image(
            src=f"{PATH}/../demo/{carousel_images[Globals.image_index]}",
            width=600,
            height=600,
        )

        cmd_str = ft.TextField(
            value=Globals.demo_cmd_str,
            text_size=12,
            bgcolor=ft.colors.BLACK,
            color=ft.colors.WHITE,
            text_style=ft.TextStyle(font_family="Courier New"),
            width=1500,
            max_lines=10,
        )

        plot_num = ft.Text(
            f"Plot {Globals.image_index + 1} of {len(carousel_images)}",
            text_align=ft.TextAlign.CENTER,
        )

        demo_modal = ft.AlertDialog(
            title=ft.Text("Demo Plots"),
            content=ft.Column(
                controls=[plot_num, demo_image, ft.VerticalDivider(), cmd_str]
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[
                ft.ElevatedButton(text="Prev", on_click=lambda e: prev_image(e)),
                ft.ElevatedButton(text="Next", on_click=lambda e: next_image(e)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = demo_modal
        demo_modal.open = True
        page.update()

        return demo_view

    def dev_notes():
        """Displays developer notes.

        Developer notes are displayed in an alert dialog when the application is started
        Things shown are known issues and future features

        Args:
            none

        Returns:
            none
        """
        show_popup = page.client_storage.get("show_notes")

        notes = ft.AlertDialog(
            title=ft.Text("Welcome to Craterstats IV"),
            content=ft.Column(
                controls=[
                    ft.Text(
                        "This is an alpha version of the Craterstats IV GUI. Known issues and future features are listed below:"
                    ),
                    ft.Text("Known Issues:"),
                    ft.Text(
                        "1. After data is uploaded, rate and chronology plot presentation settings are not functioning."
                    ),
                    ft.Text(
                        "2. Currently a .plt file needs to be uploaded for the GUI to function."
                    ),
                    ft.Text(
                        "3. The color and symbol options aren't correctly linked to the right options (e.g. Point options shows cross symbol)."
                    ),
                    ft.Text("4. The GUI is not fully functional and may have bugs."),
                    ft.Text("Future Features:"),
                    ft.Text("1. Add the ability to create multiple subplots."),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Checkbox(
                                    label="Don't show this message again",
                                    on_change=lambda e: page.client_storage.set(
                                        "show_notes", False
                                    ),
                                ),
                                ft.FilledButton(
                                    text="Start Graphing!",
                                    on_click=lambda e: page.close(notes),
                                ),
                            ]
                        ),
                        alignment=ft.alignment.center,  # Center the button
                        padding=10,  # Add some padding if needed
                    ),
                ]
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
        )
        if show_popup:
            page.dialog = notes
            notes.open = True
            page.update()

    def error_view(error_message):
        """Displays pop up at bottom of screen when error occurs

        A Flet bottom sheet is displayed when an error occurs on the application
        when an option is changed

        Args:
            none

        Returns:
            none
        """
        error_sheet = ft.BottomSheet(
            bgcolor=ft.colors.RED,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Text(error_message, expand=1),
                                ft.IconButton(
                                    icon=ft.icons.CLOSE,
                                    on_click=lambda e: page.close(error_sheet),
                                ),
                            ],
                            alignment="spaceBetween",  # Align the message and close button
                        ),
                    ],
                    tight=True,
                ),
                padding=10,
            ),
        )

        page.dialog = error_sheet
        error_sheet.open = True
        page.update()

    def data_file_picker_result(e: FilePickerResultEvent):
        source_file = e.files[0]
        if source_file.path.endswith(".scc") or source_file.path.endswith(".diam"):
            if platform.system() == "Windows":
                source_file_entry.value = source_file.path[2:]
            else:
                source_file_entry.value = source_file.path
            update_config_dict()
        else:
            pass  # error dialouge here

    def file_picker_result(e: FilePickerResultEvent):
        """Fills out data based off of file.

        Data in application is filled out based off of the file that is selected.
        Data that is filled out is dependent on the file.

        File types allowed: .plt

        Args:
            e: FilePickerResultEvent

        Returns:
            none
        """

        selected_chip = next(
            (chip for chip in plot_lists.controls if chip.selected), None
        )

        if e.files[0].path.endswith(".plt") and len(e.files) >= 1:
            # Reads through each line of data and sets data based off of line
            config = {}
            current_dict_name = None
            current_item_list = None

            with open(e.files[0].path, "r") as file:
                config = {}
                current_dict_name = None
                current_item_dict = None  # Dictionary for 'set' or other sections

                for line in file:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Detect start of a new section
                    if line.endswith("{"):  # Start of a new block (e.g., set = {)
                        current_dict_name = line.split("=")[0].strip()

                        if current_dict_name == "plot":
                            # Create a list for plot items
                            config[current_dict_name] = []
                            current_item_list = config[current_dict_name]
                        else:
                            # For other sections (including 'set'), initialize as a dictionary
                            config[current_dict_name] = {}
                            current_item_dict = config[current_dict_name]

                    elif "=" in line:  # Key-value pair inside the block
                        key, value = line.split("=", 1)
                        key = key.strip()
                        value = value.strip()

                        # Handle lists in the form [value1, value2]
                        if value.startswith("[") and value.endswith("]"):
                            value = value[1:-1].split(",")
                            value = [v.strip().strip("'") for v in value]

                        # Handle strings enclosed in single quotes
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # For 'plot', append the dictionary to the list
                        if current_dict_name == "plot":
                            if key == "source":
                                current_item_list.append({key: value})
                            else:
                                if current_item_list and isinstance(
                                    current_item_list[-1], dict
                                ):
                                    last_item = current_item_list[-1]
                                    if len(last_item) == 1 and "source" in last_item:
                                        current_item_list.append({key: value})
                                    else:
                                        last_item[key] = value
                                else:
                                    current_item_list.append({key: value})
                        else:
                            # For 'set' or other sections, update the dictionary directly
                            current_item_dict[key] = value

                    elif line == "}":  # End of the block
                        current_dict_name = None
                        current_item_dict = None

            """
            TODO HERE: ADD CITE_FUNCTIONS, INVERT, LEGEND, SHOW_LEGEND_AREA TO SET SETTINGS
                       ADD RESURF, resurf_showall, ISOCHRON, OFFSET_AGE TO PLOT SETTINGS
            """

            if "chronology_system" in config["set"]:
                body.value = get_body(config["set"]["chronology_system"])
                set_chron_sys(body.value, None)
                chron_sys.value = config["set"]["chronology_system"]
            if "cite_functions" in config["set"]:
                cite_func.value = (
                    True if config["set"]["cite_functions"] == "1" else False
                )
            if "epochs" in config["set"]:
                epoch.value = (
                    config["set"]["epochs"] if config["set"]["epochs"] != "" else "none"
                )
            if "equilibrium" in config["set"]:
                equil_func.value = (
                    config["set"]["equilibrium"]
                    if config["set"]["equilibrium"] != ""
                    else "none"
                )
            if "isochrons" in config["set"]:
                iso_text.value = config["set"]["isochrons"]
            if "mu" in config["set"]:
                mu_legend.value = config["set"]["mu"]
            if "presentation" in config["set"]:
                plot_view.value = config["set"]["presentation"]
            if "print_dimensions" in config["set"]:

                if type(config["set"]["print_dimensions"]) == list:
                    config["set"]["print_dimensions"] = "x".join(
                        config["set"]["print_dimensions"]
                    )

                print_scale_entry.value = config["set"]["print_dimensions"]
            if "pt_size" in config["set"]:
                if type(config["set"]["pt_size"]) == list:
                    text_size.value = max(config["set"]["pt_size"])
                else:
                    text_size.value = config["set"]["pt_size"]
            if "randomness" in config["set"]:
                rand_legend.value = config["set"]["randomness"]
            if "ref_diameter" in config["set"]:
                ref_diam.value = config["set"]["ref_diameter"]
            if "sig_figs" in config["set"]:
                sf_entry.value = config["set"]["sig_figs"]
            if "show_isochrons" in config["set"]:
                show_iso.value = (
                    True if config["set"]["show_isochrons"] == "1" else False
                )
            if "show_subtitle" in config["set"]:
                subtitle_checkbox.value = (
                    True if config["set"]["show_subtitle"] == "1" else False
                )
            if "show_title" in config["set"]:
                title_checkbox.value = (
                    True if config["set"]["show_title"] == "1" else False
                )
            if "style" in config["set"]:
                style_options.value = config["set"]["style"]
            if "subtitle" in config["set"]:
                subtitle_entry.value = (
                    config["set"]["subtitle"]
                    if config["set"]["subtitle"] != ""
                    else None
                )
            if "title" in config["set"]:
                title_entry.value = (
                    config["set"]["title"] if config["set"]["title"] != "" else None
                )
            if "invert" in config["set"]:
                invert.value = True if config["set"]["invert"] == "1" else False
            if "show_legned_area" in config["set"]:
                legend_name.value = (
                    True if config["set"]["show_legend_area"] == "1" else False
                )
            if "xrange" in config["set"]:
                x_range.value = (
                    (config["set"]["xrange"][0]) + ", " + (config["set"]["xrange"][1])
                )
            if "yrange" in config["set"]:
                y_range.value = (
                    (config["set"]["yrange"][0]) + ", " + (config["set"]["yrange"][1])
                )

            # Plot settings
            for index, dictionary in enumerate(config["plot"]):

                if list(config["plot"][index].values())[0] == "":
                    key = list(config["plot"][index].keys())[0]
                    if key == "source":
                        continue
                    config["plot"][index][key] = None

                if "source" in dictionary and config["plot"][index]["source"] != "":
                    source_file_entry.value = config["plot"][index]["source"]

                if "name" in dictionary:
                    if config["plot"][index]["name"] == None:
                        config["plot"][index]["name"] = "Default"

                    plot_fit_text.value = config["plot"][index]["name"]
                if "range" in dictionary:
                    diam_range_entry.value = (
                        (config["plot"][index]["range"][0])
                        + ", "
                        + (config["plot"][index]["range"][1])
                    )
                if "type" in dictionary:
                    plot_fit_options.value = config["plot"][index]["type"]
                if "error_bars" in dictionary:
                    error_bars.value = (
                        True if config["plot"][index]["error_bars"] == "1" else False
                    )
                if "hide" in dictionary:
                    hide_button.value = (
                        True if config["plot"][index]["hide"] == "1" else False
                    )
                if "colour" in dictionary:
                    color_dropdown.value = Globals.colours[
                        int(config["plot"][index]["colour"])
                    ]
                if "psym" in dictionary:
                    symbol_dropdown.value = Globals.symbols[
                        int(config["plot"][index]["psym"])
                    ]
                if "binning" in dictionary:
                    binning_options.value = config["plot"][index]["binning"]
                if "age_left" in dictionary:
                    align_left.value = (
                        True if config["plot"][index]["age_left"] == "1" else False
                    )
                if "display_age" in dictionary:
                    display_age.value = (
                        True if config["plot"][index]["display_age"] == "1" else False
                    )
                if "resurf" in dictionary:
                    resurf.value = (
                        True if config["plot"][index]["resurf"] == "1" else False
                    )
                if "resurf_showall" in dictionary:
                    resurf_showall.value = (
                        True
                        if config["plot"][index]["resurf_showall"] == "1"
                        else False
                    )
                if "offset_age" in dictionary:
                    offset_age.value = (
                        config["plot"][index]["offset_age"][0]
                        + ", "
                        + config["plot"][index]["offset_age"][1]
                    )

            selected_chip.data = config["plot"]
            Globals.template_dict["set"] = config["set"]
            Globals.template_dict["plot"] = selected_chip.data

        update_legend()
        create_plot_lists()
        run_plot_async()

        page.update()

    def filter_crater_plot(crater_plot):
        seen = set()
        unique_crater_plot = []

        for plot in crater_plot:

            identifier = plot["source"]

            if identifier not in seen:
                seen.add(identifier)
                unique_crater_plot.append(plot)

        return unique_crater_plot

    def get_body(chron_sys):

        body_val = ""

        chron_sys_body = str(chron_sys).split(",")[0].replace("[", "")

        if chron_sys_body == "Mars":

            body_val = "Mars"

        elif chron_sys_body == "Moon":

            body_val = "Moon"

        elif chron_sys_body == "Mercury":

            body_val = "Mercury"

        elif chron_sys_body == "Vesta":

            body_val = "Vesta"

        elif chron_sys_body == "Ceres":

            body_val = "Ceres"

        elif chron_sys_body == "Ida":

            body_val = "Ida"

        elif chron_sys_body == "Gaspra":

            body_val = "Gaspra"

        elif chron_sys_body == "Lutetia":

            body_val = "Lutetia"

        elif chron_sys_body == "Phobos":

            body_val = "Phobos"

        return body_val

    def get_legend_value():

        value = ""

        if legend_name.value:

            value += "n"
        if legend_area.value:

            value += "a"
        if legend_perimeter.value:

            value += "p"
        if legend_cratercount.value:

            value += "c"
        if legend_range.value:

            value += "r"
        if legend_n_dref.value:

            value += "N"

        return value

    def handle_keypress_events(e: ft.KeyboardEvent):
        if e.key == "O" and (e.ctrl or e.meta):
            pick_files_dialog.pick_files()

        if e.key == "E" and (e.ctrl or e.meta):
            save_file_dialog.save_file()

    def loading_circle(text_to_display):

        loading = ft.AlertDialog(
            title=ft.Text(text_to_display),
            content=ft.ProgressRing(stroke_cap=ft.StrokeCap.BUTT, stroke_width=5),
        )

        page.dialog = loading
        loading.open = True
        page.update()

        return loading

    def new_subplot():
        """Creates new subplots.

        Create new subplots on button press to allow for more customization of the plots


        Args:
            none

        Returns:
            none
        """

        subplot = [
            {"source": ""},
            {
                "name": "",
                "range": [0, 100],
                "type": "data",
                "error_bars": 1,
                "hide": 0,
                "colour": 0,
                "psym": "1",
                "binning": "pseudo-log",
                "age_left": 0,
                "display_age": 1,
                "resurf": 0,
                "resurf_showall": 0,
                "offset_age": [0, 0],
            },
        ]

        Globals.template_dict["plot"].append(subplot[0])
        Globals.template_dict["plot"].append(subplot[1])

        newChip = PlotChip(
            label=ft.Text("Default"),
            selected=False,
            selected_color=ft.colors.BLUE,
            show_checkmark=True,
            on_click=lambda e: (chip_on_click(e), update_config_dict()),
        )
        plot_lists.controls.append(newChip)

        page.update()

    def on_resize(e):
        # Trigger UI update when window is resized
        page.update()

    def open_about_dialog(e):
        """Opens and fills about text.

        Opens about popup in application and fills out about section with the
        information about craterstats taken from CraterstatsIII with additions
        to include the Lunar Pit Patrol Team and contribution

        Args:
            none

        Returns:
            none
        """

        dlg = ft.AlertDialog(
            title=ft.Text("CraterstatsIV"),
            content=ft.Text(
                "\n".join(
                    [
                        "GUI Developed by The Lunar Pit Patrol, Senior Capstone group for NAU",
                        "Lunar Pit Patrol Team:",
                        "Evan Palmisano",
                        "Ibrahim Hmood",
                        "Alden Smith",
                        "Caden Tedeschi",
                        "Levi Watlington\n",
                        "Craterstats Program developed by Greg Michael",
                        "Version: 0.2",
                        "",
                        "Explanations of concepts and calculations used in the software are given in publications below:",
                        "",
                        "Standardisation of crater count data presentation",
                        "Arvidson R.E., Boyce J., Chapman C., Cintala M., Fulchignoni M., Moore H., Neukum G., Schultz P., Soderblom L., Strom R., Woronow A., Young R. "
                        "Standard techniques for presentation and analysis of crater size–frequency data. Icarus 37, 1979.",
                        "",
                        "Formulation of a planetary surface chronology model",
                        "Neukum G., Meteorite bombardment and dating of planetary surfaces (English translation, 1984). Meteoritenbombardement und Datierung planetarer Oberflächen (German original, 1983).",
                        "",
                        "Resurfacing correction for cumulative fits; production function differential forms",
                        "Michael G.G., Neukum G., Planetary surface dating from crater size-frequency distribution measurements: Partial resurfacing events and statistical age uncertainty. EPSL 294, 2010.",
                        "",
                        "Differential fitting; binning bias correction; revised Mars epoch boundaries",
                        "Michael G.G., Planetary surface dating from crater size-frequency distribution measurements: Multiple resurfacing episodes and differential isochron fitting. Icarus, 2013.",
                        "",
                        "Poisson timing analysis; mu-notation",
                        "Michael G.G., Kneissl T., Neesemann A., Planetary surface dating from crater size-frequency distribution measurements: Poisson timing analysis. Icarus, 2016.",
                        "",
                        "Poisson calculation for buffered crater count",
                        "Michael G.G., Yue Z., Gou S., Di K., Dating individual several-km lunar impact craters from the rim annulus in "
                        "region of planned Chang’E-5 landing Poisson age-likelihood calculation for a buffered crater counting area. EPSL 568, 2021.",
                        "",
                        "Full references for specific chronology or other functions are listed with the function definitions in `config/functions.txt`.",
                        "",
                    ]
                )
            ),
            shape=ft.BeveledRectangleBorder(radius=5),
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Function to update the displayed image
    def print_plot():
        """Creates plot images.

        Craterstats plots are created either by using the functions that are selected in the GUI or by uploading
        a .plt file. This function is mostly pulled from the craterstats cli.py main function with some modifications
        to fit our GUI.

        Args:
            none

        Returns:
            none
        """

        template = PATH + "/assets/config files/default.plt"
        functions = PATH + "/assets/config files/functions.txt"
        functions_user = PATH + "/assets/config files/functions_user.txt"

        selected_chip = next(
            (chip for chip in plot_lists.controls if chip.selected), None
        )

        arg = Namespace(
            about=False,
            autoscale=axis_auto_button.value,
            chronology_system=set_chron_str()[-2:].replace(" ", ""),
            cite_function=cite_func.value,
            demo=Globals.demo_mode,
            epochs=epoch.value if epoch.value != "none" else None,
            equilibrium=equil_func.value if equil_func.value != "none" else None,
            format=None,
            input=None,
            invert=invert.value,
            isochrons=iso_text.value,
            lcs=False,
            legend=get_legend_value(),
            lpc=False,
            mu=mu_legend.value,
            out="",
            plot=Globals.template_dict["plot"],
            presentation=plot_view.value,
            print_dim=print_scale_entry.value,
            pt_size=text_size.value if text_size.value != "" else "8",
            ref_diameter=ref_diam.value,
            show_isochrons=show_iso.value,
            sig_figs="3",
            src=None,
            style=style_options.value,
            subtitle=subtitle_entry.value if subtitle_checkbox.value else None,
            template=Globals.template_dict if Globals.template_dict else None,
            title=title_entry.value if title_checkbox.value else None,
            transparent=False,
            xrange=[
                float(num)
                for num in x_range.value.replace(" ", "").strip("[]").split(",")
            ],
            yrange=[
                float(num)
                for num in y_range.value.replace(" ", "").strip("[]").split(",")
            ],
        )

        if arg.demo:
            toggle_demo(None)
            return

        if type(arg.template) == str:
            settings = read_textstructure(
                template if arg.template is None else arg.template
            )

        else:
            settings = arg.template

            if isinstance(settings["plot"], list) and settings["plot"]:
                plot_data = {}
                for item in settings["plot"]:
                    if isinstance(item, dict):
                        plot_data.update(item)

        if settings["set"]["epochs"] == "none":
            settings["set"]["epochs"] = ""
        if settings["set"]["equilibrium"] == "none":
            settings["set"]["equilibrium"] = ""

        systems = read_textfile(functions, ignore_hash=True, strip=";", as_string=True)
        if file_exists(functions_user):
            systems += read_textfile(
                functions_user, ignore_hash=True, strip=";", as_string=True
            )

        functionStr = read_textstructure(systems, from_string=True)

        try:
            if arg.plot[0]["source"] == "" or (
                arg.presentation == "chronology" or arg.presentation == "rate"
            ):
                arg.plot = None
            craterPlot = cli.construct_plot_dicts(arg, {"plot": plot_data})
            craterPlot = filter_crater_plot(craterPlot)
            defaultFilename = generate_output_file_name()
            craterPlotSet = cli.construct_cps_dict(
                arg, settings, functionStr, defaultFilename
            )

            if "a" in craterPlotSet["legend"] and "b-poisson" in [
                d["type"] for d in craterPlot
            ]:
                craterPlotSet["legend"] += "p"

            plot = [Craterplot(d) for d in craterPlot]

            plotSettings = Craterplotset(craterPlotSet, craterPlot=plot)

            plotSettings.craterplot = plot

            if plot and arg.autoscale:
                x_range.value = ", ".join(map(str, plotSettings.xrange))
                y_range.value = ", ".join(map(str, plotSettings.yrange))
                try:
                    plotSettings.autoscale()
                except BaseException:
                    error_view("No data within range selected")

            newFileName = generate_output_file_name()

            craterPlotSet["out"] = PATH + "/assets/plots/" + newFileName

            if Globals.SUMMARY:
                plotSettings.format = {"txt"}

            drawn = False
            for format in plotSettings.format:
                if format in {"png", "jpg", "pdf", "svg", "tif"}:
                    if not drawn:
                        plotSettings.draw()
                        drawn = True
                    plotSettings.fig.savefig(
                        craterPlotSet["out"], dpi=500, transparent=arg.transparent
                    )
                    plot_image.src = craterPlotSet["out"] + ".png"
                    plot_image.update()
                if format in {"txt"}:
                    try:
                        plotSettings.create_summary_table()
                        setattr(Globals, "SUMMARY", False)
                    except UnboundLocalError:
                        setattr(Globals, "SUMMARY", False)
                        error_view(
                            "Please select one of the following types: 'c-fit', 'd-fit', 'poisson', 'b-poisson'"
                        )

            set_cmd_line_str()
            page.update()

        except BaseException as err:
            error_view(err)
            traceback.print_exc()

    def run_plot_async():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(print_plot)

            try:
                result = future.result()
            except BaseException as e:
                error_view(e)
                traceback.print_exc()

    def save_image(e):

        if save_file_dialog.result and save_file_dialog.result.path:
            export_path = save_file_dialog.result.path

            if not export_path.lower().endswith(".png"):
                export_path += ".png"

            shutil.copy(plot_image.src, export_path)
            page.update()

    def save_plot_file(e):

        if save_plot_dialog.result and save_plot_dialog.result.path:
            export_path = save_plot_dialog.result.path

            if not export_path.lower().endswith(".plt"):
                export_path += ".plt"

            with open(export_path, "w") as file:
                file.write(
                    f"""set = {{
                        chronology_system={chron_sys.value}
                        cite_functions= {1 if cite_func.value else 0}
                        epochs= {epoch.value}
                        equilibrium= {equil_func.value}
                        isochrons= {iso_text.value}
                        mu= {mu_legend.value}
                        presentation= {plot_view.value}
                        print_dimensions= {print_scale_entry.value}
                        pt_size= {text_size.value}
                        randomness= {rand_legend.value}
                        ref_diameter= {1 if ref_diam.value else 0}
                        sig_figs= {sf_entry.value}
                        show_isochrons= {1 if show_iso.value else 0}
                        show_subtitle= {1 if subtitle_checkbox.value else 0}
                        show_title= {1 if title_checkbox.value else 0}
                        style= {style_options.value}
                        subtitle= {subtitle_entry.value}
                        title= {title_entry.value}
                        invert= {1 if invert.value else 0}
                        show_legend_area= {1 if legend_name.value else 0}
                        xrange= {x_range.value.replace(" ","").split(",")}
                        yrange= {y_range.value.replace(" ","").split(",")}
                        }}

                        plot = {{
                        source={source_file_entry.value},
                        name={plot_fit_text.value},
                        range={diam_range_entry.value.replace(" ","").split(",")}
                        type={plot_fit_options.value}
                        error_bars={1 if error_bars.value else 0}
                        hide={1 if hide_button.value else 0}
                        colour={colours.index(color_dropdown.value)}
                        psym={symbols.index(symbol_dropdown.value)}
                        binning={binning_options.value}
                        age_left={1 if align_left.value else 0}
                        display_age={1 if display_age.value else 0}
                        resurf={1 if resurf.value else 0}
                        resurf_showall={1 if resurf_showall.value else 0}
                        offset_age={offset_age.value.replace(" ","").split(",")}
                        }}"""
                )

    def set_chron_func(value, e):
        """Sets chronology function.

        Chronology function on the Global Settings paged is changed dependent on
        which Chronology System is selected

        Args:
            Value: None
            e: Eventhandler

        Returns:
            none
        """
        if e is None:
            check_value = value
        else:
            check_value = e.control.value

        for system in chron_systems:

            if check_value == system:
                chron_func.value = chron_systems[system][0]
                chron_func.options = [ft.dropdown.Option(chron_systems[system][0])]
                prod_func.value = chron_systems[system][1]
                prod_func.options = [ft.dropdown.Option(chron_systems[system][1])]

        page.update()

    def set_chron_sys(value, e):
        """Changes chronology system

        Chronology System on the Global Settings page is changed dependent on what
        celestial body is selected

        Args:
            Value: None
            e: Eventhandler

        Returns:
            none
        """
        if e is None:
            check_value = value
        else:
            check_value = e.control.value

        items = []
        chron_func_str = ""
        prod_func_str = ""

        if check_value == "Moon":
            items = [
                ft.dropdown.Option("Moon, Neukum (1983)"),
                ft.dropdown.Option("Moon, Neukum et al. (2001)"),
                ft.dropdown.Option("Moon, Hartmann 2010 iteration"),
                ft.dropdown.Option("Moon, Yue et al. (2022)"),
            ]
            chron_func_str = "Moon, Neukum (1983)"
            prod_func_str = "Moon, Neukum (1983)"

        elif check_value == "Mars":
            items = [
                ft.dropdown.Option("Mars, Neukum-Ivanov (2001)"),
                ft.dropdown.Option("Mars, Ivanov (2001)"),
                ft.dropdown.Option("Mars, Hartmann 2004 iteration"),
                ft.dropdown.Option("Mars, Hartmann & Daubar (2016)"),
            ]
            chron_func_str = "Mars, Hartmann & Neukum (2001)"
            prod_func_str = "Mars, Ivanov (2001)"

        elif check_value == "Mercury":
            items = [
                ft.dropdown.Option("Mercury, Strom & Neukum (1988)"),
                ft.dropdown.Option("Mercury, Neukum et al. (2001)"),
                ft.dropdown.Option("Mercury, Le Feuvre and Wieczorek 2011 non-porous"),
                ft.dropdown.Option("Mercury, Le Feuvre and Wieczorek 2011 porous"),
            ]
            chron_func_str = "Mercury, Strom & Neukum (1988)"
            prod_func_str = "Mercury, Strom & Neukum (1988)"

        elif check_value == "Vesta":
            items = [
                ft.dropdown.Option("Vesta, Rev4, Schmedemann et al (2014)"),
                ft.dropdown.Option("Vesta, Rev3, Schmedemann et al (2014)"),
                ft.dropdown.Option("Vesta, Marchi & O'Brien (2014)"),
            ]
            chron_func_str = "Vesta, Rev4, Schmedemann et al (2014)"
            prod_func_str = "Vesta, Rev4, Schmedemann et al (2014)"

        elif check_value == "Ceres":
            items = [ft.dropdown.Option("Ceres, Hiesinger et al. (2016)")]
            chron_func_str = "Ceres, Hiesinger et al. (2016)"
            prod_func_str = "Ceres, Hiesinger et al. (2016)"

        elif check_value == "Ida":
            items = [ft.dropdown.Option("Ida, Schmedemann et al (2014)")]
            chron_func_str = "Ida, Schmedemann et al (2014)"
            prod_func_str = "Ida, Schmedemann et al (2014)"

        elif check_value == "Gaspra":
            items = [ft.dropdown.Option("Gaspra, Schmedemann et al (2014)")]
            chron_func_str = "Gaspra, Schmedemann et al (2014)"
            prod_func_str = "Gaspra, Schmedemann et al (2014)"

        elif check_value == "Lutetia":
            items = [ft.dropdown.Option("Lutetia, Schmedemann et al (2014)")]
            chron_func_str = "Lutetia, Schmedemann et al (2014)"
            prod_func_str = "Lutetia, Schmedemann et al (2014)"

        elif check_value == "Phobos":
            items = [
                ft.dropdown.Option("Phobos, Case A - SOM, Schmedemann et al (2014)"),
                ft.dropdown.Option("Phobos, Case B - MBA, Schmedemann et al (2014)"),
            ]
            chron_func_str = "Phobos, Case A - SOM, Schmedemann et al (2014)"
            prod_func_str = "Phobos, Case A - SOM, Schmedemann et al (2014)"

        if not (check_value == "Moon" or check_value == "Mars"):
            epoch.options = [ft.dropdown.Option("none")]
            epoch.value = "none"
        elif check_value == "Moon":
            epoch.options = [
                ft.dropdown.Option("none"),
                ft.dropdown.Option("Moon, Wilhelms (1987)"),
            ]
            epoch.value = "none"
        elif check_value == "Mars":
            epoch.options = [
                ft.dropdown.Option("none"),
                ft.dropdown.Option("Mars, Michael (2013)"),
            ]
            epoch.value = "none"

        chron_sys.options = items
        chron_sys.value = items[0].key
        chron_func.options = [ft.dropdown.Option(chron_func_str)]
        chron_func.value = chron_func_str
        prod_func.options = [ft.dropdown.Option(prod_func_str)]
        prod_func.value = prod_func_str

        page.update()

    def set_chron_str():
        """Sets Chronolgy System command line string.

        Sets the command line string for the Chronology System that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-cs 1'
        """

        new_str = ""

        if chron_sys.value == "Moon, Neukum (1983)":
            new_str = " -cs 1"
        elif chron_sys.value == "Moon, Neukum et al. (2001)":
            new_str = " -cs 2"
        elif chron_sys.value == "Moon, Hartmann 2010 iteration":
            new_str = " -cs 3"
        elif chron_sys.value == "Moon, Yue et al. (2022)":
            new_str = " -cs 4"
        elif chron_sys.value == "Mars, Neukum-Ivanov (2001)":
            new_str = " -cs 5"
        elif chron_sys.value == "Mars, Ivanov (2001)":
            new_str = " -cs 6"
        elif chron_sys.value == "Mars, Hartmann 2004 iteration":
            new_str = " -cs 7"
        elif chron_sys.value == "Mars, Hartmann & Daubar (2016)":
            new_str = " -cs 8"
        elif chron_sys.value == "Mercury, Strom & Neukum (1988)":
            new_str = " -cs 9"
        elif chron_sys.value == "Mercury, Neukum et al. (2001)":
            new_str = " -cs 10"
        elif chron_sys.value == "Mercury, Le Feuvre and Wieczorek 2011 non-porous":
            new_str = " -cs 11"
        elif chron_sys.value == "Mercury, Le Feuvre and Wieczorek 2011 porous":
            new_str = " -cs 12"
        elif chron_sys.value == "Vesta, Rev4, Schmedemann et al (2014)":
            new_str = " -cs 13"
        elif chron_sys.value == "Vesta, Rev3, Schmedemann et al (2014)":
            new_str = " -cs 14"
        elif chron_sys.value == "Vesta, Marchi & O'Brien (2014)":
            new_str = " -cs 15"
        elif chron_sys.value == "Ceres, Hiesinger et al. (2016)":
            new_str = " -cs 16"
        elif chron_sys.value == "Ida, Schmedemann et al (2014)":
            new_str = " -cs 17"
        elif chron_sys.value == "Gaspra, Schmedemann et al (2014)":
            new_str = " -cs 18"
        elif chron_sys.value == "Lutetia, Schmedemann et al (2014)":
            new_str = " -cs 19"
        elif chron_sys.value == "Phobos, Case A - SOM, Schmedemann et al (2014)":
            new_str = " -cs 20"
        elif chron_sys.value == "Phobos, Case B - MBA, Schedemann et al (2014)":
            new_str = " -cs 21"

        return new_str

    def set_cite_function_str():
        pass

    def set_cmd_line_str():
        """Sets command line string.

        Takes all of the different data in the current applicaiton and sets it
        equal to its command line counterpart

        Args:
            none
        Return:
            none
        """

        chron_sys_str = ""
        equil_func_str = ""
        epoch_str = ""
        title_str = ""
        subtitle_str = ""
        plot_view_str = ""
        xrange_str = ""
        yrange_str = ""
        iso_str = ""
        show_iso_str = ""
        legend_str = ""
        cite_function_str = ""
        mu_str = ""
        style_str = ""
        print_dim_str = ""
        pt_size_str = ""
        p_str = ""

        cmd_line_str = ""

        chron_sys_str = set_chron_str()
        equil_func_str = set_equil_str()
        epoch_str = set_epoch_str()
        title_str = set_title_str()
        subtitle_str = set_subtitle_str()
        plot_view_str = set_plot_view_str()
        iso_str = set_isochron_str()
        show_iso_str = set_show_isochron_str()
        legend_str = set_legend_str()
        cite_function_str = set_cite_function_str()
        mu_str = set_mu_str()
        style_str = set_style_str()
        print_dim_str = set_print_dim_str()
        pt_size_str = set_pt_size_str()
        p_str = set_p_str()

        cmd_line_str = (
            f'craterstats{chron_sys_str if chron_sys_str is not None else ""}'
            f'{equil_func_str if equil_func_str is not None else ""}'
            f'{epoch_str if epoch_str is not None else ""}'
            f'{title_str if title_str is not None else ""}'
            f'{subtitle_str if subtitle_str is not None else ""}'
            f'{plot_view_str if plot_view_str is not None else ""}'
            f'{xrange_str if xrange_str is not None else ""}'
            f'{yrange_str if yrange_str is not None else ""}'
            f'{iso_str if iso_str is not None else ""}'
            f'{show_iso_str if show_iso_str is not None else ""}'
            f'{legend_str if legend_str is not None else ""}'
            f'{cite_function_str if cite_function_str is not None else ""}'
            f'{mu_str if mu_str is not None else ""}'
            f'{style_str if style_str is not None else ""}'
            f'{print_dim_str if print_dim_str is not None else ""}'
            f'{pt_size_str if pt_size_str is not None else ""}'
            f'{p_str if p_str is not None else ""}'
        )

        cmd_str.value = cmd_line_str
        page.update()

    def set_epoch_str():
        """Sets epoch command line string.

        Sets the command line string for the epoch that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-ep moon'
        """

        new_str = ""

        if epoch.value == "Moon, Wilhelms (1987)":
            new_str = " -ep moon"

        elif epoch.value == "Mars, Michael (2013)":
            new_str = " -ep mars"

        return new_str

    def set_equil_str():
        """Sets equilbrium function command line string.

        Sets the command line string for the Equilibrium Function that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-ef standard'
        """
        new_str = ""

        if equil_func.value == "Standard lunar equilibrium (Trask, 1966)":
            new_str = " -ef standard"
        elif equil_func.value == "Hartmann (1984)":
            new_str = " -ef hartmann"

        return new_str

    def set_isochron_str():
        """Sets isochron command line string.

        Sets the command line string for the isochron that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-isochrons 0.1,0.1,0.1'
        """
        new_str = f" -isochrons {iso_text.value}"

        return new_str

    def set_legend_str():
        return None

    def set_mu_str():
        """Sets mu command line string.

        Sets the command line string if mu is selected

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            ' -mu 1'
        """

        new_str = f' -mu {"1" if mu_legend.value else "0"}'

        return new_str

    def set_p_str():
        """Sets overplot command line string.

        Sets the command line string for the overplot settings that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-p source=txt,name=txt,range=[min,max],type=data,error_bars=0,hide=0,colour=0,psym=0,binning=0,age_left=0,display_age=0'
        """
        new_str = ""

        if (
            not Globals.template_dict["plot"]
            or Globals.template_dict["plot"][0]["source"] == ""
        ):
            return ""

        if (
            source_file_entry.value
            or plot_fit_options.value
            or error_bars.value
            or hide_button.value
            or color_dropdown.value
            or symbol_dropdown.value
            or binning_options.value
            or align_left.value
            or display_age.value
        ):

            new_str += " -p "

            if source_file_entry.value:
                new_str += f"source={source_file_entry.value} -p "

            if plot_fit_options.value:
                new_str += f"name={plot_fit_text.value},"

            if error_bars.value:
                new_str += "error_bars=1,"

            if hide_button.value:
                new_str += "hide=1,"

            if color_dropdown.value:
                new_str += f"colour={color_dropdown.value},"

            if symbol_dropdown.value:
                new_str += f"psym={symbol_dropdown.value},"

            if binning_options.value:
                new_str += f"binning={binning_options.value},"

            if align_left.value:
                new_str += "age_left=1,"

            if display_age.value:
                new_str += "display_age=1,"

        return new_str[:-1]

    def set_plot_info(e):
        """Sets plotsetting info for subplots

        Changes the settings on the Plot Settings tab depending on which subplot is
        selected

        Args:
            e: EventHandler

        Returns:
            none
        """

        data = e.control.data

        source_file_entry.value = data[0]["source"]
        plot_fit_text.value = data[1]["name"]
        diam_range_entry.value = f"{data[1]['range'][0]},{data[1]['range'][1]}"
        plot_fit_options.value = data[1]["type"]
        error_bars.value = True if data[1]["error_bars"] == "1" else False
        hide_button.value = True if data[1]["hide"] == "1" else False
        color_dropdown.value = Globals.colours[int(data[1]["colour"])]
        symbol_dropdown.value = Globals.symbols[int(data[1]["psym"])]
        binning_options.value = data[1]["binning"]
        align_left.value = True if data[1]["age_left"] == "1" else False
        display_age.value = True if data[1]["display_age"] == "1" else False
        resurf.value = True if data[1]["resurf"] == "1" else False
        resurf_showall.value = True if data[1]["resurf_showall"] == "1" else False
        offset_age.value = f"{data[1]['offset_age'][0]},{data[1]['offset_age'][1]}"

        page.update()

    def set_plot_view_str():
        """Sets plot view command line string.

        Sets the command line string for the plot view that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-pr cumulative'
        """
        new_str = ""

        if plot_view.value == "cumulative":
            new_str = " -pr cumulative"
        elif plot_view.value == "differential":
            new_str = " -pr differential"
        elif plot_view.value == "R-plot":
            new_str = " -pr R-plot"
        elif plot_view.value == "Hartmann":
            new_str = " -pr Hartmann"
        elif plot_view.value == "chronology":
            new_str = " -pr chronology"
        elif plot_view.value == "rate":
            new_str = " -pr rate"

        return new_str

    def set_print_dim_str():
        """Sets print dimension command line string.

        Sets the command line string for the  dimenstion that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-print_dim {7.5x7.5}'
        """
        new_str = f' - print_dim {print_scale_entry.value if len(print_scale_entry.value) == 1 else f"{{{print_scale_entry.value}}}"}'

        return new_str

    def set_pt_size_str():
        """Sets font size command line string.

        Sets the command line string for the font size that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-pt_size 8'
        """

        new_str = f" -pt_size {text_size.value}"

        return new_str

    def set_ref_diameter_str():
        pass

    def set_show_isochron_str():
        """Sets show isochron command line string.

        Sets the command line string if show isochrons is an option

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-show_isochron 1'
        """

        new_str = f' -show_isochron {"1" if show_iso.value else "0"}'

        return new_str

    def set_style_str():
        """Sets style command line string.

        Sets the command line string for the style that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-style decadel'
        """

        new_str = f" -style {style_options.value}"

        return new_str

    def set_subtitle_str():
        """Sets subtitle command line string.

        Sets the command line string for the subtitle that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-subtitle isochrons low'
        """

        new_str = f" -subtitle {subtitle_entry.value}"

        if subtitle_checkbox.value and subtitle_entry.value != "":
            return new_str

        return None

    def set_title_str():
        """Sets title command line string.

        Sets the command line string for the title that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-title Hartmann and Neukum isochrons'
        """

        new_str = f" -title {title_entry.value}"

        if title_checkbox.value and title_entry.value != "":
            return new_str

        return None

    def toggle_demo(e):

        if Globals.DEMO_RAN == False:

            loading = loading_circle("Creating Demo Plots...")

            cli.demo()

            Globals.command_dict = parse_demo_commands(PATH + "/../demo/")

            loading.open = False

        page.update()
        demo = demo_view(Globals.command_dict)

        Globals.DEMO_RAN = True
        Globals.demo_mode = False

    def update_config_dict():

        config = {"set": {}, "plot": []}

        config["set"] = {
            "chronology_system": chron_sys.value,
            "cite_functions": "1" if cite_func.value else "0",
            "epochs": epoch.value,
            "equilibrium": equil_func.value,
            "invert": "1" if invert.value else "0",
            "isochrons": iso_text.value,
            "legend": get_legend_value(),
            "mu": "1" if mu_legend.value else "0",
            "presentation": plot_view.value,
            "print_dimensions": print_scale_entry.value,
            "pt_size": text_size.value,
            "randomness": "1" if rand_legend.value else "0",
            "ref_diam": ref_diam.value,
            "sig_figs": sf_entry.value,
            "show_isochrons": "1" if show_iso.value else "0",
            "show_legend_area": "1" if legend_area.value else "0",
            "show_subtitle": "1" if subtitle_checkbox.value else "0",
            "show_title": "1" if title_checkbox.value else "0",
            "style": style_options.value,
            "subtitle": subtitle_entry.value,
            "title": title_entry.value,
            "xrange": x_range.value.replace(" ", "").split(","),
            "yrange": y_range.value.replace(" ", "").split(","),
            "format": list(Globals.template_dict["set"]["format"]),
        }

        config["plot"].append({"source": source_file_entry.value})
        config["plot"].append(
            {
                "name": plot_fit_text.value,
                "range": diam_range_entry.value.replace(" ", "").split(","),
                "type": plot_fit_options.value,
                "error_bars": "1" if error_bars.value else "0",
                "hide": "1" if hide_button.value else "0",
                "colour": str(Globals.colours.index(color_dropdown.value)),
                "psym": str(Globals.symbols.index(symbol_dropdown.value)),
                "binning": binning_options.value,
                "age_left": "1" if align_left.value else "0",
                "display_age": "1" if display_age.value else "0",
                "resurf": "1" if resurf.value else "0",
                "resurf_showall": "1" if resurf_showall.value else "0",
                "isochron": "1" if show_iso.value else "0",
                "offset_age": offset_age.value.replace(" ", "").split(","),
            }
        )

        selected_chip = next(
            (chip for chip in plot_lists.controls if chip.selected), None
        )

        if selected_chip is not None:

            selected_chip.data = config["plot"]

        Globals.template_dict["set"] = config["set"]
        Globals.template_dict["plot"] = selected_chip.data

        update_legend_options()
        # update_range_to_presentation()
        run_plot_async()

    def update_legend():

        for index, dictionary in enumerate(Globals.template_dict["set"]):

            if "legend" in dictionary:

                if "n" in Globals.template_dict["set"]["legend"]:

                    legend_name.value = True
                else:

                    legend_name.value = False

                if "a" in Globals.template_dict["set"]["legend"]:

                    legend_area.value = True
                else:

                    legend_area.value = False

                if "p" in Globals.template_dict["set"]["legend"]:

                    legend_perimeter.value = True
                else:

                    legend_perimeter.value = False

                if "c" in Globals.template_dict["set"]["legend"]:

                    legend_cratercount.value = True
                else:

                    legend_cratercount.value = False

                if "r" in Globals.template_dict["set"]["legend"]:

                    legend_range.value = True
                else:

                    legend_range.value = False

                if "N" in Globals.template_dict["set"]["legend"]:

                    legend_n_dref.value = True
                else:

                    legend_n_dref.value = False

        page.update()

    def update_legend_options():
        """Updates Legend options availability settings.

        Updates the legend options availability settings depending on the
        plot type

        Args:
            none
        Returns:
            none

        """

        # Check for 'data' plot type
        if plot_fit_options.value == "data":

            # Disable the correct legend options
            legend_name.disabled = False
            legend_area.disabled = False
            legend_perimeter.disabled = True
            legend_cratercount.disabled = True
            legend_range.disabled = True
            legend_n_dref.disabled = True

            legend_perimeter.value = False
            legend_cratercount.value = False
            legend_range.value = False
            legend_n_dref.value = False

        else:

            # Enable the correct legend options
            legend_name.disabled = True
            legend_area.disabled = True
            legend_perimeter.disabled = False
            legend_cratercount.disabled = False
            legend_range.disabled = False
            legend_n_dref.disabled = True

            legend_area.value = False
            legend_name.value = False

        if plot_view.value == "rate" or plot_view.value == "chronology":

            legend_name.disabled = True
            legend_area.disabled = True
            legend_perimeter.disabled = True
            legend_cratercount.disabled = True
            legend_range.disabled = True
            legend_n_dref.disabled = False

            legend_name.value = False
            legend_area.value = False
            legend_perimeter.value = False
            legend_cratercount.value = False
            legend_range.value = False
            legend_n_dref.disabled = False

            legend_area.value = False
            legend_name.value = False

    def update_range_to_presentation():
        """Updates x and y ranges.

        Updates the X and Y ranges to the default for the presentation selected

        Args:
            none
        Returns:
            none

        """

        # Check if source file is uploaded or plot settings filled
        if not template_dict["plot"] or template_dict["plot"][0]["source"] == "":

            # grab the current plot presentation
            presentation = plot_view.value

            # set the x and y ranges to the default for the presentation
            Globals.template_dict["set"]["xrange"] = (
                str(constants.DEFAULT_XRANGE[presentation][0])
                + ", "
                + str(constants.DEFAULT_XRANGE[presentation][1])
            )
            Globals.template_dict["set"]["yrange"] = (
                str(constants.DEFAULT_YRANGE[presentation][0])
                + ", "
                + str(constants.DEFAULT_YRANGE[presentation][1])
            )

            x_range.value = Globals.template_dict["set"]["xrange"]
            y_range.value = Globals.template_dict["set"]["yrange"]
            page.update()

    """
    Default Settings for the application
    """
    page.title = "Craterstats IV"  # Application title
    page.theme_mode = ft.ThemeMode.DARK  # Flet Default dark theme
    page.window.width = 1024  # Application width
    page.window.height = 768  # Application Height
    page.window.resizable = True  # Application size is static
    page.window.left = 0  # Set the window position to the leftmost side
    page.window.top = 0
    page.window.resizable = True
    # Fonts that can be used inside the application
    page.fonts = {
        "Courier New": "Fonts/Courier New.ttf",
        "Nasa": "Fonts/nasalization-rg.otf",
        "Arial": "Fonts/Arial Unicode.ttf",
    }
    # Default font for the application
    page.theme = ft.Theme(font_family="Arial")
    page.update()

    def toggle_sublist(sublist):
        sublist.visible = not sublist.visible  # Toggle visibility
        page.update()

    """
    Start of FLET GUI options
    """
    # This sets up an event listener for window resizing
    page.window.prevent_close = True

    page.window.on_event = handle_window_event

    page.on_resize = on_resize

    pick_files_dialog = ft.FilePicker(on_result=file_picker_result)

    page.overlay.append(pick_files_dialog)

    pick_data_file_dialog = ft.FilePicker(on_result=data_file_picker_result)

    page.overlay.append(pick_data_file_dialog)

    save_file_dialog = ft.FilePicker(on_result=save_image)

    save_plot_dialog = ft.FilePicker(on_result=save_plot_file)

    page.overlay.append(save_file_dialog)

    page.overlay.append(save_plot_dialog)

    # Plot view Radio options
    plot_view = ft.RadioGroup(
        ft.Row(
            [
                ft.Radio(value="cumulative", label="Cumulative"),
                ft.Radio(value="differential", label="Differential"),
                ft.Radio(value="R-plot", label="Relative (R)"),
                ft.Radio(value="Hartmann", label="Hartmann"),
                ft.Radio(value="chronology", label="Chronology"),
                ft.Radio(value="rate", label="Rate"),
            ]
        ),
        value="differential",
        on_change=lambda e: (
            update_range_to_presentation(),
            update_config_dict(),
        ),
    )

    # Celestial body fropdown options
    body = ft.Dropdown(
        width=500,
        options=[
            ft.dropdown.Option("Moon"),
            ft.dropdown.Option("Mars"),
            ft.dropdown.Option("Mercury"),
            ft.dropdown.Option("Vesta"),
            ft.dropdown.Option("Ceres"),
            ft.dropdown.Option("Ida"),
            ft.dropdown.Option("Gaspra"),
            ft.dropdown.Option("Lutetia"),
            ft.dropdown.Option("Phobos"),
        ],
        label="Body",
        value="Moon",
        dense=True,
        on_change=lambda e: (
            set_chron_sys(None, e),
            update_config_dict(),
        ),
    )

    # Chronolgy System dropdown options
    chron_sys = ft.Dropdown(
        width=500,
        label="Chronology System",
        options=[
            ft.dropdown.Option("Moon, Neukum (1983)"),
            ft.dropdown.Option("Moon, Neukum et al. (2001)"),
            ft.dropdown.Option("Moon, Hartmann 2010 iteration"),
            ft.dropdown.Option("Moon, Yue et al. (2022)"),
        ],
        value="Moon, Neukum (1983)",
        dense=True,
        on_change=lambda e: (
            set_chron_func(None, e),
            update_config_dict(),
        ),
    )

    # Chronology Function Dropdown options
    chron_func = ft.Dropdown(
        width=500,
        label="Chronology Function",
        value="Moon, Neukum (1983)",
        options=[
            ft.dropdown.Option("Moon, Neukum (1983)"),
        ],
        dense=True,
        on_change=lambda e: (update_config_dict(),),
    )

    # Production function dropdown options
    prod_func = ft.Dropdown(
        width=500,
        label="Production Function",
        value="Moon, Neukum (1983)",
        options=[
            ft.dropdown.Option("Moon, Neukum (1983)"),
        ],
        dense=True,
        on_change=lambda e: (update_config_dict(),),
    )

    # Epoch dropdown options
    epoch = ft.Dropdown(
        width=500,
        label="Epochs",
        value="none",
        options=[
            ft.dropdown.Option("none"),
            ft.dropdown.Option("Moon, Wilhelms (1987)"),
            ft.dropdown.Option("Mars, Michael (2013)"),
        ],
        dense=True,
        on_change=lambda e: (update_config_dict(),),
    )

    # Equilibrium function dropdown options
    equil_func = ft.Dropdown(
        width=500,
        label="Equilibrium Function",
        value="none",
        options=[
            ft.dropdown.Option("none"),
            ft.dropdown.Option("Standard lunar equilibrium (Trask, 1966)"),
            ft.dropdown.Option("Hartmann (1984)"),
        ],
        dense=True,
        on_change=lambda e: (update_config_dict(),),
    )

    iso_label = ft.Text("Isochrons")

    # Isochron text field
    iso_text = ft.TextField(
        width=500,
        dense=True,
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    show_legends = ft.Checkbox(
        label="Show Legends", value=True, on_change=lambda e: (update_config_dict(),)
    )

    # Data legend checkbox
    legend_name = ft.Checkbox(
        label="Name", value=False, on_change=lambda e: (update_config_dict(),)
    )

    # Fit legend checkbox
    legend_area = ft.Checkbox(
        label="Area", value=False, on_change=lambda e: (update_config_dict(),)
    )

    # Function legend checkbox
    legend_perimeter = ft.Checkbox(
        label="Perimeter", value=False, on_change=lambda e: (update_config_dict(),)
    )

    # Crater Count Legend
    legend_cratercount = ft.Checkbox(
        label="Crater Count", value=False, on_change=lambda e: (update_config_dict(),)
    )

    # Range Legend
    legend_range = ft.Checkbox(
        label="Range", value=False, on_change=lambda e: (update_config_dict(),)
    )

    # N(d_ref) legend
    legend_n_dref = ft.Checkbox(
        label="N(d_ref)", value=False, on_change=lambda e: (update_config_dict(),)
    )

    sf_label = ft.Text("Sig Figs")

    # Sig Fig entry
    sf_entry = ft.TextField(
        width=50,
        dense=True,
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # randomness legend checkbox
    rand_legend = ft.Checkbox(
        label="Randomness", on_change=lambda e: (update_config_dict(),)
    )

    # Mu legend checkbox
    mu_legend = ft.Checkbox(
        label="µ notation", on_change=lambda e: (update_config_dict(),)
    )

    # Cite functions checkbox
    cite_func = ft.Checkbox(
        label="Cite Functions", value=True, on_change=lambda e: (update_config_dict(),)
    )

    # Reference Diameter text field
    ref_diam = ft.TextField(
        width=100,
        dense=True,
        bgcolor=ft.colors.GREY_900,
        value="1",
        on_blur=lambda e: (update_config_dict(),),
    )

    ref_diam_lbl = ft.Text("Ref diameter, km")

    invert = ft.Checkbox(
        label="Invert", value=False, on_change=lambda e: (update_config_dict(),)
    )

    # Axis Log D Textfield
    x_range = ft.TextField(
        width=150,
        dense=True,
        value="-3, 2",
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # Axis y TextField
    y_range = ft.TextField(
        width=150,
        dense=True,
        value="-5, 5",
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # Auto Axis button
    axis_auto_button = ft.Checkbox(
        label="Auto", on_change=lambda e: (update_config_dict(),)
    )

    # Style options dropdown
    style_options = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("natural"),
            ft.dropdown.Option("root-2"),
        ],
        value="natural",
        dense=True,
        on_change=lambda e: (update_config_dict(),),
    )

    # Title entry textfield
    title_entry = ft.TextField(
        expand=True,
        dense=True,
        content_padding=ft.padding.all(8),
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # Title checkbox
    title_checkbox = ft.Checkbox(
        label="Title", value=True, on_change=lambda e: (update_config_dict(),)
    )

    # Print scale textfield
    print_scale_entry = ft.TextField(
        dense=True,
        value="7.5x7.5",
        content_padding=ft.padding.all(8),
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # Subtitle entry textfield
    subtitle_entry = ft.TextField(
        dense=True,
        content_padding=ft.padding.all(8),
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # subtitle checkbox
    subtitle_checkbox = ft.Checkbox(
        label="Subtitle", value=True, on_change=lambda e: (update_config_dict(),)
    )

    # Font size textfield
    text_size = ft.TextField(
        dense=True,
        value="8",
        bgcolor=ft.colors.GREY_900,
        content_padding=ft.padding.all(8),
        on_blur=lambda e: (update_config_dict(),),
    )

    # Plot lists list view
    plot_lists = ft.ListView(
        height=250,
        width=250,
        item_extent=30,
        spacing=10,
        padding=10,
        controls=[
            PlotChip(
                label=ft.Text("Default"),
                selected=True,
                selected_color=ft.colors.BLUE,
                show_checkmark=True,
                on_click=lambda e: (chip_on_click(e), update_config_dict()),
            )
        ],
        first_item_prototype=True,
    )

    # Plot list container
    plot_lists_container = ft.Container(
        content=plot_lists,
        border=ft.border.all(2, ft.colors.WHITE),
        alignment=ft.alignment.top_left,
    )

    """Plot Lists buttons"""
    new_button = ft.ElevatedButton(
        text="New", width=115, on_click=lambda e: new_subplot()
    )

    # duplicate_button = ft.ElevatedButton(text="Duplicate", width=115)

    # delete_button = ft.ElevatedButton(text="Delete", width=115)

    # Plot fit text field
    plot_fit_text = ft.TextField(
        width=300,
        dense=True,
        value="Default",
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(), change_subplot_name(e)),
    )

    # Plot fit dropdown
    plot_fit_options = ft.Dropdown(
        width=200,
        dense=True,
        options=[
            ft.dropdown.Option("data"),
            ft.dropdown.Option("poisson"),
            ft.dropdown.Option("b-poisson"),
            ft.dropdown.Option("c-fit"),
            ft.dropdown.Option("d-fit"),
        ],
        value="data",
        on_change=lambda e: (update_config_dict(),),
    )

    # Hide Button
    hide_button = ft.Checkbox(
        label="Hide plot", value=False, on_change=lambda e: (update_config_dict())
    )

    # Source file label
    source_file_label = ft.Text("Source file:")

    # Source file textfield
    source_file_entry = ft.TextField(
        width=500, dense=True, read_only=True, bgcolor=ft.colors.GREY_900
    )

    # File Browse button
    browse_button = ft.ElevatedButton(
        text="Browse...",
        width=115,
        on_click=lambda _: pick_data_file_dialog.pick_files(),
    )

    # Diameter Range textfield
    diam_range_entry = ft.TextField(
        width=150,
        dense=True,
        value="0, 10",
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # Plot point color dropdown
    color_dropdown = ft.Dropdown(
        dense=True,
        width=180,
        options=[
            ft.dropdown.Option("Black"),
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Yellow"),
            ft.dropdown.Option("Violet"),
            ft.dropdown.Option("Grey"),
            ft.dropdown.Option("Blue - 1"),
            ft.dropdown.Option("Blue - 2"),
            ft.dropdown.Option("Blue - 3"),
            ft.dropdown.Option("Blue - 4"),
            ft.dropdown.Option("Brown - 1"),
            ft.dropdown.Option("Brown - 2"),
            ft.dropdown.Option("Brown - 3"),
            ft.dropdown.Option("Brown - 4"),
            ft.dropdown.Option("Green - 1"),
            ft.dropdown.Option("Green - 2"),
            ft.dropdown.Option("Green - 3"),
            ft.dropdown.Option("Orange"),
            ft.dropdown.Option("Pink - 1"),
            ft.dropdown.Option("Pink - 2"),
            ft.dropdown.Option("Pink - 3"),
            ft.dropdown.Option("Purple - 1"),
            ft.dropdown.Option("Purple - 2"),
            ft.dropdown.Option("Red - 1"),
            ft.dropdown.Option("Red - 2"),
            ft.dropdown.Option("Red - 3"),
            ft.dropdown.Option("Teal - 1"),
            ft.dropdown.Option("Teal - 2"),
            ft.dropdown.Option("Yellow - 1"),
            ft.dropdown.Option("Yellow - 2"),
            ft.dropdown.Option("Yellow - Green"),
        ],
        value="Black",
        on_change=lambda e: (update_config_dict(),),
    )

    # Plot point color symbol
    symbol_dropdown = ft.Dropdown(
        dense=True,
        width=210,
        options=[
            ft.dropdown.Option("Square"),
            ft.dropdown.Option("Circle"),
            ft.dropdown.Option("Star (4 points)"),
            ft.dropdown.Option("Triangle"),
            ft.dropdown.Option("Star (5 points)"),
            ft.dropdown.Option("Diagonal cross"),
            ft.dropdown.Option("Cross"),
            ft.dropdown.Option("Point"),
            ft.dropdown.Option("Inverted triangle"),
            ft.dropdown.Option("Filled square"),
            ft.dropdown.Option("Filled circle"),
            ft.dropdown.Option("Filled star (4 points)"),
            ft.dropdown.Option("Filled triangle"),
            ft.dropdown.Option("Filled star (5 points)"),
            ft.dropdown.Option("Filled inverted triangle"),
        ],
        value="Square",
        on_change=lambda e: (update_config_dict(),),
    )

    """PLOT SETTINGS OPTIONS"""
    error_bars = ft.Checkbox(
        label="Error bars", value=True, on_change=lambda e: (update_config_dict(),)
    )

    display_age = ft.Checkbox(
        label="Display age", value=True, on_change=lambda e: (update_config_dict(),)
    )

    align_left = ft.Checkbox(
        label="Align age left", on_change=lambda e: (update_config_dict(),)
    )

    show_iso = ft.Checkbox(
        label="Show isochron", value=True, on_change=lambda e: (update_config_dict(),)
    )

    plot_fit_error = ft.Checkbox(
        label="Plot fit", value=True, on_change=lambda e: (update_config_dict(),)
    )

    resurf = ft.Checkbox(
        label="Resurf", value=False, on_change=lambda e: (update_config_dict(),)
    )

    resurf_showall = ft.Checkbox(
        label="Resurf all", value=False, on_change=lambda e: (update_config_dict(),)
    )

    offset_age = ft.TextField(
        width=150,
        dense=True,
        value="0, 0",
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(),),
    )

    # Binning options dropdown
    binning_options = ft.Dropdown(
        width=150,
        dense=True,
        options=[
            ft.dropdown.Option("pseudo-log"),
            ft.dropdown.Option("20/decade"),
            ft.dropdown.Option("10/decade"),
            ft.dropdown.Option("x2"),
            ft.dropdown.Option("root-2"),
            ft.dropdown.Option("4th root-2"),
            ft.dropdown.Option("none"),
        ],
        value="pseudo-log",
        on_change=lambda e: (update_config_dict(),),
    )

    # Default command line string
    cmd_str = ft.TextField(
        dense=True,
        value="craterstats -cs 1 -pr differential -isochrons  -show_isochron 1 -mu 0 -style natural -print_dim {7.5x7.5} -pt_size 8",
        text_size=12,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        text_style=ft.TextStyle(font_family="Courier New"),
        width=1500,
    )

    legend_options_container = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        legend_name,
                        legend_area,
                        legend_perimeter,
                        legend_cratercount,
                        legend_range,
                        legend_n_dref,
                    ]
                ),
                ft.Row(
                    [
                        rand_legend,
                        mu_legend,
                        cite_func,
                        ref_diam_lbl,
                        ref_diam,
                        invert,
                        sf_label,
                        sf_entry,
                    ]
                ),
            ]
        ),
        padding=10,
        visible=False,
    )

    legend_options = ft.Column(
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "Legend Options", style=ft.TextStyle(size=16, weight="bold")
                        ),
                        ft.IconButton(
                            icon=ft.icons.EXPAND_MORE,
                            on_click=lambda e: toggle_sublist(legend_options_container),
                        ),
                    ]
                ),
            ),
            legend_options_container,
        ],
    )

    list_view = ft.ListView(expand=True, spacing=10, controls=[legend_options])

    # Global Settings Tab Container
    global_settings = ft.Column(
        [
            plot_view,
            ft.Divider(),
            body,
            chron_sys,
            chron_func,
            prod_func,
            epoch,
            equil_func,
            ft.Divider(),
            ft.Row([iso_label, iso_text, show_legends]),
            ft.Row([list_view]),
            ft.Row(
                [
                    ft.Text("X Range"),
                    x_range,
                    ft.Text("Y Range"),
                    y_range,
                    axis_auto_button,
                ]
            ),
            ft.Row([ft.Text("Style:"), style_options]),
        ],
        scroll="auto",
    )

    # Plot settings tab container
    plot_settings = ft.Column(
        [
            ft.Text(),
            ft.GridView(
                runs_count=5,
                child_aspect_ratio=5.0,
                controls=[
                    title_entry,
                    title_checkbox,
                    ft.VerticalDivider(),
                    ft.Text(
                        "Print scale. cm/decade (or plot width x height. cm):",
                        style=ft.TextStyle(height=1, size=11),
                    ),
                    print_scale_entry,
                    subtitle_entry,
                    subtitle_checkbox,
                    ft.VerticalDivider(),
                    ft.Text("Text size. pt:"),
                    text_size,
                ],
                spacing=20,
            ),
            ft.Row(
                [
                    plot_lists_container,
                    ft.Column(
                        [
                            new_button,
                        ]
                    ),
                ]
            ),
            ft.Divider(),
            ft.Row(
                [
                    plot_fit_text,
                    plot_fit_options,
                    hide_button,
                ]
            ),
            ft.Row([source_file_label, source_file_entry, browse_button]),
            ft.Row(
                [
                    ft.Text("Range:"),
                    diam_range_entry,
                    ft.Text("Binning"),
                    binning_options,
                ]
            ),
            ft.Row(
                [ft.Text("Colour"), color_dropdown, ft.Text("Symbol"), symbol_dropdown]
            ),
            ft.Column(
                [
                    ft.Row(
                        [
                            error_bars,
                            display_age,
                            align_left,
                            show_iso,
                            plot_fit_error,
                        ]
                    ),
                    ft.Row(
                        [resurf, resurf_showall, ft.Text("Offset age:"), offset_age]
                    ),
                ]
            ),
        ]
    )

    # plot image
    plot_image = ft.Image(
        src="/plots/blank_plot.png",
        height=page.window.width,
        width=page.window.width * 0.8,
        fit=ft.ImageFit.FIT_WIDTH,
    )

    plot_image.resizable = True

    # Plot Tab container
    plot = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Diameter"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Bin"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("n"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("y"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Age"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("N(1)"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("a0"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True,
                            ),
                        ],
                    ),
                ],
            ),
            plot_image,
            cmd_str,
        ],
    )

    # Tabs
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=150,
        tabs=[
            ft.Tab(
                text="Global Settings",
                icon=ft.icons.SETTINGS,
                content=global_settings,
            ),
            ft.Tab(
                text="Plot Settings",
                icon=ft.icons.SCATTER_PLOT_OUTLINED,
                content=plot_settings,
            ),
        ],
        expand=1,
        on_change=lambda _: (
            set_cmd_line_str(),
            update_config_dict(),
        ),
    )

    # FILE|PLOT|EXPORT|UTILITIES Menu bar
    menubar = ft.MenuBar(
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            mouse_cursor={
                ft.MaterialState.HOVERED: ft.MouseCursor.WAIT,
                ft.MaterialState.DEFAULT: ft.MouseCursor.ZOOM_OUT,
            },
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}
                        ),
                        on_click=lambda _: save_plot_dialog.save_file(
                            dialog_title="Save the plot",
                            file_type=ft.FilePickerFileType.ANY,
                        ),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Open"),
                        leading=ft.Icon(ft.icons.FILE_UPLOAD),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}
                        ),
                        on_click=lambda _: pick_files_dialog.pick_files(),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Close"),
                        leading=ft.Icon(ft.icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}
                        ),
                        on_click=lambda _: close_app(),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Plot"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("New"), leading=ft.Icon(ft.icons.NEW_LABEL)
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Duplicate"),
                        leading=ft.Icon(ft.icons.CONTROL_POINT_DUPLICATE),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Delete"), leading=ft.Icon(ft.icons.DELETE)
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Export"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Image"),
                        leading=ft.Icon(ft.icons.IMAGE),
                        on_click=lambda _: save_file_dialog.save_file(
                            dialog_title="Save the image",
                            file_type=ft.FilePickerFileType.IMAGE,
                        ),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Summary table"),
                        leading=ft.Icon(ft.icons.FILE_DOWNLOAD),
                        on_click=lambda _: (
                            setattr(Globals, "SUMMARY", True),
                            run_plot_async(),
                        ),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text(".stat table"),
                        leading=ft.Icon(ft.icons.TABLE_CHART),
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Utilities"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Demo"),
                        leading=ft.Icon(ft.icons.PLAY_ARROW_ROUNDED),
                        on_click=lambda e: (
                            setattr(Globals, "demo_mode", True),
                            update_config_dict(),
                        ),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Show dev notes"),
                        leading=ft.Icon(ft.icons.NOTES),
                        on_click=lambda e: (
                            page.client_storage.set("show_note", True),
                            dev_notes(),
                        ),
                    ),
                ],
            ),
            ft.MenuItemButton(content=ft.Text("About"), on_click=open_about_dialog),
        ],
    )

    two_column_layout = ft.Row(
        controls=[
            ft.Container(content=tabs, expand=6, width=page.window.width * 0.5),
            ft.Container(
                content=plot_image if not Globals.demo_mode else None,
                expand=5,
                width=page.window.width,
            ),
        ],
        expand=True,
    )

    bottom_row = ft.Row(
        controls=[cmd_str],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    page_layout = ft.Column(
        controls=[two_column_layout, ft.Divider(), bottom_row], expand=True
    )

    dev_notes()

    page.add(menubar)
    page.add(page_layout)

    page.on_keyboard_event = handle_keypress_events


try:
    ft.app(target=main, assets_dir="assets")

finally:
    delete_temp_plots(PATH + "/assets/plots/", ["png", "jpg", "pdf", "svg", "tif"])
    delete_temp_plots(PATH + "/../demo/", None)
