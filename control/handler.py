import socket
import threading
import struct
import smbus
import subprocess
import sys
import os
import numpy as np
from time import sleep
import math
import library
from disp import display
from h39 import rmotor, lightBulb
from event import ServoEvent
from datetime import datetime


class ClientThread(threading.Thread):
	def __init__(self, ip, port, debug = False):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
		self.m_speed = 95
		self.k_turn = 0.4
		self.boost = 1
		self.dstate = 1
		self.sstate = 1
		self.mstate = 1
		self.lstate = 1
		self.setupDisplay()
		self.setupLamp()
		self.setupMotors()
		self.setupServo()
		print("[+] New server started from:", ip + " " + str(port))
		if (self.sstate == 1 and self.mstate == 1 and self.lstate == 1 and self.dstate == 1):
			print("Rover is ready")

		self.display.show_params(["display:  ", "lighBukb:  ", "motors:  ", "servs:  "], [library.state[self.dstate], library.state[self.lstate], library.state[self.mstate], library.state[self.sstate]])

	def setupConnection(self):
		try:
			print("Waiting for connection")
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind((library.HOST, library.PORT))
			self.socket.listen(5)
			self.clientsocket, self.address = self.socket.accept()
			print(f"Connected from {self.address} has been refused!")
		except Exception as e:
			raise ConnectionError(f"Failed to connect to {self.address}", str(e))

	def closeConnection(self):
		self.display.show_params(["ip", "connection closed", "", ""], [f"{self.address}", "at",datetime.now().strftime("%X"), ""])
		self.socket.close()
		print(f"Closing connection to {self.address}")

	def reciever(self):
		_exit = 1
		count = 0
		while _exit != 0:
			try:
				data = self.clientsocket.recv(self._defaultpackage)
				if (self.debug):
					print("Size of recieving data", len(data))

				if (len(data) < 26):
					count = count + 1

				if (len(data) == 26):
					self.r_data = np.frombuffer(data, dtype=np.uint8)
					if ((np.sum(self.r_data) - self.r_data[25]) % 2) != self.r_data[25]:
						#print(self.r_data)
						count = count + 1
					count = 0
				else:
					print("Recieved data is corrupted")
					self.motor.motor_stop()
					self.lamp.lampOff()
					self.r_data = [0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
  						       0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
						       0]

				if count > 10:
					self.motor.motor_stop()
					_exit = 0
					self.closeConnection()
				sleep(library.pulsebeat)

			except:
				self.motor.motor_stop()
				_exit = 0
				self.closeConnection()

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
			sleep(library.pulsebeat)
			if self.r_data[library.keyboard["x"]] == 1:
				if self.boost <= 0.95:
					self.boost = self.boost + 0.05
					self.display.show_params(["speed", "", "", ""], [round(self.boost, 2), "", "", ""])
					print("current speed", round(self.boost, 2))
				self.motor.motor_speed_dercrese(self.m_speed, self.boost)
				sleep(library.time_delay_seconds)
			if self.r_data[library.keyboard["z"]] == 1:
				if self.boost > 0.3:
					self.boost = self.boost - 0.05
					self.display.show_params(["speed", "", "", ""], [round(self.boost, 2), "", "", ""])
					print("z", round(self.boost, 2))
				self.motor.motor_speed_increase(self.m_speed, self.boost)
				sleep(library.time_delay_seconds)

			if self.r_data[library.keyboard["v"]] == 1:
				self.lamp.lampOn()
				sleep(library.time_delay_seconds)

			if self.r_data[library.keyboard["b"]] == 1:
				self.lamp.lampOff()
				sleep(library.time_delay_seconds)

			if (self.r_data[library.keyboard["1"]] == 1) and  (self.r_data[library.keyboard["z"]] == 1) and  (self.r_data[library.keyboard["p"]] == 1):
				self.closeConnection()
				self.display.show_params(["shutdown", "", "", ""], ["......", "......", "...", ""])
				os.system("shutdown now")


	def servorer(self):
		while True:
			sleep(library.pulsebeat)
			if self.sstate == 1:
				try:
					if self.r_data[library.keyboard["r"]] == 1:
						self.serv.calibrationR()
						sleep(library.time_delay_seconds)

					if self.r_data[library.keyboard["t"]] == 1:
						self.serv.calibrationE()
						sleep(library.time_delay_seconds)

					if self.r_data[library.keyboard["1"]] == 1:
						self.serv.decreaseCamAngle(1)
					if self.r_data[library.keyboard["2"]] == 1:
						self.serv.increaseCamAngle(1)

					if self.r_data[library.keyboard["q"]] == 1:
						self.serv.decreaseWheelAngle(5)
					if self.r_data[library.keyboard["e"]] == 1:
						self.serv.increaseWheelAngle(5)

					if self.r_data[library.keyboard["u"]] == 1:
						self.serv.increaseManAngle(library.servoName["man1"], 2)
					if self.r_data[library.keyboard["h"]] == 1:
						self.serv.decreaseManAngle(library.servoName["man1"], 2)

					if self.r_data[library.keyboard["i"]] == 1:
						self.serv.increaseManAngle(library.servoName["man2"], 2)
					if self.r_data[library.keyboard["j"]] == 1:
						self.serv.decreaseManAngle(library.servoName["man2"], 2)

					if self.r_data[library.keyboard["o"]] == 1:
						self.serv.increaseManAngle(library.servoName["man3"], 3)
					if self.r_data[library.keyboard["k"]] == 1:
						self.serv.decreaseManAngle(library.servoName["man3"], 3)

					if self.r_data[library.keyboard["p"]] == 1:
						self.serv.increaseManAngle(library.servoName["man4"], 4)
					if self.r_data[library.keyboard["l"]] == 1:
						self.serv.decreaseManAngle(library.servoName["man4"], 4)

					if self.r_data[library.keyboard["g"]] == 1:
						self.serv.increaseManAngle(library.servoName["man5"], 3)
					if self.r_data[library.keyboard["y"]] == 1:
						self.serv.decreaseManAngle(library.servoName["man5"], 3)

				except AttributeError:
					pass

	def machinist(self):
		while True:
			sleep(library.pulsebeat)
			if self.mstate == 1:
				try:
					if self.r_data[library.keyboard["w"]] == 1:
						self.motor.rotate_clockwise()
					elif self.r_data[library.keyboard["s"]] == 1:
						self.motor.rotate_counterwise()
					elif self.r_data[library.keyboard["a"]] == 1:
						self.motor.turn_right()
					elif self.r_data[library.keyboard["d"]] == 1:
						self.motor.turn_left()
					else:
						self.motor.motor_stop()
				except AttributeError:
					pass

	def setupDisplay(self):
		try:
			self.display = display.Display()
			print("display: OK")

		except:
			self.dstate = 0
			print("display: error 0x3c")

	def setupLamp(self):
		try:
			self.lamp = lightBulb()
			self.lamp.setup()
			print("lamp: OK")
		except:
			self.lstate = 0
			self.lamp.destruct()
			print("lamp: error")

	def setupMotors(self):
		try:
			self.motor = rmotor()
			self.motor.modify_pwm1(rmotor.pwm_signal, 100, 1000)
			self.motor.modify_pwm2(rmotor.pwm_signal1, 100, 1000)
			print("motor: OK")
		except:
			self.mstate = 0
			print("motor: error")

	def setupServo(self):
		try:
			self.serv = ServoEvent()
			print("servo: OK")
		except:
			self.sstate = 0
			print("servo: error 0x40")

if __name__ == "__main__":
	try:
		print("Waiting for connection")
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((library.HOST, library.PORT))
		s.listen(5)
		clientsocket, address = s.accept()
		print("Connected from {address} has been refused!")
	except Exception as e:
		raise ConnectionError(f"Failed to connect to {address}", str(e))

	newconnection = ClientThread(library.HOST, library.PORT)
	newconnection.run()

	while True:
		try:
			sleep(10)
		except KeyboardInterrupt:
			s.close()
			break
