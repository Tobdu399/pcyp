"""
Description:

    -----------------------| pycp.py |-----------------------
    |                                                       |
    |        A file of the Python Color Picker tool.        |
    |                                                       |
    |                  Creator: Tobdu 399                   |
    |                                                       |
    ---------------------------------------------------------
"""

from lib.misc import *


def RGBtoHEX(RGB):
    # Convert RGB color code to HEX
    hex_value = "#%02x%02x%02x" % RGB
    return hex_value


def updateWindow():
    # Set the current color as the background color 
    # of the tkinter window
    global HEX_COLOR
    if not PICKING_COLOR:
        HEX_COLOR = RGBtoHEX((r_slider.get(), g_slider.get(), b_slider.get()))
    
    display.config(bg=HEX_COLOR)


def updateSliders():
    # Update the color sliders and also set the text
    # color to white and black depending on the
    # current color's brightness
    global TXT_COLOR
    if int(r_slider.get()) + int(g_slider.get()) + int(b_slider.get()) >= 355:
        TXT_COLOR = "#000000"
    else:
        TXT_COLOR = "#ffffff"

    r_slider.config(bg=HEX_COLOR, fg=TXT_COLOR)
    g_slider.config(bg=HEX_COLOR, fg=TXT_COLOR)
    b_slider.config(bg=HEX_COLOR, fg=TXT_COLOR)

    if PICKING_COLOR and COLOR_UNDER_CURSOR != None:
        r, g, b = COLOR_UNDER_CURSOR
        r_slider.set(r)
        g_slider.set(g)
        b_slider.set(b)


def updateSliderLabels():
    # Update the labels of the sliders with the sliders'
    # current value
    global TXT_BACKGROUND

    if not PICKING_COLOR:
        r = int(r_slider.get()) - 20 if int(r_slider.get()) >= 20 else int(r_slider.get())
        g = int(g_slider.get()) - 20 if int(g_slider.get()) >= 20 else int(g_slider.get())
        b = int(b_slider.get()) - 20 if int(b_slider.get()) >= 20 else int(b_slider.get())
        TXT_BACKGROUND = RGBtoHEX((r, g, b))

    r_label.config(text=f"R {r_slider.get()}", bg=TXT_BACKGROUND, fg=TXT_COLOR)
    g_label.config(text=f"G {g_slider.get()}", bg=TXT_BACKGROUND, fg=TXT_COLOR)
    b_label.config(text=f"B {b_slider.get()}", bg=TXT_BACKGROUND, fg=TXT_COLOR)


def showColorCode():
    # Update the label that contains the current
    # color code
    color_code.config(text=HEX_COLOR.upper(), bg=TXT_BACKGROUND, fg=TXT_COLOR)


def updateColorPickerButton():
    # Disable the color picker button when clicked and
    # other visual stuff for the button
    if PICKING_COLOR:
        color_picker.config(relief="sunken", state="disabled")
    else:
        color_picker.config(relief="groove", state="normal")


def activateColorPicker():
    # Start the thread, that is used for the color picking
    # from the screen
    global PICKING_COLOR
    PICKING_COLOR = True
    threading.Thread(target=pickColorFromScreen, daemon=True).start()


def update():
    # Function to update the tkinter window and all it's
    # contents
    updateWindow()
    updateSliders()
    updateSliderLabels()
    showColorCode()


def onClosing():
    # When closing the window, save the current color to a file
    pickle.dump((int(r_slider.get()), int(g_slider.get()), int(b_slider.get())), open("cache/cache.pycp", "wb"))
    display.destroy()


def getColorInPos(pos):
    # Get the color of the pixel in the given location
    x, y  = pos
    color = win32gui.GetPixel(win32gui.GetDC(0),x, y)
    color = (color & 0xff), ((color >> 8) & 0xff), ((color >> 16) & 0xff)
    return color


def copyToClipboard():
    # Copy the current color code to clipboard
    display.clipboard_clear()
    display.clipboard_append(HEX_COLOR.upper())


