import RPi.GPIO as GPIO
import time
direction = True
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup((8,10,16,18), GPIO.OUT)
GPIO.output((10,18), direction)
GPIO.output((8,16), not direction)
time.sleep(5)
direction = False
GPIO.output((10,18), direction)
GPIO.output((8,16), not direction)
time.sleep(5)
GPIO.cleanup()

