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
from zkbm1 import rmotor
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
			       0, 0, 0, 0]
		self._defaultpackage = 48
		self.debug = debug
		self.m_speed = 95
		self.k_turn = 0.4
		self.boost = 1
		self.mstate = 1
		self.setupMotors()
		print("[+] New server started from:", ip + " " + str(port))
		if (self.mstate == 1):
			print("Robot is ready")

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

				if (len(data) < 24):
					count = count + 1

				if (len(data) == 24):
					self.r_data = np.frombuffer(data, dtype=np.uint8)
					if ((np.sum(self.r_data) - self.r_data[23]) % 2) != self.r_data[23]:
						#print(self.r_data)
						count = count + 1
					count = 0
				else:
					print("Recieved data is corrupted")
					self.motor.motor_stop()
					self.r_data = [0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
  						       0, 0, 0, 0, 0,
						       0, 0, 0, 0, 0,
						       0, 0, 0, 0]

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
		thread4=threading.Thread(target=self.utiliter, daemon=True)
		thread4.start()

	def utiliter(self):
		while True:
			sleep(library.pulsebeat)
			if (self.r_data[library.keyboard["1"]] == 1) and  (self.r_data[library.keyboard["z"]] == 1) and  (self.r_data[library.keyboard["p"]] == 1):
				self.closeConnection()
				os.system("shutdown now")


	def machinist(self):
		while True:
			sleep(library.pulsebeat)
			if self.mstate == 1:
				try:
					if (self.r_data[library.keyboard["w"]] == 1 or self.r_data[library.keyboard["s"]]) and self.r_data[library.keyboard["d"]] == 1:
						self.motor.turn_right()
					elif (self.r_data[library.keyboard["w"]] == 1 or self.r_data[library.keyboard["s"]]) and self.r_data[library.keyboard["a"]] == 1:
						self.motor.turn_left()					
					elif self.r_data[library.keyboard["w"]] == 1:
						self.motor.rotate_clockwise()
					elif self.r_data[library.keyboard["s"]] == 1:
						self.motor.rotate_counterwise()
					elif self.r_data[library.keyboard["a"]] == 1:
						self.motor.crab_left()
					elif self.r_data[library.keyboard["d"]] == 1:
						self.motor.crab_right()
					elif self.r_data[library.keyboard["e"]] == 1:
						self.motor.diagonal_right()
					elif self.r_data[library.keyboard["q"]] == 1:
						self.motor.diagonal_left()
					else:
						self.motor.motor_stop()
				except AttributeError:
					pass

	def setupMotors(self):
		try:
			self.motor = rmotor()
			self.motor.calibrate()
			self.motor.motor_stop()
			print("motor: OK")
		except:
			self.mstate = 0
			print("motor: error")


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
