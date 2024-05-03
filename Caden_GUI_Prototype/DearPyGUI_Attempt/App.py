import dearpygui.dearpygui as dpg
import platform
import time

"""
Functions
"""


def select_graph():
    print("Graph Selected")


def set_plot_fit_text(sender, app_data):
    dpg.set_value('plot_fit_text', app_data)


def set_chron_func(sender, app_data):
    chron_func_str = ''
    prod_func_str = ''

    if app_data[:4] == "Moon":
        chron_func_str = app_data

    elif app_data[:4] == "Mars":

        if app_data == 'Mars, Neukum-Ivanov (2001)':
            chron_func_str = 'Mars, Hartmann & Neukum (2001)'
        elif app_data == 'Mars, Ivanov (2001)':
            chron_func_str = app_data
        elif app_data == 'Mars, Hartmann 2004 iteration':
            chron_func_str = 'Mars, Hartmann (2005) [Michael (2013)]'
        elif app_data == 'Mars, Hartmann & Daubar (2016)':
            chron_func_str = 'Mars, Hartmann (2005) [Michael (2013)]'

    elif app_data[:4] == "Merc":

        if app_data == 'Mercury, Le Feuvre and Wieczorek 2011 non-porous':
            chron_func_str = 'Mercury, Le Feuvre and Wieczorek (2011) non-porous'
        elif app_data == 'Mercury, Le Feuvre and Wieczorek 2011 porous':
            chron_func_str = 'Mercury, Le Feuvre and Wieczorek (2011) porous'
        else:
            chron_func_str = app_data

    elif app_data[:4] == "Vest":

        if app_data == "Vesta, Marchi & O'Brien (2014)":
            chron_func_str = "Vesta, O'Brien et al. (2014)"
        else:
            chron_func_str = app_data

    elif app_data[:4] == "Cere":

        chron_func_str = app_data

    elif app_data[:4] == "Ida,":

        chron_func_str = app_data

    elif app_data[:4] == "Gasp":

        chron_func_str = app_data

    elif app_data[:4] == "Lute":

        chron_func_str = app_data

    elif app_data[:4] == "Phob":

        chron_func_str = app_data

    dpg.set_value(chron_func, chron_func_str)

    if app_data[:4] == 'Moon':

        if app_data == 'Moon, Yue et al. (2022)':
            prod_func_str = 'Moon, Neukum et al. (2001)'
        else:
            prod_func_str = app_data

    elif app_data[:4] == 'Mars':

        if app_data == 'Mars, Neukum-Ivanov (2001)':
            prod_func_str = 'Mars, Ivanov (2001)'
        elif app_data == 'Mars, Ivanov (2001)':
            prod_func_str = app_data
        elif app_data == 'Mars, Hartmann 2004 iteration':
            prod_func_str = 'Mars, Hartmann (2005)'
        elif app_data == 'Mars, Hartmann & Daubar (2016)':
            prod_func_str = app_data

    elif app_data[:4] == "Merc":

        if app_data == 'Mercury, Le Feuvre and Wieczorek 2011 non-porous':
            prod_func_str = 'Mercury, Le Feuvre and Wieczorek (2011) non-porous'
        elif app_data == 'Mercury, Le Feuvre and Wieczorek 2011 porous':
            prod_func_str = 'Mercury, Le Feuvre and Wieczorek (2011) porous'
        else:
            prod_func_str = app_data

    elif app_data[:4] == "Vest":

        if app_data == "Vesta, Marchi & O'Brien (2014)":
            prod_func_str = 'Vesta, Marchi et al (2013) [inferred, NS]'
        else:
            prod_func_str = app_data

    elif app_data[:4] == "Cere":

        prod_func_str = app_data

    elif app_data[:4] == "Ida,":

        prod_func_str = app_data

    elif app_data[:4] == "Gasp":

        prod_func_str = app_data

    elif app_data[:4] == "Lute":

        prod_func_str = app_data

    elif app_data[:4] == "Phob":

        prod_func_str = app_data

    dpg.set_value(prod_func, prod_func_str)


