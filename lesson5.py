from robot import *
import time

blinkLed(3)
led.on()
waitForButton()
blinkLed(2)
led.on()

speed(50)
drive(150)
speed(20)
time.sleep(1)
rotate(160)
speed(50)
time.sleep(1)
drive(150)

led.off()