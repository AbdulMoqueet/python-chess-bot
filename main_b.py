import cv2 as cv
import pyautogui
import numpy as np
import os
import time
from windowcapture import WindowCapture

# board = cv.imread('u2.jpg', cv.IMREAD_UNCHANGED)
empty_white = cv.imread('empty_white.jpg', cv.IMREAD_UNCHANGED)
empty_black = cv.imread('empty_black.jpg', cv.IMREAD_UNCHANGED)
black__white = cv.imread('black.jpg', cv.IMREAD_UNCHANGED)
black__black = cv.imread('black__black.jpg', cv.IMREAD_UNCHANGED)

board = None
previous = None
# initialize the WindowCapture class
wincap = WindowCapture('Screen Stream')


def enginePlay(x, y):
    x = 29 + (x*50)
    y = 88 + (y*50)
    pyautogui.click(x, y)


def get_location(image_to_find, threshold, adj):

    result = cv.matchTemplate(
        board, image_to_find, cv.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print('confidence: %s' % str(max_val))

    x = max_loc[0] + 22
    y = max_loc[1] + (22 - adj)

    if (max_val >= threshold):
        # cv.drawMarker(board, (x, y),
        #               color=(0, 0, 255), markerType=cv.MARKER_CROSS, thickness=2)
        # cv.imshow('Computer Vision', board)

        # cv.waitKey()
        return ((x-20)//40, (y-20)//40)

    else:
        # cv.imshow('Computer Vision', board)
        return 0


while(True):
    time.sleep(0.3)
    loop_time = time.time()
    opponent_from = 0
    opponent_to = 0
    # get an updated image of the game
    board = wincap.get_screenshot()
    # board = cv.imread('bb6.jpg', cv.IMREAD_UNCHANGED)

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))

    # from --- white <---> white
    res = get_location(empty_white, 0.995, 0)
    print('Res:', res)
    if(res == 0):
        opponent_from = get_location(empty_black, 0.995, 0)
    else:
        opponent_from = res

    # to --- white <---> white
    res = get_location(black__white, 0.975, 22)
    print('Res: black__white', res)

    if(res == 0):
        opponent_to = get_location(black__black, 0.975, 22)
        print('Res: black__black', opponent_to)
    else:
        opponent_to = res

    if(opponent_from != 0 and opponent_to != 0):

        if(previous != opponent_from):
            print('From:', opponent_from)
            enginePlay(opponent_from[0], opponent_from[1])
            print('To:', opponent_to)
            enginePlay(opponent_to[0], opponent_to[1])
            previous = opponent_from
            time.sleep(1)

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
    # if cv.waitKey(1) == ord('q'):
    #     cv.destroyAllWindows()
    #     break

print('Done.')
