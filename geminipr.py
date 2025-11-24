# KMK has a built in steno module! But in this version of kmk it's not working...
try:
    from typing import Optional, Tuple, Union
except ImportError:
    pass
from micropython import const

import kmk.handlers.stock as handlers
from kmk.keys import Key, KC, make_key
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules import Module
from kmk.utils import Debug
from supervisor import ticks_ms

import usb_cdc

# Protocol documented at https://docs.qmk.fm/features/stenography
keycodes = [
'Fn',
'N1',
'N2',
'N3',
'N4',
'N5',
'N6',

'S1',
'S2',
'LT',
'LK',
'LP',
'LW',
'LH',

'LR',
'LA',
'LO',
'ST1',
'ST2',
'RES1',
'RES2',

'PWR',
'ST3',
'ST4',
'RE',
'RU',
'RF',
'RR',

'RP',
'RB',
'RL',
'RG',
'RT',
'RS',
'RD',

'N7',
'N8',
'N9',
'A',
'B',
'C',
'RZ',
]

class GeminiKey(Key):
    def __init__(self, code):
        self.code = code
        super().__init__()

for key in keycodes:
    make_key(names = ("G_" + key,), constructor = GeminiKey, code = key)


class Gemini(Module):
    def __init__(self):
        self.reset()

    def reset(self):
        self.chord = set()

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, GeminiKey):
            return key

        code = key.code

        if is_pressed:
            self.chord.add(code)
        else:
            # keys_pressed is the USB report; coordkeys is real keys (kmk internal)
            if len(keyboard._coordkeys_pressed) == 0:
                self.send_packet()
                self.reset()

    def create_byte(self, idx, initial = 0):
        byte = initial
        for i in range(7):
            if keycodes[idx * 7 + i] in self.chord:
                byte |= (1 << (6 - i)) 

        return byte

    def send_packet(self):
        if len(self.chord) == 0:
            return
        b = bytearray([self.create_byte(0, 0b1000_0000)] + [self.create_byte(i, 0) for i in range(1, 6)])
        print("Byte: ", b)
        usb_cdc.data.write(b)
        usb_cdc.data.flush()

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass


