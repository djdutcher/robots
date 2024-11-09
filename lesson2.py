from robot import *
import time

led.off()
waitForButton()
led.on()
print('On')
time.sleep(0.5)

waitForButton()
led.off()

print('Done')