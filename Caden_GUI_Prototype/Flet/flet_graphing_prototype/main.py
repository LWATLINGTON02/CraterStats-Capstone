import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import matplotlib
import matplotlib.pyplot as plt


def main(page: ft.Page):

    def add_point(event):
        if x_entry.value == '' or y_entry.value == '':
            x_entry.value = '0'
            y_entry.value = '0'
        x_points.append(int(x_entry.value))
        y_points.append(int(y_entry.value))
        ax.plot(x_points, y_points, plot_type)
        page.update()

    x_points = [1]
    y_points = [1]
    plot_type = 'ro'

    fig, ax = plt.subplots()

    ax.plot(x_points, y_points, plot_type)

    ax.axis([0, 10, 0, 10])


    x_entry = ft.TextField(
        label='X Value',
    )
    y_entry = ft.TextField(
        label='Y Value',
    )
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
            add_point_btn
        ])
        )


ft.app(target=main)
