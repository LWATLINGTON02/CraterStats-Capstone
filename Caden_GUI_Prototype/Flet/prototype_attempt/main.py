import platform
import flet as ft
from flet import FilePickerResultEvent

chron_systems = {
    # Moon Systems
    "Moon, Neukum (1983)": ["Moon, Neukum (1983)",
                            "Moon, Neukum (1983)"],
    "Moon, Neukum et al. (2001)": ['Moon, Neukum et al. (2001)',
                                   'Moon, Neukum et al. (2001)'],
    # Mars systems
    "Mars, Neukum-Ivanov 2001": ['Mars, Hartmann & Neukum (2001)',
                                 'Mars, Ivanov (2001)'],
    "Mars, Ivanov 2001": ['Mars, Ivanov (2001)',
                          'Mars, Ivanov (2001)'],
    "Mars, Hartmann 2004 iteration": ['Mars, Hartmann (2005) [Michael (2013)]',
                                      'Mars, Hartmann (2005)'],
    "Mars, Hartmann & Daubar (2016)": ['Mars, Hartmann (2005) [Michael (2013)]',
                                       'Mars, Hartmann & Daubar (2016)'],
    # Mercury Systems
    "Mercury, Strom & Neukum (1988)": ['Mercury, Strom & Neukum (1988)',
                                       'Mercury, Strom & Neukum (1988)'],
    'Mercury, Neukum et al. (2001)': ['Mercury, Neukum et al. (2001)',
                                      'Mercury, Neukum et al. (2001)'],
    'Mercury, Le Feuvre and Wieczorek 2011 non-porous': ['Mercury, Le Feuvre and Wieczorek (2011) non-porous',
                                                         'Mercury, Le Feuvre and Wieczorek (2011) non-porous'],
    'Mercury, Le Feuvre and Wieczorek 2011 porous': ['Mercury, Le Feuvre and Wieczorek (2011) porous',
                                                     'Mercury, Le Feuvre and Wieczorek (2011) porous'],
    ### SMALL BODIES ###
    # Vesta
    'Vesta, Rev4, Schmedemann et al (2014)': ['Vesta, Rev4, Schmedemann et al (2014)',
                                              'Vesta, Rev4, Schmedemann et al (2014)'],
    'Vesta, Rev3, Schmedemann et al (2014)': ['Vesta, Rev3, Schmedemann et al (2014)',
                                              'Vesta, Rev3, Schmedemann et al (2014)'],
    "Vesta, Marchi & O'Brien (2014)": ["Vesta, O'Brien et al. (2014)",
                                       'Vesta, Marchi et al (2013) [inferred, NS]'],
    # Ceres
    'Ceres, Hiesinger et al. (2016)': ['Ceres, Hiesinger et al. (2016)',
                                       'Ceres, Hiesinger et al. (2016)'],

    # Ida
    'Ida, Schmedemann et al (2014)': ['Ida, Schmedemann et al (2014)',
                                      'Ida, Schmedemann et al (2014)'],

    # Gaspra
    'Gaspra, Schmedemann et al (2014)': ['Gaspra, Schmedemann et al (2014)',
                                         'Gaspra, Schmedemann et al (2014)'],

    # Lutetia
    'Lutetia, Schmedemann et al (2014)': ['Lutetia, Schmedemann et al (2014)',
                                          'Lutetia, Schmedemann et al (2014)'],

    # Phobos
    'Phobos, Case A - SOM, Schmedemann et al (2014)': ['Phobos, Case A - SOM, Schmedemann et al (2014)',
                                                       'Phobos, Case A - SOM, Schmedemann et al (2014)'],
    'Phobos, Case B - MBA, Schmedemann et al (2014)': ['Phobos, Case B - MBA, Schmedemann et al (2014)',
                                                       'Phobos, Case B - MBA, Schmedemann et al (2014)']

}

plots_dict = {}

def print_tree(dictionary, indent=0):
    for key, value in dictionary.items():
        print('  ' * indent + str(key))
        if isinstance(value, dict):
            print_tree(value, indent + 1)
        else:
            print('  ' * (indent + 1) + str(value))

