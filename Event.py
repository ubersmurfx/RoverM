from servo import ServoController


class ServoEvent():
	def __init__(self):
		self.controller = ServoController(0x40, debug=False)
		self.controller.setPWMFreq(50)
		self.angle1 = 255
		self.angle2 = 250
		self.angle3 = 250
		self.angle4 = 225
		self.cam_angle = 250
		self.man1_angle = 230
		self.man2_angle = 230
		self.man3_angle = 237
		self.man4_angle = 250
		self.calibrateAngles = [255, 250, 250, 225, 244, 230, 230, 237, 250] 
		
		self.maxAngles = {
		0: 0,
		1: 0,
		2: 0,
		3: 310,
		4: 275,
		5: 326,
		6: 390,
		7: 320,
		8: 440
		}
		self.minAngles = {
		0: 0,
		1: 0,
		2: 0,
		3: 140,
		4: 185,
		5: 140,
		6: 170,
		7: 130,
		8: 115
		}
		print("init servo")
		
	
	def set_angle90(self, channel, required_angle):
		self.controller.Set_Pulse(channel, ServoController.map(required_angle, 0, 90, servo_min, servo_max))
		
	def set_angle120(self, channel, required_angle):
		self.controller.Set_Pulse(channel, ServoController.map(required_angle, 0, 120, servo_min, servo_max))
		
	def set_angle180(self, channel, required_angle):
		self.controller.Set_Pulse(channel, ServoController.map(required_angle, 0, 180, servo_min, servo_max))	
		
		
	def calibrationR(self):
		self.angle1 = self.calibrateAngles[0]
		self.angle2 = self.calibrateAngles[1]
		self.angle3 = self.calibrateAngles[2]
		self.angle4 = self.calibrateAngles[3]
		self.cam_angle = self.calibrateAngles[4]
		self.man1_angle = self.calibrateAngles[5]
		self.man2_angle = self.calibrateAngles[6]
		self.man3_angle = self.calibrateAngles[7]
		self.man4_angle = self.calibrateAngles[8]
		
		set_angle90(0, self.angle1)
		set_angle90(1, self.angle2)
		set_angle90(2, self.angle3)
		set_angle90(3, self.angle4)
		set_angle90(4, self.cam_angle)
		set_angle90(5, self.man1_angle)
		set_angle120(6, self.man2_angle)
		set_angle120(7, self.man3_angle)
		set_angle90(8, self.man4_angle)
		print("calibrate servo")
		
	def decreaseAngle(self, channel, required_angle, value):
		if required_angle > self.minAngles[channel]:
			required_angle =- value
			set_angle90(channel, required_angle)
			return required_angle
		else:
			required_angle =+ value
			return required_angle
			
	def increaseAngle(self, channel, required_angle, value):
		if required_angle < self.maxAngles[channel]:
			required_angle =+ value
			set_angle90(channel, required_angle)
			return required_angle
		else:
			required_angle =- value
			return required_angle		
	
