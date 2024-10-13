import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
time_delay_seconds = 0.1

''''Motor driver ZK BM1 10A'''

'''BCM SETUP PINS '''

R1_HIGH = 6
''' IN1 1st driver'''

R1_LOW = 12
''' IN2 1st driver'''

R2_HIGH = 5
''' IN3 1st driver'''

R2_LOW = 1
'''IN4 1st driver'''

L1_HIGH = 21
''' R1 IN1 2nd driver'''

L1_LOW = 20
'''L1 IN2 2nd driver'''

L2_HIGH = 19
'''R2 IN3 2nd driver '''

L2_LOW = 26
'''L2 IN4 2nd driver'''


class rmotor:
    def __init__(self, debug = False):
        self.debug = debug

    GPIO.setup(R1_HIGH, GPIO.OUT)
    GPIO.setup(R1_LOW, GPIO.OUT)
    GPIO.setup(R2_HIGH, GPIO.OUT)
    GPIO.setup(R2_LOW, GPIO.OUT)
#    GPIO.setup(PWM1, GPIO.OUT)

    GPIO.setup(L1_HIGH, GPIO.OUT)
    GPIO.setup(L1_LOW, GPIO.OUT)
    GPIO.setup(L2_HIGH, GPIO.OUT)
    GPIO.setup(L2_LOW, GPIO.OUT)
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

        GPIO.output(R1_HIGH, GPIO.LOW)
        GPIO.output(R1_LOW, GPIO.LOW)
        GPIO.output(R2_HIGH, GPIO.LOW)
        GPIO.output(R2_LOW, GPIO.LOW)
        GPIO.output(L1_HIGH, GPIO.LOW)
        GPIO.output(L1_LOW, GPIO.LOW)
        GPIO.output(L2_HIGH, GPIO.LOW)
        GPIO.output(L2_LOW, GPIO.LOW)

    def rotate_clockwise(self):
        if (self.debug):
                print("Rotate clockwise")

        GPIO.output(R1_HIGH, GPIO.HIGH)
        GPIO.output(R1_LOW, GPIO.LOW)
        GPIO.output(R2_HIGH, GPIO.HIGH)
        GPIO.output(R2_LOW, GPIO.LOW)
        GPIO.output(L1_HIGH, GPIO.HIGH)
        GPIO.output(L1_LOW, GPIO.LOW)
        GPIO.output(L2_HIGH, GPIO.HIGH)
        GPIO.output(L2_LOW, GPIO.LOW)

    def rotate_counterwise(self):
        if (self.debug):
                print("Rotate counterwise")

        GPIO.output(R1_HIGH, GPIO.LOW)
        GPIO.output(R1_LOW, GPIO.HIGH)
        GPIO.output(R2_HIGH, GPIO.LOW)
        GPIO.output(R2_LOW, GPIO.HIGH)
        GPIO.output(L1_HIGH, GPIO.LOW)
        GPIO.output(L1_LOW, GPIO.HIGH)
        GPIO.output(L2_HIGH, GPIO.LOW)
        GPIO.output(L2_LOW, GPIO.HIGH)
        
    def turn_left(self):
        if (self.debug):
                print("turn left")

        GPIO.output(R1_HIGH, GPIO.HIGH)
        GPIO.output(R1_LOW, GPIO.LOW)
        GPIO.output(R2_HIGH, GPIO.HIGH)
        GPIO.output(R2_LOW, GPIO.LOW)
        GPIO.output(L1_HIGH, GPIO.LOW)
        GPIO.output(L1_LOW, GPIO.HIGH)
        GPIO.output(L2_HIGH, GPIO.LOW)
        GPIO.output(L2_LOW, GPIO.HIGH)

    def turn_right(self):
        if (self.debug):
                print("Turning right")

        GPIO.output(R1_HIGH, GPIO.LOW)
        GPIO.output(R1_LOW, GPIO.HIGH)
        GPIO.output(R2_HIGH, GPIO.LOW)
        GPIO.output(R2_LOW, GPIO.HIGH)
        GPIO.output(L1_HIGH, GPIO.HIGH)
        GPIO.output(L1_LOW, GPIO.LOW)
        GPIO.output(L2_HIGH, GPIO.HIGH)
        GPIO.output(L2_LOW, GPIO.LOW)

    def crab_right(self):
        if (self.debug):
                print("Crab right")

        GPIO.output(R1_HIGH, GPIO.LOW)
        GPIO.output(R1_LOW, GPIO.HIGH)
        GPIO.output(R2_HIGH, GPIO.HIGH)
        GPIO.output(R2_LOW, GPIO.LOW)
        GPIO.output(L1_HIGH, GPIO.HIGH)
        GPIO.output(L1_LOW, GPIO.LOW)
        GPIO.output(L2_HIGH, GPIO.LOW)
        GPIO.output(L2_LOW, GPIO.HIGH)

    def crab_left(self):
        if (self.debug):
                print("Crab left")

        GPIO.output(R1_HIGH, GPIO.HIGH)
        GPIO.output(R1_LOW, GPIO.LOW)
        GPIO.output(R2_HIGH, GPIO.LOW)
        GPIO.output(R2_LOW, GPIO.HIGH)
        GPIO.output(L1_HIGH, GPIO.LOW)
        GPIO.output(L1_LOW, GPIO.HIGH)
        GPIO.output(L2_HIGH, GPIO.HIGH)
        GPIO.output(L2_LOW, GPIO.LOW)

    def diagonal_right(self):
        if (self.debug):
                print("Diagonal right")

        GPIO.output(R1_HIGH, GPIO.LOW)
        GPIO.output(R1_LOW, GPIO.LOW)
        GPIO.output(R2_HIGH, GPIO.HIGH)
        GPIO.output(R2_LOW, GPIO.LOW)
        GPIO.output(L1_HIGH, GPIO.HIGH)
        GPIO.output(L1_LOW, GPIO.LOW)
        GPIO.output(L2_HIGH, GPIO.LOW)
        GPIO.output(L2_LOW, GPIO.LOW)

    def diagonal_left(self):
        if (self.debug):
                print("Diagonal left")

        GPIO.output(R1_HIGH, GPIO.HIGH)
        GPIO.output(R1_LOW, GPIO.LOW)
        GPIO.output(R2_HIGH, GPIO.LOW)
        GPIO.output(R2_LOW, GPIO.LOW)
        GPIO.output(L1_HIGH, GPIO.LOW)
        GPIO.output(L1_LOW, GPIO.LOW)
        GPIO.output(L2_HIGH, GPIO.HIGH)
        GPIO.output(L2_LOW, GPIO.LOW)


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