import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture

# board = cv.imread('u2.jpg', cv.IMREAD_UNCHANGED)
empty_white = cv.imread('empty_white.jpg', cv.IMREAD_UNCHANGED)
empty_black = cv.imread('empty_black.jpg', cv.IMREAD_UNCHANGED)
white__white = cv.imread('white.jpg', cv.IMREAD_UNCHANGED)
white__black = cv.imread('white__black.jpg', cv.IMREAD_UNCHANGED)

board = None

# initialize the WindowCapture class
wincap = WindowCapture('Screen Stream')


def get_location(image_to_find, threshold, adj):

    result = cv.matchTemplate(
        board, image_to_find, cv.TM_CCORR_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    print('confidence: %s' % str(max_val))

    x = max_loc[0] + 20
    y = max_loc[1] + adj

    print(x-20, y-50)

    if (max_val >= threshold):
        cv.drawMarker(board, (x, y),
                      color=(0, 0, 255), markerType=cv.MARKER_CROSS, thickness=2)
        cv.imshow('Computer Vision', board)

        # cv.imshow('result.jpg', board)
        # cv.waitKey()
        return 'x: '+str(((x-20)//40)+1) + ' y: '+str(((y-50)//40)+1)

    else:
        cv.imshow('Computer Vision', board)
        return 0


while(True):
    loop_time = time.time()
    opponent_from = 0
    opponent_to = 0
    # get an updated image of the game
    board = wincap.get_screenshot()

    # debug the loop rate
    print('FPS {}'.format(1 / (time.time() - loop_time)))

    # from --- white <---> white
    res = get_location(empty_white, 0.995, 15)
    if(res == 0):
        opponent_from = get_location(empty_black, 0.995, 15)
    else:
        opponent_from = res

    # to --- white <---> white
    res = get_location(white__white, 0.986, -15)
    if(res == 0):
        opponent_to = get_location(white__black, 0.986, -15)
    else:
        opponent_to = res

    if(opponent_from != 0 and opponent_to != 0):
        print('We have info...')
        print('From:', opponent_from)
        print('To:', opponent_to)
        break

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
