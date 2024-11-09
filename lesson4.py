from robot import *
import time


blinkLed(3)
waitForButton()
led.on()

drive(200)
time.sleep(1)
drive(-200)
