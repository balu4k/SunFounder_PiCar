#!/usr/bin/env python
'''
**********************************************************************
* Filename    : back_wheels.py
* Description : A module to control the back wheels of RPi Car
* Author      : Cavon
* Brand       : SunFounder
* E-mail      : service@sunfounder.com
* Website     : www.sunfounder.com
* Update      : Cavon    2016-09-13    New release
*               Cavon    2016-11-04    fix for submodules
**********************************************************************
'''

from picar.SunFounder_TB6612 import TB6612
from picar.SunFounder_PCA9685 import PCA9685
from picar import filedb
import RPi.GPIO as GPIO



class Back_Wheels(object):
	''' Back wheels control class '''
	Motor_A1 = 14  #board pin 08
	Motor_A2 = 15  #board pin 10
	Motor_B1 = 23  #board pin 16
	Motor_B2 = 24  #board pin 18

	PWM_A = 4 #board pin 07
	PWM_B = 17 #board pin 11

	_DEBUG = False
	_DEBUG_INFO = 'DEBUG "back_wheels.py":'

	def __init__(self, debug=False, bus_number=1, db="config"):
		'''Turn related variables '''


		'''Trun related code is complete'''

		''' Init the direction channel and pwm channel '''
		self.forward_A = True
		self.forward_B = True

		self.db = filedb.fileDB(db=db)

		self.forward_A = int(self.db.get('forward_A', default_value=1))
		self.forward_B = int(self.db.get('forward_B', default_value=1))

		self.left_wheel = TB6612.Motor(self.Motor_A1, self.Motor_A2, offset=self.forward_A)
		self.right_wheel = TB6612.Motor(self.Motor_B1,self.Motor_B2, offset=self.forward_B)





		GPIO.setup((self.PWM_A, self.PWM_B), GPIO.OUT)

		try:
			self.pwm_a = GPIO.PWM(self.PWM_A, 1000)
			self.pwm_a.start(0)
			self.pwm_b = GPIO.PWM(self.PWM_B, 1000)
			self.pwm_b.start(0)
		except:
			ex = 'already available'

		finally:
			ex = 'already available'

		def _set_a_pwm(value):
			self.pwm_a.ChangeDutyCycle(value)

		def _set_b_pwm(value):
			self.pwm_b.ChangeDutyCycle(value)

		self.left_wheel.pwm  = _set_a_pwm
		self.right_wheel.pwm = _set_b_pwm

		self._speed = 0

		self.debug = debug
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Set left wheel to #%d, PWM channel to %d' % (self.Motor_A, self.PWM_A))
			print(self._DEBUG_INFO, 'Set right wheel to #%d, PWM channel to %d' % (self.Motor_B, self.PWM_B))

	def forward(self):
		''' Move both wheels forward '''
		self.left_wheel.forward()
		self.right_wheel.forward()
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Running forward')

	def backward(self):
		''' Move both wheels backward '''
		self.left_wheel.backward()
		self.right_wheel.backward()
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Running backward')

	def left_turn(self):
		self.left_wheel.forward()
		self.right_wheel.backward()
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Running left turn')

	def right_turn(self):
		self.left_wheel.backward()
		self.right_wheel.forward()
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Running right turn')

	def stop(self):
		''' Stop both wheels '''
		self.left_wheel.stop()
		self.right_wheel.stop()
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Stop')

	@property
	def speed(self, speed):
		return self._speed

	@speed.setter
	def speed(self, speed):
		self._speed = speed
		''' Set moving speeds '''
		self.left_wheel.speed = self._speed
		self.right_wheel.speed = self._speed
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Set speed to', self._speed)

	@property
	def debug(self):
		return self._DEBUG

	@debug.setter
	def debug(self, debug):
		''' Set if debug information shows '''
		if debug in (True, False):
			self._DEBUG = debug
		else:
			raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

		if self._DEBUG:
			print(self._DEBUG_INFO, "Set debug on")
			self.left_wheel.debug = True
			self.right_wheel.debug = True
			#self.pwm.debug = True
		else:
			print(self._DEBUG_INFO, "Set debug off")
			self.left_wheel.debug = False
			self.right_wheel.debug = False
			#self.pwm.debug = False

	def ready(self):
		''' Get the back wheels to the ready position. (stop) '''
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Turn to "Ready" position')
		self.left_wheel.offset = self.forward_A
		self.right_wheel.offset = self.forward_B
		self.speed = 100
		self.stop()

	def calibration(self):
		''' Get the front wheels to the calibration position. '''
		if self._DEBUG:
			print(self._DEBUG_INFO, 'Turn to "Calibration" position')
		self.speed = 50
		self.forward()
		self.cali_forward_A = self.forward_A
		self.cali_forward_B = self.forward_B

	def cali_left(self):
		''' Reverse the left wheels forward direction in calibration '''
		self.cali_forward_A = (1 + self.cali_forward_A) & 1
		self.left_wheel.offset = self.cali_forward_A
		self.forward()

	def cali_right(self):
		''' Reverse the right wheels forward direction in calibration '''
		self.cali_forward_B = (1 + self.cali_forward_B) & 1
		self.right_wheel.offset = self.cali_forward_B
		self.forward()

	def cali_ok(self):
		''' Save the calibration value '''
		self.forward_A = self.cali_forward_A
		self.forward_B = self.cali_forward_B
		self.db.set('forward_A', self.forward_A)
		self.db.set('forward_B', self.forward_B)
		self.stop()

def test():
	import time
	back_wheels = Back_Wheels()
	DELAY = 0.01
	try:
		back_wheels.forward()
		back_wheels.speed = 100
		time.sleep(3)

		back_wheels.backward()
		back_wheels.speed = 100
		time.sleep(3)

	except KeyboardInterrupt:
		print("KeyboardInterrupt, motor stop")
		back_wheels.stop()
	finally:
		print("Finished, motor stop")
		back_wheels.stop()

if __name__ == '__main__':
	test()
