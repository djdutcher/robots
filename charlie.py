import robot as r
import time

r.speed(30)

while True:
    r.led.on()
    r.waitForButton()
    r.led.off()
    
    r.rotate(-32)
    r.runToPosition(100)
    r.rotate(15)
    r.runToPosition(500)
    
