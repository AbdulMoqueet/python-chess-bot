from ppadb.client import Client
from pynput.keyboard import Key, Listener
import cv2 as cv
import pyautogui
import numpy as np
import os
import time
from random import randrange
from windowcapture import WindowCapture

adb = Client(host="127.0.0.1", port=5037)
devices = adb.devices()
device = devices[0]

wincap = WindowCapture('Screen Stream', 32, 8, 8)
winCapBlue = WindowCapture('BlueStacks', 42, 4, 2)
blueStack = winCapBlue.get_screenshot()
board = wincap.get_screenshot()

# cv.imwrite('blue.jpg', blueStack)

# piece = cv.imread('15.jpg', cv.IMREAD_UNCHANGED)
opponent_black = False
android_img_path = 'black/'

xcon = 0

# Read Current Opponent Turn & return XY <----------


def get_opponent_xy(endLimit, startLimit=0, threshold=0.99):

    for i in range(startLimit, endLimit):

        needle = cv.imread(android_img_path+str(i)+'.jpg', cv.IMREAD_UNCHANGED)
        needle_w = needle.shape[1]
        needle_h = needle.shape[0]

        result = cv.matchTemplate(board, needle, cv.TM_CCORR_NORMED)
        min_val, confidence, min_loc, max_loc = cv.minMaxLoc(result)

        if(confidence >= threshold):

            top_left = max_loc
            bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

            center_x = top_left[0] + int(needle_w/2)
            center_y = top_left[1] + int(needle_h/2)

            print('x:', center_x, 'y:', center_y,
                  '<---- confidence: ', confidence)

            # cv.rectangle(board, top_left, bottom_right,
            #              color=(0, 0, 255), thickness=2, lineType=cv.LINE_4)

            # cv.drawMarker(board, (center_x, center_y),
            #               color=(255, 0, 0), markerType=cv.MARKER_CROSS,
            #               markerSize=40, thickness=2)
            # cv.imshow('Computer Vision', board)
            # cv.waitKey()

            # return (center_x//40, center_y//40)
            return (center_x, center_y)


def our_turn():
    b, g, r = (board[461, 95])
    # cv.drawMarker(board, (95, 461),
    #               color=(255, 0, 0), markerType=cv.MARKER_CROSS,
    #               markerSize=6, thickness=1)
    # cv.imshow('Computer Vision', board)
    # cv.waitKey()

    if(b >= 220 and g >= 220 and r >= 220):
        return True
    print('Waiting for: Opponent Turn...')
    return False


def wait_for_engine_turn(blueStack):
    # global xcon
    x1 = 534
    x2 = 583
    y1 = 48
    y2 = 49

    # xcon = xcon + 1

    # cv.imwrite('cv_vision/'+str(xcon)+'.jpg', current_blue_board)
    crp = blueStack[y1:y2, x1:x2]

    # cv.imshow('original', blueStack)
    # cv.imshow('crop', crp)
    # cv.waitKey()

    for i in range(x2-x1):

        b, g, r = (crp[0, i])
        if(b >= 100):
            return True  # <---------- yes its engine turn

    return False


def starting_first_env(color):
    # Changing to blueStack
    time.sleep(0.2)
    pyautogui.keyDown('alt')
    pyautogui.keyDown('tab')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('tab')

    time.sleep(0.5)
    # Calling Macro In Blue Stack
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('alt')
    pyautogui.keyDown(color)
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('alt')
    pyautogui.keyUp(color)
    time.sleep(4)
    # main()


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
        threshold = 0.99
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
                # top_left = (x, y)
                # bottom_right = (x+w, y+h)
                # cv.rectangle(board, top_left, bottom_right, (0, 0, 255), cv.LINE_4)
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                # print(center_x//40, center_y//40)
                xx = center_x//40
                yy = center_y//40
                board_map[xx+(yy*8)] = '**'
                # print(xx+(yy*8))

                # cv.drawMarker(board, (center_x, center_y),
                #               (0, 0, 255), cv.MARKER_CROSS)
    return board_map


def both_map_are_same(prev_board_map, current_board_map):
    # return false if not same
    # return true if same
    for i in range(64):
        if(prev_board_map[i] != current_board_map[i]):
            return False
    return True


def convert_bit_map__xy(prev_board_map, current_board_map):

    move_for_android = {'from': None, 'to': None}
    for i in range(64):
        if(prev_board_map[i] != current_board_map[i]):
            if(prev_board_map[i] == 'em'):
                print('to:', i)
                x = i % 8
                y = i//8
                print('x:', x, 'y:', y)
                move_for_android['to'] = (x, y)
            else:
                print('from:', i)
                x = i % 8
                y = i//8
                print('x:', x, 'y:', y)
                move_for_android['from'] = (x, y)
    return move_for_android


def play_in_adb(best_move):
    print(best_move['from'])
    print(best_move['to'])
    from_x = 80+((best_move['from'])[0]*80)+randrange(10)
    from_y = 520+((best_move['from'])[1]*80)+randrange(10)
    from_adb = 'input tap ' + str(from_x)+' '+str(from_y)

    to_x = 80+((best_move['to'])[0]*80)+randrange(10)
    to_y = 520+((best_move['to'])[1]*80)+randrange(10)
    to_adb = 'input tap ' + str(to_x)+' '+str(to_y)

    print(from_adb)
    device.shell(from_adb)
    print(to_adb)
    device.shell(to_adb)


def play_in_blueStack(opp_from, opp_two):

    pyautogui.click(opp_from[0]+10, opp_from[1]+42)
    pyautogui.click(opp_to[0]+10, opp_to[1]+42)
    while True:
        time.sleep(0.5)
        blueStack = winCapBlue.get_screenshot()
        if(wait_for_engine_turn(blueStack) == False):
            print('Engine Made Move breaking loop')
            break  # <------- Engine Made Move breaking loop
        print('Waiting for engine...')

# Listening for keys ------------------


def keyPress(key):
    if key == Key.space:
        opponent_black = True
        print('Opponent is Black...')
        starting_first_env('b')
    else:
        opponent_black = False
        print('Opponent is White...')
        starting_first_env('w')
    return False


# <----------- Entry Point
print('Opponent: Black | Press: [Space]')
with Listener(on_press=keyPress) as listener:
    listener.join()
# ----------------------------------

# <---------- Main()
prev_board_map = None
current_board_map = None
if(opponent_black):
    android_img_path = 'black/'
else:
    android_img_path = 'white/'
while True:
    # <--------- opponent is white:
    board = wincap.get_screenshot()
    blueStack = winCapBlue.get_screenshot()
    if(our_turn()):
        time.sleep(0.3)
        board = wincap.get_screenshot()
        opp_from = get_opponent_xy(3)
        opp_to = get_opponent_xy(14, 2)
        prev_board_map = covert_gui_to_bit(blueStack)

        print('Before: ')
        tmp_print(prev_board_map)
        play_in_blueStack(opp_from, opp_to)

        print('After: ')
        mm = 0
        while True:
            current_blue_bd = winCapBlue.get_screenshot()
            current_board_map = covert_gui_to_bit(current_blue_bd)
            tmp_print(current_board_map)
            if (both_map_are_same(prev_board_map, current_board_map) == False):
                mm = mm+1
                cv.imwrite('cv_vision/'+str(mm)+'.jpg', current_blue_bd)
                best_move = convert_bit_map__xy(
                    prev_board_map, current_board_map)
                play_in_adb(best_move)
                print('Not Same, return value: False [[[We R Good]]]')
                break
            else:
                print('Both Map Are Same [[[Wrong]]]]')

    time.sleep(0.250)
