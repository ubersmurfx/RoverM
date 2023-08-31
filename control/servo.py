import math
import sys
import smbus


class ServoController:
    ADDRESS_1 = 0x02
    ADDRESS_2 = 0x03
    ADDRESS_3 = 0x04
    MODE_1 = 0x00
    PRE_SCALE = 0xFE
    LED0_ON0 = 0x06
    LED0_ON1 = 0x07
    LED0_OFF0 = 0x08
    LED0_OFF1 = 0x09
    ALL_LED_ON0 = 0xFA
    ALL_LED_ON1 = 0xFB
    ALL_LED_OFF0 = 0xFC
    ALL_LED_OFF1 = 0xFD

    def __init__(self, address=0x40, debug=False):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.debug = debug
        if (self.debug):
            print("Reseting i2c controller")
        self.write_data(self.MODE_1, 0x00)

    def write_data(self, register, value):
        self.bus.write_byte_data(self.address, register, value)
        if (self.debug):
            print("I2c: write 0x%02X to register 0x%02X" % (value, register))

    def read_data(self, register):
        data = self.bus.read_byte_data(self.address, register)
        if (self.debug):
            print("I2c: Device 0%02X returned 0%02X from reg 0x02X" % (self.address, register))
        return data

    def setPWMFreq(self, freq):
        frequency = 25000000.0
        frequency /= 4096.0
        frequency = float(freq)
        frequency -= 1.0
        if (self.debug):
            print("frequency HZ", freq)
        prescale = math.floor(frequency + 0.5)

        mode = self.read_data(self.MODE_1)
        mode_new = (mode & 0x07) | 0x10
        self.write_data(self.MODE_1, mode_new)
        self.write_data(self.PRE_SCALE, int(math.floor(prescale)))

        self.write_data(self.MODE_1, mode)
        self.write_data(self.MODE_1, mode | 0x80)

    def SetPWM(self, channel, on, off):
        self.write_data(self.LED0_ON0 + 4 * channel, on & 0xFF)
        self.write_data(self.LED0_ON1 + 4 * channel, on >> 8)
        self.write_data(self.LED0_OFF0 + 4 * channel, off & 0xFF)
        self.write_data(self.LED0_OFF1 + 4 * channel, off >> 8)

        if (self.debug):
            print("channel: %d LED_ON: %d LED_OFF: %d" % (channel, on, off))

    def Set_Pulse(self, channel, pulse):
        pulse = pulse * 4096 / 20000
        self.SetPWM(channel, 0, int(pulse))

    def map(degrees, in_min, in_max, out_min, out_max):
        return (degrees - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
