from servo import ServoController


class ServoEvent():
	def __init__(self, debug=False):
		self.controller = ServoController(0x40, debug=False)
		self.controller.setPWMFreq(50)
		self.debug = debug

		self.angle1 = 90
		self.angle2 = 90
		self.angle3 = 90
		self.angle4 = 90
		self.cam_angle = 90
		self.man = [90, 90, 90, 90, 90]
		self.calibrateAngles = [90, 90, 90, 90, 90, 90, 90, 90, 90]

		self.maxAngles = {
		0: 800,
		1: 800,
		2: 800,
		3: 800,
		4: 800,
		5: 800,
		6: 800,
		7: 800,
		8: 800,
		9: 800
		}
		self.minAngles = {
		0: -1000,
		1: -1000,
		2: -1000,
		3: -1000,
		4: -1000,
		5: -1000,
		6: -1000,
		7: -1000,
		8: -1000,
		9: -1000
		}
		print("init servo")

	def set_angle90(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 90, 500, 2500))
		print("90", k)
		self.controller.Set_Pulse(channel, k)

	def set_angle120(self, channel, required_angle):
		#required_angle = 0
		k = int(ServoController.map(required_angle, 0, 120, 2200, 6000))
		print("120", k)
		self.controller.Set_Pulse(channel, k)

	def set_angle150(self, channel, required_angle):
		required_angle = int(required_angle)
		k = int(ServoController.map(required_angle, 0, 150, 1400, 6000))
		print("150", k)
		self.controller.Set_Pulse(channel, k)

	def set_angle180(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 180, 1400, 6100))
		print("180", k)
		self.controller.Set_Pulse(channel, k)

	def set_angle270(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 270, 1300, 6300))
		print("270", k)
		self.controller.Set_Pulse(channel, k)


	def set_pulse_(self, channel, pulse):
		self.controller.Set_Pulse(channel, pulse)

	def calibrationE(self):
		self.angle1 = self.maxAngles[0]
		self.angle2 = self.minAngles[1]
		self.angle3 = self.maxAngles[2]
		self.angle4 = self.minAngles[3]

		self.set_angle180(0, self.angle1)
		self.set_angle180(1, self.angle2)
		self.set_angle180(2, self.angle3)
		self.set_angle180(3, self.angle4)

		if 2>1:
			print("1: ", self.angle1, "2: ", self.angle2, "3: ", self.angle3, "4: ", self.angle4)

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

		#self.Controller.Set_Pulse(0, 500)


	def decreaseWheelAngle(self, value):
		if self.angle4 < self.maxAngles[3]:
			self.angle1 = self.angle1 + value
			self.angle2 = self.angle2 - value
			self.angle3 = self.angle3 - value
			self.angle4 = self.angle4 + value

			self.set_angle180(0, self.angle1)
			self.set_angle120(1, self.angle2)
			self.set_angle270(2, self.angle3)
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
			self.set_angle120(1, self.angle2)
			self.set_angle270(2, self.angle3)
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
			self.set_angle150(4, self.cam_angle)
		else:
			self.cam_angle = self.cam_angle - value

		if (self.debug == False):
			print("cam angle: ", self.cam_angle)

	def decreaseCamAngle(self, value):
		if self.cam_angle > self.minAngles[4]:
			self.cam_angle = self.cam_angle - value
			self.set_angle150(4, self.cam_angle)
		else:
			self.cam_angle = self.cam_angle + value

		if (self.debug == False):
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
