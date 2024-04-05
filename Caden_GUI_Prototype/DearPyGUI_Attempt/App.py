import dearpygui.dearpygui as dpg


def save_callback():
    print("Save Clicked")


def select_graph():
    print("Graph Selected")


def set_plot_fit_text(sender, app_data):
    dpg.set_value('plot_fit_text', app_data)


def collapse_window(sender, app_data):
    dpg.configure_item("Global Settings", collapsed=True)
    dpg.configure_item("Plot Settings", collapsed=True)


dpg.create_context()


width, height, channels, data = dpg.load_image(
    'Frames\moonpic.png')

dpg.create_viewport(title='CraterStats', width=1048,
                    height=768, resizable=False)
dpg.setup_dearpygui()

with dpg.texture_registry():
    texture_id = dpg.add_static_texture(width, height, data)

with dpg.window(no_close=True, no_title_bar=True, pos=(0, 0), width=dpg.get_viewport_width(), height=dpg.get_viewport_height(), no_move=True):
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

        with dpg.menu(label="About"):
            pass

    with dpg.tab_bar(tag="tab_bars"):
        with dpg.tab(label='Global Settings'):
            with dpg.group(tag='plot_view'):
                plot_view = dpg.add_radio_button(
                    items=("Cumulative", 'Differential',
                           'Relative (R)', 'Hartmann', 'Chronology'),
                    callback=select_graph,
                    horizontal=True)
                dpg.add_spacer(height=15)

            with dpg.group(tag='func_dropdowns'):
                chron_func = dpg.add_combo(
                    items=('func1', 'func2', 'func3'),
                    label='Chronolgy Function'
                )
                dpg.add_spacer(height=5)

                prod_func = dpg.add_combo(
                    items=('func1', 'func2', 'func3'),
                    label='Production Function'
                )
                dpg.add_spacer(height=5)

                equil_func = dpg.add_combo(
                    items=('func1', 'func2', 'func3'),
                    label='Equilibrium Function'
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
                    label='Data'
                )
                fit_legend_checkbox = dpg.add_checkbox(
                    label='Fit'
                )
                func_legend_checkbox = dpg.add_checkbox(
                    label='Functions'
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
                    width=75
                )
                axis_y_input_box = dpg.add_text(
                    default_value='log y:'
                )
                dpg.add_input_text(
                    width=50
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
                    items=("decadel", 'root-2'),
                    horizontal=True
                )

            dpg.add_spacer(height=15)

        with dpg.tab(label='Plot Settings'):
            with dpg.group(tag='title', horizontal=True):

                dpg.add_input_text(
                    width=150
                )
                dpg.add_checkbox(
                    label="Title",
                )

                dpg.add_spacer(width=200)

                dpg.add_text(
                    default_value='Print scale. cm/decade (or plot width x height. cm):'
                )
                dpg.add_input_text(
                    width=75
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='subtitle', horizontal=True):
                dpg.add_input_text(
                    width=150
                )
                dpg.add_checkbox(
                    label='Subtitle'
                )

                dpg.add_spacer(width=445)

                dpg.add_text(
                    default_value='Text size. pt:'
                )
                dpg.add_input_text(
                    width=50
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='plot_fit', horizontal=False):
                plot_fit_list = dpg.add_listbox(
                    items=('data', 'age fit', 'resurfacing fit'),
                    width=150,
                    default_value='resurfacing fit',
                    callback=set_plot_fit_text
                )

                with dpg.group(tag='top_buttons', horizontal=True):
                    new_button = dpg.add_button(
                        label="New",
                        width=75,
                        callback=collapse_window
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
                    hint=dpg.get_value(plot_fit_list),
                    width=150,
                    tag='plot_fit_text'
                )
                plot_fit_options = dpg.add_combo(
                    items=('fit1', 'fit2', 'fit3'),
                    width=150
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
                    width=125
                )
                binning_label = dpg.add_text(
                    default_value='Binning',
                )
                binning_options = dpg.add_combo(
                    items=("bin1", "bin2", "bin3"),
                    width=75
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag="plot_color_symbols", horizontal=True):
                color_text = dpg.add_text(
                    default_value='Colour'
                )
                color_dropdown = dpg.add_combo(
                    items=('Red', 'Black', 'Green', 'Blue', 'Yellow'),
                    width=65
                )

                symbol_text = dpg.add_text(
                    default_value='Symbol',
                )
                symbol_dropdown = dpg.add_combo(
                    items=('Diamond', 'Square', 'Circle'),
                    width=75
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='extra_settings', horizontal=True):
                error_bar_check = dpg.add_checkbox(
                    label='Error bars'
                )
                display_age_check = dpg.add_checkbox(
                    label='Display age'
                )
                align_left_check = dpg.add_checkbox(
                    label='Align age left'
                )

            dpg.add_spacer(height=15)

            with dpg.group(tag='extra_settings_2', horizontal=True):
                show_iso_check = dpg.add_checkbox(
                    label='Show isochron'
                )

                dpg.add_spacer(width=80)

                plot_fit_error_check = dpg.add_checkbox(
                    label='Plot fit',
                )

            dpg.add_spacer(height=15)

        with dpg.tab(label='Plot'):
            plot_image = dpg.add_image(
                texture_id,
                width=500,
                height=500,
                pos=(
                    (dpg.get_viewport_height() - 250) / 2, 150),
                border_color='#F00'
            )

            cmd_line_arg = dpg.add_text(
                default_value='craterstats -cs neukumivanov -p source=%sample%/Pickering.scc,psym=o -p type=d-fit,range=[.2,.7],isochron=1 -p range=[2,5],colour=red',
                pos=(50, dpg.get_item_pos(plot_image)[1] + 550)
            )

            diameter_info = dpg.add_text(
                default_value='Diameter',
                pos=(dpg.get_item_pos(plot_image)[0] - 18,
                     dpg.get_item_pos(plot_image)[1] - 55)
            )
            diameter_info_input = dpg.add_input_text(
                width=70,
                pos=(dpg.get_item_pos(plot_image)[0] - 25,
                     dpg.get_item_pos(plot_image)[1] - 30)
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
                readonly=True
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
                readonly=True
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

with dpg.theme() as dark_mode:

    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,
                            (60, 60, 60), category=dpg.mvThemeCat_Core)

with dpg.theme() as light_mode:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg,
                            (225, 225, 225), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0),
                            category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_MenuBarBg,
                            (200, 200, 200), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TabActive,
                            (180, 180, 180), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Tab,
                            (150, 150, 150), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button,
                            (42, 97, 235), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered,
                            (107, 135, 219), category=dpg.mvThemeCat_Core)

dpg.bind_theme(light_mode)
dpg.show_style_editor()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
