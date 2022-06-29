import pyautogui as pt
from time import sleep

while True:
    posXY = pt.position()
    print(posXY, pt.pixel(posXY[0], posXY[1]))
    sleep(1)
    if posXY[0] == 0:
      break


#smile - Point(x=669, y=993) (32, 44, 51)
#msgBox - Point(x=839, y=1002) (42, 57, 66)
#receivedMsg - Point(x=764, y=930) (0, 120, 215)
#copy - Point(x=808, y=650) (82, 82, 94)