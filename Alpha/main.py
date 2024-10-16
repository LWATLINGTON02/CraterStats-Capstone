from argparse import Namespace

import concurrent.futures

import flet as ft
from craterstats import cli, Craterplot, Craterplotset
from flet import FilePickerResultEvent
import shutil

from Globals import *
from gm.file import file_exists, read_textstructure, read_textfile, filename
from helperFunctions import *
import Globals

import traceback


# GM Folder from CraterstatsIII
# Also from craterstats
PATH = os.path.dirname(os.path.abspath(__file__))


"""Main Function - EVERYTHING FLET IS INSIDE THIS FUNCTION"""


def main(page: ft.Page):

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

        plot_names = {}

        if plots_dict is not None:

            for plots in plots_dict:
                plot_names[plots] = plots_dict[plots][f"{plots}.name"]

            for plots in plot_names:
                content_list.append(
                    ft.Chip(ft.Text(plot_names[plots]), on_click=lambda e: (set_plot_info(e), update_config_dict(), run_plot_async())))

        # print(plot_lists.controls)
        plot_lists.controls = content_list

        page.update()

    def demo_view(demo_dict):
        carousel_images = list(demo_dict.keys())
        setattr(Globals, 'demo_cmd_str',
                demo_dict[carousel_images[Globals.image_index]])

        print_tree(demo_dict, 0)
        print(len(demo_dict.keys()))

        def update_image():
            # Update the image based on the current index
            print(demo_dict[carousel_images[Globals.image_index]])
            setattr(Globals, 'demo_cmd_str',
                    demo_dict[carousel_images[Globals.image_index]])
            cmd_str.value = Globals.demo_cmd_str
            demo_image.src = f"{PATH}/../demo/{carousel_images[Globals.image_index]}"
            plot_num.value = f"Plot {Globals.image_index + 1} of {len(carousel_images)}"
            plot_num.update()
            demo_image.update()
            page.update()

        # Function to go to the next image
        def next_image(e):
            print(len(carousel_images))
            setattr(Globals, 'image_index', Globals.image_index + 1)
            print(Globals.image_index)

            if Globals.image_index >= 24:
                print("index >= 24")
                # Loop back to the first image
                setattr(Globals, 'image_index', 0)
            update_image()

        # Function to go to the previous image
        def prev_image(e):
            print(len(carousel_images))
            setattr(Globals, 'image_index', Globals.image_index - 1)
            print(Globals.image_index)

            if Globals.image_index < 0:
                print("index < 0")
                # Loop back to the last image
                setattr(Globals, 'image_index', len(carousel_images) - 1)
                print(Globals.image_index)
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
            f"Plot {Globals.image_index + 1} of {len(carousel_images)}", text_align=ft.TextAlign.CENTER)

        demo_modal = ft.AlertDialog(
            title=ft.Text("Demo Plots"),
            content=ft.Column(
                controls=[
                    plot_num,
                    demo_image,
                    ft.VerticalDivider(),
                    cmd_str
                ]
            ),
            shape=ft.RoundedRectangleBorder(radius=5),
            actions=[
                ft.ElevatedButton(
                    text="Prev", on_click=lambda e: prev_image(e)),
                ft.ElevatedButton(
                    text="Next", on_click=lambda e: next_image(e)),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )

        page.dialog = demo_modal
        demo_modal.open = True
        page.update()

        return demo_view

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
        """
        NEED TO DO: ADD INVERT, XRANGE, YRANGE, AND NEW LEGEND OPTIONS
                    CHANGE SIG FIGS TO TEXTFIELD INSTEAD OF CHECKBOX

        """

        if e.files[0].path.endswith(".plt"):
            # Reads through each line of data and sets data based off of line
            config = {}
            current_dict_name = None
            current_item_list = None

            with open(e.files[0].path, 'r') as file:
                for line in file:
                    line = line.strip()

                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue

                    # Detect start of a new section
                    if line.endswith("{"):  # Start of a new block (e.g., set = {)
                        current_dict_name = line.split("=")[0].strip()
                        # List to store the dictionaries
                        config[current_dict_name] = []
                        current_item_list = config[current_dict_name]

                    elif "=" in line:  # Key-value pair inside the block
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()

                        # Handle lists in the form [value1, value2]
                        if value.startswith("[") and value.endswith("]"):
                            value = value[1:-1].split(',')
                            value = [v.strip().strip("'") for v in value]

                        # Handle strings enclosed in single quotes
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]

                        # Convert to a dictionary and add to the list for the current block
                        current_item_list.append({key: value})

                    elif line == "}":  # End of the block
                        current_dict_name = None
                        current_item_list = None

            """
            TODO HERE: ADD CITE_FUNCTIONS, INVERT, LEGEND, SHOW_LEGEND_AREA TO SET SETTINGS
                       ADD RESURF, RESURF_ALL, ISOCHRON, OFFSET_AGE TO PLOT SETTINGS
            """

            # Set settings
            for index, dictionary in enumerate(config['set']):

                if 'chronology_system' in dictionary:
                    body.value = get_body(
                        config['set'][index]['chronology_system'])
                    set_chron_sys(body.value, None)
                    chron_sys.value = config['set'][index]['chronology_system']
                if 'epochs' in dictionary:
                    epoch.value = config['set'][index]['epochs'] if config['set'][index]['epochs'] != '' else 'none'
                if 'equilibrium' in dictionary:
                    equil_func.value = config['set'][index]['equilibrium']
                if 'isochrons' in dictionary:
                    iso_text.value = config['set'][index]['isochrons']
                if 'mu' in dictionary:
                    mu_legend.value = config['set'][index]['mu']
                if 'presentation' in dictionary:
                    plot_view.value = config['set'][index]['presentation']
                if 'print_dimensions' in dictionary:
                    print_scale_entry.value = config['set'][index]['print_dimensions']
                if 'pt_size' in dictionary:
                    text_size.value = max(config['set'][index]['pt_size'])
                if 'randomness' in dictionary:
                    rand_legend.value = config['set'][index]['randomness']
                if 'ref_diameter' in dictionary:
                    ref_diam.value = config['set'][index]['ref_diameter']
                if 'sig_figs' in dictionary:
                    sf_legend.value = True if config['set'][index]['sig_figs'] else False
                if 'show_isochrons' in dictionary:
                    show_iso.value = True if config['set'][index]['show_isochrons'] else False
                if 'show_subtitle' in dictionary:
                    subtitle_checkbox.value = True if config['set'][index]['show_subtitle'] else False
                if 'show_title' in dictionary:
                    title_checkbox.value = True if config['set'][index]['show_title'] else False
                if 'style' in dictionary:
                    style_options.value = config['set'][index]['style']
                if 'subtitle' in dictionary:
                    subtitle_entry.value = config['set'][index]['subtitle'] if config['set'][index]['subtitle'] != '' else None
                if 'title' in dictionary:
                    title_entry.value = config['set'][index]['title'] if config['set'][index]['title'] != '' else None

            # Plot settings
            for index, dictionary in enumerate(config['plot']):

                if 'source' in dictionary:
                    source_file_entry.value = config['plot'][index]['source']
                if 'name' in dictionary:
                    plot_fit_text.value = config['plot'][index]['name']
                if 'range' in dictionary:
                    diam_range_entry.value = (
                        config['plot'][index]['range'][0]) + ", " + (config['plot'][index]['range'][1])
                if 'type' in dictionary:
                    plot_fit_options.value = config['plot'][index]['type']
                if 'error_bars' in dictionary:
                    error_bars.value = True if config['plot'][index]['error_bars'] else False
                if 'hide' in dictionary:
                    hide_button.value = True if config['plot'][index]['hide'] else False
                if 'colour' in dictionary:
                    color_dropdown.value = Globals.colours[int(
                        config['plot'][index]['colour'])]
                if 'psym' in dictionary:
                    symbol_dropdown.value = Globals.symbols[int(
                        config['plot'][index]['psym'])]
                if 'binning' in dictionary:
                    binning_options.value = config['plot'][index]['binning']
                if 'age_left' in dictionary:
                    align_left.value = True if config['plot'][index]['age_left'] else False
                if 'display_age' in dictionary:
                    display_age.value = True if config['plot'][index]['display_age'] else False

            Globals.template_dict = config

        create_plot_lists()
        run_plot_async()

        page.update()

    def get_body(chron_sys):

        body_val = ''

        chron_sys_body = str(chron_sys).split(",")[0].replace("[", "")

        if chron_sys_body == 'Mars':

            body_val = 'Mars'

        elif chron_sys_body == 'Moon':

            body_val = 'Moon'

        elif chron_sys_body == 'Mercury':

            body_val = 'Mercury'

        elif chron_sys_body == 'Vesta':

            body_val = 'Vesta'

        elif chron_sys_body == 'Ceres':

            body_val = 'Ceres'

        elif chron_sys_body == 'Ida':

            body_val = 'Ida'

        elif chron_sys_body == 'Gaspra':

            body_val = 'Gaspra'

        elif chron_sys_body == 'Lutetia':

            body_val = 'Lutetia'

        elif chron_sys_body == 'Phobos':

            body_val = 'Phobos'

        return body_val

    def handle_keypress_events(e: ft.KeyboardEvent):
        if (e.key == "O" and (e.ctrl or e.meta)):
            print("Button is pressed")
            pick_files_dialog.pick_files()

    def loading_circle():

        loading = ft.AlertDialog(
            title=ft.Text("Creating Demo Plots..."),
            content=ft.ProgressRing(
                stroke_cap=ft.StrokeCap.BUTT,
                stroke_width=5
            )
        )

        page.dialog = loading
        loading.open = True
        page.update()

        return loading
    
    def on_resize(e):
        # Trigger UI update when window is resized
        page.update()

    def open_about_dialog(e):
        """ Opens and fills about text.

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
                '\n'.join(["GUI Developed by The Lunar Pit Patrol, Senior Capstone group for NAU",
                           "Lunar Pit Patrol Team:",
                           "Evan Palmisiano",
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
                           ])),
            shape=ft.BeveledRectangleBorder(radius=5)
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    # Function to update the displayed image
    def print_plot():
        """ Creates plot images.

        Craterstats plots are created either by using the functions that are selected in the GUI or by uploading
        a .plt file. This function is mostly pulled from the craterstats cli.py main function with some modifications
        to fit our GUI.

        Args:
            none

        Returns:
            none
        """

        template = PATH + "/craterstats_config_files/default.plt"
        functions = PATH + "/craterstats_config_files/functions.txt"
        functions_user = PATH + "/craterstats_config_files/functions_user.txt"

        arg = Namespace(
            about=False,
            autoscale=False,
            chronology_system=set_chron_str()[-2:].replace(' ', ''),
            cite_function=func_legend.value,
            demo=Globals.demo_mode,
            epochs=set_epoch_str()[-2:].replace(' ',
                                                '') if epoch.value != 'none' else None,
            equilibrium=equil_func.value if equil_func.value != 'none' else None,
            format=None,
            input=None,
            invert=None,
            isochrons=iso_text.value,
            lcs=False,
            legend=None,
            lpc=False,
            mu=mu_legend.value,
            out='',
            plot=Globals.template_dict['plot'],
            presentation=plot_view.value,
            print_dim=print_scale_entry.value,
            pt_size=text_size.value if text_size.value != '' else '8',
            ref_diameter=ref_diam.value,
            show_isochrons=show_iso.value,
            sig_figs='3',
            src=None,
            style=style_options.value,
            subtitle=subtitle_entry.value if subtitle_checkbox.value else None,
            template=None,
            title=title_entry.value if title_checkbox.value else None,
            transparent=False,
            xrange=None,
            yrange=None
        )

        if arg.demo:
            toggle_demo(None)
            return

        print("Template", template)

        # if type(arg.template) == str:
        settings = read_textstructure(
            template if arg.template is None else arg.template)

        print("Settings", settings)
        # else:
        #     settings = arg.template
        # print(settings['plot']['source'])
        systems = read_textfile(
            functions, ignore_hash=True, strip=';', as_string=True)
        if file_exists(functions_user):
            systems += read_textfile(functions_user,
                                     ignore_hash=True, strip=';', as_string=True)

        functionStr = read_textstructure(systems, from_string=True)

        try:
            craterPlot = cli.construct_plot_dicts(arg, settings)
            defaultFilename = generate_output_file_name()

            craterPlotSet = cli.construct_cps_dict(
                arg, settings, functionStr, defaultFilename)

            print(f"\n\nCraterplotSet format", craterPlotSet['format'])

            if 'a' in craterPlotSet['legend'] and 'b-poisson' in [d['type'] for d in craterPlot]:
                craterPlotSet['legend'] += 'p'

            plot = [Craterplot(d) for d in craterPlot]

            print(f"\n\nPlot {plot}\n\n")

            if craterPlotSet['ref_diameter'] == '':
                craterPlotSet['ref_diameter'] = '1.0'

            plotSettings = Craterplotset(craterPlotSet, craterPlot=plot)

            # if plot:
            #     plotSettings.autoscale(self=plotSettings)
            newFileName = generate_output_file_name()

            craterPlotSet['out'] = PATH + '/assets/plots/' + newFileName

            drawn = False
            for format in plotSettings.format:
                if format in {'png', 'jpg', 'pdf', 'svg', 'tif'}:
                    if not drawn:
                        plotSettings.draw()
                        drawn = True
                    plotSettings.fig.savefig(
                        craterPlotSet['out'], dpi=500, transparent=arg.transparent)
                    plot_image.src = craterPlotSet['out'] + '.png'
                    plot_image.update()
                if format in {'txt'}:
                    plotSettings.create_summary_table()

            set_cmd_line_str()
            page.update()

        # except SystemExit as err:
        #     print("Error couldn't create craterplotset")
        #     print("Error:", err)
        except Exception as err:
            print("Other Error", err)
            traceback.print_exc()

    def run_plot_async():
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(print_plot)

            result = future.result()

            # try:
            #     result = future.result()
            # except SystemExit as e:
            #     print(f"Caught {e}")

            # except Exception as e:
            #     print(f"Caught Unexpected: {e}")
            #     print(f"{chron_sys.value}")

    def save_image(e):

        if save_file_dialog.result and save_file_dialog.result.path:
            export_path = save_file_dialog.result.path

            if not export_path.lower().endswith(".png"):
                export_path += ".png"
                
                shutil.copy(plot_image.src, export_path)
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

        plot_names = {}

        if plots_dict is not None:

            for plots in plots_dict:
                plot_names[plots] = plots_dict[plots][f"{plots}.name"]

            for plots in plot_names:
                content_list.append(
                    ft.Chip(ft.Text(plot_names[plots]), on_click=lambda e: set_plot_info(e) or run_plot_async()))

        # print(plot_lists.controls)
        plot_lists.controls = content_list

        page.update()

    def set_plot_info(e):
        """Sets plotsetting info for subplots

        Changes the settings on the Plot Settings tab depending on which subplot is
        selected

        Args:
            e: EventHandler

        Returns:
            none
        """

        correct_key = ''

        # print(e.control.label.value)
        for key, val in plots_dict.items():
            # print(val)

            try:
                try:
                    if val["plot1.name"] == e.control.label.value:
                        # print("Plot1 Name Found")
                        correct_key = key
                except KeyError:
                    pass
                try:
                    if val["plot2.name"] == e.control.label.value:
                        # print("Plot2 Name Found")
                        correct_key = key
                except KeyError:
                    pass
                try:
                    if val["plot3.name"] == e.control.label.value:
                        # print("Plot3 Name Found")
                        correct_key = key
                except KeyError:
                    pass
            except KeyError:
                print("No values")

        source_file_entry.value = plots_dict[correct_key][f"{correct_key}.source"]

        range_start = float(plots_dict[correct_key][f"{correct_key}.range"][0])
        range_end = float(plots_dict[correct_key][f"{correct_key}.range"][1])
        range_val = ''

        print(range_start, range_end, type(range_start), type(range_end))

        if range_start < 1:

            if range_end < 1:

                range_val = f"[{int(range_start * 100)} m, {int(range_end * 100)} m]"

            else:
                range_val = f"[{int(range_start * 100)} m, {int(range_end)} km]"

        else:
            range_val = f"[{int(range_start)} km, {int(range_end)} km]"

        diam_range_entry.value = range_val.strip("[]")

        plot_options = plots_dict[correct_key][f"{correct_key}.type"]

        if plot_options == "data":
            plot_fit_options.value = "crater count"

        elif plot_options == "diff_fit":
            plot_fit_options.value = "differential fit"

        elif plot_options == "cumu_fit":
            plot_fit_options.value = "cumulative fit"

        elif plot_options == "poisson":
            plot_fit_options.value = "Poisson pdf"

        elif plot_options == "poisson_buffer":
            plot_fit_options.value = "Poisson buffer pdf"

        error_bars.value = plots_dict[correct_key][f"{correct_key}.error_bars"]

        hide_button.value = plots_dict[correct_key][f"{correct_key}.hide"]

        color_dropdown.value = colours[int(
            plots_dict[correct_key][f"{correct_key}.colour"])]

        symbol_dropdown.value = symbols[int(
            plots_dict[correct_key][f"{correct_key}.psym"])]

        binning_options.value = plots_dict[correct_key][f"{correct_key}.binning"]
        binning_options.options = [ft.dropdown.Option(
            plots_dict[correct_key][f"{correct_key}.binning"])]

        align_left.value = plots_dict[correct_key][f"{correct_key}.age_left"]

        display_age.value = plots_dict[correct_key][f"{correct_key}.display_age"]

        plot_fit_text.value = plots_dict[correct_key][f"{correct_key}.name"]

        page.update()

    """
    Default Settings for the application
    """
    page.title = 'Craterstats IV'  # Application title
    page.theme_mode = ft.ThemeMode.DARK  # Flet Default dark theme
    page.window.width = 1920  # Application width
    page.window.height = 1080  # Application Height
    page.window.resizable = True  # Application size is static
    page.window.left = 0    # Set the window position to the leftmost side
    page.window.top = 0
    page.window.resizable = True
    # Fonts that can be used inside the application
    page.fonts = {
        "Courier New": "Fonts/Courier New.ttf",
        "Nasa": "Fonts/nasalization-rg.otf",
        "Arial": "Fonts/Arial Unicode.ttf"
    }
    # Default font for the application
    page.theme = ft.Theme(font_family="Arial")
    page.update()

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
                chron_func.options = [
                    ft.dropdown.Option(chron_systems[system][0])]
                prod_func.value = chron_systems[system][1]
                prod_func.options = [
                    ft.dropdown.Option(chron_systems[system][1])]

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
        chron_func_str = ''
        prod_func_str = ''

        if check_value == 'Moon':
            items = [ft.dropdown.Option('Moon, Neukum (1983)'),
                     ft.dropdown.Option('Moon, Neukum et al. (2001)'),
                     ft.dropdown.Option('Moon, Hartmann 2010 iteration'),
                     ft.dropdown.Option('Moon, Yue et al. (2022)')]
            chron_func_str = 'Moon, Neukum (1983)'
            prod_func_str = 'Moon, Neukum (1983)'

        elif check_value == "Mars":
            items = [ft.dropdown.Option('Mars, Neukum-Ivanov (2001)'),
                     ft.dropdown.Option('Mars, Ivanov 2001'),
                     ft.dropdown.Option('Mars, Hartmann 2004 iteration'),
                     ft.dropdown.Option('Mars, Hartmann & Daubar (2016)')]
            chron_func_str = 'Mars, Hartmann & Neukum (2001)'
            prod_func_str = 'Mars, Ivanov (2001)'

        elif check_value == "Mercury":
            items = [ft.dropdown.Option('Mercury, Strom & Neukum (1988)'),
                     ft.dropdown.Option('Mercury, Neukum et al. (2001)'),
                     ft.dropdown.Option(
                         'Mercury, Le Feuvre and Wieczorek 2011 non-porous'),
                     ft.dropdown.Option('Mercury, Le Feuvre and Wieczorek 2011 porous')]
            chron_func_str = 'Mercury, Strom & Neukum (1988)'
            prod_func_str = 'Mercury, Strom & Neukum (1988)'

        elif check_value == 'Vesta':
            items = [ft.dropdown.Option('Vesta, Rev4, Schmedemann et al (2014)'),
                     ft.dropdown.Option(
                         'Vesta, Rev3, Schmedemann et al (2014)'),
                     ft.dropdown.Option('Vesta, Marchi & O\'Brien (2014)')]
            chron_func_str = "Vesta, Rev4, Schmedemann et al (2014)"
            prod_func_str = "Vesta, Rev4, Schmedemann et al (2014)"

        elif check_value == 'Ceres':
            items = [ft.dropdown.Option('Ceres, Hiesinger et al. (2016)')]
            chron_func_str = 'Ceres, Hiesinger et al. (2016)'
            prod_func_str = 'Ceres, Hiesinger et al. (2016)'

        elif check_value == 'Ida':
            items = [ft.dropdown.Option('Ida, Schmedemann et al (2014)')]
            chron_func_str = 'Ida, Schmedemann et al (2014)'
            prod_func_str = 'Ida, Schmedemann et al (2014)'

        elif check_value == 'Gaspra':
            items = [ft.dropdown.Option('Gaspra, Schmedemann et al (2014)')]
            chron_func_str = 'Gaspra, Schmedemann et al (2014)'
            prod_func_str = 'Gaspra, Schmedemann et al (2014)'

        elif check_value == 'Lutetia':
            items = [ft.dropdown.Option('Lutetia, Schmedemann et al (2014)')]
            chron_func_str = 'Lutetia, Schmedemann et al (2014)'
            prod_func_str = 'Lutetia, Schmedemann et al (2014)'

        elif check_value == 'Phobos':
            items = [ft.dropdown.Option('Phobos, Case A - SOM, Schmedemann et al (2014)'),
                     ft.dropdown.Option('Phobos, Case B - MBA, Schmedemann et al (2014)')]
            chron_func_str = 'Phobos, Case A - SOM, Schmedemann et al (2014)'
            prod_func_str = 'Phobos, Case A - SOM, Schmedemann et al (2014)'

        if not (check_value == 'Moon' or check_value == 'Mars'):
            epoch.options = [ft.dropdown.Option('none')]
            epoch.value = 'none'
        elif check_value == 'Moon':
            epoch.options = [ft.dropdown.Option('none'),
                             ft.dropdown.Option('Moon, Wilhelms (1987)')]
            epoch.value = 'none'
        elif check_value == 'Mars':
            epoch.options = [ft.dropdown.Option('none'),
                             ft.dropdown.Option('Mars, Michael (2013)')]
            epoch.value = 'none'

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

        new_str = ''

        if chron_sys.value == 'Moon, Neukum (1983)':
            new_str = ' -cs 1'
        elif chron_sys.value == 'Moon, Neukum et al. (2001)':
            new_str = ' -cs 2'
        elif chron_sys.value == 'Moon, Hartmann 2010 iteration':
            new_str = ' -cs 3'
        elif chron_sys.value == 'Moon, Yue et al. (2022)':
            new_str = ' -cs 4'
        elif chron_sys.value == 'Mars, Neukum-Ivanov (2001)':
            new_str = ' -cs 5'
        elif chron_sys.value == 'Mars, Ivanov (2001)':
            new_str = ' -cs 6'
        elif chron_sys.value == 'Mars, Hartmann 2004 iteration':
            new_str = ' -cs 7'
        elif chron_sys.value == 'Mars, Hartmann & Daubar (2016)':
            new_str = ' -cs 8'
        elif chron_sys.value == 'Mercury, Strom & Neukum (1988)':
            new_str = ' -cs 9'
        elif chron_sys.value == 'Mercury, Neukum et al. (2001)':
            new_str = ' -cs 10'
        elif chron_sys.value == 'Mercury, Le Feuvre and Wieczorek 2011 non-porous':
            new_str = ' -cs 11'
        elif chron_sys.value == 'Mercury, Le Feuvre and Wieczorek 2011 porous':
            new_str = ' -cs 12'
        elif chron_sys.value == 'Vesta, Rev4, Schmedemann et al (2014)':
            new_str = ' -cs 13'
        elif chron_sys.value == 'Vesta, Rev3, Schmedemann et al (2014)':
            new_str = ' -cs 14'
        elif chron_sys.value == 'Vesta, Marchi & O\'Brien (2014)':
            new_str = ' -cs 15'
        elif chron_sys.value == 'Ceres, Hiesinger et al. (2016)':
            new_str = ' -cs 16'
        elif chron_sys.value == 'Ida, Schmedemann et al (2014)':
            new_str = ' -cs 17'
        elif chron_sys.value == 'Gaspra, Schmedemann et al (2014)':
            new_str = ' -cs 18'
        elif chron_sys.value == 'Lutetia, Schmedemann et al (2014)':
            new_str = ' -cs 19'
        elif chron_sys.value == 'Phobos, Case A - SOM, Schmedemann et al (2014)':
            new_str = ' -cs 20'
        elif chron_sys.value == 'Phobos, Case B - MBA, Schedemann et al (2014)':
            new_str = ' -cs 21'

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

        chron_sys_str = ''
        equil_func_str = ''
        epoch_str = ''
        title_str = ''
        subtitle_str = ''
        plot_view_str = ''
        xrange_str = ''
        yrange_str = ''
        iso_str = ''
        show_iso_str = ''
        legend_str = ''
        cite_function_str = ''
        mu_str = ''
        style_str = ''
        print_dim_str = ''
        pt_size_str = ''
        p_str = ''

        cmd_line_str = ''

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

        cmd_line_str = (f'craterstats{chron_sys_str if chron_sys_str is not None else ""}'
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
                        f'{p_str if p_str is not None else ""}')

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

            '-ep 1'
        """

        new_str = ''

        if epoch.value == 'Moon, Wilhelms (1987)':
            new_str = ' -ep 1'

        elif epoch.value == 'Mars, Michael (2013)':
            new_str = ' -ep 2'

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

            '-ef 1'
        """
        new_str = ''

        if equil_func.value == 'Standard lunar equilibrium (Trask, 1966)':
            new_str = ' -ef 1'
        elif equil_func.value == 'Hartmann (1984)':
            new_str = ' -ef 2'

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
        new_str = f' -isochrons {iso_text.value}'

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
        new_str = ''

        if source_file_entry.value or plot_fit_options.value or error_bars.value or hide_button.value or color_dropdown.value or symbol_dropdown.value or binning_options.value or align_left.value or display_age.value:

            new_str += ' -p '

            if source_file_entry.value:
                new_str += f"source={source_file_entry.value},"

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

        return new_str

    def set_plot_info(e):
        """Sets plotsetting info for subplots

        Changes the settings on the Plot Settings tab depending on which subplot is
        selected

        Args:
            e: EventHandler

        Returns:
            none
        """

        correct_key = ''

        # print(e.control.label.value)
        for key, val in plots_dict.items():
            # print(val)

            try:
                try:
                    if val["plot1.name"] == e.control.label.value:
                        # print("Plot1 Name Found")
                        correct_key = key
                except KeyError:
                    pass
                try:
                    if val["plot2.name"] == e.control.label.value:
                        # print("Plot2 Name Found")
                        correct_key = key
                except KeyError:
                    pass
                try:
                    if val["plot3.name"] == e.control.label.value:
                        # print("Plot3 Name Found")
                        correct_key = key
                except KeyError:
                    pass
            except KeyError:
                print("No values")

        source_file_entry.value = plots_dict[correct_key][f"{correct_key}.source"]

        range_start = float(plots_dict[correct_key][f"{correct_key}.range"][0])
        range_end = float(plots_dict[correct_key][f"{correct_key}.range"][1])
        range_val = ''

        print(range_start, range_end, type(range_start), type(range_end))

        if range_start < 1:

            if range_end < 1:

                range_val = f"[{int(range_start * 100)} m, {int(range_end * 100)} m]"

            else:
                range_val = f"[{int(range_start * 100)} m, {int(range_end)} km]"

        else:
            range_val = f"[{int(range_start)} km, {int(range_end)} km]"

        diam_range_entry.value = range_val.strip("[]")

        plot_options = plots_dict[correct_key][f"{correct_key}.type"]

        if plot_options == "data":
            plot_fit_options.value = "crater count"

        elif plot_options == "diff_fit":
            plot_fit_options.value = "differential fit"

        elif plot_options == "cumu_fit":
            plot_fit_options.value = "cumulative fit"

        elif plot_options == "poisson":
            plot_fit_options.value = "Poisson pdf"

        elif plot_options == "poisson_buffer":
            plot_fit_options.value = "Poisson buffer pdf"

        error_bars.value = plots_dict[correct_key][f"{correct_key}.error_bars"]

        hide_button.value = plots_dict[correct_key][f"{correct_key}.hide"]

        color_dropdown.value = colours[int(
            plots_dict[correct_key][f"{correct_key}.colour"])]

        symbol_dropdown.value = symbols[int(
            plots_dict[correct_key][f"{correct_key}.psym"])]

        binning_options.value = plots_dict[correct_key][f"{correct_key}.binning"]
        binning_options.options = [ft.dropdown.Option(
            plots_dict[correct_key][f"{correct_key}.binning"])]

        align_left.value = plots_dict[correct_key][f"{correct_key}.age_left"]

        display_age.value = plots_dict[correct_key][f"{correct_key}.display_age"]

        plot_fit_text.value = plots_dict[correct_key][f"{correct_key}.name"]

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
        new_str = ''

        if plot_view.value == "cumulative":
            new_str = ' -pr cumulative'
        elif plot_view.value == "differential":
            new_str = ' -pr differential'
        elif plot_view.value == "R-plot":
            new_str = ' -pr R-plot'
        elif plot_view.value == "Hartmann":
            new_str = ' -pr Hartmann'
        elif plot_view.value == "chronology":
            new_str = ' -pr chronology'
        elif plot_view.value == "rate":
            new_str = ' -pr rate'

        return new_str

    def set_print_dim_str():
        """Sets print dimension command line string.

        Sets the command line string for the print dimenstion that is selected
        in the application

        Args:
            none
        Returns:
            A string corresponding to the command line applications equivalent option
            Example:

            '-print_dim {7.5x7.5}'
        """
        new_str = f' -print_dim {print_scale_entry.value if len(print_scale_entry.value) == 1 else f"{{{print_scale_entry.value}}}"}'

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

        new_str = f' -pt_size {text_size.value}'

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

        new_str = f' -style {style_options.value}'

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

        new_str = f' -subtitle {subtitle_entry.value}'

        if subtitle_checkbox.value and subtitle_entry.value != '':
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

        if title_checkbox.value and title_entry.value != '':
            return new_str

        return None

    def toggle_demo(e):

        command_dict = {}

        loading = loading_circle()

        cli.demo()

        command_dict = parse_demo_commands(PATH + "/../demo/")

        loading.open = False
        page.update()
        demo = demo_view(command_dict)

        Globals.demo_mode = False

    def update_config_dict():
        config = {
            "set": [],
            "plot": []
        }

        config["set"].append({
            "chronology_system": chron_sys.value,
            "epochs": epoch.value,
            "equilibrium": equil_func.value,
            "isochrons": iso_text.value,
            "mu": mu_legend.value,
            "presentation": plot_view.value,
            "print_dimensions": print_scale_entry.value,
            "pt_size": text_size.value,
            "randomness": rand_legend.value,
            "ref_diameter": ref_diam.value,
            "sig_figs": sf_legend.value,
            "show_isochrons": show_iso.value,
            "show_subtitle": subtitle_checkbox.value,
            "show_title": title_checkbox.value,
            "style": style_options.value,
            "subtitle": subtitle_entry.value,
            "title": title_entry.value
        })

        config["plot"].append({
            "source": source_file_entry.value,
            "name": plot_fit_text.value,
            "range": diam_range_entry.value.split(","),
            "type": plot_fit_options.value,
            "error_bars": error_bars.value,
            "hide": hide_button.value,
            "colour": color_dropdown.value,
            "psym": symbol_dropdown.value,
            "binning": binning_options.value,
            "age_left": align_left.value,
            "display_age": display_age.value
        })

        Globals.template_dict = config

    """
    Default Settings for the application
    """
    page.title = 'Craterstats IV'  # Application title
    page.theme_mode = ft.ThemeMode.DARK  # Flet Default dark theme
    page.window.width = 1920  # Application width
    page.window.height = 1080  # Application Height
    page.window.resizable = True  # Application size is static
    page.window.left = 0    # Set the window position to the leftmost side
    page.window.top = 0
    # Fonts that can be used inside the application
    page.fonts = {
        "Courier New": "Fonts/Courier New.ttf",
        "Nasa": "Fonts/nasalization-rg.otf",
        "Arial": "Fonts/Arial Unicode.ttf"
    }
    # Default font for the application
    page.theme = ft.Theme(font_family="Arial")
    page.update()

    """
    Start of FLET GUI options
    """
    # This sets up an event listener for window resizing
    page.on_resize = on_resize

    pick_files_dialog = ft.FilePicker(on_result=file_picker_result)

    page.overlay.append(pick_files_dialog)

    save_file_dialog = ft.FilePicker(on_result=save_image)

    page.overlay.append(save_file_dialog)

    # Plot view Radio options
    plot_view = ft.RadioGroup(ft.Row([
        ft.Radio(value="cumulative", label="Cumulative"),
        ft.Radio(value="differential", label="Differential"),
        ft.Radio(value="R-plot", label="Relative (R)"),
        ft.Radio(value="Hartmann", label="Hartmann"),
        ft.Radio(value="chronology", label="Chronology"),
        ft.Radio(value='rate', label="Rate")
    ]),
        value="differential",
        on_change=lambda e:  (update_config_dict(), run_plot_async())
    )

    # Celestial body fropdown options
    body = ft.Dropdown(
        width=500,
        options=[ft.dropdown.Option("Moon"),
                 ft.dropdown.Option("Mars"),
                 ft.dropdown.Option("Mercury"),
                 ft.dropdown.Option("Vesta"),
                 ft.dropdown.Option("Ceres"),
                 ft.dropdown.Option("Ida"),
                 ft.dropdown.Option("Gaspra"),
                 ft.dropdown.Option("Lutetia"),
                 ft.dropdown.Option("Phobos")],
        label="Body",
        value="Moon",
        dense=True,
        on_change=lambda e: (set_chron_sys(None, e),
                             update_config_dict(), run_plot_async())
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
        on_change=lambda e: (set_chron_func(None, e),
                             update_config_dict(), run_plot_async())
    )

    # Chronology Function Dropdown options
    chron_func = ft.Dropdown(
        width=500,
        label="Chronology Function",
        value="Moon, Neukum (1983)",
        options=[ft.dropdown.Option("Moon, Neukum (1983)"), ],
        dense=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Production function dropdown options
    prod_func = ft.Dropdown(
        width=500,
        label="Production Function",
        value="Moon, Neukum (1983)",
        options=[ft.dropdown.Option("Moon, Neukum (1983)"), ],
        dense=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
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
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Equilibrium function dropdown options
    equil_func = ft.Dropdown(
        width=500,
        label="Equilibrium Function",
        value="none",
        options=[
            ft.dropdown.Option("none"),
            ft.dropdown.Option(
                "Standard lunar equilibrium (Trask, 1966)"),
            ft.dropdown.Option("Hartmann (1984)"),
        ],
        dense=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Isochron text field
    iso_text = ft.TextField(
        width=150,
        dense=True,
        bgcolor=ft.colors.GREY_900,
        on_blur=lambda e: (update_config_dict(), run_plot_async())
    )

    # Isochron Label
    iso_label = ft.Checkbox(
        label="Isochrons, Ga",
        value=False,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Data legend checkbox
    data_legend = ft.Checkbox(
        label="Data",
        value=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Fit legend checkbox
    fit_legend = ft.Checkbox(
        label="Fit",
        value=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Function legend checkbox
    func_legend = ft.Checkbox(
        label="Functions",
        value=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # 3sf legend checckbox
    sf_legend = ft.Checkbox(
        label="3sf",
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # randomness legend checkbox
    rand_legend = ft.Checkbox(
        label="Randomness",
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Mu legend checkbox
    mu_legend = ft.Checkbox(
        label="µ notation",
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Reference Diameter text field
    ref_diam = ft.TextField(
        width=50, dense=True, bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # Reference Diameter label
    ref_diam_lbl = ft.Text("Ref diameter,km")

    # Axis Log D Textfield
    axis_d_input_box = ft.TextField(
        width=75, dense=True, value="-3.2", bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # Axis y TextField
    axis_y_input_box = ft.TextField(
        width=50, dense=True, value="5.5", bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # Auto Axis button
    axis_auto_button = ft.ElevatedButton(
        text="Auto", width=80, on_click=lambda e: (update_config_dict(), run_plot_async()))

    # Style options dropdown
    style_options = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("natural"),
            ft.dropdown.Option("root-2"),
        ],
        value="natural",
        dense=True,
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Title entry textfield
    title_entry = ft.TextField(expand=True, dense=True, content_padding=ft.padding.all(8),
                               bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # Title checkbox
    title_checkbox = ft.Checkbox(
        label="Title", value=True, on_change=lambda e: (update_config_dict(), run_plot_async()))

    # Print scale textfield
    print_scale_entry = ft.TextField(dense=True, value="7.5x7.5", content_padding=ft.padding.all(8),
                                     bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # Subtitle entry textfield
    subtitle_entry = ft.TextField(dense=True, content_padding=ft.padding.all(8),
                                  bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # subtitle checkbox
    subtitle_checkbox = ft.Checkbox(
        label="Subtitle", value=True, on_change=lambda e: (update_config_dict(), run_plot_async()))

    # Font size textfield
    text_size = ft.TextField(dense=True, value="8", bgcolor=ft.colors.GREY_900, content_padding=ft.padding.all(8),
                             on_blur=lambda e: (update_config_dict(), run_plot_async()) or print(text_size.value) or print(type(text_size.value)))

    # Plot lists list view
    plot_lists = ft.ListView(
        height=250,
        width=250,
        item_extent=30,
        spacing=10,
        padding=10,
        controls=[ft.Chip(ft.Text("default"),
                          on_click=lambda e: (update_config_dict(), run_plot_async()))],
        first_item_prototype=True,
    )

    # Plot list container
    plot_lists_container = ft.Container(
        content=plot_lists,
        border=ft.border.all(2, ft.colors.WHITE),
        alignment=ft.alignment.top_left
    )

    """Plot Lists buttons"""
    new_button = ft.ElevatedButton(text="New", width=115)

    duplicate_button = ft.ElevatedButton(text="Duplicate", width=115)

    delete_button = ft.ElevatedButton(text="Delete", width=115)

    up_button = ft.ElevatedButton(text="Up", width=115)

    down_button = ft.ElevatedButton(text="Down", width=115)

    # Plot fit text field
    plot_fit_text = ft.TextField(width=300, dense=True, value="Default",
                                 bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

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
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Hide Button
    hide_button = ft.Checkbox(label="Hide plot", value=False)

    # Source file label
    source_file_label = ft.Text("Source file:")

    # Source file textfield
    source_file_entry = ft.TextField(
        width=500, dense=True, read_only=True, bgcolor=ft.colors.GREY_900)

    # File Browse button
    browse_button = ft.ElevatedButton(
        text="Browse...", width=115, on_click=lambda _: pick_files_dialog.pick_files())

    # Diameter Range textfield
    diam_range_entry = ft.TextField(
        width=150, dense=True, value="0.0", bgcolor=ft.colors.GREY_900, on_blur=lambda e: (update_config_dict(), run_plot_async()))

    # Plot point color dropdown
    color_dropdown = ft.Dropdown(
        dense=True,
        width=120,
        options=[
            ft.dropdown.Option("Black"),
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Yellow"),
            ft.dropdown.Option("Violet"),
            ft.dropdown.Option("GREY_900"),
            ft.dropdown.Option("Brown"),
            ft.dropdown.Option("Orange"),
            ft.dropdown.Option("Pink"),
            ft.dropdown.Option("Purple"),
            ft.dropdown.Option("Teal"),
        ],
        value="Black",
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    # Plot point color symbol
    symbol_dropdown = ft.Dropdown(
        dense=True,
        width=210,
        options=[
            ft.dropdown.Option("Square"),
            ft.dropdown.Option("Circle"),
            ft.dropdown.Option("Star"),
            ft.dropdown.Option("Triangle"),
            ft.dropdown.Option("Diagonal cross"),
            ft.dropdown.Option("Cross"),
            ft.dropdown.Option("Point"),
            ft.dropdown.Option("Inverted triangle"),
            ft.dropdown.Option("Filled square"),
            ft.dropdown.Option("Filled circle"),
            ft.dropdown.Option("Filled star"),
            ft.dropdown.Option("Filled triangle"),
            ft.dropdown.Option("Filled inverted triangle"),
        ],
        value='Square',
        on_change=lambda e: (update_config_dict(), run_plot_async())
    )

    """PLOT SETTINGS OPTIONS"""
    error_bars = ft.Checkbox(
        label="Error bars", value=True, on_change=lambda e: (update_config_dict(), run_plot_async()))

    display_age = ft.Checkbox(
        label="Display age", value=True, on_change=lambda e: (update_config_dict(), run_plot_async()))

    align_left = ft.Checkbox(label="Align age left",
                             on_change=lambda e: (update_config_dict(), run_plot_async()))

    show_iso = ft.Checkbox(label="Show isochron", value=True,
                           on_change=lambda e: (update_config_dict(), run_plot_async()))

    plot_fit_error = ft.Checkbox(
        label="Plot fit", value=True, on_change=lambda e: (update_config_dict(), run_plot_async()))

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
        value='pseudo-log',
        on_change=lambda e: (update_config_dict(), run_plot_async())
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
            ft.Row([iso_text, iso_label]),
            ft.Row([data_legend, fit_legend, func_legend,
                    sf_legend, rand_legend, mu_legend, ref_diam, ref_diam_lbl]),
            ft.Row([
                ft.Text("Axes. log D:"),
                axis_d_input_box,
                ft.Text("log y:"),
                axis_y_input_box,
                axis_auto_button
            ]),
            ft.Row([
                ft.Text("Style:"),
                style_options
            ])
        ]
    )

    # Plot settings tab container
    plot_settings = ft.Column([
        ft.Text(),
        ft.GridView(
            runs_count=5,
            child_aspect_ratio=5.0,
            controls=[
                title_entry,
                title_checkbox,
                ft.VerticalDivider(),
                ft.Text("Print scale. cm/decade (or plot width x height. cm):",
                        style=ft.TextStyle(height=1, size=11)),
                print_scale_entry,
                subtitle_entry,
                subtitle_checkbox,
                ft.VerticalDivider(),
                ft.Text("Text size. pt:"),
                text_size,
            ],
            spacing=20

        ),
        ft.Row([
            plot_lists_container,
            ft.Column([
                new_button,
                duplicate_button,
                delete_button,
            ]),
            ft.Column([
                up_button,
                down_button,
            ])
        ]),
        ft.Divider(),
        ft.Row([
            plot_fit_text,
            plot_fit_options,
            hide_button,
        ]),
        ft.Row([
            source_file_label,
            source_file_entry,
            browse_button
        ]),
        ft.Row([
            ft.Text("Diameter range:"),
            diam_range_entry,
            ft.Text("Binning"),
            binning_options
        ]),
        ft.Row([
            ft.Text("Colour"),
            color_dropdown,
            ft.Text("Symbol"),
            symbol_dropdown
        ]),
        ft.Column([
            ft.Row([
                error_bars,
                display_age,
                align_left,
                show_iso,
                plot_fit_error,
            ]),
        ])
    ])

    # plot image
    plot_image = ft.Image(
        src="/plots/blank_plot.png",
        height=page.window.height * 0.55,
        width=page.window.width * 0.55,
        fit=ft.ImageFit.CONTAIN
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
                                read_only=True
                            ),

                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Bin"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True
                            ),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("n"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True
                            ),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("y"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True
                            ),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Age"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True
                            ),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("N(1)"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True
                            ),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("a0"),
                            ft.TextField(
                                width=100,
                                dense=True,
                                bgcolor=ft.colors.GREY_900,
                                read_only=True
                            ),
                        ]
                    )
                ]
            ),
            plot_image,
            cmd_str
        ]

    )

    # Tabs
    tabs = ft.Tabs(
        selected_index=1,
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
        on_change=lambda _: (set_cmd_line_str(),
                             update_config_dict(), run_plot_async())
    )

    # FILE|PLOT|EXPORT|UTILITIES Menu bar
    menubar = ft.MenuBar(
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            mouse_cursor={ft.MaterialState.HOVERED: ft.MouseCursor.WAIT,
                          ft.MaterialState.DEFAULT: ft.MouseCursor.ZOOM_OUT},
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Open"),
                        leading=ft.Icon(ft.icons.FILE_UPLOAD),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=lambda _: pick_files_dialog.pick_files()
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Close"),
                        leading=ft.Icon(ft.icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=lambda _: page.window_close()
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Plot"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("New"),
                        leading=ft.Icon(ft.icons.NEW_LABEL)
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Duplicate"),
                        leading=ft.Icon(ft.icons.CONTROL_POINT_DUPLICATE)
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Delete"),
                        leading=ft.Icon(ft.icons.DELETE)
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Export"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Image"),
                        leading=ft.Icon(ft.icons.IMAGE),
                        on_click=lambda _: save_file_dialog.save_file(
                            dialog_title="Save the image",
                            file_type="image/png")
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Summary file"),
                        leading=ft.Icon(ft.icons.FILE_DOWNLOAD)
                    ),
                    ft.MenuItemButton(
                        content=ft.Text(".stat table"),
                        leading=ft.Icon(ft.icons.TABLE_CHART)
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Utilities"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Demo"),
                        leading=ft.Icon(ft.icons.PLAY_ARROW_ROUNDED),
                        on_click=lambda e: (setattr(
                            Globals, 'demo_mode', True), update_config_dict(), run_plot_async())
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("sum .stat files"),
                        leading=ft.Icon(ft.icons.ADD)
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("merge .diam files"),
                        leading=ft.Icon(ft.icons.MERGE)
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("randomness analysis"),
                        leading=ft.Icon(ft.icons.ANALYTICS)
                    )
                ]
            ),
            ft.MenuItemButton(
                content=ft.Text("About"),
                on_click=open_about_dialog
            )
        ]
    )

    print(Globals.demo_mode)

    two_column_layout = ft.Row(
        controls=[
            ft.Container(
                content=tabs,
                expand=2,
                width=page.window.width * 0.5
            ),
            ft.Container(
                content=plot_image if not Globals.demo_mode else None,
                expand=2,
                width=page.window.width * 0.5
            ),
        ],
        expand=True
    )

    bottom_row = ft.Row(
        controls=[cmd_str],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    page_layout = ft.Column(
        controls=[
            two_column_layout,
            ft.Divider(),
            bottom_row
        ],
        expand=True
    )

    page.add(menubar)
    page.add(page_layout)

    page.on_keyboard_event = handle_keypress_events


ft.app(target=main, assets_dir="assets")

delete_temp_plots(PATH + "/assets/plots/", ['png', 'jpg', 'pdf', 'svg', 'tif'])
delete_temp_plots(PATH + "/../demo/", None)
