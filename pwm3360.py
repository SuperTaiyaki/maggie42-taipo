# TODO: proper GPL-2.0 tag (since this is from KMK)
# Hacked up from the ADNS9800 module (hence the adns naming)
# The PWM3360 is a relative
import busio
import digitalio
import microcontroller

import time

from kmk.keys import AX, KC, Key, make_key
from kmk.modules import Module
from kmk.utils import Debug

debug = Debug(__name__)
class TrackballKey(Key):
    def __init__(self, code):
        self.code = code
        super().__init__()

for key in ('TB_LMB','TB_MMB', 'TB_RMB', 'TB_MOD', 'TB_SCROLL'):
    make_key(names=(key,), constructor = TrackballKey, code = key)

# the pimoroni trackball module does some interesting stuff with handler modes
# I want the same for this
# button to toggle between cursor and scroll
# maybe button to slow down the cursor

# HEEEEY this looks a lot like the PWM register list
# It's also a PixArt
# LOL this is probably usable
class REG:
    Product_ID = 0x0
    Revision_ID = 0x1
    MOTION = 0x2
    DELTA_X_L = 0x3
    DELTA_X_H = 0x4
    DELTA_Y_L = 0x5
    DELTA_Y_H = 0x6
    Configuration_I = 0xF
    Configuration_II = 0x10
    Observation = 0x24
    SROM_ID = 0x2A
    Power_Up_Reset = 0x3A
    Shutdown = 0x3B
    Snap_Angle = 0x42
    Motion_Burst = 0x50


class PWM3360(Module):
    tswr = tsww = 180 # not 120
    tsrw = tsrr = 20
    tsrad = 160 # not 100
    tbexit = 1 # actually 500, but we don't go that fast anyway
    baud = 2000000
    cpol = 1
    cpha = 1
    DIR_WRITE = 0x80
    DIR_READ = 0x7F

    def __init__(self, cs, sclk, miso, mosi, invert_x=False, invert_y=False):
        self.cs = digitalio.DigitalInOut(cs)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.spi = busio.SPI(clock=sclk, MOSI=mosi, MISO=miso)
        self.invert_x = invert_x
        self.invert_y = invert_y
        self.scroll_mode = False
        self.slow_mode = False
        self.mod_pressed = False
        self.scroll_pressed = False

        self.delta_x = 0
        self.delta_y = 0

    def adns_start(self):
        self.cs.value = False

    def adns_stop(self):
        self.cs.value = True

    def adns_write(self, reg, data):
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([reg | self.DIR_WRITE, data]))
        finally:
            self.spi.unlock()
            self.adns_stop()

    def adns_read(self, reg):
        result = bytearray(1)
        while not self.spi.try_lock():
            pass
        try:
            # Wait why do this every time???
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([reg & self.DIR_READ]))
            microcontroller.delay_us(self.tsrad)
            self.spi.readinto(result)
        finally:
            self.spi.unlock()
            self.adns_stop()

        return result[0]

    def delta_to_int(self, high, low):
        comp = (high << 8) | low
        if comp & 0x8000:
            return (-1) * (0xFFFF + 1 - comp)
        return comp

    def adns_read_motion(self):
        result = bytearray(6) # Don't need anything after this
        while not self.spi.try_lock():
            pass
        try:
            self.spi.configure(baudrate=self.baud, polarity=self.cpol, phase=self.cpha)
            self.adns_start()
            self.spi.write(bytes([REG.Motion_Burst & self.DIR_READ]))
            microcontroller.delay_us(self.tsrad)
            self.spi.readinto(result)
        finally:
            self.spi.unlock()
            self.adns_stop()
        microcontroller.delay_us(self.tbexit)
        self.adns_write(REG.MOTION, 0x0)
        return result

    def during_bootup(self, keyboard):

        self.adns_write(REG.Power_Up_Reset, 0x5A)
        time.sleep(0.1)
        self.adns_read(REG.MOTION)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_X_L)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_X_H)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_Y_L)
        microcontroller.delay_us(self.tsrr)
        self.adns_read(REG.DELTA_Y_H)
        microcontroller.delay_us(self.tsrw)

        self.adns_write(REG.Configuration_I, 0xA0) # DPI setting

        microcontroller.delay_us(self.tsww)

        if debug.enabled:
            debug('ADNS: Product ID ', hex(self.adns_read(REG.Product_ID)))
            microcontroller.delay_us(self.tsrr)
            debug('ADNS: Revision ID ', hex(self.adns_read(REG.Revision_ID)))
            microcontroller.delay_us(self.tsrr)
            debug('ADNS: SROM ID ', hex(self.adns_read(REG.SROM_ID)))
            microcontroller.delay_us(self.tsrr)
            if self.adns_read(REG.Observation) & 0x20:
                debug('ADNS: Sensor is running SROM')
            else:
                debug('ADNS: Error! Sensor is not running SROM!')

        return

    def before_matrix_scan(self, keyboard):
        motion = self.adns_read_motion()
        if motion[0] & 0x80:
            delta_y = self.delta_to_int(motion[3], motion[2])
            delta_x = self.delta_to_int(motion[5], motion[4])

            if self.invert_x:
                delta_x *= -1
            if self.invert_y:
                delta_y *= -1

            if self.scroll_mode or self.scroll_pressed:
                self.delta_y += delta_y
                if self.delta_y >= 300:
                    AX.W.move(keyboard, -1)
                    self.delta_y -= 300
                elif self.delta_y <= -300:
                    AX.W.move(keyboard, 1)
                    self.delta_y += 300
            else:
                if self.mod_pressed:
                    delta_x >>= 2
                    delta_y >>= 2
                self.delta_x += delta_x
                self.delta_y += delta_y
                if self.delta_x >= 0x10 or self.delta_x <= -0x10:
                    AX.X.move(keyboard, self.delta_x >> 4)
                    self.delta_x &= 0xF
                if self.delta_y >= 0x10 or self.delta_y <= -0x10:
                    AX.Y.move(keyboard, self.delta_y >> 4)
                    self.delta_y &= 0xF

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, TrackballKey):
            return key
        if key.code == 'TB_MOD':
            self.mod_pressed = is_pressed
        if key.code == 'TB_SCROLL':
            self.scroll_pressed = is_pressed

        if self.mod_pressed:
            if key.code == 'TB_LMB' and is_pressed:
                self.scroll_mode = not self.scroll_mode
            elif key.code == 'TB_RMB':
                keyboard.pre_process_key(KC.MB_MMB, is_pressed)
        else:
            if key.code == 'TB_LMB':
                keyboard.pre_process_key(KC.MB_LMB, is_pressed)
            elif key.code == 'TB_RMB':
                keyboard.pre_process_key(KC.MB_RMB, is_pressed)
            elif key.code == 'TB_MMB':
                keyboard.pre_process_key(KC.MB_MMB, is_pressed)

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

