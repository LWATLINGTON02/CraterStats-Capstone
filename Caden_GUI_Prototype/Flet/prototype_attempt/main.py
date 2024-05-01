import flet as ft


def main(page: ft.Page):

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
        print(f"{e.control.content.value}.on_click")
        page.show_snack_bar(ft.SnackBar(content=ft.Text(
            f"{e.control.content.value} was clicked!")))
        page.update()

    def handle_on_open(e):
        print(f"{e.control.content.value}.on_open")

    def handle_on_close(e):
        print(f"{e.control.content.value}.on_close")

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    def set_chron_func(e):
        chron_func_str = ''
        prod_func_str = ''

        if (e.control.content.value[:4] == "Moon"):
            chron_func_str = e.value
        elif (e.control.content.value[:4] == "Mars"):
            if e.control.content.value == 'Mars, Neukum-Ivanov (2001)':
                chron_func_str = 'Mars, Hartmann & Neukum (2001)'
            elif e.control.content.value == 'Mars, Ivanov (2001)':
                chron_func_str = e.control.content.value
            elif e.control.content.value == 'Mars, Hartmann 2004 iteration':
                chron_func_str = 'Mars, Hartmann (2005) [Michael (2013)]'
            elif e.control.content.value == 'Mars, Hartmann & Daubar (2016)':
                chron_func_str = 'Mars, Hartmann (2005) [Michael (2013)]'
        elif e.control.content.value[:4] == "Merc":

            if e.control.content.value == 'Mercury, Le Feuvre and Wieczorek 2011 non-porous':
                chron_func_str = 'Mercury, Le Feuvre and Wieczorek (2011) non-porous'
            elif e.control.content.value == 'Mercury, Le Feuvre and Wieczorek 2011 porous':
                chron_func_str = 'Mercury, Le Feuvre and Wieczorek (2011) porous'
            else:
                chron_func_str = e.control.content.value

        elif e.control.content.value[:4] == "Vest":

            if e.control.content.value == "Vesta, Marchi & O'Brien (2014)":
                chron_func_str = "Vesta, O'Brien et al. (2014)"
            else:
                chron_func_str = e.control.content.value

        elif e.control.content.value[:4] == "Cere":

            chron_func_str = e.control.content.value

        elif e.control.content.value[:4] == "Ida,":

            chron_func_str = e.control.content.value

        elif e.control.content.value[:4] == "Gasp":

            chron_func_str = e.control.content.value

        elif e.control.content.value[:4] == "Lute":

            chron_func_str = e.control.content.value

        elif e.control.content.value[:4] == "Phob":

            chron_func_str = e.control.content.value

    plot_view = ft.RadioGroup(ft.Row([
        ft.Radio(value="cumu", label="Cumulative"),
        ft.Radio(value="diff", label="Differential"),
        ft.Radio(value="rel", label="Relative (R)"),
        ft.Radio(value="hart", label="Hartmann"),
        ft.Radio(value="chron", label="Chronology"),
    ]),
        value="diff"
    )

    body = ft.Dropdown(
        width=360,
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
        dense=True
    )

    chron_sys = ft.Dropdown(
        width=360,
        label="Chronology System",
        options=[
            ft.dropdown.Option("Moon, Neukem (1983)"),
            ft.dropdown.Option("Moon, Neukem et al (2001)"),
        ],
        value="Moon, Neukem (1983)",
        dense=True

    )

    chron_func = ft.Dropdown(
        width=360,
        label="Chronology Function",
        value="Moon, Neukem (1983)",
        options=[ft.dropdown.Option("Moon, Neukem (1983)"),],
        dense=True
    )

    prod_func = ft.Dropdown(
        width=360,
        label="Production Function",
        value="Moon, Neukem (1983)",
        options=[ft.dropdown.Option("Moon, Neukem (1983)"), ],
        dense=True

    )

    epoch = ft.Dropdown(
        width=360,
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
        width=360,
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

    picto_legend = ft.Checkbox(
        label="Pictogram",
    )

    rand_legend = ft.Checkbox(
        label="Randomness",
    )

    axis_d_input_box = ft.TextField(width=75, dense=True, value="-3.2")

    axis_y_input_box = ft.TextField(width=50, dense=True, value="5.5")

    axis_auto_button = ft.ElevatedButton(text="Auto", width=80)

    style_options = ft.Dropdown(
        width=150,
        options=[
            ft.dropdown.Option("natural"),
            ft.dropdown.Option("decadel"),
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

    browse_button = ft.ElevatedButton(text="Browse...", width=115)

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
                   picto_legend, rand_legend]),
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
                            ft.TextField(width=100, dense=True),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("n"),
                            ft.TextField(width=100, dense=True),
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
            ft.Image(
                src="DearPyGUI_Attempt\\00-demo.png",
                height=500,
                width=500,
                fit=ft.ImageFit.CONTAIN
            ),
            ft.TextField(
                dense=True,
                value="-cs neukumivanov -title Differential plot -subtitle with two differential fit age evaluations -p source=%sample%/Pickering.scc,psym=o -p type=d-fit,range=[.2,.7],isochron=1 -p range=[2,5],colour=red",
                text_size=12,
                bgcolor=ft.colors.BLACK,
                color=ft.colors.WHITE,
                text_style=ft.TextStyle(font_family="Courier New")
            )
        ]

    )

    t = ft.Tabs(
        selected_index=2,
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


ft.app(main)
