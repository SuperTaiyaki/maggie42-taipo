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

    def _set_4bit(self):
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
            c = ord(char) if isinstance(char, str) else char
            high = (c & 0xf0) | BACKLIGHT_ON | RAM_ON
            low = ((c << 4) & 0xf0) | BACKLIGHT_ON | RAM_ON
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

        self.write_cmd([0x80 | target])

    def clear(self):
        self.write_cmd([0x1, 0x2])

    def write_row(self, row, text):
        self.setpos(row, 0)
        self.write_chars(text[:20])

    def backspace(self):
        display.write_cmd([0x4, 0x10]) # Reverse direction, step 1
        display.write_chars([" "])
        display.write_cmd([0x4 | 0x2, 0x14]) # Normal direction then one to the right

class DisplayMode:
    def receive(self, char):
        pass

    def backspace(self):
        pass

    def setup(self):
        display.clear()

# Probably need an intermediate class that flattens out the display memory
class Editor(DisplayMode):
    def __init__(self):
        self.buffer = bytearray([ord(' ')] * 2_048) # who knows
        self.pointer_head = 0
        self.pointer_lines = [0, 0, 0, 0]
        self.pointer_cursor_buffer = 0
        
        self.cursor_row = 0 # logical
        self.cursor_column = 0

        self.lines = bytearray([ord(' ')] * 80) # on-screen text data, in logical order (not screen order)
        self.current_word = bytearray(20)
        self.current_word_length = 0

    def reformat(self):
        pointer = self.pointer_head

        next_word = bytearray(20)
        for line in range(0, 3):
            line_pointer = 0

            word_chars = 0
            while buffer[pointer] != ' ':
                next_word[word_chars] = buffer[pointer]
                pointer += 1
                word_chars += 1

            if word_chars + line_pointer + 1 < 20:
                self.lines[line][line_pointer] = ' '
                line_pointer += 1
                for i in range(word_chars):
                    self.lines[line][line_pointer] = next_word[i]
            # ARGH the else case flows into the next line


    def receive(self, char):
        self.buffer[self.pointer_cursor_buffer] = ord(char)
        self.pointer_cursor_buffer += 1

        self.lines[self.cursor_row * 20 + self.cursor_column] = ord(char)
        display.write_chars([char])

        self.cursor_column += 1
        if self.cursor_column > 19:
            self.cursor_column = 0
            self.cursor_row += 1

            # Updating lines is purely for the redraw
            if self.cursor_row > 3:
                self._shift_up()

            display.setpos(self.cursor_row, self.cursor_column)

    def backspace(self):
        print("Column: ", self.cursor_column)
        if self.cursor_column > 0:
            display.backspace()
            self.cursor_column -= 1
        else:
            if self.cursor_row == 0:
                # The user can't see what they're deleting, block it (the logic is too hard here)
                return
            # jump -> write jump seems cleanest
            self.cursor_column = 19
            self.cursor_row -= 1
            display.setpos(self.cursor_row, self.cursor_column)
            display.write_chars([" "])
            display.setpos(self.cursor_row, self.cursor_column)

    def _next_line(self, partial_word = None):
        self.cursor_column = 0
        self.cursor_row += 1
        if self.cursor_row == 4:
            self._shift_up()
            self.cursor_row = 3

        display.jump(self.cursor_row, 0)
        if partial_word:
            # Write it out to the screen and the line buffer (but not the text buffer)
            pass
        
    def _shift_up(self):
        # move the 3 on-screen lines up
        for i in range(60):
            self.lines[i] = self.lines[i + 20]
        for i in range(60, 80):
            self.lines[i] = ord(' ')
        # Would be nice to have a better way to express this... oh well
        display.write_row(0, self.lines[0:20])
        display.write_row(1, self.lines[20:40])
        display.write_row(2, self.lines[40:60])
        display.write_row(3, self.lines[60:80])

        self.cursor_row = 3
        self.cursor_column = 0

# On tab key, call this to break across lines
# TODO: paragraph breaks, manual line breaks, whatever
# ALSO: this leaves the last line empty to continue typing, is that ok?
# ARGH. Ideally we want to backfill this, so it ... uhh... 
# Was going to be, finishes in the right place, but maybe use scroll up/down for that
# up/down should forcefully reformat, I guess
# Also what to do about line alignment, kind of difficult.
    def _reformat(self):
        # Roughly equivalent to fill_lines...
        offset = self.pointer_head
        word = [' '] * 20
        word_index = 0

        line = 0
        line_index = 0
        overflow = False

        while line < 3:
            if offset > 2047:
                break
            if self.buffer[offset] == ord(' '):
                for i in range(word_index):
                    self.lines[line * 20 + line_index] = word[i]
                    line_index += 1
                word_index = 0
                offset += 1

                # TODO: overflow? If this is at 20, don't need it
                self.lines[line * 20 + line_index] = ord(' ')

                overflow = False

                line_index += 1
            else:
                word[word_index] = self.buffer[offset]
                offset += 1
                word_index += 1
                if word_index > 20:
                    # Give up - dump it out to the screen and just keep writing until the next space
                    overflow = True
                if word_index + line_index > 18:
                    for x in range(line_index, 19):
                        self.lines[line * 20 + x] = ord(' ')

                    self.line_lengths[line] = line_index
                    line += 1
                    line_index = 0
                    if line == 4:
                        pass # TODO something