def main(page: ft.Page):
    def file_picker_result(e: FilePickerResultEvent):
        count = 0

        data = open(e.files[0].path)

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
                presentation_val = specifics[1][1:-2].replace("'","")[:4].lower()

            if specifics[0] == 'set.print_dimensions':
                print_dimensions = (specifics[1].replace("'", "").strip("[]\n").split(","))[0]

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
                print(type(specifics[1]))

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
        chron_sys.value = list(chron_systems.keys())[list(chron_systems.values()).index([chron_func_val, prod_func_val])]
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

        if plots_dict is not None:
            plot_lists.clean()

            for index, plots in enumerate(plots_dict, 1):

                label_ = ft.Chip(label=ft.Text(plots[f"plot{index}.name"]))

    def set_plot_info():
        pass

    page.title = 'Craterstats IV'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1200
    page.window_height = 900
    page.window_resizable = False
    page.fonts = {
        "Courier New": "DearPyGUI_Attempt\\Fonts\\Courier New.ttf",
        "Nasa": "DearPyGUI_Attempt\\Fonts\\nasalization-rg.otf",
        "Arial": "DearPyGUI_Attempt\\Fonts\\Arial Unicode.ttf"
    }
    page.update()

    def handle_menu_item_click(e):
        print(f"{e.control.value}.on_click")
        page.show_snack_bar(ft.SnackBar(content=ft.Text(
            f"{e.control.value} was clicked!")))
        page.update()

    def handle_on_open(e):
        print(f"{e.control.value}.on_open")

    def handle_on_close(e):
        print(f"{e.control.value}.on_close")

    def handle_on_hover(e):
        print(f"{e.control.value}.on_hover")

    def set_chron_func(value, e):
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
                     ft.dropdown.Option('Mercury, Le Feuvre and Wieczorek 2011 non-porous'),
                     ft.dropdown.Option('Mercury, Le Feuvre and Wieczorek 2011 porous')]
            chron_func_str = 'Mercury, Strom & Neukum (1988)'
            prod_func_str = 'Mercury, Strom & Neukum (1988)'

        elif check_value == 'Vesta':
            items = [ft.dropdown.Option('Vesta, Rev4, Schmedemann et al (2014)'),
                     ft.dropdown.Option('Vesta, Rev3, Schmedemann et al (2014)'),
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

    pick_files_dialog = ft.FilePicker(on_result=file_picker_result)

    page.overlay.append(pick_files_dialog)

    plot_view = ft.RadioGroup(ft.Row([
        ft.Radio(value="cumu", label="Cumulative"),
        ft.Radio(value="diff", label="Differential"),
        ft.Radio(value="rela", label="Relative (R)"),
        ft.Radio(value="hart", label="Hartmann"),
        ft.Radio(value="chro", label="Chronology"),
    ]),
        value="diff"
    )

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

    chron_sys = ft.Dropdown(
        width=500,
        label="Chronology System",
        options=[
            ft.dropdown.Option("Moon, Neukum (1983)"),
            ft.dropdown.Option("Moon, Neukum et al. (2001)"),
        ],
        value="Moon, Neukum (1983)",
        dense=True,
        on_change=lambda e: set_chron_func(None, e)
    )

    chron_func = ft.Dropdown(
        width=500,
        label="Chronology Function",
        value="Moon, Neukum (1983)",
        options=[ft.dropdown.Option("Moon, Neukum (1983)"), ],
        dense=True
    )

    prod_func = ft.Dropdown(
        width=500,
        label="Production Function",
        value="Moon, Neukum (1983)",
        options=[ft.dropdown.Option("Moon, Neukum (1983)"), ],
        dense=True

    )

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

    iso_text = ft.TextField(
        width=150,
        dense=True
    )

    iso_label = ft.Checkbox(
        label="Isochrons, Ga",
        value=False,
    )

    data_legend = ft.Checkbox(
        label="Data",
        value=True,
    )

    fit_legend = ft.Checkbox(
        label="Fit",
        value=True,
    )

    func_legend = ft.Checkbox(
        label="Functions",
        value=True,
    )

    sf_legend = ft.Checkbox(
        label="3sf",
    )

    rand_legend = ft.Checkbox(
        label="Randomness",
    )

    mu_legend = ft.Checkbox(
        label="µ notation"
    )

    ref_diam = ft.TextField(width=50, dense=True)

    ref_diam_lbl = ft.Text("Ref diameter,km")

    axis_d_input_box = ft.TextField(width=75, dense=True, value="-3.2")

    axis_y_input_box = ft.TextField(width=50, dense=True, value="5.5")

    axis_auto_button = ft.ElevatedButton(text="Auto", width=80)

    style_options = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("natural"),
            ft.dropdown.Option("decadal"),
            ft.dropdown.Option("root-2"),
        ],
        value="natural",
        dense=True
    )

    title_entry = ft.TextField(width=150, dense=True, text_vertical_align=0)

    title_checkbox = ft.Checkbox(label="Title", value=True)

    print_scale_entry = ft.TextField(width=150, dense=True, value="7.5x7.5")

    subtitle_entry = ft.TextField(width=150, dense=True, text_vertical_align=0)

    subtitle_checkbox = ft.Checkbox(label="Subtitle", value=True)

    text_size = ft.TextField(width=150, dense=True, value="8")

    plot_lists = ft.Container(
        alignment=ft.alignment.top_left,
        bgcolor=ft.colors.WHITE60,
        content=ft.Chip(ft.Text("Default")),
        width=200,
        height=200,
        border_radius=10,
        border=ft.border.all(1, ft.colors.BLACK)
    )

    new_button = ft.ElevatedButton(text="New", width=115)

    duplicate_button = ft.ElevatedButton(text="Duplicate", width=115)

    delete_button = ft.ElevatedButton(text="Delete", width=115)

    up_button = ft.ElevatedButton(text="Up", width=115)

    down_button = ft.ElevatedButton(text="Down", width=115)

    plot_fit_text = ft.TextField(width=200, dense=True, value="Default")

    plot_fit_options = ft.Dropdown(
        width=200,
        dense=True,
        options=[
            ft.dropdown.Option("crater count"),
            ft.dropdown.Option("cumulative fit"),
            ft.dropdown.Option("differential fit"),
            ft.dropdown.Option("Poisson pdf"),
            ft.dropdown.Option("Poisson buffer pdf"),
        ]
    )

    hide_button = ft.Checkbox(label="Hide plot", value=False)

    source_file_label = ft.Text("Source file:")

    source_file_entry = ft.TextField(width=250, dense=True, read_only=True)

    browse_button = ft.ElevatedButton(text="Browse...", width=115, on_click=lambda _: pick_files_dialog.pick_files())

    diam_range_entry = ft.TextField(width=150, dense=True, value="0.0")

    color_dropdown = ft.Dropdown(
        dense=True,
        width=80,
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Black"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Yellow"),
        ],
        value="Black"
    )

    symbol_dropdown = ft.Dropdown(
        dense=True,
        width=100,
        options=[
            ft.dropdown.Option("Diamond"),
            ft.dropdown.Option("Square"),
            ft.dropdown.Option("Circle"),
        ],
        value='Square'
    )

    error_bars = ft.Checkbox(label="Error bars", value=True)

    display_age = ft.Checkbox(label="Display age", value=True)

    align_left = ft.Checkbox(label="Align age left")

    show_iso = ft.Checkbox(label="Show isochron", value=True)

    plot_fit_error = ft.Checkbox(label="Plot fit", value=True)

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
            plot_lists,
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

    print(platform.system())

    plot_image = ft.Image(
        src="00-demo.png",
        height=500,
        width=500,
        fit=ft.ImageFit.CONTAIN
    )

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
                            ft.TextField(width=100, dense=True, read_only=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("n"),
                            ft.TextField(width=100, dense=True, read_only=True),
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
            ft.TextField(
                dense=True,
                value="-cs neukumivanov -title Differential plot -subtitle with two differential fit age evaluations -p source=%sample%/Pickering.scc,psym=o -p type=d-fit,range=[.2,.7],isochron=1 -p range=[2,5],colour=red",
                text_size=12,
                bgcolor=ft.colors.BLACK,
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(font_family="Courier New"),
                width=1200
            )
        ]

    )

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
    )

    menubar = ft.MenuBar(
        style=ft.MenuStyle(
            alignment=ft.alignment.top_left,
            mouse_cursor={ft.MaterialState.HOVERED: ft.MouseCursor.WAIT,
                          ft.MaterialState.DEFAULT: ft.MouseCursor.ZOOM_OUT},
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                on_open=handle_on_open,
                on_close=handle_on_close,
                on_hover=handle_on_hover,
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.icons.SAVE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=handle_menu_item_click
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Open"),
                        leading=ft.Icon(ft.icons.FILE_UPLOAD),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=handle_menu_item_click
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Close"),
                        leading=ft.Icon(ft.icons.CLOSE),
                        style=ft.ButtonStyle(
                            bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=handle_menu_item_click
                    )
                ]
            ),
            ft.SubmenuButton(
                content=ft.Text("Plot"),
                on_open=handle_on_open,
                on_close=handle_on_close,
                on_hover=handle_on_hover,
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
            ft.SubmenuButton(
                content=ft.Text("About"),
            )
        ]
    )

    page.add(menubar)
    page.add(t)


ft.app(target=main, assets_dir="assets")
