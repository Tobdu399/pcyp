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

path = str(pathlib.Path(__file__).resolve().parent)
pyglet.font.add_file(f"{path}/fonts/Inconsolata.ttf")
