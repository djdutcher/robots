from robot import *
import time

#buttonLed()

blinkLed(3)
waitForButton()
blinkLed(3)

left()
time.sleep(2)
right()
time.sleep(2)
run()
time.sleep(2)
stop()


time.sleep(1)
drive(150)
#runb()
#run()
