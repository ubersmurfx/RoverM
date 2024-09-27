import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
time_delay_seconds = 0.1

''''Motor driver ZK BM1 10A'''

'''BCM SETUP PINS '''

R1 = 20
''' IN1'''

L1 = 21
''' IN2 '''

R2 = 19
''' IN3 '''

L2 = 26
'''IN4'''


class rmotor:
    def __init__(self, debug = False):
        self.debug = debug

    GPIO.setup(R1, GPIO.OUT)
    GPIO.setup(L1, GPIO.OUT)
#    GPIO.setup(PWM1, GPIO.OUT)

    GPIO.setup(R2, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
#    GPIO.setup(PWM2, GPIO.OUT)

#    pwm_signal1 = GPIO.PWM(PWM2, 30)
#    pwm_signal1.start(0)
#    pwm_signal = GPIO.PWM(PWM1, 30)
#    pwm_signal.start(0)


#    def modify_pwm1(self, pwm_signal, dutycycle, freq):
#        pwm_signal.ChangeDutyCycle(dutycycle)
#        pwm_signal.ChangeFrequency(freq)

#    def modify_pwm2(self, pwm_signal1, dutycycle, freq):
#        pwm_signal1.ChangeDutyCycle(dutycycle)
#        pwm_signal1.ChangeFrequency(freq)


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
        sleep(0.5)
        self.motor_stop()
        sleep(0.5)
        self.rotate_counterwise()
        sleep(0.5)
        self.motor_stop()
        sleep(0.5)
        self.turn_left()
        sleep(0.5)
        self.turn_right()
        sleep(0.5)
        self.motor_stop()
        print("Calibration complete")

 #   def motor_speed_dercrese(self, m_speed, boost):
 #       self.modify_pwm1(self.pwm_signal, m_speed * boost, 1000)
 #       self.modify_pwm2(self.pwm_signal1, m_speed * boost, 1000)


 #   def motor_speed_increase(self, m_speed, boost):
 #       self.modify_pwm1(self.pwm_signal, m_speed * boost, 1000)
 #       self.modify_pwm2(self.pwm_signal1, m_speed * boost, 1000)

if __name__=="__main__":
    robot = rmotor()
    robot.calibrate()
