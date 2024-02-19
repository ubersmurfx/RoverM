#https://duino.ru/oled-sh1106.html/image-128x64/
import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess


class Display():
	def __init__(self, debug=False):
		self.debug = debug
		self.oled_reset = digitalio.DigitalInOut(board.D4)
		self.WIDTH = 128
		self.HEIGHT = 64
		self.BORDER = 5
		self.LOOPTIME = 1.0
		self.i2c = board.I2C()
		self.oled = adafruit_ssd1306.SSD1306_I2C(self.WIDTH, self.HEIGHT, self.i2c, addr=0x3C, reset=self.oled_reset)
		self.oled.fill(0)
		self.oled.show()
		self.image = Image.new("1", (self.oled.width, self.oled.height))
		self.draw = ImageDraw.Draw(self.image)
		self._exit = False
		self.greeting_time = 35
		self.counter = 0

	def operator(self):
		self.font = ImageFont.truetype('/bin/autostart-scripts/PixelOperator.ttf', 16)

	def show_robot_stats(self):
		exitStats = False
		while(exitStats != True): 
			self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)	
			cmd = "hostname -I | cut -d\' \' -f1"
			IP = subprocess.check_output(cmd, shell = True )
			cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
			CPU = subprocess.check_output(cmd, shell = True )
			cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
			MemUsage = subprocess.check_output(cmd, shell = True )
			cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
			Disk = subprocess.check_output(cmd, shell = True )
			cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
			Temp = subprocess.check_output(cmd, shell = True )

			self.draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=self.font, fill=255)
			self.draw.text((0, 16), str(CPU,'utf-8') + "LA", font=self.font, fill=255)
			self.draw.text((80, 16), str(Temp,'utf-8') , font=self.font, fill=255)
			self.draw.text((32, 48), "00:00:" + str(self.counter) ,font=self.font, fill=255)


			self.counter = self.counter + 1

			self.oled.image(self.image)
			self.oled.show()
			time.sleep(self.LOOPTIME)

			if (self.counter > self.greeting_time):
				exitStats = True

#0 - 15 initial screen
#15 - 35 stats

	def initial_screen(self):
		self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
		while(self._exit != True):
			cmd = "hostname -I | cut -d\' \' -f1"
			IP = subprocess.check_output(cmd, shell = True )

			self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
			self.draw.text((0, 16), str(IP, 'utf-8'), font=self.font, fill=255)
			self.draw.text((0, 0), "Made by SCTB", font=self.font, fill=255)
			self.draw.text((32, 48), "00:00:" + str(self.counter) ,font=self.font, fill=255)

			self.oled.image(self.image)
			self.oled.show()
			time.sleep(self.LOOPTIME)
			self.counter = self.counter + 1

			if (self.counter > 15):
				self.show_robot_stats()
				self.show_image()
			if (self.counter > self.greeting_time + 1):
				self._exit = True

	def show_image(self):
		self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)

		self.image = Image.open('/bin/autostart-scripts/rtc.jpg').convert('1')

		self.oled.image(self.image)
		self.oled.show()

	def run(self):
		self.operator()
		self.initial_screen()

if __name__=="__main__":
	startingDisplay = Display()
	startingDisplay.run()
