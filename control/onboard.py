import socket
import threading
import struct
import smbus
import subprocess
import sys
import numpy as np
from time import sleep
import math

from h39 import rmotor, lightBulb
from event import ServoEvent
import library

'''TIMINGS '''
pulsebeat = 0.04
time_delay_seconds = 0.05
time_calibrate = 0.1

'''LAMP INIT'''
try:
	lamp = lightBulb()
	sleep(time_calibrate)
	lamp.setup()
	print("Lamp init complete")
except:
	lamp.destruct()


'''MOTOR INIT'''
try:
	motor = rmotor()
	sleep(time_calibrate)
	motor.modify_pwm1(rmotor.pwm_signal, 80, 3000)
	motor.modify_pwm2(rmotor.pwm_signal1, 80, 3000)
	print("Motor init complete")
	sleep(time_calibrate)
except:
	print("Motor init error")

'''SERVO MOTOR'S INIT'''
try:
	serv = ServoEvent()
	sleep(time_calibrate * 3)
	serv.calibrationR()
	sleep(time_calibrate * 3)
	print("Servo init complete")
except:
	print("Servo init error")


class ClientThread(threading.Thread):
	def __init__(self, ip, port, debug = False):
		self.ip = ip
		self.port = port
		self.r_data = [0, 0, 0, 0, 0,
			       0, 0, 0, 0, 0,
			       0, 0, 0, 0, 0,
			       0, 0, 0, 0, 0,
			       0, 0, 0, 0, 0,
			       0]
		self._defaultpackage = 52
		self.debug = debug
		self.m_speed = 80
		self.k_turn = 0.4
		self.boost = 1
		self.sstate = 0
		self.mstate = 1
		self.lampState = 0
		print("[+] New server started from: ", ip + str(port))

	def reciever(self):
		_exit = 1
		count = 0
		while _exit != 0:
			try:
				data = clientsocket.recv(self._defaultpackage)
				if (self.debug):
					print("Size of recieving data", len(data))
				if (len(data) < 26):
					count = count + 1
				if len(data) == 26:
					self.r_data = np.frombuffer(data, dtype=np.uint8)
					if ((np.sum(self.r_data) - self.r_data[25]) % 2) != self.r_data[25]:
						print("Parity bit")
						count = count + 1
					count = 0
				else:
					print("Recieved data is corrupted")
					motor.motor_stop()
					lamp.lampOff()
					self.r_data = [0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
  						       0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
						       0]
				if count > 10:
					motor.motor_stop()
					_exit = 0
					print(f"Closing connection to {address}")
					s.close()
				sleep(pulsebeat)

			except:
				motor.motor_stop()
				_exit = 0
				print(f"Closing connection to {address}")
				s.close()

	def run(self):
		thread1=threading.Thread(target=self.reciever, daemon=False)
		thread1.start()
		thread2=threading.Thread(target=self.machinist, daemon=True)
		thread2.start()
		thread3=threading.Thread(target=self.servorer, daemon=True)
		thread3.start()
		thread4=threading.Thread(target=self.utiliter, daemon=True)
		thread4.start()

	def utiliter(self):
		while True:
			sleep(pulsebeat)
			if self.r_data[library.keyboard["1"]] == 1:
				serv.decreaseCamAngle(3)
			if self.r_data[library.keyboard["2"]] == 1:
				serv.increaseCamAngle(3)

			if self.r_data[library.keyboard["x"]] == 1:
				self.boost = 1
				motor.motor_speed_dercrese(self.m_speed, self.boost)
				sleep(time_delay_seconds)
			if self.r_data[library.keyboard["z"]] == 1:
				self.boost = 0.4
				motor.motor_speed_increase(self.m_speed, self.boost)
				sleep(time_delay_seconds)

			if self.r_data[library.keyboard["r"]] == 1:
				serv.calibrationR()
				sleep(time_delay_seconds)

			if self.r_data[library.keyboard["v"]] == 1:
				lamp.lampOn()
				sleep(time_delay_seconds)
			if self.r_data[library.keyboard["b"]] == 1:
				lamp.lampOff()
				sleep(time_delay_seconds)

	def servorer(self):
		while True:
			sleep(pulsebeat)
			if self.sstate == 1:
				try:

					if self.r_data[library.keyboard["q"]] == 1:
						serv.decreaseWheelAngle(7)
					if self.r_data[library.keyboard["e"]] == 1:
						serv.increaseWheelAngle(7)

					if self.r_data[library.keyboard["u"]] == 1:
						serv.increaseManAngle(library.servoName["man1"], 4)
					if self.r_data[library.keyboard["h"]] == 1:
						serv.decreaseManAngle(library.servoName["man1"], 4)

					if self.r_data[library.keyboard["i"]] == 1:
						serv.increaseManAngle(library.servoName["man2"], 4)
					if self.r_data[library.keyboard["j"]] == 1:
						serv.decreaseManAngle(library.servoName["man2"], 4)

					if self.r_data[library.keyboard["o"]] == 1:
						serv.increaseManAngle(library.servoName["man3"], 4)
					if self.r_data[library.keyboard["k"]] == 1:
						serv.decreaseManAngle(library.servoName["man3"], 4)

					if self.r_data[library.keyboard["p"]] == 1:
						serv.increaseManAngle(library.servoName["man4"], 6)
					if self.r_data[library.keyboard["l"]] == 1:
						serv.decreaseManAngle(library.servoName["man4"], 6)

					if self.r_data[library.keyboard["g"]] == 1:
						serv.increaseManAngle(library.servoName["man5"], 6)
					if self.r_data[library.keyboard["y"]] == 1:
						serv.decreaseManAngle(library.servoName["man5"], 6)
				except AttributeError:
					pass

	def machinist(self):
		while True:
			sleep(pulsebeat)
			if self.mstate == 1:
				try:
					if self.r_data[library.keyboard["w"]] == 1:
						motor.rotate_clockwise()
					elif self.r_data[library.keyboard["s"]] == 1:
						motor.rotate_counterwise()
					elif self.r_data[library.keyboard["d"]] == 1:
						motor.turn_right()
					elif self.r_data[library.keyboard["a"]] == 1:
						motor.turn_left()

					else:
						motor.motor_stop()
				except AttributeError:
					pass

'''SOCKET MODULE '''
HOST = "192.168.0.95"
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