class Trainer(DisplayMode):
    def __init__(self):
        self.pointer_head = 0
        self.pointer_lines = [0, 0, 0, 0]
        self.pointer_cursor_buffer = 0
        
        self.cursor_row = 0 # logical
        self.cursor_column = 0

        self.lines = bytearray([ord(' ')] * 80) # on-screen text data, in logical order (not screen order)
        self.current_word = bytearray(20)
        self.current_word_length = 0

        self.line_lengths = [0] * 4

        self.errors = 5

    def setup(self):
        self.buffer = bytearray([ord(x) for x in " ".join(random.choice(wordlist) for x in range(100))])
        self._fill_lines(0)

    def receive(self, char):
        if self.buffer[self.pointer_head] == ord(char):
            self.pointer_head += 1
            # Kick one right
            self.cursor_column += 1

            if self.cursor_column == self.line_lengths[self.cursor_row]:
                self.cursor_row += 1
                self.cursor_column = 0
                display.setpos(self.cursor_row, self.cursor_column)

                if self.cursor_row == 3:
                    self._fill_lines(self.pointer_head)
                    self.cursor_row = 0
                    self.cursor_column = 0

            else:
                display.write_cmd([0x4 | 0x2, 0x14]) # Normal direction then one to the right

        else:
            self.errors -= 1
            self.lines[60 + self.errors * 2 + 1] = 20
            display.setpos(3, self.errors * 2)
            display.write_chars("  ")
            display.setpos(self.cursor_row, self.cursor_column)

    def _fill_lines(self, offset):
        word = [' '] * 20
        word_index = 0

        line = 0
        line_index = 0

        while line < 3:
            if offset > 2047:
                break
            if self.buffer[offset] == ord(' '):
                for i in range(word_index):
                    self.lines[line * 20 + line_index] = word[i]
                    line_index += 1
                word_index = 0
                offset += 1

                # TODO: overflow? If this is at 20, don't need it
                self.lines[line * 20 + line_index] = ord(' ')
                line_index += 1
            else:
                word[word_index] = self.buffer[offset]
                offset += 1
                word_index += 1
                if word_index > 20:
                    print(word)
                if word_index + line_index > 18:
                    for x in range(line_index, 19):
                        self.lines[line * 20 + x] = ord(' ')
                    # self.lines[line * 20 + line_index] = ord(' ')

                    self.line_lengths[line] = line_index
                    line += 1
                    line_index = 0

        for x in range(0, self.errors * 2, 2):
            self.lines[60 + x] = 20
            self.lines[60 + x + 1] = 0b11110111

        display.write_row(0, self.lines[0:20])
        display.write_row(1, self.lines[20:40])
        display.write_row(2, self.lines[40:60])
        display.write_row(3, self.lines[60:80])



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

        display.setup()
        display.write_cmd([0x80 | 84]) # There's some sort of offset...?
        display.write_chars("MW 4/10")
        display.write_cmd([0x80 | 0]) # Could just jump home, but anyway

        mode.setup()


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

class Menu(DisplayMode):
    def __init__(self):
        pass

    def setup(self):
        display.setpos(0, 0)
        display.write_chars("a. Writer")
        display.setpos(1, 0)
        display.write_chars("s. Practice")


    def receive(self, char):
        global mode
        if char == 'a':
            mode = Editor()
            mode.setup()
        elif char == 's':
            mode = Trainer()
            mode.setup()


display = Display()
mode = Menu()

sequence = [random.choice(wordlist) for x in range(8)]
sample = " ".join(sequence[0:4])
#sample = ""

position = 0

# in kmk_keyboard.c, hook this into the USB report generator
def handle_report(usb_report):
    global position
    # print("Received key report: ", usb_report)
    # NEXT: Change to a Writer instance

    # Need to process modifiers first
    shifted = False
    for c in usb_report:
        if isinstance(c, ModifierKey) and (c.code == 0x20 or c.code == 0x02): # should grab these from dvorak...
            shifted = True

    for c in usb_report:
        if isinstance(c, ModifierKey):
            continue
        if c.code == dvorak.BACKSPACE:
            mode.backspace()
        if c.code in dvorak.scancodes:
            char = dvorak.scancodes[c.code]
            if shifted:
                char = char.upper()

            mode.receive(char)

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
