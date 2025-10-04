import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice
from array import array
import time

import dvorak

from kmk.keys import ModifierKey, KeyboardKey

from kmk.extensions import Extension

BACKLIGHT_ON = 0x08
CS_ON = 0x04
RAM_ON = 0x1

i2c = None
lcd = None
try:
    i2c = busio.I2C(board.GP3, board.GP2)
    lcd = I2CDevice(i2c, 0x27)
except Exception:
    pass

# Keyboard scan codes: 0x1 = a, 0x81 is A

# ARGH FUCKING
# character codes are ... anyway US-layout scancodes, need to at least get the main ones un-mapped in here

def write_cmd(chain):
    with lcd:
        for char in chain:
            high = char & 0xf0 | BACKLIGHT_ON
            low = (char << 4) & 0xf0 | BACKLIGHT_ON

            buffer = ([high] * 2 +
                       [high | CS_ON] * 2 +
                       [high] * 1 +
                       [low] * 1 +
                       [low | CS_ON] * 2 +
                       [low] * 8
                      )
            lcd.write(bytearray(buffer))
            time.sleep(0.001)

def write_chars(string):
    buffer = []
    for char in string:
        high = (ord(char) & 0xf0) | BACKLIGHT_ON | RAM_ON
        low = ((ord(char) << 4) & 0xf0) | BACKLIGHT_ON | RAM_ON
        buffer += ([high] * 2 +
                   [high | CS_ON] * 2 +
                   [high] * 1 +
                   [low] * 1 +
                   [low | CS_ON] * 2 +
                   [low] * 8
                   )

    with lcd:
        lcd.write(bytearray(buffer)) # TODO: Array directly

def set_4bit():
    with lcd:
        byte = 0x30
        for _ in range(3):
            lcd.write(bytearray([byte] * 2 +
                                [byte | CS_ON] * 2))
        lcd.write(bytearray([0x20] * 2 +
                            [0x20 | CS_ON] * 2 +
                            [0x20 | BACKLIGHT_ON] * 2))

def init():
    write_cmd([
        0x28 | 0x4,
        0x1, # clear
        0x2, # home
        0x4 | 0x2, # moving right
        0x8 | 0x4 | 0x2, # display on, cursor on
        ])

position = 0
sample = "sample text goes here"

# in kmk_keyboard.c, hook this into the USB report generator
def handle_report(usb_report):
    global position
    print("Received key report: ", usb_report)

    # Need to process modifiers first
    shifted = False
    for c in usb_report:
        if isinstance(c, ModifierKey) and (c.code == 0x20 or c.code == 0x02): # should grab these from dvorak...
            shifted = True

    for c in usb_report:
        if c.code == dvorak.BACKSPACE:
            write_cmd([0x4]) # Reverse direction
            write_chars([" ", " "])
            write_cmd([0x4 | 0x2, 0x14]) # Normal direction then one to the right
            position -= 1
        if c.code in dvorak.scancodes:
            char = dvorak.scancodes[c.code]
            if shifted:
                char = char.upper()

            write_chars([char])

            if True or sample[position] == char:
                #write_cmd([0x4 | 0x2, 0x14]) # Push the cursor one right
                position += 1

                if (position == 20):
                    write_cmd([0x80 | 44])
                if (position == 40):
                    write_cmd([0x80 | 20])
                if (position == 60):
                    write_cmd([0x80 | 84])
                if (position == 80):
                    position = 0
                #write_cmd([0x80 | 44])
            # Argh need to handle actual position and whatever logic somewhere

class Writer(Extension):
    def on_runtime_enabled(self, _):
        return
    
    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        set_4bit()
        init()

        #write_chars(sample)
        write_cmd([0x80 | 84]) # There's some sort of offset...?
        write_chars("MW 4/10")
        write_cmd([0x80 | 0]) # Could just jump home, but anyway


    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return



# Is this fucking with the power-on? Delay it to later...?
#set_4bit()
#init()

