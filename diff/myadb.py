import cv2 as cv
import pyautogui
import numpy as np
import os
import time
from windowcapture import WindowCapture

xcon = 0

winCapBlue = WindowCapture('BlueStacks', 42, 4, 2)


def wait_for_engine_turn():
    global xcon
    x1 = 534
    x2 = 583
    y1 = 48
    y2 = 49

    xcon = xcon + 1

    current_blue_board = winCapBlue.get_screenshot()
    crp = current_blue_board[y1:y2, x1:x2]

    # cv.imshow('original', blueStack)
    # cv.imshow('crop', crp)
    # cv.waitKey()

    for i in range(x2-x1):

        b, g, r = (crp[0, i])
        if(b >= 100):
            print('yes its engine turn')
            cv.imwrite('cv_vision/'+str(xcon)+'.jpg', current_blue_board)
            return True  # <---------- yes its engine turn

    return False


print('3 sec to start')
time.sleep(3)
print('started')
while True:
    if(wait_for_engine_turn() == True):
        break
    time.sleep(0.250)
