import machine
from machine import Pin, PWM
import time

button = Pin(32, Pin.IN, Pin.PULL_UP)
led = Pin(19, Pin.OUT)
servo = PWM(Pin(21, Pin.OUT))
servo.freq(50)

mind = int(1.0 / 20.0 * 1024)
center = int(1.5 / 20.0 * 1024)
maxd = int(2.0 / 20.0 * 1024)
print(mind, center, maxd)
servo.duty(center)

def setServo(a):
    d = int(mind + (a * (maxd - mind) / 100.0))
    #print(d)
    servo.duty(d)
    

def sweep():
    while True:
        setServo(0)
        time.sleep(0.4)
        setServo(100)
        time.sleep(0.4)
        if button.value() == 0:
            break

def test():
    x = 50
    a = input()
    while a != 'q':
        x += 1
        print(x, x / 51.2)
        servo.duty(x)
        a = input()
        if a == '':
            continue
        if a == 'q':
            break
        x = int(a)
        
        
def run():
    while True:
        #print(button.value())
        if button() == 1:
            led(0)
            setServo(0)
        else:
            led(1)
            setServo(100)
        #time.sleep(0.2)

run()
