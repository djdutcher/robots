import machine
from machine import Pin, PWM
import time
import MPU6050

pulseCount = 0

m1 = Pin(26, Pin.OUT)
m2 = Pin(27, Pin.OUT)
m3 = Pin(33, Pin.OUT)
m4 = Pin(25, Pin.OUT)

led = Pin(2, Pin.OUT)
led.off()

button = Pin(4, Pin.IN, Pin.PULL_UP)

def incrementPulseCount(pin):
    global pulseCount
    pulseCount += 1

encoderPin = Pin(32, Pin.IN)
encoderPin.irq(trigger=Pin.IRQ_RISING, handler=incrementPulseCount)

_minDS = 24000
_maxDS = 64000
_dutyCycle = 48000
_gn = 60

_leftBoost = 1.0
_rightBoost = 1.0

pwm0 = PWM(Pin(18, Pin.OUT), freq=1000, duty_u16=_dutyCycle)
pwm1 = PWM(Pin(19, Pin.OUT), freq=1000, duty_u16=_dutyCycle)

i2c = machine.I2C(1, sda=machine.Pin(21), scl=machine.Pin(22))
mpu = MPU6050.MPU6050(i2c)


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
    m2.on()
    m4.on()
    
def runb():
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

def drive(pos):
    clearCount()
    runf = run
    if pos < 0:
        runf = runb
        pos = abs(pos)
    runf()
    while pulseCount < pos:
        pass
    stop()
    time.sleep(0.1)

def stepRotate(steps):
    clearCount()
    if steps < 0:
        steps = abs(steps)
        spinb()
    else:
        spin()
    while pulseCount < steps:
        pass
    stop()
    time.sleep(0.1)
    
def rotate(deg):
    spinf = spinb
    if deg < 0:
        spinf = spin        
    
    mpu.wake()
    time.sleep(0.01)
    yaw = 0
    spinf()
    tstart = tloop = time.ticks_ms()
    while True:
        gyro = mpu.read_gyro_data()
        tend = time.ticks_ms()
        yaw += gyro[2] * (tend - tloop) * 0.001
        if abs(yaw) > abs(deg):
            break
        if tend - tstart > 10000:
            break
        tloop = time.ticks_ms()
    stop()
    mpu.sleep()
    
            
def waitForButton():
    while True:
        while button.value() == 1:
            pass
        time.sleep(0.01)
        if button.value() == 0:
            break
        

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
