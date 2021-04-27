import cv2 as cv
import numpy as np
import os

#ChangeDirectory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Capture
haystack_img = cv.imread('img/Minecraft.png', cv.IMREAD_UNCHANGED)
# What i'm searching
poppy_img = cv.imread('img/poppy.png', cv.IMREAD_UNCHANGED)

# TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
result = cv.matchTemplate(haystack_img, poppy_img, cv.TM_SQDIFF_NORMED)

#threshold is inverted to work with TM_SQDIFF_NORMED
threshold = 0.06455

locations = np.where(result <= threshold)
locations = list(zip(*locations[::-1]))
print(locations)

if locations:
    print('Found poppy.')

    poppy_w = poppy_img.shape[1]
    poppy_h = poppy_img.shape[0]
    line_color = (0, 255, 0)
    line_type = cv.LINE_4

    # Loop over all the locations and draw their rectangle
    for loc in locations:
        # Determine the box positions
        top_left = loc
        bottom_right = (top_left[0] + poppy_w, top_left[1] + poppy_h)
        # Draw the box
        cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)

    cv.imshow('Matches', haystack_img)
    cv.waitKey()
    #cv.imwrite('result.jpg', haystack_img)

else:
    print('Needle not found.')