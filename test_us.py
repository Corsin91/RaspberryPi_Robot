from robot import Robot
import time

try:
	r=Robot()
	r.autoPilotUSon()
except:
	r.motor.stop()
