import robot
from machine import Pin
import time

led = Pin(2, Pin.OUT)
led.off()

for _ in range(6):
    led.value(not led.value())
    time.sleep(.250)
    
robot.runToPosition(150)
