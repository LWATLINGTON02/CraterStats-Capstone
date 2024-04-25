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

width, height, channels, data = load_image(
    'Caden_GUI_Prototype\\DearPyGUI_Attempt\\00-demo.png')

with texture_registry():
    texture_id = add_static_texture(width, height, data)


def change_to_sin(sender, data):

    if data == 13 or sender == "sin" or sender == "sin_step_value":

        step_value = get_value('sin_step_value')

        # Generate x values from 0 to 2*pi with a step size of 0.1
        x = np.arange(0, 2*np.pi, step_value)
        # Calculate y values using the sine function
        y = np.sin(x)

        # Plot the sine function
        plt.figure(figsize=(5, 5))

        plt.plot(x, y)
        plt.title('Sine Function')
        plt.xlabel('x')
        plt.ylabel('sin(x)')
        plt.grid(True)
        plt.savefig("figure.png", dpi=200)
        plt.close()

        width, height, channels, data = load_image(
            'figure.png')

        with texture_registry():
            texture_id = add_static_texture(width, height, data)

        configure_item(plot_image, texture_tag=texture_id)


def change_to_cos(sender, data):

    if data == 13 or sender == "cos" or sender == "cos_step_value":

        step_value = get_value('cos_step_value')

        # Generate x values from 0 to 2*pi with a step size of 0.1
        x = np.arange(0, 2*np.pi, step_value)
        # Calculate y values using the cosine function
        y = np.cos(x)

        # Plot the cosine function
        plt.figure(figsize=(5, 5))
        plt.plot(x, y)
        plt.title('Cosine Function')
        plt.xlabel('x')
        plt.ylabel('cos(x)')
        plt.grid(True)
        plt.savefig("figure.png", dpi=200)
        plt.close()

        width, height, channels, data = load_image(
            'figure.png')

        with texture_registry():
            texture_id = add_static_texture(width, height, data)

        configure_item(plot_image, texture_tag=texture_id)


def change_to_spirograph(sender, data):

    if data == 13 or sender == "spirograph" or sender == "spirograph_step_value":

        step_value = get_value('spirograph_step_value')

        # Parameters: R = radius of fixed circle, r = radius of moving circle, l = distance of pen point from center of moving circle

        # Generate theta values from 0 to 2*pi with a step size of 0.01
        theta = np.arange(0, 2*np.pi, step_value)

        # Set parameters for the Spirograph
        R = 5
        r = 3
        l = 2

        # Parametric equations for Spirograph pattern
        x = (R + r) * np.cos(theta) - l * np.cos((R + r) / r * theta)
        y = (R + r) * np.sin(theta) - l * np.sin((R + r) / r * theta)

        # Plot the Spirograph pattern
        plt.figure(figsize=(5, 5))

        plt.plot(x, y)
        plt.title('Spirograph')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axis('equal')  # Equal aspect ratio
        plt.grid(True)
        plt.savefig("figure.png", dpi=200)
        plt.close()

        width, height, channels, data = load_image(
            'figure.png')

        with texture_registry():
            texture_id = add_static_texture(width, height, data)

        configure_item(plot_image, texture_tag=texture_id)


with window(label='Matplotlib graph', no_collapse=True, no_resize=True, no_close=True, no_move=True, width=640, height=720, pos=[0, 0]):
    plot_image = add_image(
        texture_tag=texture_id,
        width=500,
        height=500,
    )

    add_button(
        label='Graph Settings',
        callback=lambda sender, data: show_item('Graph Settings')
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
        set_axis_ticks(last_item(), (("10 m", 0), ("100 m", 1),
                       ("1 km", 2), ("10 km", 3), ("100 km", 4)))

        add_plot_axis(mvYAxis, label="y", tag="yaxis")
        set_axis_limits(last_item(), 0, 9)
        set_axis_ticks(last_item(), (("10^-5", 0), ("10^-4", 1), ("10^-3", 2), ("10^-2", 3),
                       ("10^-1", 4), ("10^0", 5), ("10^1", 6), ("10^2", 7), ("10^3", 8)))

with window(label='Graph Settings', popup=True, width=200, height=400, show=False, tag='Graph Settings'):

    with group(horizontal=True):

        add_button(
            label="Sine Graph",
            callback=change_to_sin,
            tag='sin'
        )

        add_input_float(
            label='Step Value',
            default_value=0.1,
            tag='sin_step_value',
            step=0.05,
            callback=change_to_sin
        )

    with group(horizontal=True):

        add_button(
            label="Cosine Graph",
            callback=change_to_cos,
            tag='cos'
        )

        add_input_float(
            label='Step Value',
            default_value=0.1,
            tag='cos_step_value',
            step=0.05,
            callback=change_to_cos
        )

    with group(horizontal=True):

        add_button(
            label="Spirograph Graph",
            callback=change_to_spirograph,
            tag='spirograph'
        )

        add_input_float(
            label='Step Value',
            default_value=0.01,
            tag='spirograph_step_value',
            step=0.01,
            callback=change_to_spirograph
        )

show_viewport()
start_dearpygui()
destroy_context()
