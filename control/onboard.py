from handler import ClientThread
import library
import sys
from time import sleep



if __name__ == "__main__":

	rover = ClientThread(library.HOST, library.PORT)
	rover.setupConnection()
	rover.run()
	counter = 0

	while counter < 2:
		try:
			sleep(1)
			counter = counter + 1
		except KeyboardInterrupt:
			rover.closeConnection()
			break
