import time
import board
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import subprocess

#Define the reset pin
oled_reset = digitalio.DigitalInOut(board.D4)

WIDTH = 128
HEIGHT = 64
BORDER = 5

LOOPTIME = 2.0

# I2C
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C, reset=oled_reset)

# Clear display
oled.fill(0)
oled.show()

# Create blank image for drawing
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new("1", (oled.width, oled.height))

# Get drawing object to draw on image
draw = ImageDraw.Draw(image)

# Draw a white background
draw.rectangle((0, 0, oled.width, oled.height), outline=255, fill=255)

font = ImageFont.truetype('PixelOperator.ttf', 16)
#font = ImageFont.load_default()

counter = 0

while True:
	draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
	# Draw a black filled box to clear the image


	if counter < 60:
		draw.text((0, 0), "Loading the system", font=font, fill=255)
		if (counter > 30):
			draw.text((0, 48), "." * (counter - 30), font=font, fill=255)

		draw.text((0, 32), "." * counter, font=font, fill=255)
	elif counter > 62:


		cmd = "hostname -I | cut -d\' \' -f2"
		IP = subprocess.check_output(cmd, shell = True )
		cmd = "top -bn1 | grep load | awk '{printf \"CPU: %.2f\", $(NF-2)}'"
		CPU = subprocess.check_output(cmd, shell = True )
		cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
		MemUsage = subprocess.check_output(cmd, shell = True )
		cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
		Disk = subprocess.check_output(cmd, shell = True )
		cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
		Temp = subprocess.check_output(cmd, shell = True )

		# Pi Display
		draw.text((0, 0), "IP: " + str(IP,'utf-8'), font=font, fill=255)
		draw.text((0, 16), str(CPU,'utf-8') + "LA", font=font, fill=255)
		draw.text((80, 16), str(Temp,'utf-8') , font=font, fill=255)
		draw.text((0, 32), str(MemUsage,'utf-8'), font=font, fill=255)
		draw.text((0, 48), str(Disk,'utf-8'), font=font, fill=255)

	# Display image
	oled.image(image)
	oled.show()
	time.sleep(LOOPTIME)
	counter = counter + 1
