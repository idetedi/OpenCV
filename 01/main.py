import cv2 as cv
import numphy as np

# Capture
hystack_img = cv.imread('img/Minecraft.png', cv.IMREAD_UNCHANGED)
# What i'm searching
needle_img = cv.imread('img/poppy.png', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(hystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# Get the best location
min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

print('Best match top left position: %s' % str(max_loc))
print('Best match confidence: %s' % str(max_val))

# Confidence
threshold = 0.8
if max_val >= threshold:
    print('Found poppy')

    # get dimensions of the poppy
    poppy_w = needle_img.shape[1]
    poppy_h = needle_img.shape[0]

    top_left = max_loc
    bottom_right = (top_left[0] + poppy_w, top_left[1] + poppy_h)

    cv.rectangle(hystack_img, top_left, bottom_right, color=(0, 255, 0), thickness=2, lineType=cv.LINE_4)

    # cv.imshow('Result', hystack_img)
    # cv.waitKey()
    cv.imwrite('01/img/result.png', hystack_img)
else:
    print('Poppy not found.')
