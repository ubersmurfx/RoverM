from servo import ServoController


class ServoEvent():
	def __init__(self, debug=False):
		self.controller = ServoController(0x40, debug=False)
		self.controller.setPWMFreq(50)
		self.debug = debug
		self.diff = 0.5
		self.angle1 = 80
		self.angle2 = 90
		self.angle3 = 90
		self.angle4 = 90
		self.cam_angle = 90
		self.man = [140, 130, 130, 90]
		self.calibrateAngles = [90, 90, 100, 80, 90, 140, 130, 130, 90]

		self.deltaAngle = 45
		self.maxAngles = {
		0: self.calibrateAngles[0] + self.deltaAngle,
		1: self.calibrateAngles[1] + self.deltaAngle,
		2: self.calibrateAngles[2] + self.deltaAngle,
		3: self.calibrateAngles[3] + self.deltaAngle,
		4: 80,
		5: 220,
		6: 250,
		7: 200,
		8: 180
		}
		self.minAngles = {
		0: self.calibrateAngles[0] - self.deltaAngle,
		1: self.calibrateAngles[1] - self.deltaAngle,
		2: self.calibrateAngles[2] - self.deltaAngle,
		3: self.calibrateAngles[3] - self.deltaAngle,
		4: 20,
		5: 60,
		6: 60,
		7: 45,
		8: 0
		}

	def cstate_get_angle(self, angle):
		return angle

	def set_angle90(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 90, 500, 2500))
		if (self.debug):
			print("90", "pulse", k, "angle:", required_angle)
		self.controller.Set_Pulse(channel, k)

	def set_angle120(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 120, 2200, 6000))
		if (self.debug):
			print("120", "pulse", k, "angle:", required_angle)
		self.controller.Set_Pulse(channel, k)

	def set_angle150(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 150, 1400, 6000))
		if (self.debug):
			print("150", "pulse", k, "angle:", required_angle)
		self.controller.Set_Pulse(channel, k)

	def set_angle180(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 180, 1400, 6100))
		if (self.debug):
			print("180", "pulse", k, "angle:", required_angle)
		self.controller.Set_Pulse(channel, k)

	def set_angle270(self, channel, required_angle):
		k = int(ServoController.map(required_angle, 0, 270, 1300, 6300))
		if (self.debug):
			print("270", "pulse", k, "angle:", required_angle)
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
		self.set_angle270(5, self.man[0])
		self.set_angle270(6, self.man[1])
		self.set_angle270(7, self.man[2])
		self.set_angle180(8, self.man[3])

	def decreaseWheelAngle(self, value):
#turn left
		if (self.angle4 <= self.maxAngles[3] and self.angle1 <= self.maxAngles[0]):
			if (self.angle1 <= 80):
				self.angle1 = self.angle1 + value
				self.angle2 = self.angle2 - value
			else:
				self.angle1 = self.angle1 + value * self.diff
				self.angle2 = self.angle2 - value * self.diff

			if (self.angle1 >= 80):
				self.angle3 = self.angle3 - value
				self.angle4 = self.angle4 + value
			else:
				self.angle3 = self.angle3 - value * self.diff
				self.angle4 = self.angle4 + value * self.diff

			self.set_angle180(0, self.angle1)
			self.set_angle180(1, self.angle2)
			self.set_angle180(2, self.angle3)
			self.set_angle180(3, self.angle4)
		else:
			if (self.angle1 <= 80): #минимальное крайнее положение
				self.angle1 = self.angle1 - value
				self.angle2 = self.angle2 + value
			else:
				self.angle1 = self.angle1 - value * self.diff
				self.angle2 = self.angle2 + value * self.diff

			if (self.angle1 >= 80): #крайнее правое положение
				self.angle3 = self.angle3 + value
				self.angle4 = self.angle4 - value
			else:
				self.angle3 = self.angle3 + value * self.diff
				self.angle4 = self.angle4 - value * self.diff

	def increaseWheelAngle(self, value):
#turn right
		if (self.angle4 >= self.minAngles[3] and self.angle1 >= self.minAngles[0]):
			if (self.angle1 <= 80):
				self.angle1 = self.angle1 - value
				self.angle2 = self.angle2 + value
			else:
				self.angle1 = self.angle1 - value * self.diff
				self.angle2 = self.angle2 + value * self.diff

			if (self.angle1 >= 80):
				self.angle3 = self.angle3 + value
				self.angle4 = self.angle4 - value
			else:
				self.angle3 = self.angle3 + value * self.diff
				self.angle4 = self.angle4 - value * self.diff

			self.set_angle180(0, self.angle1)
			self.set_angle180(1, self.angle2)
			self.set_angle180(2, self.angle3)
			self.set_angle180(3, self.angle4)
		else:
			if (self.angle1 <= 80):
				self.angle1 = self.angle1 + value
				self.angle2 = self.angle2 - value
			else:
				self.angle1 = self.angle1 + value * self.diff
				self.angle2 = self.angle2 - value * self.diff

			if (self.angle1 >= 80):
				self.angle3 = self.angle3 - value
				self.angle4 = self.angle4 + value
			else:
				self.angle3 = self.angle3 - value * self.diff
				self.angle4 = self.angle4 + value * self.diff

	def increaseCamAngle(self, value):
		if self.cam_angle < self.maxAngles[4]:
			self.cam_angle = self.cam_angle + value
			self.set_angle150(4, self.cam_angle)
		else:
			self.cam_angle = self.cam_angle - value

	def decreaseCamAngle(self, value):
		if self.cam_angle > self.minAngles[4]:
			self.cam_angle = self.cam_angle - value
			self.set_angle150(4, self.cam_angle)
		else:
			self.cam_angle = self.cam_angle + value

	def increaseManAngle(self, channel, value):
		select = channel - 5
		if self.man[select] < self.maxAngles[channel]:
			self.man[select] = self.man[select] + value
			if (select == 0 or select == 1 or select == 2):
				self.set_angle270(channel, self.man[select])
			else:
				self.set_angle180(channel, self.man[select])
		else:
			self.man[select] = self.man[select] - value

	def decreaseManAngle(self, channel, value):
		select = channel - 5
		if self.man[select] > self.minAngles[channel]:
			self.man[select] = self.man[select] - value
			if (select == 0 or select == 1 or select == 2):
				self.set_angle270(channel, self.man[select])
			else:
				self.set_angle180(channel, self.man[select])
		else:
			self.man[select] = self.man[select] + value
