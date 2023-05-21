import socket
import threading
import struct
from time import sleep
import smbus
import math
from motor import *
import subprocess
import sys
#from gpiozero import LoadAverage
from servo import *

print("pi pins setup:", GPIO.getmode())
Lineleft = 24
Lineright = 23
GPIO.setup(Lineleft, GPIO.IN)
GPIO.setup(Lineright, GPIO.IN)

'''SERVO INIT'''
servo_min = 500
servo_max = 3000
controller = ServoController(0x40, debug=False)
controller.setPWMFreq(50)



controller.Set_Pulse(0, ServoController.map(240, 0, 180, servo_min, servo_max))
#print("1")
controller.Set_Pulse(1, ServoController.map(270, 0, 180, servo_min, servo_max))
#print("2")
controller.Set_Pulse(2, ServoController.map(240, 0, 180, servo_min, servo_max))
#print("3")
controller.Set_Pulse(3, ServoController.map(240, 0, 180, servo_min, servo_max))
#print("4")


'''MOTOR INIT'''
motor = rmotor()
motor.motor_enabled()
sleep(0.1)
motor.modify_pwm1(rmotor.pwm_signal, 80, 3000)
motor.modify_pwm2(rmotor.pwm_signal1, 80, 3000)
print("init complete")
sleep(0.1)
#motor.calibrate()


'''TIMINGS must match'''
pulsebeat = 0.04
time_delay_seconds = 0.05


