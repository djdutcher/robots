import robot
from machine import Pin
import time

robot.speed(30)

while True:
    robot.led.on()
    robot.waitForButton()

    robot.led.off()
    time.sleep(0.5)
    robot.led.on()

    robot.drive(85)
    time.sleep(0.5)
    robot.rotate(70)
    time.sleep(0.5)
    robot.drive(85)
    time.sleep(0.5)
    robot.drive(-85)
    time.sleep(0.5)
    robot.rotate(-70)
    time.sleep(0.5)
    robot.drive(200)
    time.sleep(0.5)

"""

    for i in range(4):
        robot.drive(85)
        time.sleep(1)
        robot.rotate(70)
        time.sleep(1)
"""
    
    
