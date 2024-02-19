import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
time_delay_seconds = 0.1

''''Motor driver IBT2-BTS7960 43A'''

'''BCM SETUP PINS '''

R1 = 5
L1 = 6
PWM1 = 19

R2 = 20
L2 = 16
PWM2 = 12

LAMP = 17

class lightBulb:
	def __init__(self, pin = LAMP, debug = False):
		self.debug = debug
		self.pin = pin

	def setup(self):
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, GPIO.LOW)

	def lampOn(self):
                GPIO.output(self.pin, GPIO.HIGH)

	def lampOff(self):
		GPIO.output(self.pin, GPIO.LOW)

	def destruct(self):
		GPIO.output(self.pin, GPIO.LOW)
		GPIO.cleanup()


class rmotor:
    def __init__(self, debug = False):
        self.debug = debug

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(PWM1, GPIO.OUT)

    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(PWM2, GPIO.OUT)

    pwm_signal1 = GPIO.PWM(PWM2, 30)
    pwm_signal1.start(0)
    pwm_signal = GPIO.PWM(PWM1, 30)
    pwm_signal.start(0)


    def modify_pwm1(self, pwm_signal, dutycycle, freq):
        pwm_signal.ChangeDutyCycle(dutycycle)
        pwm_signal.ChangeFrequency(freq)

    def modify_pwm2(self, pwm_signal1, dutycycle, freq):
        pwm_signal1.ChangeDutyCycle(dutycycle)
        pwm_signal1.ChangeFrequency(freq)


    def motor_stop(self):
        if (self.debug):
                print("motor stopped")

        GPIO.output(R1, GPIO.LOW)
        GPIO.output(L1, GPIO.LOW)
        GPIO.output(R2, GPIO.LOW)
        GPIO.output(L2, GPIO.LOW)

    def rotate_clockwise(self):
        if (self.debug):
                print("Rotate clockwise")

        GPIO.output(R1, GPIO.HIGH)
        GPIO.output(L1, GPIO.LOW)
        GPIO.output(L2, GPIO.LOW)
        GPIO.output(R2, GPIO.HIGH)

    def rotate_counterwise(self):
        if (self.debug):
                print("Rotate counterwise")

        GPIO.output(R1, GPIO.LOW)
        GPIO.output(L1, GPIO.HIGH)
        GPIO.output(L2, GPIO.HIGH)
        GPIO.output(R2, GPIO.LOW)

    def turn_left(self):
        if (self.debug):
                print("turn left")

        GPIO.output(R1, GPIO.HIGH)
        GPIO.output(L1, GPIO.LOW)
        GPIO.output(L2, GPIO.HIGH)
        GPIO.output(R2, GPIO.LOW)

    def turn_right(self):
        if (self.debug):
                print("Turning right")
        GPIO.output(R1, GPIO.LOW)
        GPIO.output(L1, GPIO.HIGH)
        GPIO.output(L2, GPIO.LOW)
        GPIO.output(R2, GPIO.HIGH)


    def calibrate(self):
        self.rotate_clockwise()
        sleep(0.2)
        self.motor_stop()
        sleep(0.2)
        self.rotate_counterwise()
        sleep(0.2)
        self.motor_stop()
        print("Calibration complete")

    def motor_speed_dercrese(self, m_speed, boost):
        self.modify_pwm1(self.pwm_signal, m_speed * boost, 1000)
        self.modify_pwm2(self.pwm_signal1, m_speed * boost, 1000)


    def motor_speed_increase(self, m_speed, boost):
        self.modify_pwm1(self.pwm_signal, m_speed * boost, 1000)
        self.modify_pwm2(self.pwm_signal1, m_speed * boost, 1000)