def set_chron_sys(sender, app_data):
    items = []
    chron_func_str = ''
    prod_func_str = ''

    if app_data == 'Moon':
        items = ['Moon, Neukem (1983)', 'Moon, Neukem et al (2001)', 'Moon, Hartmann 2010 iteration',
                 'Moon, Yue et al. (2022)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == "Mars":
        items = ['Mars, Neukum-Ivanov (2001)', 'Mars, Ivanov (2001)', 'Mars, Hartmann 2004 iteration',
                 'Mars, Hartmann & Daubar (2016)']
        chron_func_str = 'Mars, Hartmann & Neukum (2001)'
        prod_func_str = 'Mars, Ivanov (2001)'

    elif app_data == "Mercury":
        items = ['Mercury, Strom & Neukum (1988)', 'Mercury, Neukum et al. (2001)',
                 'Mercury, Le Feuvre and Wieczorek 2011 non-porous', 'Mercury, Le Feuvre and Wieczorek 2011 porous']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == 'Vesta':
        items = ['Vesta, Rev4, Schmedemann et al (2014)', 'Vesta, Rev3, Schmedemann et al (2014)',
                 'Vesta, Marchi & O\'Brien (2014)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == 'Ceres':
        items = ['Ceres, Hiesinger et al. (2016)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == 'Ida':
        items = ['Ida, Schmedemann et al (2014)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == 'Gaspra':
        items = ['Gaspra, Schmedemann et al (2014)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == 'Lutetia':
        items = ['Lutetia, Schmedemann et al (2014)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    elif app_data == 'Phobos':
        items = [
            'Phobos, Case A - SOM, Schmedemann et al (2014)', 'Phobos, Case B - MBA, Schmedemann et al (2014)']
        chron_func_str = items[0]
        prod_func_str = items[0]

    if not (app_data == 'Moon' or app_data == 'Mars'):
        dpg.configure_item(epoch_combo, items=['none'])
        dpg.set_value(epoch_combo, 'none')
    elif app_data == 'Moon':
        dpg.configure_item(epoch_combo, items=[
                           'none', 'Moon, Wilhelms (1987)'])
        dpg.set_value(epoch_combo, 'none')
    elif app_data == 'Mars':
        dpg.configure_item(epoch_combo, items=['none', 'Mars, Michael (2013)'])
        dpg.set_value(epoch_combo, 'none')

    dpg.configure_item(chron_sys, items=items)
    dpg.set_value(chron_sys, items[0])
    dpg.set_value(chron_func, chron_func_str)
    dpg.set_value(prod_func, prod_func_str)


def increase_progress():
    index = 0.0
    window = dpg.get_windows()[1]
    dpg.configure_item(item="progress_bar", show=True)
    dpg.configure_item(item="start button", show=False)

    while index <= 1:

        dpg.set_value("progress_bar", index)
        if index < 0.5:
            index += 0.1
        else:
            index += 0.2
        time.sleep(0.15)

    dpg.set_value("progress_bar", 1)

    dpg.configure_item(item=window, show=False)


"""
GUI
"""

dpg.create_context()

if platform.platform()[:5] == 'macOS':
    width, height, channels, data = dpg.load_image(
        'DearPyGUI_Attempt/00-demo.png')
else:
    width, height, channels, data = dpg.load_image(
        'DearPyGUI_Attempt\\00-demo.png')

dpg.create_viewport(title='CraterStats IV', width=1048,
                    height=768, resizable=False)
dpg.setup_dearpygui()

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, data)

with dpg.window(no_close=True, no_title_bar=True, pos=(0, 0), width=dpg.get_viewport_width(),
                height=dpg.get_viewport_height(), no_move=True, no_resize=True):
    # Create a menu bar
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save")
            dpg.add_menu_item(label="Open")
            dpg.add_menu_item(label="Close")
            dpg.add_menu_item(label="Exit")

        with dpg.menu(label="Plot"):
            dpg.add_menu_item(label="New")
            dpg.add_menu_item(label="Duplicate")
            dpg.add_menu_item(label="Delete")

        with dpg.menu(label="Export"):
            dpg.add_menu_item(label="Image")
            dpg.add_menu_item(label="Summary file")
            dpg.add_menu_item(label=".stat table")

        with dpg.menu(label="Utilities"):
            dpg.add_menu_item(label="sum .stat files")
            dpg.add_menu_item(label="merge .diam files")
            dpg.add_menu_item(label="randomness analysis")

        about_menu = dpg.add_menu_item(label="About")

        # with dpg.popup(about_menu, tag="About", modal=True, mousebutton=dpg.mvMouseButton_Left):
    #     dpg.add_text("CraterStats is a program designed to analyze crater data and produce plots based on the data.")
    #     dpg.add_text("This program was created by Caden Tedeschi")
    #     dpg.add_text("Version 1.0")
    #     dpg.add_text("2024")

    with dpg.tab_bar(tag="tab_bars"):
        with dpg.tab(label='Global Settings'):
            with dpg.group(tag='plot_view'):
                plot_view = dpg.add_radio_button(
                    items=("Cumulative", 'Differential',
                           'Relative (R)', 'Hartmann', 'Chronology'),
                    callback=select_graph,
                    horizontal=True,
                    default_value='Differential',
                )
                dpg.add_spacer(height=15)

            with dpg.group(tag='func_dropdowns'):
                body = dpg.add_combo(
                    items=('Moon', 'Mars', 'Mercury', 'Vesta', 'Ceres',
                           'Ida', 'Gaspra', 'Lutetia', 'Phobos'),
                    label='Body',
                    callback=set_chron_sys,
                    default_value='Moon'
                )

                dpg.add_spacer(height=5)

                chron_sys = dpg.add_combo(
                    items=('Moon, Neukem (1983)', 'Moon, Neukem et al (2001)'),
                    label='Chronology System',
                    callback=set_chron_func,

                    default_value='Moon, Neukem (1983)'
                )

                dpg.add_spacer(height=5)

                chron_func = dpg.add_combo(
                    items=('func1', 'func2', 'func3'),
                    label='Chronolgy Function',
                    default_value='Moon, Neukem (1983)',
                    enabled=False,
                )
                dpg.add_spacer(height=5)

                prod_func = dpg.add_combo(
                    items=[''],
                    label='Production Function',
                    default_value='Moon, Neukem (1983)',
                    enabled=False
                )
                dpg.add_spacer(height=5)

                epoch_combo = dpg.add_combo(
                    items=('None', 'Wilhelms (1987)'),
                    label='Epochs',
                    default_value='none',
                )

                dpg.add_spacer(height=5)

                equil_func = dpg.add_combo(
                    items=(
                        'none', 'Standard lunar equilibrium (Trask, 1966)', 'Hartmann (1984)'),
                    label='Equilibrium Function',
                    default_value='none',
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='iso', horizontal=True):
                iso_text = dpg.add_input_text(
                    width=75
                )
                iso_label = dpg.add_checkbox(
                    label='Isochrons, Ga'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='legend_options', horizontal=True):
                data_legend_checkbox = dpg.add_checkbox(
                    label='Data',
                    default_value=True
                )
                fit_legend_checkbox = dpg.add_checkbox(
                    label='Fit',
                    default_value=True
                )
                func_legend_checkbox = dpg.add_checkbox(
                    label='Functions',
                    default_value=True
                )
                picto_legend_checkbox = dpg.add_checkbox(
                    label='Pictogram'
                )
                rand_legend_checkbox = dpg.add_checkbox(
                    label='Randomness'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag="axes", horizontal=True):
                axes_label = dpg.add_text(
                    default_value="Axes. log D:"
                )
                axis_d_input_box = dpg.add_input_text(
                    width=75,
                    default_value="-3.2"
                )
                axis_y_input_box = dpg.add_text(
                    default_value='log y:'
                )
                dpg.add_input_text(
                    width=50,
                    default_value="-5.5"
                )
                axis_auto_button = dpg.add_button(
                    label="Auto",
                    width=50
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='axes_styles', horizontal=True):
                style_label = dpg.add_text(
                    default_value='Stlye:'
                )
                style_options = dpg.add_radio_button(
                    items=('natural', "decadel", 'root-2'),
                    horizontal=True,
                    default_value='natural'
                )

            dpg.add_spacer(height=15)

        with dpg.tab(label='Plot Settings'):
            with dpg.group(tag='title', horizontal=True):
                dpg.add_input_text(
                    width=150
                )
                dpg.add_checkbox(
                    label="Title",
                    default_value=True
                )

                dpg.add_spacer(width=200)

                dpg.add_text(
                    default_value='Print scale. cm/decade (or plot width x height. cm):'
                )
                dpg.add_input_text(
                    width=75,
                    default_value="7.5x7.5"
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='subtitle', horizontal=True):
                dpg.add_input_text(
                    width=150
                )
                dpg.add_checkbox(
                    label='Subtitle',
                    default_value=True
                )

                dpg.add_spacer(width=445)

                dpg.add_text(
                    default_value='Text size. pt:'
                )
                dpg.add_input_text(
                    width=50,
                    default_value="8"
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='plot_fit', horizontal=False):
                plot_fit_list = dpg.add_listbox(
                    items=['default'],
                    width=150,
                    default_value='default',
                )

                with dpg.group(tag='top_buttons', horizontal=True):
                    new_button = dpg.add_button(
                        label="New",
                        width=75,
                    )

                    duplicate_button = dpg.add_button(
                        label="Duplicate",
                        width=75
                    )
                    delete_button = dpg.add_button(
                        label="Delete",
                        width=75
                    )

                    up_button = dpg.add_button(
                        label="Up",
                        width=75,
                    )
                    down_button = dpg.add_button(
                        label="Down",
                        width=75,
                    )

            dpg.add_spacer(height=15)

            with dpg.group(tag='fit_type', horizontal=True):
                plot_fit_text = dpg.add_input_text(
                    default_value='default',
                    width=150,
                    tag='plot_fit_text',
                )
                plot_fit_options = dpg.add_combo(
                    items=('crater count', 'cumulative fit',
                           'differential fit', 'Poisson pdf', 'Poisson buffer pdf'),
                    width=150,
                    default_value='crater count'
                )
                hide_button = dpg.add_checkbox(
                    label='Hide plot'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='source_file', horizontal=True):
                source_file_label = dpg.add_text(
                    default_value='Source file'
                )
                source_file_text = dpg.add_input_text(
                    readonly=True,
                    width=200
                )
                source_file_button = dpg.add_button(
                    label='Browse...',
                    width=75
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='diam_range', horizontal=True):
                diam_range_label = dpg.add_text(
                    default_value='Diameter range:'
                )
                diam_range_input = dpg.add_input_text(
                    width=125,
                    default_value='0.0'
                )
                binning_label = dpg.add_text(
                    default_value='Binning',
                )

                binning_options = dpg.add_combo(
                    items=("bin1", "bin2", "bin3"),
                    width=110,
                    default_value='psuedo-log'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag="plot_color_symbols", horizontal=True):
                color_text = dpg.add_text(
                    default_value='Colour'
                )
                color_dropdown = dpg.add_combo(
                    items=('Red', 'Black', 'Green', 'Blue', 'Yellow'),
                    width=80,
                    default_value='Black'
                )

                symbol_text = dpg.add_text(
                    default_value='Symbol',
                )
                symbol_dropdown = dpg.add_combo(
                    items=('Diamond', 'Square', 'Circle'),
                    width=90,
                    default_value='Square'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='extra_settings', horizontal=True):
                error_bar_check = dpg.add_checkbox(
                    label='Error bars',
                    default_value=True
                )
                display_age_check = dpg.add_checkbox(
                    label='Display age',
                    default_value=True
                )
                align_left_check = dpg.add_checkbox(
                    label='Align age left'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='extra_settings_2', horizontal=True):
                show_iso_check = dpg.add_checkbox(
                    label='Show isochron',
                    default_value=True
                )

                dpg.add_spacer(width=69)

                plot_fit_error_check = dpg.add_checkbox(
                    label='Plot fit',
                )

            dpg.add_spacer(height=15)

        with dpg.tab(label='Plot'):
            plot_image = dpg.add_image(
                texture_tag=texture_id,
                width=500,
                height=500,
                pos=(
                    (dpg.get_viewport_height() - 250) / 2, 150),
                border_color='#F00'
            )

            cmd_line_arg = dpg.add_input_text(
                default_value='craterstats -cs neukumivanov -p source=%sample%/Pickering.scc,psym=o -p type=d-fit,'
                              'range=[.2,.7],isochron=1 -p range=[2,5],colour=red',
                pos=(50, dpg.get_item_pos(plot_image)[1] + 550),
                width=dpg.get_viewport_width() - 105,
            )

            diameter_info = dpg.add_text(
                default_value='Diameter',
                pos=(dpg.get_item_pos(plot_image)[0] - 18,
                     dpg.get_item_pos(plot_image)[1] - 55),
            )
            diameter_info_input = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] - 25,
                     dpg.get_item_pos(plot_image)[1] - 30),
            )

            bin_label = dpg.add_text(
                default_value="Bin",
                pos=(dpg.get_item_pos(plot_image)[0] + 80,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            bin_input_text = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] + 55,
                     dpg.get_item_pos(plot_image)[1] - 30),
                readonly=True,
            )

            n_label = dpg.add_text(
                default_value='n',
                pos=(dpg.get_item_pos(plot_image)[0] + 165,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            n_entry_box = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] + 135,
                     dpg.get_item_pos(plot_image)[1] - 30),
                readonly=True,
            )

            y_label = dpg.add_text(
                default_value='y',
                pos=(dpg.get_item_pos(plot_image)[0] + 245,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            y_entry_box = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] + 215,
                     dpg.get_item_pos(plot_image)[1] - 30)
            )

            age_label = dpg.add_text(
                default_value='Age',
                pos=(dpg.get_item_pos(plot_image)[0] + 320,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            age_entry_box = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] + 295,
                     dpg.get_item_pos(plot_image)[1] - 30)
            )

            n_value_label = dpg.add_text(
                default_value='N(1)',
                pos=(dpg.get_item_pos(plot_image)[0] + 397,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            n_value_entry_box = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] + 375,
                     dpg.get_item_pos(plot_image)[1] - 30)
            )

            a_zero_label = dpg.add_text(
                default_value='a0',
                pos=(dpg.get_item_pos(plot_image)[0] + 482,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            a_zero_entry_box = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] + 455,
                     dpg.get_item_pos(plot_image)[1] - 30)
            )

