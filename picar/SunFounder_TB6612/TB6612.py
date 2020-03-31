#!/usr/bin/env python
'''
**********************************************************************
* Filename    : motor.py
* Description : A driver module for ln298
* Author      : Bala Sakthivel
* E-mail      : balu4k@gmail.com
* Update      : Bala  2019-03-29    New release
**********************************************************************
'''
import RPi.GPIO as GPIO

class Motor(object):
    _DEBUG = False
    _DEBUG_INFO = 'DEBUG "motor.py":'
    GPIO.setmode(GPIO.BCM)

    def __init__(self, control_pin_1, control_pin_2, pwm=None, offset=True):
        if self._DEBUG:
            print(self._DEBUG_INFO, "Debug on")
        self.control_pin_1 = control_pin_1
        self.contol_pin_2 = control_pin_2
        self._pwm = pwm
        self._offset = offset
        self.forward_offset = self._offset
        self.backward_offset = not self.forward_offset
        self._speed = 0

        GPIO.setwarnings(False)

        if self._DEBUG:
            print(self._DEBUG_INFO, 'setup motor pin number at', control_pin_1, control_pin_2)
            print(self._DEBUG_INFO, 'setup motor pwm number as', self._pwm.__name__)
        GPIO.setup(self.control_pin_1, GPIO.OUT)
        GPIO.setup(self.contol_pin_2, GPIO.OUT)

    @property
    def speed(self):
        return self._speed

    @property
    def debug(self, debug):
        return self._DEBUG

    @property
    def pwm(self):
        return self._pwm

    @pwm.setter
    def pwm(self, pwm):
        if self._DEBUG:
            print(self._DEBUG_INFO, 'pwm set')
        self._pwm = pwm

    @speed.setter
    def speed(self, speed):
        ''' Set Speed with giving value '''
        if speed not in list(range(0, 101)):
            raise ValueError('speed ranges from 0 to 100, not "{0}"'.format(speed))
        if not callable(self._pwm):
            raise ValueError(
                'pwm is not callable, please set Motor.pwm to a pwm control function with only 1 variable speed')
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Set speed to: ', speed)
        self._speed = speed
      #  self._pwm(self._speed)

    def forward(self):
        ''' Set the motor direction to forward '''
        GPIO.output(self.control_pin_1, self.forward_offset)
        GPIO.output(self.contol_pin_2, not self.forward_offset)
        self.speed = self._speed
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor moving forward (%s)' % str(self.forward_offset))

    def backward(self):
        ''' Set the motor direction to backward '''
        GPIO.output(self.control_pin_1, self.backward_offset)
        GPIO.output(self.contol_pin_2, not self.backward_offset)
        self.speed = self._speed
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor moving backward (%s)' % str(self.backward_offset))

    def stop(self):
        ''' Stop the motor by giving a 0 speed '''
        if self._DEBUG:
            print(self._DEBUG_INFO, 'Motor stop')
        self.speed = 0

    @debug.setter
    def debug(self, debug):
        ''' Set if debug information shows '''
        if debug in (True, False):
            self._DEBUG = debug
        else:
            raise ValueError('debug must be "True" (Set debug on) or "False" (Set debug off), not "{0}"'.format(debug))

        if self._DEBUG:
            print(self._DEBUG_INFO, "Set debug on")
        else:
            print(self._DEBUG_INFO, "Set debug off")

def test():
    import time
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    pwm_a = GPIO.PWM(7, 1000)
    pwm_a.start(0)

    delay = 5

    def pwm_a_speed(value):
        pwm_a.ChangeDutyCycle(value)

    motor_a = Motor(8, 10)
    motor_a.debug = True
    motor_a.pwm = pwm_a_speed

    motor_a.forward()
    motor_a.speed = 50
    time.sleep(delay)
    motor_a.speed= 100
    time.sleep(delay)

    motor_a.backward()
    motor_a.speed = 50
    time.sleep(delay)
    motor_a.speed = 100
    time.sleep(delay)


    GPIO.cleanup()

if __name__ == '__main__':
	test()

