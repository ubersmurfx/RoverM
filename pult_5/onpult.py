import struct
import sys
import threading
from time import sleep
import socket
import cval

try:
    import numpy as np
except ImportError:
    print("NumpPy module is not installed. Use the command 'pip install numpy' in the terminal")

try:
    from pynput import keyboard
except ImportError:
    print("Pynput module is not installed. Use the command 'pip install pynput' in the terminal")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((cval.HOST, cval.PORT))
    send_data = []
except Exception as e:
    print(sys.exc_info(), "\t", e)


def send_to_robot(package):
    package = np.clip(package, 0, 1).astype(np.uint8)
    payload = struct.pack(cval.dataType,
        package[0], package[1], package[2], package[3], package[4],
            package[5], package[6], package[7], package[8], package[9],
            package[10],package[11],package[12],package[13],package[14],
            package[15],package[16],package[17],package[18],package[19],
            package[20],package[21],package[22],package[23],package[24],
            package[25])
    s.send(payload)
def set_value(pos, value, payload):
    payload[pos] = value

class Control(threading.Thread):
    payload = [0, 0, 0, 0, 0,
               0, 0, 0, 0, 0,
               0, 0, 0, 0, 0,
               0, 0, 0, 0, 0,
               0, 0, 0, 0, 0,
               0]
    ''' 25: первый бит отвечает за направление отправки данных, последний отвечает за побитовую сумму '''

    parityBit = 0
    # parityBit (бит честности) отвечает за целостность данных

    reverseBit = 1
    # reverseBit (бит направления отпрвки данных) отвечаюет за отправку данных на сервер
    payload[0] = reverseBit

    def __init__(self):
        self.payload = Control.payload
        self.parityBit = Control.parityBit
        self.reverseBit = Control.reverseBit
        print("init control class")
        threading.Thread.__init__(self, daemon=True)
        self._keyboard = None

    def from_keyboard(self):
        self.connect_keyboard_handlers()

    def connect_keyboard_handlers(self):
        def on_press(key):
            try:
                if key.char in cval.keyboard:
                    set_value(cval.keyboard[key.char], 1, self.payload)
                else:
                    pass
            except AttributeError:
                pass
        def on_release(key):
            try:
                if key.char in cval.keyboard:
                    set_value(cval.keyboard[key.char], 0, self.payload)
                else:
                    pass
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

                Control.parityBit = (np.sum(Control.payload) - Control.payload[25]) % 2
                Control.payload[25] = Control.parityBit

                print(Control.payload)
                send_to_robot(Control.payload)

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
    connection = Control()
    connection.from_keyboard()
    connection.start()
except Exception:
    print(sys.exc_info())
