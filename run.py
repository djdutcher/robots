from robot import *
import time

motorTest = 0
buttonTest = 0
encoderTest = 0
imuTest = 1

blinkLed(3)

if imuTest:
    print('IMU Test')
    testIMU()
    print('Done')

if buttonTest:
    print('Wait for button')
    waitForButton()
    blinkLed(3)

if motorTest:
    print('Left')
    left()
    time.sleep(2)
    print('Right')
    right()
    time.sleep(2)
    print('Both')
    run()
    time.sleep(2)
    stop()

time.sleep(0.5)

if encoderTest:
    print('Encoder')
    drive(150)
