from dearpygui.dearpygui import *
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from math import sin, cos

create_context()
create_viewport(title='Graphing Prototype', width=1280,
                height=720, resizable=False)
setup_dearpygui()

# creating data
sindatax = []
sindatay = []
for i in range(0, 500):
    sindatax.append(i / 1000)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 1000))
sindatay2 = []
for i in range(0, 100):
    sindatay2.append(2 + 0.5 * sin(50 * i / 100))


with window(label='Matplotlib graph', no_collapse=True, no_resize=True, no_close=True, no_move=True, width=640, height=720, pos=[0, 0]):
    with plot(label="Bar Series", height=-1, width=-1):
        add_plot_legend()

        # create x axis
        add_plot_axis(mvXAxis, label="Student", no_gridlines=True)
        set_axis_ticks(last_item(), (("S1", 11), ("S2", 21), ("S3", 31)))

        # create y axis
        add_plot_axis(mvYAxis, label="Score", tag="yaxis_tag")

        # add series to y axis
        add_bar_series([10, 20, 30], [100, 75, 90], label="Final Exam", weight=1, parent="yaxis_tag")
        add_bar_series([11, 21, 31], [83, 75, 72], label="Midterm Exam", weight=1, parent="yaxis_tag")
        add_bar_series([12, 22, 32], [42, 68, 23], label="Course Grade", weight=1, parent="yaxis_tag")

    add_button(
        label='Graph Settings',
        callback=lambda: show_item('Graph Settings')
    )

with window(label='DearPyGUI graph', no_collapse=True, no_resize=True, no_close=True, no_move=True, width=640, height=720, pos=[640, 0]):
    add_text('DearPyGUI graph')

    

    # create plot
    with plot(tag="plot", label="Line Series", height=500, width=420):

        # optionally create legend
        add_plot_legend()

        # REQUIRED: create x and y axes
        add_plot_axis(mvXAxis, label="x")
        set_axis_limits(last_item(), 0, 4.25)
        set_axis_ticks(last_item(), (("10 m", 0), ("100 m", 1), ("1 km", 2), ("10 km", 3), ("100 km", 4)))

        add_plot_axis(mvYAxis, label="y", tag="yaxis")
        set_axis_limits(last_item(), 0, 9)
        set_axis_ticks(last_item(), (("10^-5", 0), ("10^-4", 1), ("10^-3", 2), ("10^-2", 3), ("10^-1", 4), ("10^0", 5), ("10^1", 6), ("10^2", 7), ("10^3", 8)))






show_viewport()
start_dearpygui()
destroy_context()
