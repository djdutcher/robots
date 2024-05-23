import machine
from machine import Pin, PWM
import time

pulseCount = 0

m1 = Pin(26, Pin.OUT)
m2 = Pin(27, Pin.OUT)
m3 = Pin(33, Pin.OUT)
m4 = Pin(25, Pin.OUT)

def incrementPulseCount(pin):
    global pulseCount
    pulseCount += 1

encoderPin = Pin(32, Pin.IN)
encoderPin.irq(trigger=Pin.IRQ_RISING, handler=incrementPulseCount)

_minDS = 24000
_maxDS = 64000
_dutyCycle = 48000
_gn = 60

_leftBoost = 1.1
_rightBoost = 1.0

pwm0 = PWM(Pin(18, Pin.OUT), freq=1000, duty_u16=_dutyCycle)
pwm1 = PWM(Pin(19, Pin.OUT), freq=1000, duty_u16=_dutyCycle)

def speed(n):
    global _gn
    global _dutyCycle
    n = max(0, n)
    n = min(99, n)
    _gn = n
    _dutyCycle = _minDS + ((_maxDS - _minDS) * n // 100)
    pwm0.duty_u16(int(_dutyCycle * _rightBoost))
    pwm1.duty_u16(int(_dutyCycle * _leftBoost))
    return n

def clearCount():
    global pulseCount
    pulseCount = 0

def stop():
    m1.off()
    m2.off()
    m3.off()
    m4.off()

def run():
    stop()
    m1.on()
    m3.on()
    
def spin():
    stop()
    m1.on()
    m4.on()
    
def spinb():
    stop()
    m2.on()
    m3.on()

def runToPosition(pos):
    clearCount()
    run()
    while pulseCount < pos:
        pass
    stop()

def rotate(steps):
    clearCount()
    if steps < 0:
        steps = abs(steps)
        spinb()
    else:
        spin()
    while pulseCount < steps:
        pass
    stop()

def t():
    n = 50
    speed(50)
    
    line = ''
    prev = 'w'
    while line != 'q':
        print(_gn)
        print(_dutyCycle)
        line = input('Up or down:').strip()
        
        if line != '':
            prev = line
        else:
            line = prev
            
        if line == 'w':
            n += 1
        elif line == 's':
            n -= 1
        n = speed(n)

stop()
speed(50)
