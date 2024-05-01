import flet as ft


def main(page: ft.Page):

    page.title = 'Craterstats IV'
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = False
    page.update()

    def handle_menu_item_click(e):
        print(f"{e.control.content.value}.on_click")
        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"{e.control.content.value} was clicked!")))
        page.update()

    def handle_on_open(e):
        print(f"{e.control.content.value}.on_open")

    def handle_on_close(e):
        print(f"{e.control.content.value}.on_close")

    def handle_on_hover(e):
        print(f"{e.control.content.value}.on_hover")

    global_settings = ft.Column(
        [
            ft.RadioGroup(ft.Row([
                ft.Radio(value="cumu", label="Cumulative"),
                ft.Radio(value="diff", label="Differential"),
                ft.Radio(value="rel", label="Relative (R)"),
                ft.Radio(value="hart", label="Hartmann"),
                ft.Radio(value="chron", label="Chronology"),
                ]),
                value="diff"
            ),
            ft.Divider(),
            ft.Dropdown(
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
            ),
            ft.Dropdown(
                width=360,
                label="Chronology System",
                options=[
                    ft.dropdown.Option("Moon, Neukem (1983)"),
                    ft.dropdown.Option("Moon, Neukem et al (2001)"),
                ],
                value="Moon, Neukem (1983)",
                dense=True

            ),
            ft.Dropdown(
                width=360,
                label="Chronology Function",
                value="Moon, Neukem (1983)",
                options=[ft.dropdown.Option("Moon, Neukem (1983)"),],
                dense=True

            ),
            ft.Dropdown(
                width=360,
                label="Production Function",
                value="Moon, Neukem (1983)",
                options=[ft.dropdown.Option("Moon, Neukem (1983)"), ],
                dense=True

            ),
            ft.Dropdown(
                width=360,
                label="Epochs",
                value="none",
                options=[
                    ft.dropdown.Option("none"),
                    ft.dropdown.Option("Moon, Wilhelms (1987)"),
                    ft.dropdown.Option("Mars, Michael (2013)"),
                ],
                dense=True

            ),
            ft.Dropdown(
                width=360,
                label="Equilibrium Function",
                value="none",
                options=[
                    ft.dropdown.Option("none"),
                    ft.dropdown.Option("Standard lunar equilibrium (Trask, 1966)"),
                    ft.dropdown.Option("Hartmann (1984)"),
                ],
                dense=True
            ),
            ft.Divider(),
            ft.Row([
                ft.TextField(
                    width=150,
                    dense=True
                ),
                ft.Checkbox(
                    label="Isochrons, Ga",
                    value=False,
                )
            ]),
            ft.Row([
                ft.Checkbox(
                    label="Data",
                    value=True,
                ),
                ft.Checkbox(
                    label="Fit",
                    value=True,
                ),
                ft.Checkbox(
                    label="Functions",
                    value=True,
                ),
                ft.Checkbox(
                    label="Pictogram",
                ),
                ft.Checkbox(
                    label="Randomness",
                )
            ]),
            ft.Row([
                ft.Text("Axes. log D:"),
                ft.TextField(width=75, dense=True, value="-3.2"),
                ft.Text("log y:"),
                ft.TextField(width=50, dense=True, value="5.5"),
                ft.ElevatedButton(text="Auto", width=80)
            ]),
            ft.Row([
                ft.Text("Style:"),
                ft.Dropdown(
                    width=150,
                    options=[
                        ft.dropdown.Option("natural"),
                        ft.dropdown.Option("decadel"),
                        ft.dropdown.Option("root-2"),
                        ],
                    value="natural",
                    dense=True
                )
            ])


        ]
    )

    plot_settings = ft.Column([
        ft.Text(),
        ft.GridView(
            runs_count=5,
            child_aspect_ratio=5.0,
            controls=[
                ft.TextField(width=150, dense=True, text_vertical_align=0),
                ft.Checkbox(label="Title", value=True),
                ft.VerticalDivider(),
                ft.Text("Print scale. cm/decade (or plot width x height. cm):"),
                ft.TextField(width=150, dense=True, value="7.5x7.5"),
                ft.TextField(width=150, dense=True, text_vertical_align=0),
                ft.Checkbox(label="Subtitle", value=True),
                ft.VerticalDivider(),
                ft.Text("Text size. pt:"),
                ft.TextField(width=150, dense=True, value="8"),
            ]),
        ft.Row([
            ft.Container(
                alignment=ft.alignment.top_left,
                bgcolor=ft.colors.WHITE60,
                content=ft.Chip(ft.Text("Default")),
                width=200,
                height=200,
                border_radius=10,
                border=ft.border.all(1, ft.colors.BLACK)
            ),
            ft.Column([
                ft.ElevatedButton(text="New", width=115),
                ft.ElevatedButton(text="Duplicate", width=115),
                ft.ElevatedButton(text="Delete", width=115),
            ]),
            ft.Column([
                ft.ElevatedButton(text="Up", width=115),
                ft.ElevatedButton(text="Down", width=115),
            ])
        ]),
        ft.Divider(),
        ft.Row([
            ft.TextField(width=200, dense=True, value="Default"),
            ft.Dropdown(
                width=200,
                dense=True,
                options=[
                    ft.dropdown.Option("crater count"),
                    ft.dropdown.Option("cumulative fit"),
                    ft.dropdown.Option("differential fit"),
                    ft.dropdown.Option("Poisson pdf"),
                    ft.dropdown.Option("Poisson buffer pdf"),
                ]
            ),
            ft.Checkbox(label="Hide plot", value=False),
        ]),
        ft.Row([
            ft.Text("Diameter range:"),
            ft.TextField(width=150, dense=True, value="0.0"),
            ft.Text("Binning"),
            ft.Dropdown(
                width=150,
                dense=True,
                options=[
                    ft.dropdown.Option("psuedo-log"),
                    ft.dropdown.Option("log"),
                    ft.dropdown.Option("log"),
                ],
                value='psuedo-log',
            )
        ]),
        ft.Row([
            ft.Text("Colour"),
            ft.Dropdown(
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
            ),
            ft.Text("Symbol"),
            ft.Dropdown(
                dense=True,
                width=100,
                options=[
                    ft.dropdown.Option("Diamond"),
                    ft.dropdown.Option("Square"),
                    ft.dropdown.Option("Circle"),
                ],
                value='Square'
            )
        ]),
        ft.Column([
            ft.Row([
                ft.Checkbox(label="Error bars", value=True),
                ft.Checkbox(label="Display age", value=True),
                ft.Checkbox(label="Align age left"),
                ft.Checkbox(label="Show isochron", value=True),
                ft.Checkbox(label="Plot fit", value=True),
            ]),
        ])
    ])
    plot = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row([
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
            ]),
            ft.Image(
                src="Caden_GUI_Prototype/DearPyGUI_Attempt/00-demo.png",
                height=500,
                width=500,
                fit=ft.ImageFit.CONTAIN
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
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=handle_menu_item_click
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Open"),
                        leading=ft.Icon(ft.icons.FILE_UPLOAD),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
                        on_click=handle_menu_item_click
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Close"),
                        leading=ft.Icon(ft.icons.CLOSE),
                        style=ft.ButtonStyle(bgcolor={ft.MaterialState.HOVERED: ft.colors.GREEN_100}),
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