def pickColorFromScreen():
    # This is a thread loop, used for picking a color
    # from the display
    global PICKING_COLOR, COLOR_UNDER_CURSOR, HEX_COLOR, TXT_BACKGROUND

    while PICKING_COLOR:
        updateColorPickerButton()
        state_left = win32api.GetKeyState(0x01)

        x, y               = win32gui.GetCursorPos()
        COLOR_UNDER_CURSOR = getColorInPos((x, y))
        HEX_COLOR          = RGBtoHEX(COLOR_UNDER_CURSOR)
        
        r, g, b = [val - 20 if val >= 20 else val for val in COLOR_UNDER_CURSOR]
        TXT_BACKGROUND = RGBtoHEX((r, g, b))

        update()

        if state_left < 0:
            PICKING_COLOR = False
    
    updateColorPickerButton()


def loadPrevious():
    # Load the previous color, if a save file is found
    global PREVIOUS_COLOR
    if pathlib.Path("cache").is_dir():
        if pathlib.Path("cache/cache.pycp").is_file():
            PREVIOUS_COLOR = pickle.load(open("cache/cache.pycp", "rb"))
    else:
        pathlib.Path("cache").mkdir()


def gui():
    """
    Python Color Picker's Graphical User Interface
    """

    # Set the needed variables that are declared inside this function
    # global, so that they can be used outside from this function
    global display
    global r_slider, g_slider, b_slider
    global r_label, g_label, b_label
    global color_code, color_picker

    loadPrevious()

    # Create a tkinter window
    display = Tk()
    display.title("Color Picker")
    
    # Set a titlebar icon
    display.iconbitmap(f"{path}/pictures/icon.ico")
    
    # Set the window size
    display.geometry("450x175")

    # Make the window unresizable
    display.resizable(False, False)

    # Keep the window always on top
    display.attributes("-topmost", True)

    # Color sliders
    r_slider = Scale(display, from_=0, to=255, orient=HORIZONTAL, highlightthickness=0, showvalue=False, tickinterval=255, length=250, command=lambda x=None: update())
    g_slider = Scale(display, from_=0, to=255, orient=HORIZONTAL, highlightthickness=0, showvalue=False, tickinterval=255, length=250, command=lambda x=None: update())
    b_slider = Scale(display, from_=0, to=255, orient=HORIZONTAL, highlightthickness=0, showvalue=False, tickinterval=255, length=250, command=lambda x=None: update())
    
    # Color sliders labels (RGB)
    r_label = Label(display, text="RGB", width=7, font=("Inconsolata", 11))
    g_label = Label(display, text="RGB", width=7, font=("Inconsolata", 11))
    b_label = Label(display, text="RGB", width=7, font=("Inconsolata", 11))

    # Pick color and copy buttons images
    color_picker_image = PhotoImage(file=f"{path}/pictures/colorpicker.png")
    color_picker = Button(display, image=color_picker_image, width=22, height=22, bg="#0093f0", activebackground="#00b0f0", command=lambda x=None: activateColorPicker())

    # Pick color and copy buttons
    copy_button_image = PhotoImage(file=f"{path}/pictures/copy.png")
    copy_button = Button(display, image=copy_button_image, width=56, height=22, bg="#0093f0", relief="groove", activebackground="#00b0f0", command=lambda x=None: copyToClipboard())

    # Color code
    color_code = Label(display, text="#------", width=13, font=("Inconsolata", 11))

    # Position sliders
    r_slider.place(x=10, y=30)
    g_slider.place(x=10, y=70)
    b_slider.place(x=10, y=110)

    # Position slidrs labels
    r_label.place(x=280, y=30-4)
    g_label.place(x=280, y=70-4)
    b_label.place(x=280, y=110-4)

    # Position buttons
    color_picker.place(x=345, y=70-4)
    copy_button.place(x=380, y=70-4)

    # Position color code
    color_code.place(x=345, y=110-4)   

    # If a previous color was loaded, use it on startup,
    # othrwise use the default color
    if PREVIOUS_COLOR != None:
        r_slider.set(PREVIOUS_COLOR[0])
        g_slider.set(PREVIOUS_COLOR[1])
        b_slider.set(PREVIOUS_COLOR[2])
        update()
    else:
        r_slider.set(random.randint(0, 255))
        g_slider.set(random.randint(0, 255))
        b_slider.set(random.randint(0, 255))
        update()

    # Set what happens, when the program is closed. In this
    # case, save the current color to a file and use it the
    # next time this program is opened
    display.protocol("WM_DELETE_WINDOW", onClosing)

    # End tkinter loop
    display.mainloop()
