import RPi.GPIO as GPIO
import time
from l293d import L293D
from ultrasonic import US
 
 
class Robot():
	def __init__(self, motor_left_pin1=23, motor_left_pin2=24, motor_right_pin1=17, motor_right_pin2=27, line_follow_pin_left=19, line_follow_pin_right=6,
			servo_pin=22, us_trigger_pin=12, us_echo_pin=13 ):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		
		# init modules
		self.ultrasonic=US(servo_pin, us_trigger_pin,us_echo_pin);
		self.motor = L293D(motor_left_pin1, motor_left_pin2, motor_right_pin1, motor_right_pin2)
		self.line_follow_pin_left  = line_follow_pin_left
		self.line_follow_pin_right = line_follow_pin_right
		
		GPIO.setup(self.line_follow_pin_left,  GPIO.IN)
		GPIO.setup(self.line_follow_pin_right, GPIO.IN)
    
	def lineFollowModeOn(self):
     
		status_left  = True
		status_right = True
	
		while True:
			status_left  =not bool(GPIO.input(self.line_follow_pin_left))  # False: not on line / sensor too distant from bottom
			status_right =not bool(GPIO.input(self.line_follow_pin_right)) # True: on line
		
			if status_left and status_right:
				# one the line, follow straight on
				self.motor.forward()
				print("on the line, straight")
			elif status_left:
				# line is on the left, move left (motor right)
				self.motor.forwardRight()
				print("line is on the left")
			elif status_right:
				# line is on the right, move right (motor left)
				self.motor.forwardLeft()
				print("line is on the right")
			else:
				# have gone astray, search line. first go back some cm
				self.motor.backward()
				time.sleep(7.5/self.motor.DIST_PER_SEC)
				self.motor.stop()
				# rotate x degrees to search the line
				degrees_to_search = 45.0
				self.motor.forwardRight()
				s = GPIO.wait_for_edge(self.line_follow_pin_left, GPIO.RISING, timeout=int(1000 * self.motor.SEC_PER_TURN / 360.0 * degrees_to_search))
				self.motor.stop()
				if s is not None:
					# line found, continue
					continue
				else:
					# nothing found, go back to original position
					self.motor.backwardRight()
					time.sleep(self.motor.SEC_PER_TURN / 360.0 * degrees_to_search)
					# search in other side
					self.motor.forwardLeft()
					s = GPIO.wait_for_edge(self.line_follow_pin_right, GPIO.RISING, timeout=int(1000 * self.motor.SEC_PER_TURN / 360.0 * degrees_to_search))
					self.motor.stop()
					if s is not None:
						# line found, continue
						print("found")
						continue
					else:
						# line could not be found, go back to original position, stop
						self.motor.backwardLeft()
						time.sleep(self.motor.SEC_PER_TURN / 360.0 * degrees_to_search)
						self.motor.stop()
						break
			time.sleep(0.001)

	def autoPilotUSon(self):
		actualIndex=int(self.ultrasonic.steps / 2)
		degreesPerStep=180.0 / (self.ultrasonic.steps-1)
		while True:
			dists=self.ultrasonic.findBestWay()
			print(dists)
			maxIndex=dists.index(max(dists))
			steps=abs(90.0-maxIndex*degreesPerStep) / degreesPerStep+1
			#if distance is more than 500cm, the measurement is probably wrong -> stop
			if dists[maxIndex] > self.motor.DIST_PER_SEC/2:
				if maxIndex == int(self.ultrasonic.steps /2):
					#straigt forward
					self.motor.forward()
				elif maxIndex < int(self.ultrasonic.steps/2):
					#turn right
					self.motor.forwardRight()
					time.sleep(self.motor.SEC_PER_TURN / 360.0 * degreesPerStep * steps)
					self.motor.forward()
				elif maxIndex > int(self.ultrasonic.steps/2):
					#turn left
					self.motor.forwardLeft()
					time.sleep(self.motor.SEC_PER_TURN / 360.0 *degreesPerStep*steps)
					self.motor.forward()
				actualIndex=maxIndex
			else:
				print(dists[maxIndex], self.motor.DIST_PER_SEC)
				self.motor.stop()
				return	
