import numpy as np
import pyautogui
from statistics import mean
import time

async def screen_average_colors(verbose=False):
    """Calculate an estimated average of the colors on the screen."""
    image = pyautogui.screenshot()

    resolution = pyautogui.size()

    red = []
    green = []
    blue = []

    for i in range(0, resolution[0], 10):
        for j in range(0, resolution[1], 10):
            rgb = image.getpixel((i, j))
            red.append(rgb[0])
            green.append(rgb[1])
            blue.append(rgb[2])

    red_value = int(mean(red))
    green_value = int(mean(green))
    blue_value = int(mean(blue))

    if(verbose):
        print('R:', red_value, 'G:', green_value, 'B:', blue_value)

    return (red_value, green_value, blue_value)

async def dual_screen_average_colors(verbose=False):
    """Calculate two seperate halves of a screen's estimated average of colors."""
    image = pyautogui.screenshot()

    resolution = pyautogui.size()

    left_values = partial_screen_average_colors(image, 0, resolution[0]//2, 0, resolution[1], verbose)
    right_values = partial_screen_average_colors(image, resolution[0]//2, resolution[0], 0, resolution[1], verbose)


    return left_values, right_values

def partial_screen_average_colors(image, width1, width2, height1, height2, verbose):
    """"Gather the estimated average from a selection of the screen."""
    red = []
    green = []
    blue = []

    for i in range(width1, width2, 10):
        for j in range(height1, height2, 10):
            rgb = image.getpixel((i, j))
            red.append(rgb[0])
            green.append(rgb[1])
            blue.append(rgb[2])

    red_value = int(mean(red))
    green_value = int(mean(green))
    blue_value = int(mean(blue))

    if verbose:
        print('R:', red_value, 'G:', green_value, 'B:', blue_value)

    return (red_value, green_value, blue_value)
