import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os


current_directory = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_directory, "figure.png")

def plot_sin(step_value):
    # Generate x values from 0 to 2*pi with a step size of 0.1
    x = np.arange(0, 2 * np.pi, step_value)
    # Calculate y values using the sine function
    y = np.sin(x)

    # Plot the sine function
    plt.figure(figsize=(5, 5))

    plt.plot(x, y)
    plt.title('Sine Function')
    plt.xlabel('x')
    plt.ylabel('sin(x)')
    plt.grid(True)
    plt.savefig(image_path, dpi=200)
    plt.close()


def plot_cos(step_value):

    # Generate x values from 0 to 2*pi with a step size of 0.1
    x = np.arange(0, 2 * np.pi, step_value)
    # Calculate y values using the cosine function
    y = np.cos(x)

    # Plot the cosine function
    plt.figure(figsize=(5, 5))
    plt.plot(x, y)
    plt.title('Cosine Function')
    plt.xlabel('x')
    plt.ylabel('cos(x)')
    plt.grid(True)
    plt.savefig(image_path, dpi=200)
    plt.close()


def plot_sino(step_value):
    theta = np.arange(0, 2 * np.pi, step_value)

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
    plt.savefig(image_path, dpi=200)
    plt.close()
