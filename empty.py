import cv2 as cv
import numpy as np

haystack_img = cv.imread('3.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('empty_black.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('empty_white.jpg', cv.IMREAD_UNCHANGED)

needle_w = needle_img.shape[1] - 4
needle_h = needle_img.shape[0] - 4

#empty_white: cv.TM_CCORR_NORMED
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCORR_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('confidence: %s' % str(max_val))

x = max_loc[0]
y = max_loc[1] - 30

print(x, y)

print('x:', (x//40)+1, 'y:', (y//40)+1)

if (max_val >= 0.995):

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    # cv.rectangle(haystack_img, top_left, bottom_right, color=(0, 0, 255), thickness=2, lineType=cv.LINE_4)
    cv.drawMarker(haystack_img, (x+20, y+50), color=(
        0, 0, 255),  markerType=cv.MARKER_CROSS, thickness=2)
    # cv.drawMarker(haystack_img, (int(center_x), int(center_y)), color=(0, 255, 0),
    #                markerType=cv2.MARKER_CROSS, thickness=2)

else:
    print('Not found!!!')

cv.imshow('result.jpg', haystack_img)
cv.waitKey()