with dpg.window(no_close=True, no_title_bar=True, pos=(0, 0), width=dpg.get_viewport_width(),
                height=dpg.get_viewport_height(), no_move=True, no_resize=True,):
    title = dpg.add_text(
        default_value="Welcome to CraterStats!",
        pos=(dpg.get_viewport_width() / 2 - 325, 30),
    )

    prog_bar = dpg.add_progress_bar(
        tag="progress_bar",
        pos=(dpg.get_viewport_width() / 2 - 350,
             dpg.get_viewport_height() - 300),
        show=False,
    )

    dpg.add_button(
        label="Start Program",
        callback=increase_progress,
        pos=((dpg.get_viewport_width() - 180) / 2,
             dpg.get_item_pos(prog_bar)[1] + 50),
        tag="start button",
        height=60,
        width=180
    )

"""
FONTS
"""
with dpg.font_registry():
    nasa_font = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\nasalization-rg.otf', 15 * 2)

    nas_title_font = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\nasalization-rg.otf', 60 * 2)

    nasa_button_font = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\nasalization-rg.otf', 25 * 2)

    arial_font = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\Arial Unicode.ttf', 18 * 2)
    arial_title_font = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\Arial Unicode.ttf', 60 * 2)
    arial_button_font = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\Arial Unicode.ttf', 25 * 2)

    courier_new = dpg.add_font(
        'DearPyGUI_Attempt\\Fonts\\Courier New.ttf', 13 * 2)

