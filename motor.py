import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
time_delay_seconds = 0.1

A1 = 6
D4 = 5
D9 = 16
PWM_1 = 21

A0 = 26
D7 = 19
D8 = 13
PWM_0 = 12

#A1 = 31
#D4 = 29
#D9 = 36
#PWM_1 = 40

#A0 = 37
#D7 = 35
#D8 = 33
#PWM_0 = 32


class rmotor:
    def __init__(self):
        print("init motors")

    GPIO.setup(D9, GPIO.OUT)
    GPIO.setup(D4, GPIO.OUT)
    GPIO.setup(PWM_1, GPIO.OUT)
    GPIO.setup(A1, GPIO.OUT)
    GPIO.setup(D7, GPIO.OUT)
    GPIO.setup(D8, GPIO.OUT)
    GPIO.setup(PWM_0, GPIO.OUT)
    GPIO.setup(A0, GPIO.OUT)

    pwm_signal1 = GPIO.PWM(PWM_1, 30)
    pwm_signal1.start(0)
    pwm_signal = GPIO.PWM(PWM_0, 30)
    pwm_signal.start(0)

    def modify_pwm1(self, pwm_signal, dutycycle, freq):
        print("modify pwm ")
        pwm_signal.ChangeDutyCycle(dutycycle)
        pwm_signal.ChangeFrequency(freq)

    def modify_pwm2(self, pwm_signal1, dutycycle, freq):
        print("modify pwm ")
        pwm_signal1.ChangeDutyCycle(dutycycle)
        pwm_signal1.ChangeFrequency(freq)

    def motor_enabled(self):
        # print("motor enabled")
        GPIO.output(A1, GPIO.HIGH)
        GPIO.output(A0, GPIO.HIGH)

    def motor_stop(self):
        # print("motor stopped")
        GPIO.output(D9, GPIO.LOW)
        GPIO.output(D4, GPIO.LOW)
        GPIO.output(D7, GPIO.LOW)
        GPIO.output(D8, GPIO.LOW)

    def rotate_clockwise(self):
        #print("rotate clockwise")
        GPIO.output(D7, GPIO.HIGH)
        GPIO.output(D8, GPIO.LOW)
        GPIO.output(D9, GPIO.LOW)
        GPIO.output(D4, GPIO.HIGH)

    def rotate_counterwise(self):
        #print("rotate counterclockwise")
        GPIO.output(D7, GPIO.LOW)
        GPIO.output(D8, GPIO.HIGH)
        GPIO.output(D9, GPIO.HIGH)
        GPIO.output(D4, GPIO.LOW)

    def turn_left(self):
        # print("turn left")
        GPIO.output(D7, GPIO.HIGH)
        GPIO.output(D8, GPIO.LOW)
        GPIO.output(D9, GPIO.HIGH)
        GPIO.output(D4, GPIO.LOW)

    def turn_right(self):
        # print("turn right")
        GPIO.output(D7, GPIO.LOW)
        GPIO.output(D8, GPIO.HIGH)
        GPIO.output(D9, GPIO.LOW)
        GPIO.output(D4, GPIO.HIGH)

    def destruct(self):
        # print("motor disabled")
        GPIO.output(A0, GPIO.LOW)
        GPIO.output(A1, GPIO.LOW)
        GPIO.cleanup()

    def calibrate(self):
        self.rotate_clockwise()
        sleep(0.2)
        self.motor_stop()
        sleep(0.2)
        self.rotate_counterwise()
        sleep(0.2)
        self.motor_stop()
        print("complete")

    def soft_rotate_right(self, m_speed, boost, k_turn):
        self.modify_pwm2(self.pwm_signal1, m_speed * boost * k_turn, 3000)
        print("right: ", m_speed * boost * k_turn)
        self.rotate_clockwise()
        sleep(time_delay_seconds)
        self.modify_pwm2(self.pwm_signal1, m_speed * boost, 3000)

    def soft_rotate_left(self, m_speed, boost, k_turn):
        self.modify_pwm1(self.pwm_signal, m_speed * boost * k_turn, 3000)
        print("left: ", m_speed * boost * k_turn)
        self.rotate_clockwise()
        sleep(time_delay_seconds)
        self.modify_pwm1(self.pwm_signal, m_speed * boost, 3000)

    def motor_speed_dercrese(self, m_speed, boost):
        self.modify_pwm1(self.pwm_signal, m_speed * boost, 3000)
        self.modify_pwm2(self.pwm_signal1, m_speed * boost, 3000)

    def motor_speed_increase(self, m_speed, boost):
        self.modify_pwm1(self.pwm_signal, m_speed * boost, 3000)
        self.modify_pwm2(self.pwm_signal1, m_speed * boost, 3000)

