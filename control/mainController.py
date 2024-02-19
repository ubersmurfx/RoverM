from disp import display
from h39 import rmotor, lightBulb
from event import ServoEvent
import library
from time import sleep


class mainController:
	def __init__(self):
		self.debug = False

	def setupDisplay(self):	
		try:
			self.display = display.Display()
			self.display.show_image('disp/bentley.png')
			print("display: 200")
		except:
			print("display: error 0x3c")
	def setupLamp(self):
		try:
			self.lamp = lightBulb()
			self.lamp.setup()
			print("lamp: 200")
		except:
			self.lamp.destruct()
			print("lamp: error")

	def setupMotors(self):
		try:
			self.motor = rmotor()
			self.motor.modify_pwm1(rmotor.pwm_signal, 95, 3000)
			self.motor.modify_pwm2(rmotor.pwm_signal1, 95, 3000)
			print("motor: 200")
		except:
			print("motor: error")

	def setupServo(self):
		try:
			self.serv = ServoEvent()
			sleep(libary.time_calibrate * 3)
			#self.serv.calibrationR()
			sleep(library.time_calibrate * 3)
			print("servo: 200")
		except:
			print("servo: error 0x40")


if __name__=="__main__":
	c = mainController()
	c.setupDisplay()
	c.setupMotors()
	c.setupLamp()
	c.setupServo()
