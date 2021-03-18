import pyautogui
import time


def enginePlay(x, y):
    x = 29 + (x*50)
    y = 88 + (y*50)
    pyautogui.click(x, y)


print('doing')
time.sleep(3)
enginePlay(1, 1)
enginePlay(1, 3)
myScreenshot = pyautogui.screenshot()
myScreenshot.save('scr.jpg')

#x1, y4, y6

print('done')