class ClientThread(threading.Thread):
	def __init__(self, ip, port):
		self._defaultpackage = 256
		self.ip = ip
		self.port = port
		self._exit = 1
		self.r_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self._defaultpackage = 168
		self.angle1 = 255
		self.angle2 = 250
		self.angle3 = 250
		self.angle4 = 225
		self.cam_angle = 250
		self.man1_angle = 230
		self.man2_angle = 230
		self.man3_angle = 237
		self.man4_angle = 250
		self.lineangle = 250
		self.calibrate_angle1 = 255
		self.calibrate_angle2 = 250
		self.calibrate_angle3 = 250
		self.calibrate_angle4 = 225
		self.calibrate_cam_angle = 244
		self.calibrate_man1_angle = 230
		self.calibrate_man2_angle = 230
		self.calibrate_man3_angle = 237
		self.calibrate_man4_angle = 250
		self.m_speed = 80
		self.k_turn = 0.4
		self.boost = 1
		self.sstate = 1
		self.mstate = 1
		print("[+] New server socket thread started from: ", ip + str(port))

	def reciever(self):
		_exit = 1
		while _exit != 0:
			#try:
				data = clientsocket.recv(self._defaultpackage)
				print(len(data))
				if len(data) == 80:
					print("sucksess")
					self.r_data = struct.unpack("20i", data)
				else:
					print("error")
					self.r_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

				#print("Server received data:", self.r_data)

				sleep(pulsebeat)
			#except:
			#	print("Error in recieving data")
			#	motor.motor_stop()
			#	_exit = 0
			#	print("Socket closing")
			#	clientsocket.close()

	def run(self):
		thread1=threading.Thread(target=self.reciever, daemon=False)
		thread1.start()
		thread2=threading.Thread(target=self.machinist, daemon=True)
		thread2.start()
		thread4=threading.Thread(target=self.servorer, daemon=True)
		thread4.start()
		thread5=threading.Thread(target=self.cameraman, daemon=True)
		thread5.start()

	def cameraman(self):
		while True:
			sleep(pulsebeat)

			#if self.r_data[0] == 1 and self.r_data[1] == 1 and self.r_data[2] == 1 and self.r_data[3] == 1:
			#	print("Shutdown")
			#	clientsocket.close()
			#if self.r_data[20] == 1:
			#	self.lineangle = self.lineangle + 5
			#	controller.Set_Pulse(9, ServoController.map(self.lineangle, 0, 180, servo_min, servo_max))
			#	print(self.lineangle)
			#	sleep(0.07)
			#if self.r_data[21] == 1:
			#	self.lineangle = self.lineangle - 5
			#	controller.Set_Pulse(9, ServoController.map(self.lineangle, 0, 180, servo_min, servo_max))
			#	print(self.lineangle)
			#	sleep(0.07)

			if self.r_data[18] == 1:
				self.angle1 = self.calibrate_angle1
				self.angle2 = self.calibrate_angle2
				self.angle3 = self.calibrate_angle3
				self.angle4 = self.calibrate_angle4
				self.cam_angle = self.calibrate_cam_angle
				self.man1_angle = self.calibrate_man1_angle
				self.man2_angle = self.calibrate_man2_angle
				self.man3_angle = self.calibrate_man3_angle
				self.man4_angle = self.calibrate_man4_angle

				controller.Set_Pulse(0, ServoController.map(self.calibrate_angle1, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(1, ServoController.map(self.calibrate_angle2, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(2, ServoController.map(self.calibrate_angle3, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(3, ServoController.map(self.calibrate_angle4, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(4, ServoController.map(self.calibrate_cam_angle, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(5, ServoController.map(self.calibrate_man1_angle, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(6, ServoController.map(self.calibrate_man2_angle, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(7, ServoController.map(self.calibrate_man3_angle, 0, 180, servo_min, servo_max))
				controller.Set_Pulse(8, ServoController.map(self.calibrate_man4_angle, 0, 180, servo_min, servo_max))
				#sleep(pulsebeat - 0.01)

			if self.r_data[6] == 1:
				if self.cam_angle > 185:
					self.cam_angle = self.cam_angle - 7
					controller.Set_Pulse(4, ServoController.map(self.cam_angle, 0, 180, servo_min, servo_max))
					#print("cam: ", self.cam_angle)
					sleep(time_delay_seconds)
				else:
					self.cam_angle = self.cam_angle + 7
					#print("cam: ", self.cam_angle)

			#if self.r_data[19] == 1:
			#	if GPIO.input(Lineleft) == GPIO.HIGH and GPIO.input(Lineright) == GPIO.LOW:
			#		motor.rotate_counterwise()
			#	elif GPIO.input(Lineleft) == GPIO.LOW and GPIO.input(Lineroght) == GPIO.LOW:
			#		motor.rotate_counterwise()
			#	elif GPIO.input(Lineleft) == GPIO.HIGH:
			#		motor.turn_left()
			#	elif GPIO.input(Lineright) == GPIO.HIGH:
			#		motor.turn_right()
			#	else:
			#		pass


			if self.r_data[7] == 1:
				if self.cam_angle < 275:
					self.cam_angle = self.cam_angle + 7
					controller.Set_Pulse(4, ServoController.map(self.cam_angle, 0, 180, servo_min, servo_max))
					#print("cam: ", self.cam_angle)
					sleep(time_delay_seconds)
				else:
					self.cam_angle = self.cam_angle - 7

			if self.r_data[16] == 1:
				print("Boost enabled")
				self.boost = 1
				motor.motor_speed_dercrese(self.m_speed, self.boost)
				sleep(time_delay_seconds)

			if self.r_data[17] == 1:
				print("Boost disabled")
				self.boost = 0.25
				motor.motor_speed_increase(self.m_speed, self.boost)
				sleep(time_delay_seconds)


	def servorer(self):
		while True:
			sleep(pulsebeat)
			if self.sstate == 1:
				try:
					if self.r_data[4] == 1:
						if self.angle4 < 310:
							self.angle1 = self.angle1 + 5
							self.angle2 = self.angle2 - 3
							self.angle3 = self.angle3 - 5
							self.angle4 = self.angle4 + 5
							#print("First motor's servo angle: ", self.angle1)
							#print("Second motor's servo angle: ", self.angle2)
							#print("Third motor's servo angle: ", self.angle3)
							#print("Fourth motor's servo angle: ", self.angle4)
							controller.Set_Pulse(0, ServoController.map(self.angle1, 0, 180, servo_min, servo_max))
							controller.Set_Pulse(1, ServoController.map(self.angle2, 0, 180, servo_min, servo_max))
							controller.Set_Pulse(2, ServoController.map(self.angle3, 0, 180, servo_min, servo_max))
							controller.Set_Pulse(3, ServoController.map(self.angle4, 0, 180, servo_min, servo_max))
						else:
							self.angle1 = self.angle1 - 5
							self.angle2 = self.angle2 + 3
							self.angle3 = self.angle3 + 5
							self.angle4 = self.angle4 - 5

					if self.r_data[5] == 1:
						if self.angle4 > 140:
							self.angle1 = self.angle1 - 5
							self.angle2 = self.angle2 + 3
							self.angle3 = self.angle3 + 5
							self.angle4 = self.angle4 - 5
							#print("First motor's servo angle: ", self.angle1)
							#print("Second motor's servo angle: ", self.angle2)
							#print("Third motor's servo angle: ", self.angle3)
							#print("Fourth motor's servo angle: ", self.angle4)
							controller.Set_Pulse(0, ServoController.map(self.angle1, 0, 180, servo_min, servo_max))
							controller.Set_Pulse(1, ServoController.map(self.angle2, 0, 180, servo_min, servo_max))
							controller.Set_Pulse(2, ServoController.map(self.angle3, 0, 180, servo_min, servo_max))
							controller.Set_Pulse(3, ServoController.map(self.angle4, 0, 180, servo_min, servo_max))
						else:
							self.angle1 = self.angle1 + 5
							self.angle2 = self.angle2 - 3
							self.angle3 = self.angle3 - 5
							self.angle4 = self.angle4 + 5

					if self.r_data[8] == 1:
						if self.man1_angle < 326:
							self.man1_angle = self.man1_angle + 3
							controller.Set_Pulse(5, ServoController.map(self.man1_angle, 0, 180, servo_min, servo_max))
							#print("First man's servo anlge: ", self.man1_angle)
							sleep(time_delay_seconds)
						else:
							self.man1_angle = self.man1_angle - 3

					if self.r_data[9] == 1:
						if self.man1_angle > 140:
							self.man1_angle = self.man1_angle - 3
							controller.Set_Pulse(5, ServoController.map(self.man1_angle, 0, 180, servo_min, servo_max))
							#print("First man's servo angle: ", self.man1_angle)
							sleep(time_delay_seconds)
						else:
							self.man1_angle = self.man1_angle + 3

					if self.r_data[10] == 1:
						if self.man2_angle < 390:
							self.man2_angle = self.man2_angle + 3
							controller.Set_Pulse(6, ServoController.map(self.man2_angle, 0, 180, servo_min, servo_max))
							#print("Second man's servo angle: ", self.man2_angle)
							sleep(time_delay_seconds)
						else:
							self.man2_angle = self.man2_angle - 3

					if self.r_data[11] == 1:
						if self.man2_angle > 170:
							self.man2_angle = self.man2_angle - 3
							controller.Set_Pulse(6, ServoController.map(self.man2_angle, 0, 180, servo_min, servo_max))
							#print("Second man's servo angle: ", self.man2_angle)
							sleep(time_delay_seconds)
						else:
							self.man2_angle = self.man2_angle + 3
					if self.r_data[12] == 1:
						if self.man3_angle < 320:
							self.man3_angle = self.man3_angle + 10
							controller.Set_Pulse(7, ServoController.map(self.man3_angle, 0, 180, servo_min, servo_max))
							#print("Third man's servo anlge: ", self.man3_angle)
							sleep(time_delay_seconds)
						else:
							self.man3_angle = self.man3_angle - 10

					if self.r_data[13] == 1:
						if self.man3_angle > 130:
							self.man3_angle = self.man3_angle - 10
							controller.Set_Pulse(7, ServoController.map(self.man3_angle, 0, 180, servo_min, servo_max))
							sleep(time_delay_seconds)
							#print("Third man's servo angle: ", self.man3_angle)
						else:
							self.man3_angle = self.man3_angle + 10


					if self.r_data[14] == 1:
						if self.man4_angle < 440:
							self.man4_angle = self.man4_angle + 10
							controller.Set_Pulse(8, ServoController.map(self.man4_angle, 0, 180, servo_min, servo_max))
							sleep(time_delay_seconds)
							#print("Fourth man's servo angle: ", self.man4_angle)
						else:
							self.man4_angle = self.man4_angle - 10

					if self.r_data[15] == 1:
						if self.man4_angle > 115:
							self.man4_angle = self.man4_angle - 10
							controller.Set_Pulse(8, ServoController.map(self.man4_angle, 0, 180, servo_min, servo_max))
							sleep(time_delay_seconds)
							#print("Fourth man's servo angle: ", self.man4_angle)
						else:
							self.man4_angle = self.man4_angle + 10

				except AttributeError:
					pass

	def machinist(self):
		while True:
			sleep(pulsebeat)
			if self.mstate == 1:
				try:
					if self.r_data[0] == 1:
						#motor.rotate_counterwise()
						motor.rotate_clockwise()
						#print("Rotate clockwise")
					elif self.r_data[1] == 1:
						motor.rotate_counterwise()
						#motor.rotate_clockwise()
						#print("Rotate counterwise")

					elif self.r_data[3] == 1:
						#motor.turn_right()
						motor.turn_left()

					elif self.r_data[2] == 1:
						#motor.turn_left()
						motor.turn_right()
						#print("Turning left")

					else:
						motor.motor_stop()
				except AttributeError:
					pass

'''SOCKET MODULE '''
HOST = "192.101.77.1"
PORT = 65432

print("Waiting for connection")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
clientsocket, address = s.accept()
 
print(f"Connected from {address} has been established!")


'''MAIN MODULE '''

newconnection = ClientThread(HOST, PORT)
newconnection.run()



