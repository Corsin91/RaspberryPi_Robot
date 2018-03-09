import RPi.GPIO as GPIO
import time
from l293d import L293D
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
l = L293D(23,24,17,27)

l.stop()
 
for i in range(1):
  l.forward()
  time.sleep(0.5)
  l.forwardRight()
  time.sleep(0.5)
l.stop()
