import socket
import threading
import struct
from time import sleep
import smbus
import math
from h39 import rmotor
import subprocess
import sys
from event import ServoEvent
#from MMSmotor import rmotor



'''MOTOR INIT'''
try:
	motor = rmotor()
	sleep(0.1)
	motor.modify_pwm1(rmotor.pwm_signal, 80, 3000)
	motor.modify_pwm2(rmotor.pwm_signal1, 80, 3000)
	print("init complete")
	sleep(0.1)
	#motor.calibrate()
except:
	print("motor init error")

try:
	serv = ServoEvent()
	sleep(0.5)
	#serv.calibrationR()
	sleep(0.5)
except:
	print("servomotors init error")

'''TIMINGS '''
pulsebeat = 0.04
time_delay_seconds = 0.05


class ClientThread(threading.Thread):
	def __init__(self, ip, port, debug = False):
		self.ip = ip
		self.port = port
		self.r_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self._defaultpackage = 168
		self.debug = debug
		self.m_speed = 80
		self.k_turn = 0.4
		self.boost = 1
		self.sstate = 1
		self.mstate = 1
		print("[+] New server started from: ", ip + str(port))

	def reciever(self):
		_exit = 1
		count = 0
		while _exit != 0:
			try:
				data = clientsocket.recv(self._defaultpackage)
				print("Size of recieving data", len(data))
				if len(data) < 83:
					count = count + 1

				if len(data) == 84:
					self.r_data = struct.unpack("21i", data)
					count = 0
				else:
					print("Recieved data is corrupted")
					motor.motor_stop()
					self.r_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
					#print("Server received data:", self.r_data)

				if count > 10:
					motor.motor_stop()
					_exit = 0
					print(f"Closing connection to {address}")
					s.close()

				sleep(pulsebeat)
				
			except:
				print("Recieved data is corrupted")
				motor.motor_stop()
				_exit = 0
				print(f"Closing connection to {address}")
				s.close()
		#exit()


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
				serv.decreaseCamAngle(7)
				sleep(time_delay_seconds)
			
			if self.r_data[7] == 1:
				serv.increaseCamAngle(7)
				sleep(time_delay_seconds)
		

			if self.r_data[16] == 1:
				self.boost = 1
				motor.motor_speed_dercrese(self.m_speed, self.boost)
				sleep(time_delay_seconds)

			if self.r_data[17] == 1:
				self.boost = 0.25
				motor.motor_speed_increase(self.m_speed, self.boost)
				sleep(time_delay_seconds)

			if self.r_data[18] == 1:
				serv.calibrationR()
				sleep(time_delay_seconds)


	def servorer(self):
		while True:
			sleep(pulsebeat)
			if self.sstate == 1:
				try:

					if self.r_data[4] == 1:
						serv.decreaseWheelAngle(7)
						sleep(time_delay_seconds)

					if self.r_data[5] == 1:
						serv.increaseWheelAngle(7)
						sleep(time_delay_seconds)

					if self.r_data[8] == 1:
						serv.increaseManAngle(5, 7)
						sleep(time_delay_seconds)

					if self.r_data[9] == 1:
						serv.decreaseManAngle(5, 7)
						sleep(time_delay_seconds)

					if self.r_data[10] == 1:
						serv.increaseManAngle(6, 7)
						sleep(time_delay_seconds)

					if self.r_data[11] == 1:
						serv.decreaseManAngle(6, 7)
						sleep(time_delay_seconds)

					if self.r_data[12] == 1:
						serv.increaseManAngle(7, 7)
						sleep(time_delay_seconds)

					if self.r_data[13] == 1:
						serv.decreaseManAngle(7, 7)
						sleep(time_delay_seconds)

					if self.r_data[14] == 1:
						serv.increaseManAngle(8, 7)
						sleep(time_delay_seconds)

					if self.r_data[15] == 1:
						serv.decreaseManAngle(8, 7)
						sleep(time_delay_seconds)


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
						#motor.turn_left()
						motor.turn_right()
						

					elif self.r_data[2] == 1:
						#motor.turn_right()
						motor.turn_left()
					else:
						motor.motor_stop()
						
				except AttributeError:
					pass

'''SOCKET MODULE '''
HOST = "192.168.0.10"
PORT = 65432



'''MAIN'''
if __name__ == "__main__":
	try:
		print("Waiting for connection")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((HOST, PORT))
		s.listen(5)
		clientsocket, address = s.accept()
		print(f"Connected from {address} has been established!")
	except Exception as e:
		raise ConnectionError(f"Failed to connect to {address}", str(e))
	
	
	newconnection = ClientThread(HOST, PORT)
	newconnection.run()
	
	while True:     # бесконечный цикл
		try:
			sleep(10)
		except KeyboardInterrupt:
			s.close()
			break
		



