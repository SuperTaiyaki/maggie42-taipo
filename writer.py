import busio
import board
from adafruit_bus_device.i2c_device import I2CDevice
from array import array
import time
import random

import dvorak

from kmk.keys import ModifierKey, KeyboardKey

from kmk.extensions import Extension

from wordlist import wordlist

# TODO push these into Display
BACKLIGHT_ON = 0x08
CS_ON = 0x04
RAM_ON = 0x1

class Display:
    def __init__(self):
        self.i2c = None
        self.lcd = None
        try:
            self.i2c = busio.I2C(board.GP3, board.GP2)
            self.lcd = I2CDevice(self.i2c, 0x27)
        except Exception:
            print("ERROR: Failed to initialize I2C LCD")
            pass

    def _set_4bit():
        with self.lcd:
            byte = 0x30
            for _ in range(3):
                self.lcd.write(bytearray([byte] * 2 +
                                    [byte | CS_ON] * 2))
            self.lcd.write(bytearray([0x20] * 2 +
                                [0x20 | CS_ON] * 2 +
                                [0x20 | BACKLIGHT_ON] * 2))

    def setup(self):
        self._set_4bit()
        self.write_cmd([
            0x28 | 0x4,
            0x1, # clear
            0x2, # home
            0x4 | 0x2, # moving right
            0x8 | 0x4 | 0x2, # display on, cursor on
            ])

    # This should probably be unexposed
    def write_cmd(self, chain):
        with self.lcd:
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
                self.lcd.write(bytearray(buffer))
                time.sleep(0.001)

    def write_chars(self, string):
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

        with self.lcd:
            self.lcd.write(bytearray(buffer)) # TODO: Array directly

    def setpos(self, row, column):
        # logical... right?
        base = 0
        if row == 1:
            base = 0x40
        elif row == 2:
            base = 20
        elif row == 3:
            base = 0x40 + 20

        target = base + column

        self._write_cmd([0x80 | target])

    def clear(self):
        self.write_cmd([0x1, 0x2])

    def write_row(self, row, text):
        self.setpos(row, 0)
        self.write_chars(text[:20])

# Keyboard scan codes: 0x1 = a, 0x81 is A

display = Display()

sequence = [random.choice(wordlist) for x in range(8)]
sample = " ".join(sequence[0:4])
#sample = ""

position = 0

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
        if isinstance(c, ModifierKey):
            continue
        # End of line 1 is 0x27 (39)
        # Start of line 2 is 0x40 (64)
        # When reversing, which do we want...?
        if c.code == dvorak.BACKSPACE:
            print(position)
            display.write_cmd([0x4, 0x10]) # Reverse direction, step 1
            if position == 20:
                display.write_cmd([0x80 | 19]) # this is ok, don't fucking touch
            elif position == 40:
                display.write_cmd([0x80 | 0x40 + 19])
            elif position == 60:
                display.write_cmd([0x80 | 0x27])
            elif position == 1:
                display.write_cmd([0x80 | 0x67])
            display.write_chars([" "])
            display.write_cmd([0x4 | 0x2, 0x14]) # Normal direction then one to the right
            position -= 1
        if c.code in dvorak.scancodes:
            char = dvorak.scancodes[c.code]

            if shifted and  char == '1':
                display.write_cmd([0x1, 0x2])
                position = 0
            else:
                if shifted:
                    char = char.upper()

                display.write_chars([char])
                if True or sample[position] == char:
                    #write_cmd([0x4 | 0x2, 0x14]) # Push the cursor one right
                    position += 1

                    if (position == 20):
                        display.write_cmd([0x80 | 44])
                    if (position == 40):
                        display.write_cmd([0x80 | 20])
                    if (position == 60):
                        display.write_cmd([0x80 | 84])
                    if (position == 80):
                        position = 0
                    #write_cmd([0x80 | 44])
                # Argh need to handle actual position and whatever logic somewhere

class DisplayMode:
    def receive(self, char):
        pass

class Editor(DisplayMode):
    def __init__(self):
        self.buffer = bytearray(2_048) # who knows
        self.pointer_head = 0
        self.pointer_lines = [0, 0, 0, 0]
        self.pointer_cursor_buffer = 0
        
        self.cursor_row= 0 # logical
        self.cursor_column = 0

        # Need screen cursors too, wow.
        self.lines = bytearray(80) # on-screen text data, in logical order (not screen order)

    def receive(self, char):
        self.buffer[self.pointer_cursor] = char
        self.pointer_cursor_buffer += 1
        
        self.cursor_column += 1
        if self.cursor_column > 19:
            self.cursor_column = 0
            self.cursor_row += 1

        # Updating lines is purely for the redraw
        if self.cursor_row > 3:
            self._shift_up()
        self.lines[self.cursor_row * 20 + self.cursor_row] = char
        
    def _shift_up(self):
        # move the 3 on-screen lines up
        for i in range(60):
            self.lines[i] = self.lines[i + 20]
        for i in range(60, 80):
            self.lines[i] = " "
        self.cursor_row = 0
        self.cursor_column = 2
        # Would be nice to have a better way to express this... oh well
        self.lcd.write_row(0, self.lines[0:20])
        self.lcd.write_row(1, self.lines[20:40])
        self.lcd.write_row(2, self.lines[40:60])
        self.lcd.write_row(3, self.lines[60:80])

    # So when scrolling back, pull 20 chars back and... uhh... what's most usable?
    # Existing rows not shifting around too much is best

# This entire class exists only to delay the initialization until after the initial USB
# setup is done. Might be able to use the HID hook too, instead of hooking kmk_keyboard
# directly
class Writer(Extension):
    def on_runtime_enabled(self, _):
        return
    
    def on_runtime_disable(self, keyboard):
        return

    def during_bootup(self, keyboard):
        # Do this a little later just in case it's messing with USB init (probably not)
        set_4bit()
        init()

        write_chars(sample)
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


# TODO: line break logic
# Line scroll logic!

# Argh need to design a text editor-ish interface for this. Pretty annoying....
# Single block of text with a window (pointers) is the start
# One pointer for the start of each line, since they'll probably be reused... (line advance)
# And then stricter drawing code that controls lines and line borders - overruns not permitted
# (because the screen does stupid things. What's with that layout..?)
# Adding text like this is fine, modifying the non-bottom line is... hrm.
# And pushing it back to the main array. Hrm.

# 4 lines, movement based game
# chasing a line, just running laps around the display?

# jumping between falling characters, try not to get dropped off?
# Horizontal scroll would be better for that (and easier to work with, since the LCD can do it)
