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

def ledOn():
    led.value(1)
    
def ledOff():
    led.value(0)

def toggleLed():
    led.value(not led.value())
    
def blinkLed(times):
    ledOff()
    for _ in range(times * 2):
        toggleLed()
        time.sleep(0.25)
        
def buttonLed():
    while True:
        led.value(not button.value())
        time.sleep(0.01)

def speed(n):
    global _gn
    global _dutyCycle
    n = max(0, n)
    n = min(99, n)
    _gn = n
    _dutyCycle = _minDS + ((_maxDS - _minDS) * n // 100)
    
    right = int(_dutyCycle * _rightBoost)
    right = min(right, _maxDS)
    right = max(right, _minDS)
    
    left = int(_dutyCycle * _leftBoost)
    left = min(left, _maxDS)
    left = max(left, _minDS)
    
    pwm0.duty_u16(right)
    pwm1.duty_u16(left)
    return n
    
def speedBoost(left, right):
    _leftBoost = left
    _rightBoost = right

def clearCount():
    global pulseCount
    pulseCount = 0

def stop():
    m1.off()
    m2.off()
    m3.off()
    m4.off()

def left():
    stop()
    m2.on()
    
def right():
    stop()
    m4.on()

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

stop()
speed(50)
