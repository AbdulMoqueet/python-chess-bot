import cv2 as cv
import numpy as np

print(20//40)

haystack_img = cv.imread('3.jpg', cv.IMREAD_UNCHANGED)
needle_img = cv.imread('white.jpg', cv.IMREAD_UNCHANGED)

#empty_white: cv.TM_CCORR_NORMED
result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCORR_NORMED)

min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
print('confidence: %s' % str(max_val))

# print('x: ', max_loc[0])
print(cv.minMaxLoc(result))
if (max_val >= 0.986):
    needle_w = needle_img.shape[1] - 4
    needle_h = needle_img.shape[0] - 4

    top_left = max_loc
    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

    cv.rectangle(haystack_img, top_left, bottom_right,
                 color=(0, 0, 255), thickness=2, lineType=cv.LINE_8)
else:
    print('Not found!!!')

cv.imshow('result.jpg', haystack_img)
cv.waitKey()
