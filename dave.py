import robot
from machine import Pin
import time

led = Pin(2, Pin.OUT)
led.off()

button = Pin(4, Pin.IN, Pin.PULL_UP)


while True:
    led.value(button.value())
    time.sleep(0.01)