"""
Themes
"""

# Dark mode theme
with dpg.theme() as dark_mode:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,
                            (60, 60, 60), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (42, 97, 235), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            (107, 135, 219), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,
                            (42, 97, 235), category=dpg.mvThemeCat_Core)
        # dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
        #                     (148, 148, 148), category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvCombo, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (51, 51, 51), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text,
                            (168, 168, 168), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,
                            (51, 51, 51), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (189, 189, 189), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            (189, 189, 189), category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvCombo, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (51, 51, 51), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text,
                            (168, 168, 168), category=dpg.mvThemeCat_Core)


with dpg.theme() as light_mode:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,
                            (225, 225, 225), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0),
                            category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg,
                            (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TabActive,
                            (180, 180, 180), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Tab,
                            (150, 150, 150), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered,
                            (45, 84, 194), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (42, 97, 235), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            (107, 135, 219), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (189, 189, 189), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,
                            (148, 148, 148), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_CheckMark,
                            (42, 97, 235), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg,
                            (189, 189, 189), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Header,
                            (135, 135, 135), category=dpg.mvThemeCat_Core)

    with dpg.theme_component(dpg.mvCombo, enabled_state=False):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (51, 51, 51), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text,
                            (168, 168, 168), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered,
                            (51, 51, 51), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (189, 189, 189), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            (189, 189, 189), category=dpg.mvThemeCat_Core)

with dpg.theme() as readonly_entry:
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (51, 51, 51), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text,
                            (168, 168, 168), category=dpg.mvThemeCat_Core)

with dpg.theme() as cmd_line_arg_theme:
    with dpg.theme_component(dpg.mvInputText):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                            (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text,
                            (255, 255, 255), category=dpg.mvThemeCat_Core)

dpg.set_global_font_scale(0.5)
# dpg.bind_theme(light_mode)
# dpg.bind_item_theme(cmd_line_arg, cmd_line_arg_theme)
# dpg.bind_item_theme(bin_input_text, readonly_entry)
# dpg.bind_item_theme(n_entry_box, readonly_entry)
# dpg.bind_font(nasa_font)
# dpg.bind_item_font(title, nas_title_font)
# dpg.bind_item_font("start button", nasa_button_font)
# dpg.bind_item_font(cmd_line_arg, courier_new)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
