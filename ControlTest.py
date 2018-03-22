from robot import Robot
from bluetoothController import BlueController

try:
	r=Robot()
	bctrl=BlueController(r)
	bctrl.StartControlling()
except:
	r.motor.stop()
