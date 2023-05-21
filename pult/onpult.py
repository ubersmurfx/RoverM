import struct
import threading
import time
from pynput import keyboard
import cval
import socket

HOST = "192.101.77.1"
PORT = 65432

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    send_data = []
except Exception as e:
    print("Error start socket")


def send_to_robot(package):
    refPackage = struct.pack("20i",
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
                             package[19])
    s.send(refPackage)


def set_value(pos, value, package):
    package[pos] = value


class Control(threading.Thread):
    control_data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def __init__(self):
        self.control_data = Control.control_data
        print(send_data)
        print("init control class")
        threading.Thread.__init__(self, daemon=True)
        self._keyboard = None

    def fromKeyboard(self):
        self._connectKeyboardHandlers()

    def _connectKeyboardHandlers(self):
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
                    # case cval.LINETRACKING:
                    #    set_value(19, 1, self.control_data)
                    # case cval.LINEUP:
                    #    set_value(20, 1, self.control_data)
                    # case cval.LINEDOWN:
                    #    set_value(21, 1, self.control_data)
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
                    # case cval.LINETRACKING:
                    #    set_value(19, 0, self.control_data)
                    # case cval.LINEUP:
                    #    set_value(20, 0, self.control_data)
                    # case cval.LINEDOWN:
                    #    set_value(21, 0, self.control_data)
            except AttributeError:
                pass

        self._keyboard = keyboard.Listener(on_press=on_press, on_release=on_release)
        self._keyboard.start()
        self._keyboard.join()

    def run(self):
        self._connectKeyboardHandlers()


class pulsar(Control):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        c = 1
        while c != 0:
            try:
                print("send")
                send_to_robot(Control.control_data)
                time.sleep(0.05)
            except:
                c = 0
                print("Closing socket")
                s.close()


pulsar = pulsar()
pulsar.start()
print("starting control")
motor = Control()
motor.fromKeyboard()
motor.start()
