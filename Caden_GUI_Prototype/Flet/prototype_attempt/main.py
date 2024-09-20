import flet as ft
from flet import FilePickerResultEvent
from Globals import *



# DEBUG FUNCTION
def print_tree(dictionary, indent=0):
    for key, value in dictionary.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            print_tree(value, indent + 1)
        else:
            print('  ' * (indent + 1) + str(value))

"""Main Function - EVERYTHING FLET IS INSIDE THIS FUNCTION"""
def main(page: ft.Page):





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
                           "Craterstats Program developped by Michael G.G",
                           "Version: 0.1",
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
        count = 0

        data = open(e.files[0].path)

        # Reads through each line of data and sets data based off of line
        for line in data:
            specifics = line.split("=")
            if len(specifics) == 1:
                count += 1
                continue

            if specifics[0] == 'set.body':
                body_val = specifics[1][1:-2]

            if specifics[0] == 'set.chronology':
                chron_func_val = specifics[1][1:-2]

            if specifics[0] == 'set.epochs':
                epochs_val = specifics[1][1:-2]

            if specifics[0] == 'set.equilibrium':
                equilibrium_val = specifics[1][1:-2]

            if specifics[0] == 'set.isochrons':
                isochrons_val = specifics[1][1:-2]
                if isochrons_val is not None:
                    iso_label.value = True

            if specifics[0] == "set.legend_data":
                if specifics[1] == '0':
                    data_legend.value = False
                else:
                    data_legend.value = True

            if specifics[0] == "set.legend_fit":
                if specifics[1] == '0':
                    fit_legend.value = False
                else:
                    fit_legend.value = True

            if specifics[0] == "set.mu":
                if specifics[1] == '0':
                    mu_legend.value = False
                else:
                    mu_legend.value = True

            if specifics[0] == 'set.production':
                prod_func_val = specifics[1][1:-2]

            if specifics[0] == 'set.presentation':
                presentation_val = specifics[1][1:-
                2].replace("'", "")[:4].lower()

            if specifics[0] == 'set.print_dimensions':
                print_dimensions = (specifics[1].replace(
                    "'", "").strip("[]\n").split(","))[0]

            if specifics[0] == 'set.pt_size':
                pt_list = specifics[1].strip("[]\n").split(",")
                pt_list = [eval(i) for i in pt_list]
                font_pt = str(max(pt_list))

            if specifics[0] == "set.randomness":
                if specifics[1] == '0':
                    rand_legend.value = False
                else:
                    rand_legend.value = True

            if specifics[0] == "set.ref_diam":
                ref_diam.value = specifics[1]

            if specifics[0] == "set.sf":
                if specifics[1] == '3':
                    sf_legend.value = True
                else:
                    sf_legend.value = False

            if specifics[0] == "set.show_isocrhons":
                if specifics[1] == '0':
                    show_iso.value = False
                else:
                    show_iso.value = True

            if specifics[0] == "set.show_legend_area":
                pass

            if specifics[0] == "set.show_title":
                if int(specifics[1]) == 1:
                    title_checkbox.value = True
                else:
                    title_checkbox.value = False
                    title_entry.read_only = True

            if specifics[0] == "set.show_subtitle":
                if int(specifics[1]) == 1:
                    subtitle_checkbox.value = True

                else:
                    subtitle_checkbox.value = False
                    subtitle_entry.read_only = True

            if specifics[0] == "set.style":
                print(specifics[1][1:-2])
                style_options.value = specifics[1][1:-2]

            if specifics[0] == "set.title":
                title_entry.value = specifics[1][1:-2]

            if specifics[0] == "set.subtitle":
                subtitle_entry.value = specifics[1][1:-2]

            if specifics[0] == f"plot{count}.source":
                plots_dict[f"plot{count}"] = {}
                plots_dict[f"plot{count}"][f"plot{count}.source"] = specifics[1][1:-2]

            if specifics[0] == f"plot{count}.name":
                plots_dict[f"plot{count}"][f"plot{count}.name"] = specifics[1][1:-2]

            if specifics[0] == f"plot{count}.range":
                float_list = specifics[1].strip("[]\n").split(",")
                float_list = [eval(i) for i in float_list]
                plots_dict[f"plot{count}"][f"plot{count}.range"] = float_list

            if specifics[0] == f"plot{count}.type":
                plots_dict[f"plot{count}"][f"plot{count}.type"] = specifics[1][1:-2]

            if specifics[0] == f"plot{count}.error_bars":

                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.error_bars"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.error_bars"] = False

            if specifics[0] == f"plot{count}.hide":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.hide"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.hide"] = False

            if specifics[0] == f"plot{count}.linestyle":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.linestyle"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.linestyle"] = False

            if specifics[0] == f"plot{count}.colour":
                plots_dict[f"plot{count}"][f"plot{count}.colour"] = specifics[1]

            if specifics[0] == f"plot{count}.psym":
                plots_dict[f"plot{count}"][f"plot{count}.psym"] = specifics[1]

            if specifics[0] == f"plot{count}.binning":
                plots_dict[f"plot{count}"][f"plot{count}.binning"] = specifics[1][1:-2]

            if specifics[0] == f"plot{count}.age_left":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.age_left"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.age_left"] = False

            if specifics[0] == f"plot{count}.display_age":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.display_age"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.display_age"] = False

            if specifics[0] == f"plot{count}.resurf":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.resurf"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.resurf"] = False

            if specifics[0] == f"plot{count}.resurf_showall":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.resurf"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.resurf"] = False

            if specifics[0] == f"plot{count}.smooth":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.smooth"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.smooth"] = False

            if specifics[0] == f"plot{count}.width":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.width"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.width"] = False

            if specifics[0] == f"plot{count}.fiterr":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.fiterr"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.fiterr"] = False

            if specifics[0] == f"plot{count}.isochron":
                if int(specifics[1]) == 1:
                    plots_dict[f"plot{count}"][f"plot{count}.isochron"] = True
                else:
                    plots_dict[f"plot{count}"][f"plot{count}.isochron"] = False

            if specifics[0] == f"plot{count}.offset":
                int_list = specifics[1].strip("[]\n").split(",")
                int_list = [eval(i) for i in int_list]
                plots_dict[f"plot{count}"][f"plot{count}.offset"] = int_list

            if specifics[0] == f"plot{count}.offset_age":
                int_list = specifics[1].strip("[]\n").split(",")
                int_list = [eval(i) for i in int_list]
                plots_dict[f"plot{count}"][f"plot{count}.offset_age"] = int_list

        # print_tree(plots_dict, 0)
        body.value = body_val
        set_chron_sys(body.value, None)
        chron_sys.value = list(chron_systems.keys())[list(
            chron_systems.values()).index([chron_func_val, prod_func_val])]
        chron_func.value = chron_func_val
        chron_func.options = [ft.dropdown.Option(chron_func_val)]
        prod_func.value = prod_func_val
        prod_func.options = [ft.dropdown.Option(prod_func_val)]
        iso_text.value = isochrons_val
        equil_func.value = equilibrium_val
        epoch.value = epochs_val
        plot_view.value = presentation_val
        print_scale_entry.value = print_dimensions
        text_size.value = font_pt

        create_plot_lists()

        page.update()
        data.close()

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
                    ft.Chip(ft.Text(plot_names[plots]), on_click=set_plot_info))

        print(plot_lists.controls)
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

        print(e.control.label.value)
        for key, val in plots_dict.items():
            print(val)

            try:
                try:
                    if val["plot1.name"] == e.control.label.value:
                        print("Plot1 Name Found")
                        correct_key = key
                except KeyError:
                    pass
                try:
                    if val["plot2.name"] == e.control.label.value:
                        print("Plot2 Name Found")
                        correct_key = key
                except KeyError:
                    pass
                try:
                    if val["plot3.name"] == e.control.label.value:
                        print("Plot3 Name Found")
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

        color_dropdown.value = colours[int(plots_dict[correct_key][f"{correct_key}.colour"])]

        symbol_dropdown.value = symbols[int(plots_dict[correct_key][f"{correct_key}.psym"])]

        binning_options.value = plots_dict[correct_key][f"{correct_key}.binning"]
        binning_options.options = [ft.dropdown.Option(plots_dict[correct_key][f"{correct_key}.binning"])]

        align_left.value = plots_dict[correct_key][f"{correct_key}.age_left"]

        display_age.value = plots_dict[correct_key][f"{correct_key}.display_age"]

        plot_fit_text.value = plots_dict[correct_key][f"{correct_key}.name"]

        page.update()


    """
    Default Settings for the application
    """
    page.title = 'Craterstats IV' # Application title
    page.theme_mode = ft.ThemeMode.DARK # Flet Default dark theme
    page.window.width = 1200 # Application width
    page.window.height = 900 # Application Height
    page.window.resizable = False #Application size is static
    # Fonts that can be used inside the application
    page.fonts = {
        "Courier New": "DearPyGUI_Attempt\\Fonts\\Courier New.ttf",
        "Nasa": "DearPyGUI_Attempt\\Fonts\\nasalization-rg.otf",
        "Arial": "DearPyGUI_Attempt\\Fonts\\Arial Unicode.ttf"
    }
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
        xrange_str = set_xrange_str()
        yrange_str = set_yrange_str()
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

        match chron_sys.value:

            case 'Moon, Neukum (1983)':
                new_str = ' -cs 1'
            case 'Moon, Neukum et al. (2001)':
                new_str = ' -cs 2'
            case 'Moon, Hartmann 2010 iteration':
                new_str = ' -cs 3'
            case 'Moon, Yue et al. (2022)':
                new_str = ' -cs 4'
            case 'Mars, Neukum-Ivanov (2001)':
                new_str = ' -cs 5'
            case 'Mars, Ivanov (2001)':
                new_str = ' -cs 6'
            case 'Mars, Hartmann 2004 iteration':
                new_str = ' -cs 7'
            case 'Mars, Hartmann & Daubar (2016)':
                new_str = ' -cs 8'
            case 'Mercury, Strom & Neukum (1988)':
                new_str = ' -cs 9'
            case 'Mercury, Neukum et al. (2001)':
                new_str = ' -cs 10'
            case 'Mercury, Le Feuvre and Wieczorek 2011 non-porous':
                new_str = ' -cs 11'
            case 'Mercury, Le Feuvre and Wieczorek 2011 porous':
                new_str = ' -cs 12'
            case 'Vesta, Rev4, Schmedemann et al (2014)':
                new_str = ' -cs 13'
            case 'Vesta, Rev3, Schmedemann et al (2014)':
                new_str = ' -cs 14'
            case 'Vesta, Marchi & O\'Brien (2014)':
                new_str = ' -cs 15'
            case 'Ceres, Hiesinger et al. (2016)':
                new_str = ' -cs 16'
            case 'Ida, Schedemann et al (2014)':
                new_str = ' -cs 17'
            case 'Gaspra, Schmedemann et al (2014)':
                new_str = ' -cs 18'
            case 'Lutetia, Schmedemann et al (2014)':
                new_str = ' -cs 19'
            case 'Phobos, Case A - SOM, Schmedemann et al (2014)':
                new_str = ' -cs 20'
            case 'Phobos, Case B - MBA, Schedemann et al (2014)':
                new_str = ' -cs 21'

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

        match equil_func.value:

            case 'Standard lunar equilibrium (Trask, 1966)':
                new_str = ' -ef 1'
            case 'Hartmann (1984)':
                new_str = ' -ef 2'

        return new_str

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

        match epoch.value:

            case 'Moon, Wilhelms (1987)':
                new_str = ' -ep 1'

            case 'Mars, Michael (2013)':
                new_str = ' -ep 2'

        return new_str

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

        if title_checkbox.value or title_entry.value != '':
            return new_str

        return None

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

        if subtitle_checkbox.value or subtitle_entry.value != '':
            return new_str

        return None

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

        match plot_view.value:

            case "cumu":
                new_str = ' -pr cumulative'
            case "diff":
                new_str = ' -pr differential'
            case "rela":
                new_str = ' -pr R-plot'
            case "hart":
                new_str = ' -pr Hartmann'
            case "chro":
                new_str = ' -pr chronology'
            case "rate":
                new_str = ' -pr rate'

        return new_str

    def set_xrange_str():
        return None

    def set_yrange_str():
        return None

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

    def set_legend_str():

        return None

    def set_cite_function_str():

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
        new_str = f' -print_dim {print_scale_entry.value if len(print_scale_entry.value) == 1 else f'{{{print_scale_entry.value}}}'}'

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

        return None

    def set_p_str():

        return None

    """
    Start of FLET GUI options
    """

    pick_files_dialog = ft.FilePicker(on_result=file_picker_result)

    page.overlay.append(pick_files_dialog)


    # Plot view Radio options
    plot_view = ft.RadioGroup(ft.Row([
        ft.Radio(value="cumu", label="Cumulative"),
        ft.Radio(value="diff", label="Differential"),
        ft.Radio(value="rela", label="Relative (R)"),
        ft.Radio(value="hart", label="Hartmann"),
        ft.Radio(value="chro", label="Chronology"),
        ft.Radio(value='rate', label="Rate")
    ]),
        value="diff"
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
        on_change=lambda e: set_chron_sys(None, e)
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
        on_change=lambda e: set_chron_func(None, e)
    )

    # Chronology Function Dropdown options
    chron_func = ft.Dropdown(
        width=500,
        label="Chronology Function",
        value="Moon, Neukum (1983)",
        options=[ft.dropdown.Option("Moon, Neukum (1983)"), ],
        dense=True
    )

    # Production function dropdown options
    prod_func = ft.Dropdown(
        width=500,
        label="Production Function",
        value="Moon, Neukum (1983)",
        options=[ft.dropdown.Option("Moon, Neukum (1983)"), ],
        dense=True

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
        dense=True

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
        dense=True
    )

    # Isochron text field
    iso_text = ft.TextField(
        width=150,
        dense=True
    )

    # Isochron Label
    iso_label = ft.Checkbox(
        label="Isochrons, Ga",
        value=False,
    )

    # Data legend checkbox
    data_legend = ft.Checkbox(
        label="Data",
        value=True,
    )

    # Fit legend checkbox
    fit_legend = ft.Checkbox(
        label="Fit",
        value=True,
    )

    # Function legend checkbox
    func_legend = ft.Checkbox(
        label="Functions",
        value=True,
    )

    #3sf legend checckbox
    sf_legend = ft.Checkbox(
        label="3sf",
    )

    # randomness legend checkbox
    rand_legend = ft.Checkbox(
        label="Randomness",
    )

    # Mu legend checkbox
    mu_legend = ft.Checkbox(
        label="µ notation"
    )

    # Reference Diameter text field
    ref_diam = ft.TextField(width=50, dense=True)

    # Reference Diameter label
    ref_diam_lbl = ft.Text("Ref diameter,km")

    # Axis Log D Textfield
    axis_d_input_box = ft.TextField(width=75, dense=True, value="-3.2")

    # Axis y TextField
    axis_y_input_box = ft.TextField(width=50, dense=True, value="5.5")

    # Auto Axis button
    axis_auto_button = ft.ElevatedButton(text="Auto", width=80)

    # Style options dropdown
    style_options = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("natural"),
            ft.dropdown.Option("root-2"),
        ],
        value="natural",
        dense=True
    )

    # Title entry textfield
    title_entry = ft.TextField(width=150, dense=True, text_vertical_align=0)

    # Title checkbox
    title_checkbox = ft.Checkbox(label="Title", value=True)

    # Print scale textfield
    print_scale_entry = ft.TextField(width=150, dense=True, value="7.5x7.5")

    # Subtitle entry textfield
    subtitle_entry = ft.TextField(width=150, dense=True, text_vertical_align=0)

    # subtitle checkbox
    subtitle_checkbox = ft.Checkbox(label="Subtitle", value=True)

    # Font size textfield
    text_size = ft.TextField(width=150, dense=True, value="8")

    # Plot lists list view
    plot_lists = ft.ListView(
        height=250,
        width=250,
        item_extent=30,
        spacing=10,
        padding=10,
        controls=[ft.Chip(ft.Text("default"))],
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
    plot_fit_text = ft.TextField(width=300, dense=True, value="Default")

    # Plot fit dropdown
    plot_fit_options = ft.Dropdown(
        width=200,
        dense=True,
        options=[
            ft.dropdown.Option("crater count"),
            ft.dropdown.Option("cumulative fit"),
            ft.dropdown.Option("differential fit"),
            ft.dropdown.Option("Poisson pdf"),
            ft.dropdown.Option("Poisson buffer pdf"),
        ],
        value="crater count"
    )

    # Hide Button
    hide_button = ft.Checkbox(label="Hide plot", value=False)

    # Source file label
    source_file_label = ft.Text("Source file:")

    # Source file textfield
    source_file_entry = ft.TextField(width=500, dense=True, read_only=True)

    # File Browse button
    browse_button = ft.ElevatedButton(
        text="Browse...", width=115, on_click=lambda _: pick_files_dialog.pick_files())

    # Diameter Range textfield
    diam_range_entry = ft.TextField(width=150, dense=True, value="0.0")

    # Plot point color dropdown
    color_dropdown = ft.Dropdown(
        dense=True,
        width=90,
        options=[
            ft.dropdown.Option("Black"),
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Yellow"),
            ft.dropdown.Option("Violet"),
            ft.dropdown.Option("Grey"),
            ft.dropdown.Option("Brown"),
            ft.dropdown.Option("Orange"),
            ft.dropdown.Option("Pink"),
            ft.dropdown.Option("Purple"),
            ft.dropdown.Option("Teal"),
        ],
        value="Black"
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
        value='Square'
    )

    """PLOT SETTINGS OPTIONS"""
    error_bars = ft.Checkbox(label="Error bars", value=True)

    display_age = ft.Checkbox(label="Display age", value=True)

    align_left = ft.Checkbox(label="Align age left")

    show_iso = ft.Checkbox(label="Show isochron", value=True)

    plot_fit_error = ft.Checkbox(label="Plot fit", value=True)

    # Binning options dropdown
    binning_options = ft.Dropdown(
        width=150,
        dense=True,
        options=[
            ft.dropdown.Option("psuedo-log"),
            ft.dropdown.Option("log"),
            ft.dropdown.Option("log"),
        ],
        value='psuedo-log',
    )

    # Default command line string
    cmd_str = ft.TextField(
        dense=True,
        value="-cs neukumivanov -title Differential plot -subtitle with two differential fit age evaluations -p source=%sample%/Pickering.scc,psym=o -p type=d-fit,range=[.2,.7],isochron=1 -p range=[2,5],colour=red",
        text_size=12,
        bgcolor=ft.colors.BLACK,
        color=ft.colors.WHITE,
        text_style=ft.TextStyle(font_family="Courier New"),
        width=1200
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
                ft.Text("Print scale. cm/decade (or plot width x height. cm):"),
                print_scale_entry,
                subtitle_entry,
                subtitle_checkbox,
                ft.VerticalDivider(),
                ft.Text("Text size. pt:"),
                text_size,
            ]),
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
        src="00-demo.png",
        height=500,
        width=500,
        fit=ft.ImageFit.CONTAIN
    )

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
                            ft.TextField(width=100, dense=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Bin"),
                            ft.TextField(width=100, dense=True,
                                         read_only=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("n"),
                            ft.TextField(width=100, dense=True,
                                         read_only=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("y"),
                            ft.TextField(width=100, dense=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Age"),
                            ft.TextField(width=100, dense=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("N(1)"),
                            ft.TextField(width=100, dense=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("a0"),
                            ft.TextField(width=100, dense=True),
                        ]
                    )
                ]
            ),
            plot_image,
            cmd_str
        ]

    )

    # Tabs 
    t = ft.Tabs(
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
            ft.Tab(
                text="Plot",
                icon=ft.icons.ADD_CHART,
                content=plot,
            ),
        ],
        expand=1,
        on_change=lambda _: set_cmd_line_str()
    )

    # FILE|PLOT|EXPORT|UTILITES Menu bar
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
                        leading=ft.Icon(ft.icons.IMAGE)
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

    page.add(menubar)
    page.add(t)

ft.app(target=main, assets_dir="assets")
