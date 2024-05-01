
from dearpygui.dearpygui import *
from MatplotlibFunctions import *
import time

create_context()
create_viewport(title='Graphing Prototype', width=1280,
                height=720, resizable=False)
setup_dearpygui()

current_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_directory, "figure.png")


# creating data
sindatax = []
sindatay = []
for i in range(0, 500):
    sindatax.append(i / 100)
    sindatay.append(2 + 2 * np.sin(50 * i / 1000))
sindatay2 = []
for i in range(0, 100):
    sindatay2.append(2 + 0.5 * np.sin(50 * i / 100))

width, height, channels, data = load_image(
    '../DearPyGUI_Attempt/00-demo.png')

with texture_registry():
    texture_id = add_static_texture(width, height, data)


def change_to_sin(sender, data):

    if data == 13 or sender == "sin" or sender == "sin_step_value":

        step_value = get_value('sin_step_value')

        plot_sin(step_value)

        time.sleep(1)

        update_gui(image_path)


def change_to_cos(sender, data):

    if data == 13 or sender == "cos" or sender == "cos_step_value":
        step_value = get_value('cos_step_value')

        plot_cos(step_value)

        time.sleep(1)

        update_gui(image_path)


def change_to_spirograph(sender, data):

    if data == 13 or sender == "spirograph" or sender == "spirograph_step_value":

        step_value = get_value('spirograph_step_value')

        plot_sino(step_value)

        time.sleep(1)

        update_gui(image_path)


def update_gui(image_path):
    width, height, channels, data = load_image(image_path)

    with texture_registry():
        texture_id = add_static_texture(width, height, data)

    set_value(plot_image, texture_id)


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
    with plot(tag="plot", label="Line Series", height=600, width=600, crosshairs=True, no_menus=True):

        # optionally create legend
        add_plot_legend(
            label="Symbols",
            location=mvPlot_Location_NorthEast,
        )

        # REQUIRED: create x and y axes
        add_plot_axis(mvXAxis, label="Diameter")
        set_axis_limits(last_item(), 0, 4.2)
        set_axis_ticks(last_item(), (("10 m", 0), ("100 m", 1),
                       ("1 km", 2), ("10 km", 3), ("100 km", 4)))

        add_plot_axis(mvYAxis, label="Differential crater density, km^3", tag="yaxis")
        set_axis_limits(last_item(), 0, 8)
        set_axis_ticks(last_item(), (("10^-5", 0), ("10^-4", 1), ("10^-3", 2), ("10^-2", 3),
                       ("10^-1", 4), ("10^0", 5), ("10^1", 6), ("10^2", 7), ("10^3", 8)))

        add_plot_annotation(
            label="Epochs: Mars, Michael (2013)\n"
                  "EF: Standard lunar equilibrium (Trusk, 1966)\n"
                  "PF: Mars, Ivanov (2001)\n"
                  "CF: Mars, Hartmann & Neukum (2001)",
        )

        add_scatter_series([3], [5], parent='yaxis')

with window(label='Graph Settings', popup=True, width=200, height=400, show=False, tag='Graph Settings'):
    def add_plot_point(sender, app_data):

        if data == 13 or sender == "add_point":
            x = int(get_value('values')[1])
            y = int(get_value('values')[3])

            add_scatter_series([x], [y], parent='yaxis')

    add_text('Matplotlib graph')

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

    add_text('DearPyGUI graph')

    with group(horizontal=True):
        add_text('X, y position')

        add_input_doublex(
            default_value=(1, 2.3),
            tag='values',
            format='0.0',
            size=2,
            width=80,
        )

        add_button(
            label="Add plot point",
            callback=add_plot_point,
            tag='add_point',

        )


show_viewport()
start_dearpygui()
destroy_context()
