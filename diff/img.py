import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture

wincap = WindowCapture('Screen Stream')
board = wincap.get_screenshot()
# cv.imwrite('board.jpg', board)
piece = cv.imread('2.jpg', cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(board, piece, cv.TM_CCORR_NORMED)
threshold = 0.99
locations = np.where(result >= threshold)

locations = list(zip(*locations[::-1]))

needle_w = piece.shape[1]
needle_h = piece.shape[0]

found = 0

for loc in locations:
    found = found + 1
    print(loc)
    top_left = loc
    bottom_right = (top_left[0]+needle_w, top_left[1]+needle_h)
    cv.rectangle(board, top_left, bottom_right, (0, 0, 255), cv.LINE_4)

print(found)

matched = 0
dngr = 0


def img_to_code_name(idx):
    switcher = {
        0: 'em',
        1: 'em',
        2: 'bp',
        3: 'bp',
        4: 'br',
        5: 'br',
        6: 'bn',
        7: 'bn',
        8: 'bb',
        9: 'bb',
        10: 'bq',
        11: 'bq',
        12: 'bk',
        13: 'bk',
        14: 'em',
        15: 'em',
        16: 'bp',
        17: 'bp',
        18: 'br',
        19: 'br',
        20: 'bn',
        21: 'bn',
        22: 'bb',
        23: 'bb',
        24: 'bk',
        25: 'bk',
        26: 'bq',
        27: 'bq',
        28: 'wp',
        29: 'wp',
        30: 'wb',
        31: 'wb',
        32: 'wq',
        33: 'wq',
        34: 'wn',
        35: 'wn',
        36: 'wr',
        37: 'wr',
        38: 'wk',
        39: 'wk',
        40: 'wp',
        41: 'wp',
        42: 'wb',
        43: 'wb',
        44: 'wq',
        45: 'wq',
        46: 'wn',
        47: 'wn',
        48: 'wr',
        49: 'wr',
        50: 'wk',
        51: 'wk'
    }
    return switcher.get(idx, "Invalid")


'''
for i in range(0, 8):

    offset_y = (i*39)

    if(i >= 3 and i <= 4):
        offset_y = (i*39)+1
    elif(i >= 5):
        offset_y = (i*39)+2

    for j in range(0, 8):
        # img[y:y+h, x:x+w]
        offset_x = (j*39)

        if(j >= 3 and j <= 4):
            offset_x = (j*39)+1
        elif(j >= 5):
            offset_x = (j*39)+2

        # print('i:', i)

        cropSquare = board[offset_y:offset_y+39, offset_x:offset_x+37].copy()
        for k in range(0, 52):
            piece = cv.imread(str(k)+'.jpg', cv.IMREAD_UNCHANGED)

            result = cv.matchTemplate(
                cropSquare, piece, cv.TM_CCORR_NORMED)
            min_val, confidence, min_loc, max_loc = cv.minMaxLoc(result)

            # print('Min_Val:', min_val, ' confidence:', confidence)
            if(confidence >= 0.99):
                # print('<------Exact Match: ', img_to_code_name(k))
                matched = matched + 1
                # print('Matched:', matched)
                cv.imshow('piece', piece)
                cv.imshow('square', cropSquare)
                # cv.waitKey()
                break
            elif (confidence >= 0.98 and i == 7):
                matched = matched + 1
                print('Last Line Re-correcting', matched)
                cv.imshow('piece', piece)
                cv.imshow('square', cropSquare)
                cv.waitKey()
                break

            elif (confidence >= 0.98):
                dngr = dngr + 1
                print('Danger #############################-- No:', (i+1)*(j+1))
                print('Error:', confidence)
                cv.imshow('piece', piece)
                cv.imshow('square', cropSquare)
                cv.waitKey()
'''
print('Total Matched:', matched)
cv.imshow('Computer Vision', board)
cv.waitKey()
