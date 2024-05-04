import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('svg')

def main(page: ft.Page):

    def set_plot_title_and_subtitle(e):
        ax.set_title((title_entry.value if show_title.value else '') + ('\n' + subtitle_entry.value if show_subtitle.value else ''))

        page.update()

    def set_plot_subtitle(e):
        ax.set_title(ax.get_title() + "\n" + subtitle_entry.value if subtitle_entry.value is not None else '')

    def add_point(event):
        x_int_val = None
        y_int_val = None

        try:
            x_int_val = int(x_entry.value)
        except ValueError:
            x_entry.value = None
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a number"))
            page.snack_bar.duration = 1500
            page.snack_bar.open = True

            page.update()

        try:
            y_int_val = int(y_entry.value)
        except ValueError:
            y_entry.value = None
            page.snack_bar = ft.SnackBar(ft.Text("Please enter a number"))
            page.snack_bar.duration = 1500
            page.snack_bar.open = True
            page.update()

        if x_entry.value == '' or y_entry.value == '':
            x_entry.value = '0'
            y_entry.value = '0'
        x_points.append(x_int_val)
        y_points.append(y_int_val)
        ax.plot(x_points, y_points, plot_type)
        page.update()

    x_points = [1]
    y_points = [1]
    plot_type = 'bo'

    fig, ax = plt.subplots()

    ax.plot(x_points, y_points, plot_type)

    ax.axis([0, 10, 0, 10])


    x_entry = ft.TextField(
        label='X Value',
    )
    y_entry = ft.TextField(
        label='Y Value',
    )

    title_entry = ft.TextField(
        label='Title',
        on_change=set_plot_title_and_subtitle,
    )
    subtitle_entry = ft.TextField(
        label='Subtitle',
        on_change=set_plot_title_and_subtitle,
    )

    show_title = ft.Checkbox(label='Show Title', on_change=set_plot_title_and_subtitle)

    show_subtitle = ft.Checkbox(label='Show Subtitle', on_change=set_plot_title_and_subtitle)

    add_point_btn = ft.ElevatedButton(
        text='Add Point',
        on_click=add_point
    )
    page.add(
        MatplotlibChart(fig, expand=True),
        ft.Row([
            ft.Column([
                x_entry,
                y_entry,
            ]),
            add_point_btn,
            ft.Column([
                ft.Row([
                    title_entry,
                    show_title
                ]),
                ft.Row([
                    subtitle_entry,
                    show_subtitle
                ])

            ]),
        ])
        )



ft.app(target=main)
