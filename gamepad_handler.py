import machine
from machine import Pin, SoftI2C
from setting import *
from utility import *
from micropython import const
import time
import gamepad

MODE_DPAD = const(1)
MODE_LEFT_JOYSTICK = const(2)
MODE_RIGHT_JOYSTICK = const(3)
MODE_BOTH_JOYSTICK = const(4)


class GamepadHandler:

    def __init__(self, port):

        self.port = port
        # Grove port: GND VCC SCL SDA
        scl_pin = Pin(PORTS_DIGITAL[port][0])
        sda_pin = Pin(PORTS_DIGITAL[port][1])

        try:
            self.i2c_gp = SoftI2C(scl=scl_pin, sda=sda_pin, freq=100000)

            self.gamepad = gamepad.GamePadReceiver(self.i2c_gp)

            self.gamepad._verbose = False
            self.filter_btn_data = self.gamepad.data

        except:
            self.gamepad = None
            self.port = None
            say('Gamepad Receiver not found')

    def is_connected(self):
        return self.gamepad._isconnected

    def set_led_color(self, color):
        if self.gamepad != None:
            self.colorVal = color
            self.gamepad.set_led_color(hex_to_rgb(self.colorVal))

    def set_rumble(self, force, duration):
        if self.gamepad != None:
            new_force = translate(force, 0, 100, 0, 255)
            new_duration = translate(duration, 0, 2000, 0, 255)
            self.gamepad.set_rumble(new_force, new_duration)

    def filter_btn(self, data=None):
        self.filter_btn_data[data] = (self.filter_btn_data[data] if isinstance(
            self.filter_btn_data[data], (int, float)) else 0) + 1

        if self.filter_btn_data[data] > 1:
            self.filter_btn_data[data] = 0
            #print(data, 'is filtered')
            return False
        return True


    def process(self):
        if self.gamepad != None:
            self.gamepad.update()

