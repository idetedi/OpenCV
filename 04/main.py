import cv2 as cv
import os
from time import time

import win32gui

from window_capture import WindowCapture

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# list_windows_names()

# initialize the WindowCapture class
WindowCapture
wincap = WindowCapture('Minecraft 1.16.5 - Singleplayer')

go = True
loop_time = time()
while go:

    if wincap is not None:
        # get an updated image of the game
        screenshot = wincap.get_screenshot()

        cv.imshow('Computer Vision', screenshot)

        # debug the loop rate
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

        # press 'q' with the output window focused to exit.
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break
    else:
        print('Minecraft "Minecraft 1.16.5 - Singleplayer" not found')
        go = False

if go:
    print("ok")
    exit(0)
else:
    exit(1)
