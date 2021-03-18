import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture

# wincap = WindowCapture('Screen Stream')
# board = wincap.get_screenshot()
board = cv.imread('cv_vision/1.jpg', cv.IMREAD_UNCHANGED)


def tmp_print(board_to_print):
    for i in range(8):
        for j in range(8):
            print(board_to_print[j+(i*8)], end=' ')
        print()


def covert_gui_to_bit(board):
    board_map = [
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em',
        'em', 'em', 'em', 'em', 'em', 'em', 'em', 'em']

    for i in range(6):
        piece = cv.imread('b_black/'+str(i)+'.jpg', cv.IMREAD_UNCHANGED)
        needle_w = piece.shape[1]
        needle_h = piece.shape[0]

        result = cv.matchTemplate(board, piece, cv.TM_CCORR_NORMED)
        threshold = 0.90
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

        if len(rectangles):
            for (x, y, w, h) in rectangles:
                top_left = (x, y)
                bottom_right = (x+w, y+h)
                cv.rectangle(board, top_left, bottom_right,
                             (0, 0, 255), cv.LINE_4)
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                # print(center_x//40, center_y//40)
                xx = center_x//40
                yy = center_y//40
                board_map[xx+(yy*8)] = '**'
                # print(xx+(yy*8))

                cv.drawMarker(board, (center_x, center_y),
                              (0, 0, 255), cv.MARKER_CROSS)
    return board_map


tmp_print(covert_gui_to_bit(board))
cv.imshow('Computer Vision', board)
cv.waitKey()
