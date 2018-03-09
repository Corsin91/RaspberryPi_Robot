import RPi.GPIO as GPIO
import time

servoPIN=22
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN,GPIO.OUT)

p=GPIO.PWM(servoPIN,50) # GPIO als PWM mit 50Hz
p.start(2.5)
try:
	while True:
		p.ChangeDutyCycle(5)
		time.sleep(0.5)
		p.ChangeDutyCycle(5)
		time.sleep(0.5)
		p.ChangeDutyCycle(7.5)
		time.sleep(0.5)
		p.ChangeDutyCycle(10.0)
		time.sleep(0.5)
		p.ChangeDutyCycle(12.5)
		time.sleep(0.5)
		p.ChangeDutyCycle(10)
		time.sleep(0.5)
		p.ChangeDutyCycle(7.5)
		time.sleep(0.5)
		p.ChangeDutyCycle(5)
		time.sleep(0.5)
		p.ChangeDutyCycle(2.5)
		time.sleep(0.5)
except KeyboardInterrupt:
	p.stop()
	GPIO.cleanup()
