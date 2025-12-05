# The license on this repository is GPL2 becasue of taipo.py . This file is BSD.

# This is the not-keyboard board to run the LCD. Based on KMK because that gives me keyboard-to-keyboard communication without any mess

import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitSide
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
from kmk.hid import HIDModes
# Mouse stuff

from kmk.extensions.rgb import RGB

from cykey import Cykey

import writer

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP10,board.GP9,board.GP8,board.GP7,board.GP6,board.GP5,)
keyboard.row_pins = (board.GP27,board.GP26,board.GP15,board.GP14,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# This is a split board but no matrix on this side
split = Split(data_pin = board.GP0, use_pio = True, split_flip = False, split_target_left = False, split_side = SplitSide.RIGHT)
keyboard.modules.append(split)

keyboard.modules.append(StickyKeys(release_after = 3000))

# The RP2040s have a neopixel-ish thing, light it up
rgb = RGB(pixel_pin = board.NEOPIXEL, num_pixels = 1, hue_default = 176, sat_default = 30, val_default = 8, val_limit = 8,)
keyboard.extensions.append(rgb)

keyboard.modules.append(Cykey(rgb))

# Flip the LED depending on the layout. This only affects the USB-connected half.
class RGBKey1(Key):
    def __init__(self, mode):
        # TODO: be less lazy and don't use 1/not-1
        self.mode = mode

    def on_press(self, keyboard, coord_int = None):
        if self.mode == 1:
            layers.activate_layer(keyboard, LAYER_NORMAL)
            rgb.set_hsv_fill(30, 200, 128)
            rgb.show()
        else:
            layers.deactivate_layer(keyboard, LAYER_NORMAL)
            rgb.set_hsv_fill(176, 200, 128)
            rgb.show()

    def on_release(self, keyboard, coord_int = None):
        pass

NORMAL_ON = RGBKey1(1)
NORMAL_OFF = RGBKey1(0)
# oh right I was going to do separate left/right layouts instead of this

keyboard.keymap = [
        [
        KC.NO, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,  KC.NO,          KC.RESET, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.NO, KC.NO, 
        KC.NO, KC.TP_TLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,          KC.TP_LOT, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, 
        KC.NO, KC.TP_BLP, KC.TP_BLR, KC.LAYER2, KC.LAYER1, KC.TP_LUT,      KC.TP_RUT, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.TP_LOT, KC.TP_LIT,                  KC.TP_RIT, KC.TP_ROT, KC.NO, KC.NO, KC.NO, KC.NO, 
        ],

# Need to do something about modifiers so they stick between the layer switch
# ctrl/alt/gui, at minimum
# also, the backspace hold thing is a bit annoying - can't hold backspace through words!

# why does ctrl++ not trigger alacritty scaling? 
# keypad +...?

                   ]

keyboard.extensions.append(writer.Writer())

# TODO: better hook

if __name__ == '__main__':
    keyboard.go(hid_type = HIDModes.NOOP)

# Slightly annoying thing: HT causes a bit of lag. Layer switch doesn't (but that's a bit different....)
# a HT-ish thing that triggers on release is maybe closer to what I want
# Oh, there's a lot going on with HT so that's a bit hard



# Data about the damn battery operation:
# Main loop is running!
# but the pending flag never goes true. Are keys getting pressed?
# What's the trigger for the split sync? Is that missing...?
# Should be able to check with more diagnostics yay
# LOL AH FUCK both keyboards think they're slaves
