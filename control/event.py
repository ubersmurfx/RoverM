from servo import ServoController


class ServoEvent():
	def __init__(self, debug=False):
		self.controller = ServoController(0x40, debug=False)
		self.controller.setPWMFreq(50)
		self.servo_min = 500
		self.servo_max = 3000
		self.debug = debug
		self.angle1 = 255
		self.angle2 = 255
		self.angle3 = 255
		self.angle4 = 255
		self.cam_angle = 255
		self.man = [230, 230, 237, 250]
		self.calibrateAngles = [255, 255, 255, 255, 255, 255, 240, 255, 255]

		self.maxAngles = {
		0: 345,
		1: 345,
		2: 345,
		3: 345,
		4: 275,
		5: 310,
		6: 390,
		7: 355,
		8: 440
		}
		self.minAngles = {
		0: 145,
		1: 145,
		2: 145,
		3: 145,
		4: 185,
		5: 200,
		6: 140,
		7: 155,
		8: 120
		}
		print("init servo")

	def set_angle90(self, channel, required_angle):
		self.controller.Set_Pulse(channel, ServoController.map(required_angle, 0, 90, self.servo_min, self.servo_max))

	def set_angle120(self, channel, required_angle):
		self.controller.Set_Pulse(channel, ServoController.map(required_angle, 0, 120, self.servo_min, self. servo_max))

	def set_angle180(self, channel, required_angle):
		self.controller.Set_Pulse(channel, ServoController.map(required_angle, 0, 180, self.servo_min, self.servo_max))	

	def calibrationR(self):
		self.angle1 = self.calibrateAngles[0]
		self.angle2 = self.calibrateAngles[1]
		self.angle3 = self.calibrateAngles[2]
		self.angle4 = self.calibrateAngles[3]
		self.cam_angle = self.calibrateAngles[4]
		self.man[0] = self.calibrateAngles[5]
		self.man[1] = self.calibrateAngles[6]
		self.man[2] = self.calibrateAngles[7]
		self.man[3] = self.calibrateAngles[8]

		self.set_angle180(0, self.angle1)
		self.set_angle180(1, self.angle2)
		self.set_angle180(2, self.angle3)
		self.set_angle180(3, self.angle4)
		self.set_angle180(4, self.cam_angle)
		self.set_angle180(5, self.man[0])
		self.set_angle180(6, self.man[1])
		self.set_angle180(7, self.man[2])
		self.set_angle180(8, self.man[3])


	def decreaseWheelAngle(self, value):
		if self.angle4 < self.maxAngles[3]:
			self.angle1 = self.angle1 + value
			self.angle2 = self.angle2 - value
			self.angle3 = self.angle3 - value
			self.angle4 = self.angle4 + value

			self.set_angle180(0, self.angle1)
			self.set_angle180(1, self.angle2)
			self.set_angle180(2, self.angle3)
			self.set_angle180(3, self.angle4)
		else:
			self.angle1 = self.angle1 - value
			self.angle2 = self.angle2 + value
			self.angle3 = self.angle3 + value
			self.angle4 = self.angle4 - value


		print("Wheel's angles: ", self.angle1, "    ", self.angle2, "   ", self.angle3, "    ", self.angle4)

	def increaseWheelAngle(self, value):
		if self.angle4 > self.minAngles[3]:

			self.angle1 = self.angle1 - value
			self.angle2 = self.angle2 + value
			self.angle3 = self.angle3 + value
			self.angle4 = self.angle4 - value

			self.set_angle180(0, self.angle1)
			self.set_angle180(1, self.angle2)
			self.set_angle180(2, self.angle3)
			self.set_angle180(3, self.angle4)
		else:
			self.angle1 = self.angle1 + value
			self.angle2 = self.angle2 - value
			self.angle3 = self.angle3 - value
			self.angle4 = self.angle4 + value


		print("Wheel's angles: ", self.angle1, "    ", self.angle2, "   ", self.angle3, "    ", self.angle4)

	def increaseCamAngle(self, value):
		if self.cam_angle < self.maxAngles[4]:
			self.cam_angle = self.cam_angle + value
			self.set_angle180(4, self.cam_angle)
		else:
			self.cam_angle = self.cam_angle - value

		if (self.debug):
			print("cam angle: ", self.cam_angle)

	def decreaseCamAngle(self, value):
		if self.cam_angle > self.minAngles[4]:
			self.cam_angle = self.cam_angle - value
			self.set_angle180(4, self.cam_angle)
		else:
			self.cam_angle = self.cam_angle + value

		if (self.debug):
			print("cam angle: ", self.cam_angle)

	def increaseManAngle(self, channel, value):
		select = channel - 5
		if self.man[select] < self.maxAngles[channel]:
			self.man[select] = self.man[select] + value
			self.set_angle180(channel, self.man[select])
			#print(self.man[select])
		else:
			self.man[select] = self.man[select] - value

		if 2>1:
			print("man", channel - 5, ": ", self.man[select])

	def decreaseManAngle(self, channel, value):
		select = channel - 5
		if self.man[select] > self.minAngles[channel]:
			self.man[select] = self.man[select] - value
			self.set_angle180(channel, self.man[select])
			#print(self.man[select])
		else:
			self.man[select] = self.man[select] + value

		if 2>1:
			print("man", channel - 5, ": ", self.man[select])
