# USAGE
# python watermarking.py --watermark --input --ouput --coordinates 
from PIL import Image
import os
import sys
import PySimpleGUI as sg

# GUI Layouts
layout = [[sg.Text('Watermarking.py', size=(25,1), justification='center', font=('Helvetica',25), relief=sg.RELIEF_GROOVE)],
            [sg.Text('Select Watermark', size=(15,1)), sg.InputText('Watermark image'), sg.FileBrowse()],
            [sg.Text('Select Folder', size=(15,1)), sg.InputText('folder with images'), sg.FolderBrowse()],
    [sg.Frame(layout=[
    [sg.Radio('Top left', 'RADIO 1' , size=(10,1)),  sg.Radio('Top right', 'RADIO 1')],
    [sg.Radio('Bottom left', 'RADIO 1', size=(10,1)), sg.Radio('Bottom right', 'RADIO 1')],
    [sg.Radio('Default (center)', 'RADIO 1', default=True)]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Watermark location')],
    [sg.Text('Name of new folder'), sg.InputText( size=(15, 1))],

    [sg.Cancel('Exit'), sg.Submit('Submit')]]

window = sg.Window("Python Image Watermarking", layout, default_element_size=(40, 1) , grab_anywhere=False, location=sg.DEFAULT_WINDOW_LOCATION)

# GUI 
while True:
    window_active = True
    ev, val = window.read(timeout=100)
    if ev  == 'Exit':
        window.close()
        sys.exit() # exit program

    '''
    I prefare this way because using  the sg.WIN_CLOSED or == 'Exit' together crashes the program
    Throwing NameError, then crash
    So separating them prevents the crash
    '''
    if ev == sg.WIN_CLOSED:
        window.close()
        sys.exit() # Exit program
    # when user press the submit button
    if ev == 'Submit':

        # Getting the user values
        TL =            val[2]
        TR =         val[3]
        BL =    val[4]
        BR = val[5]
        C = val[6]
    
        # Folders
        watermark = str(val[0])
        folder = str(val[1])
        folder_new = str(val[7])

        # Closing GUI window
        window_active = False
        window.Hide() # hide the window untill it is again required
        window.close()
        break # This break statement prevents further crash

# Getting number of images watermarked
done = 0
# preparing it for dictionary
coord = None
if TL == True:
    coord = 'TL'
elif TR is True:
    coord = 'TR'
elif BL is True:
    coord = 'BL'
elif BR is True:
    coord = 'BR'
elif C is True:
    coord = 'C'

        # Program rules
        # Image size standards
        # should  be changed if need be
WATERMARK_H = 80
WATERMARK_W = 140

        # Image Size standard
        # The size can be edited to suit your program
STANDARD = 320

        # load the watermark, get height, width
try:
    if not watermark.endswith(".jpg") or (".png"):
        pass # Skip non-image
    watermark = Image.open(watermark)
except FileNotFoundError as err:
    print(str(err))
    sg.popup_notify(str(err))
    sys.exit() # exit program if watermark isn't an image

        # Check if watermark has alpha value, add if it does not
        # by converting to RGBA
if watermark.mode  == 'RGB':
    watermark = watermark.convert('RGBA')
# Get and store size
watermarkWidth, watermarkHeight = watermark.size

        # Match the watermark Width and Height with STANDARD
if watermarkWidth > WATERMARK_W or watermarkHeight > WATERMARK_H:
    watermark = watermark.resize((138, 77)) # Resize with default value NOTE: you can change it
                                                                                            # To suit your need.
    # To make sure new folder is in the inside the image folder
os.chdir(folder)
        # Create a folder to store the watermarked images
os.makedirs(folder_new, exist_ok=True)

        # walk image directory
for filename in os.listdir(folder):
    if not filename.endswith('.jpg') or filename.endswith('.png') or filename == watermark:
        continue # Skip non_image files and the watermark file itself

    try:
        im = Image.open(filename) # Open  image
        width, height = im.size
    except:
        sg.popup_notify('An error occured with {}'.format(filename), display_duration_in_ms=3, fade_in_duration=10)
    if width > STANDARD and height > STANDARD:
        if not width > STANDARD: # Some images tends to have higher width than height
            watermark = watermark.resize((int(watermarkWidth - 15), 0)) # We resize watermark width to fit image width

            # setup the coordinates
            # Calculation for the image pixels coordinates
        top_left = 0,0
        top_right = width - watermarkWidth - 5, height - watermarkHeight - 5
        bottom_left = -0 , height - watermarkHeight - 5
        Default = int(width /2 - watermarkWidth /2), int(height / 2 - watermarkHeight / 2)
        bottom_right = width - watermarkWidth - 5, height - watermarkHeight - 5

                # Reasign them the coordinates values for user coordinates option
        coordinates = {'TL': top_left, 'TR': top_right, 'BR': bottom_right, 'BL': bottom_left, 'C': Default}
        watermark_Coordinates = coordinates.get(coord, Default)
        try:
                    # paste watermark to coordinates provided
            im.paste(watermark, (watermark_Coordinates), watermark) # The 3rd arg can be removed if PIL raise
            im.save(os.path.join(folder_new, filename))                     # KeyError for transparncy issues
            done +=1
        except OSError as err:
            sg.popup_notify(str(err), display_duration_in_ms=1, fade_in_duration=2)


sg.popup(str(done) + ' Images watermarked!' )
