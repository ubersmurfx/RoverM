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
		self.font = ImageFont.truetype('disp/PixelOperator.ttf', 16)

	def show_params(self, names ,params):
		self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
		self.draw.text((0, 0), str(names[0]) + ": " + str(params[0]), font=self.font, fill=255)
		self.draw.text((0, 16), str(names[1]) + ": " + str(params[1]), font=self.font, fill=255)
		self.draw.text((0, 32), str(names[2]) + ": " + str(params[2]), font=self.font, fill=255)
		self.draw.text((0, 48), str(names[3]) + ": " + str(params[3]), font=self.font, fill=255)

		self.oled.image(self.image)
		self.oled.show()

	def show_image(self, path):
		self.draw.rectangle((0, 0, self.oled.width, self.oled.height), outline=0, fill=0)
		self.image = Image.open(path).convert('1')
		self.oled.image(self.image)
		self.oled.show()
