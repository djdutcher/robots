from robot import *
import time


#drive(100)
print('Start')
start = time.time()

while time.time() - start < 10:
    print(encoderValue())
    time.sleep(0.1)
    
print('Done')
