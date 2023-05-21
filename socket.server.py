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
from Event import ServoEvent

'''MOTOR INIT'''
try:
	motor = rmotor()
	motor.motor_enabled()
	sleep(0.1)
	motor.modify_pwm1(rmotor.pwm_signal, 80, 3000)
	motor.modify_pwm2(rmotor.pwm_signal1, 80, 3000)
	print("init complete")
	sleep(0.1)
except:
	print("motor init error")


serv = ServoEvent()
serv.calibrationR()
sleep(0.1)


'''TIMINGS must match'''
pulsebeat = 0.04
time_delay_seconds = 0.05


class ClientThread(threading.Thread):
	def __init__(self, ip, port, debug = True):
		self.ip = ip
		self.port = port
		self._exit = 1
		
		self.r_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		
		self._defaultpackage = 168
		self.debug = debug
		self.m_speed = 80
		self.k_turn = 0.4
		self.boost = 1
		self.sstate = 1
		self.mstate = 1
		print("[+] New server socket thread started from: ", ip + str(port))

	def reciever(self):
		_exit = 1
		while _exit != 0:
			try:
				data = clientsocket.recv(self._defaultpackage)
				if (self.debug):
					print("Size of recieving data", len(data))
					
				if len(data) == 80:
					print("sucksess")
					self.r_data = struct.unpack("20i", data)
				else:
					print("error")
					self.r_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				#print("Server received data:", self.r_data)
				sleep(pulsebeat)
			except:
				print("Error in recieving data")
				motor.motor_stop()
				_exit = 0
				print("Socket closing")
				clientsocket.close()

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
			if self.r_data[6] == 1:
				self.cam_angle = serv.decreaseAngle(4, self.cam_angle, 7)
				sleep(time_delay_seconds)
			
			if self.r_data[7] == 1:
				self.cam_angle = serv.increaseAngle(4, self.cam_angle, 7)
				sleep(time_delay_seconds)
		

			if self.r_data[16] == 1:
				if debug:
					print("Boost enabled")
				self.boost = 1
				motor.motor_speed_dercrese(self.m_speed, self.boost)
				sleep(time_delay_seconds)

			if self.r_data[17] == 1:
				if debug:
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
						self.angle1 = serv.increaseAngle(0, self.angle1, 5)
						self.angle4 = serv.decreaseAngle(3, self.angle4, 5)
						self.angle2 = serv.decreaseAngle(1, self.angle2, 3)
						self.angle3 = serv.increaseAngle(2, self.angle3, 5)
						sleep(time_delay_seconds)
						
						if debug:
							print("First motor's servo angle: ", self.angle1)
							print("Second motor's servo angle: ", self.angle2)
							print("Third motor's servo angle: ", self.angle3)
							print("Fourth motor's servo angle: ", self.angle4)

					if self.r_data[5] == 1:
						self.angle1 = serv.decreaseAngle(0, self.angle1, 5)
						self.angle4 = serv.increaseAngle(3, self.angle4, 5)
						self.angle2 = serv.increaseAngle(1, self.angle2, 3)
						self.angle3 = serv.decreaseAngle(2, self.angle3, 5)
						sleep(time_delay_seconds)
						
						if debug:
							print("First motor's servo angle: ", self.angle1)
							print("Second motor's servo angle: ", self.angle2)
							print("Third motor's servo angle: ", self.angle3)
							print("Fourth motor's servo angle: ", self.angle4)

					if self.r_data[8] == 1:
						self.man1_angle = serv.increaseAngle(5, self.man1_angle, 7)
						sleep(time_delay_seconds)
						if debug:
							print("First man's servo anlge: ", self.man1_angle)

					if self.r_data[9] == 1:
						self.man1_angle = serv.decreaseAngle(5, self.man1_angle, 7)
						sleep(time_delay_seconds)
						if debug:
							print("First man's servo anlge: ", self.man1_angle)

					if self.r_data[10] == 1:
						self.man2_angle = serv.increaseAngle(6, self.man2_angle, 7)
						sleep(time_delay_seconds)
						if debug:
							print("Second man's servo anlge: ", self.man2_angle)

					if self.r_data[11] == 1:
						self.man2_angle = serv.decreaseAngle(6, self.man2_angle, 7)
						sleep(time_delay_seconds)
						if debug:
							print("Second man's servo anlge: ", self.man2_angle)

					if self.r_data[12] == 1:
						self.man3_angle = serv.increaseAngle(7, self.man3_angle, 10)
						sleep(time_delay_seconds)
						if debug:
							print("Third man's servo anlge: ", self.man3_angle)

					if self.r_data[13] == 1:
						self.man3_angle = serv.decreaseAngle(7, self.man3_angle, 10)
						sleep(time_delay_seconds)
						if debug:
							print("Third man's servo anlge: ", self.man3_angle)


					if self.r_data[14] == 1:
						self.man4_angle = serv.increaseAngle(8, self.man4_angle, 10)
						sleep(time_delay_seconds)
						if debug:
							print("Fourth man's servo anlge: ", self.man4_angle)

					if self.r_data[15] == 1:
						self.man4_angle = serv.decreaseAngle(8, self.man4_angle, 10)
						sleep(time_delay_seconds)
						if debug:
							print("Fourth man's servo anlge: ", self.man4_angle)

				except AttributeError:
					pass

	def machinist(self):
		while True:
			sleep(pulsebeat)
			if self.mstate == 1:
				try:
					if self.r_data[0] == 1:
						motor.rotate_clockwise()
						
							
					elif self.r_data[1] == 1:
						motor.rotate_counterwise()
						

					elif self.r_data[3] == 1:
						motor.turn_left()
						

					elif self.r_data[2] == 1:
						motor.turn_right()
						
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



