"""
Description:

    -----------------------| misc.py |-----------------------
    |                                                       |
    |        A file of the Python Color Picker tool.        |
    |                                                       |
    |                  Creator: Tobdu 399                   |
    |                                                       |
    ---------------------------------------------------------
"""

# Import the libraries that are needed for this
# program to work
from tkinter import *
import pyglet
import pathlib
import pickle
import random
import win32api
import win32gui
import threading

HEX_COLOR          = "#ffffff"
TXT_COLOR          = None
TXT_BACKGROUND     = None
PREVIOUS_COLOR     = None
COLOR_UNDER_CURSOR = None
PICKING_COLOR      = False

# The path to this file's parent directory
path = str(pathlib.Path(__file__).resolve().parent)

# Adding a custom font
pyglet.font.add_file(f"{path}/fonts/Inconsolata.ttf")
