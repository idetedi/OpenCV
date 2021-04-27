import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def findClickPositions(poppy_img_path, minecraft_img_path, threshold=0.1, debug_mode=None):
    haystack_img = cv.imread(minecraft_img_path, cv.IMREAD_UNCHANGED)
    poppy_img = cv.imread(poppy_img_path, cv.IMREAD_UNCHANGED)

    poppy_w = poppy_img.shape[1]
    poppy_h = poppy_img.shape[0]

    # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(haystack_img, poppy_img, method)

    # Get the all the positions from the match result that exceed our threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))
    # print(locations)

    # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
    # locations by using groupRectangles().
    # First we need to create the list of [x, y, w, h] rectangles
    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), poppy_w, poppy_h]
        # Add every box to the list twice in order to retain single (non-overlapping) boxes
        rectangles.append(rect)
        rectangles.append(rect)
    # Apply group rectangles.
    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
    # print(rectangles)

    point = []
    if len(rectangles):
        # print('Found needle.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:

            # Determine the center position
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Save the points
            point.append((center_x, center_y))

            if debug_mode == 'rectangles':
                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, color=line_color,
                             lineType=line_type, thickness=2)
            elif debug_mode == 'points':
                # Draw the center point
                cv.drawMarker(haystack_img, (center_x, center_y),
                              color=marker_color, markerType=marker_type,
                              markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('Matches', haystack_img)
            cv.waitKey()
            # cv.imwrite('result_click_point.jpg', haystack_img)

    return point


points = findClickPositions('img/poppy.png', 'img/Minecraft.png', debug_mode='points')
print(points)
# points = findClickPositions('img/poppy.png', 'img/Minecraft.png',
#                            threshold=0.70, debug_mode='rectangles')
# print(points)
print('Done.')
