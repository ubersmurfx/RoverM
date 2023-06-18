import struct
import sys
import threading
from time import sleep
import socket
import cval

try:
    from pynput import keyboard
except ImportError:
    keyboard = None
    print("Pynput module is not installed. Use the command 'pip install pynput' in the terminal")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cval.HOST, cval.PORT))
    send_data = []
except Exception as e:
    print(sys.exc_info(), "\t", e)


def send_to_robot(package):
    ref_package = struct.pack("21i",
                              package[0],
                              package[1],
                              package[2],
                              package[3],
                              package[4],
                              package[5],
                              package[6],
                              package[7],
                              package[8],
                              package[9],
                              package[10],
                              package[11],
                              package[12],
                              package[13],
                              package[14],
                              package[15],
                              package[16],
                              package[17],
                              package[18],
                              package[19],
                              package[20])
    s.send(ref_package)


def set_value(pos, value, package):
    package[pos] = value


class Control(threading.Thread):
    control_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.control_data = Control.control_data
        print(send_data)
        print("init control class")
        threading.Thread.__init__(self, daemon=True)
        self._keyboard = None

    def from_keyboard(self):
        self.connect_keyboard_handlers()

    def connect_keyboard_handlers(self):
        def on_press(key):
            try:
                match key.char:
                    case cval.MOVE_FORWARD:
                        set_value(0, 1, self.control_data)
                    case cval.MOVE_BACKWARD:
                        set_value(1, 1, self.control_data)
                    case cval.TURN_TANK_LEFT:
                        set_value(2, 1, self.control_data)
                    case cval.TURN_TANK_RIGHT:
                        set_value(3, 1, self.control_data)
                    case cval.TURN_LEFT:
                        set_value(4, 1, self.control_data)
                    case cval.TURN_RIGHT:
                        set_value(5, 1, self.control_data)
                    case cval.CAM_DOWN:
                        set_value(6, 1, self.control_data)
                    case cval.CAM_UP:
                        set_value(7, 1, self.control_data)
                    case cval.MAN_1_UP:
                        set_value(8, 1, self.control_data)
                    case cval.MAN_1_DOWN:
                        set_value(9, 1, self.control_data)
                    case cval.MAN2_UP:
                        set_value(10, 1, self.control_data)
                    case cval.MAN2_DOWN:
                        set_value(11, 1, self.control_data)
                    case cval.MAN3_UP:
                        set_value(12, 1, self.control_data)
                    case cval.MAN3_DOWN:
                        set_value(13, 1, self.control_data)
                    case cval.MAN4_UP:
                        set_value(14, 1, self.control_data)
                    case cval.MAN4_DOWN:
                        set_value(15, 1, self.control_data)
                    case cval.MOTOR_BOOST:
                        set_value(16, 1, self.control_data)
                    case cval.MOTOR_DBOOST:
                        set_value(17, 1, self.control_data)
                    case cval.CALIBRATE_ALL:
                        set_value(18, 1, self.control_data)
                    case cval.LAMPON:
                        set_value(19, 1, self.control_data)
                    case cval.LAMPOFF:
                        set_value(20, 1, self.control_data)
            except AttributeError:
                pass

        def on_release(key):
            try:
                match key.char:
                    case cval.MOVE_FORWARD:
                        set_value(0, 0, self.control_data)
                    case cval.MOVE_BACKWARD:
                        set_value(1, 0, self.control_data)
                    case cval.TURN_TANK_LEFT:
                        set_value(2, 0, self.control_data)
                    case cval.TURN_TANK_RIGHT:
                        set_value(3, 0, self.control_data)
                    case cval.TURN_LEFT:
                        set_value(4, 0, self.control_data)
                    case cval.TURN_RIGHT:
                        set_value(5, 0, self.control_data)
                    case cval.CAM_DOWN:
                        set_value(6, 0, self.control_data)
                    case cval.CAM_UP:
                        set_value(7, 0, self.control_data)
                    case cval.MAN_1_UP:
                        set_value(8, 0, self.control_data)
                    case cval.MAN_1_DOWN:
                        set_value(9, 0, self.control_data)
                    case cval.MAN2_UP:
                        set_value(10, 0, self.control_data)
                    case cval.MAN2_DOWN:
                        set_value(11, 0, self.control_data)
                    case cval.MAN3_UP:
                        set_value(12, 0, self.control_data)
                    case cval.MAN3_DOWN:
                        set_value(13, 0, self.control_data)
                    case cval.MAN4_UP:
                        set_value(14, 0, self.control_data)
                    case cval.MAN4_DOWN:
                        set_value(15, 0, self.control_data)
                    case cval.MOTOR_BOOST:
                        set_value(16, 0, self.control_data)
                    case cval.MOTOR_DBOOST:
                        set_value(17, 0, self.control_data)
                    case cval.CALIBRATE_ALL:
                        set_value(18, 0, self.control_data)
                    case cval.LAMPON:
                        set_value(19, 0, self.control_data)
                    case cval.LAMPOFF:
                        set_value(20, 0, self.control_data)
            except AttributeError:
                pass

        self._keyboard = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._keyboard.start()
        self._keyboard.join()

    def run(self):
        self.connect_keyboard_handlers()


class Sender(Control):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        _exit = 1
        while _exit != 0:
            try:
                print("send")
                send_to_robot(Control.control_data)
                sleep(cval.delay)
            except Exception as err:
                _exit = 0
                print(sys.exc_info(), "\t", err)
                s.close()


try:
    data_exchanger = Sender()
    data_exchanger.start()
except Exception:
    print(sys.exc_info())

print("The remote control has been successfully configured")

try:
    motor = Control()
    motor.from_keyboard()
    motor.start()
except Exception:
    print(sys.exc_info())


