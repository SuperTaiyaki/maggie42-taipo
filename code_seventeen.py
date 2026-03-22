import board
# Taro Hayashi On The 17
# https://github.com/Taro-Hayashi/qmk_firmware/blob/tarohayashi/keyboards/tarohayashi/_archive/onthe17/keyboard.json

# REAAAALLLLY dumb idea: OSK... but with the real keyboard
# use the trackball to move the "cursor" (lit up LED)' click it to send the keystroke

# And then use the keys to jump the cursor around as an absolute pointer thing...
# It should be possible to set up a HID report like that, I guess
# Regarding the HID report: It's only 8 bits each for x and y. Should I expand that?
# I mean we can already report sixaxis and stuff.... should be interesting, let's try on another board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
# Mouse stuff
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire
from kmk.modules.rapidfire import RGB

from kmk.utils import Debug
debug = Debug(__name__)

from jackdaw import Jackdaw
from pwm3360 import PWM3360

from synchronousscanner import SynchronousScanner

import digitalio

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP29, board.GP27, board.GP23, board.GP21, board.GP14, board.GP13, board.GP12, board.GP11, board.GP10,
      board.GP9, board.GP8, board.GP7, board.GP6, board.GP5, board.GP4, board.GP2, board.GP1)
keyboard.row_pins = (board.GP25, board.GP20, board.GP3, board.GP0)
keyboard.diode_orientation = DiodeOrientation.COLUMNS
# MEMO: flip rows, not columns to minimize cycle time
keyboard.matrix = SynchronousScanner(keyboard.col_pins, keyboard.row_pins)

# 75 LEDs (ws28120) on GP15
# PWM3360 on SPI bus (CS=GP17, SCK=GP18, MISO=GP16, MOSI=GP19)
# Is the motion pin connected? Might not be

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())
keyboard.modules.append(PWM3360(cs = board.GP17, sclk = board.GP18, miso = board.GP16, mosi = board.GP19))

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

# wow there's a bunch of useless shit in the RGB module, should replace that too
# Especially wasteful on the Maggie board
# seems to be one LED per switch (64), 4 in between on the top row, 6 in between at the bottom
rgb = RGB(pixel_pin = board.GP15, num_pixels = 75, val_limit = 64)

#from taipo import Taipo
#keyboard.modules.append(Taipo())
from cykey import Cykey
keyboard.modules.append(Cykey())

keyboard.modules.append(Jackdaw(compact = True))

holdtap = HoldTap()
holdtap.tap_time = 150
keyboard.modules.append(holdtap)

keyboard.keymap = [

        # HHKB-inspired... I guess?
        # Can't have a number row because space (thumbs) ends up in an uncomfortable spot
        # As usual, want a shifted desktop flip/browser layer
        #       Probably merged with the HHKB control layer...?
        # Need F keys too, somewhere (can't merge with HHKB because up is on the top row)
[KC.TAB,     KC.Q, KC.W, KC.E, KC.R, KC.T,              KC.NO, KC.NO,      KC.Y, KC.U, KC.I, KC.O, KC.P,    KC.LBRACKET, KC.RBRACKET,         KC.NO, KC.NO,
KC.LCTL,    KC.A, KC.S, KC.D, KC.F, KC.G,               KC.NO, KC.NO,      KC.H, KC.J, KC.T, KC.L, KC.SCLN, KC.QUOT,          KC.NO,           KC.NO, KC.NO,
KC.LSFT,    KC.Z, KC.X, KC.X, KC.V, KC.B,              KC.DELETE, KC.NO,   KC.N, KC.M, KC.COMM, KC.DOT, KC.SLASH, KC.NO,      KC.NO,               KC.NO, KC.NO,
KC.LM(1, KC.LGUI),   KC.NO, KC.NO, KC.NO, KC.MO(1), KC.SPC,   KC.BSPC, KC.ENTER,   KC.SPC, KC.MO(1), KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,     KC.NO, KC.NO
 # Need to figure out the alt/GUI stuff too, bah
 # Do I need a numbers + shift key too...? or just let modifiers stack?
 ],
[
KC.ESCAPE, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,    KC.NO, KC.NO,    KC.N6, KC.N7, KC.N8, KC.N9, KC.MINUS, KC.EQUAL, KC.GRAVE,          KC.NO, KC.NO,
KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,           KC.TRNS,KC.TRNS,KC.TRNS,
KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,           KC.TRNS,KC.TRNS,KC.TRNS,
KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,KC.TRNS,           KC.TRNS,KC.TRNS,KC.TRNS
 ],

# HHKB shifted layer + browser controls
[KC.TAB,     KC.Q, KC.W, KC.E, KC.R, KC.T,   KC.NO, KC.NO,   KC.Y, KC.U, KC.I, KC.O, KC.P,    KC.UP, KC.RBRACKET,         KC.NO, KC.NO,
KC.LCTL,    KC.A, KC.S, KC.D, KC.F, KC.G,   KC.NO, KC.NO,   KC.H, KC.J, KC.HOME, KC.PGUP, KC.LEFT, KC.RIGHT,      KC.NO,     KC.NO, KC.NO,
KC.LSFT,    KC.Z, KC.X, KC.X, KC.V, KC.B,    KC.NO, KC.NO,   KC.N, KC.M, KC.END, KC.PGDN, KC.DOWN, KC.NO,   KC.NO,     KC.NO, KC.NO,
KC.LM(1, KC.LGUI),   KC.NO, KC.NO, KC.NO, KC.MO(1), KC.SPC,   KC.BSPC, KC.ENTER,   KC.SPC, KC.MO(1), KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,            KC.NO, KC.NO
 ]
# Probably need standard layer shift and GUI layer shift
# Layer shift with the entire key matrix dropped down one would work, but maybe too confusing
# And the HHKB arrow keys, and whatever else

# I could do a numpad!
# Not that I ever need one...
[
    KC.JD_1, KC.JD_4, KC.JD_C, KC.JD_W, KC.JD_N, KC.JD_X,       KC.NO, KC.NO,      KC.JD_z, KC.JD_r, KC.JD_l, KC.JD_c, KC.JD_t, KC.JD_d, KC.NO, KC.NO,
     KC.JD_3,  KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_R, KC.JD_X,     KC.NO, KC.NO,    KC.JD_z, KC.JD_n, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_e,  KC.NO, KC.NO,
    KC.LSFT, KC.LCTL, KC.LGUI, KC.LALT, KC.JD_M, KC.JD_Q,       KC.NO, KC.NO,    KC.JD_Q, KC.JD_F, KC.RALT, KC.RGUI, KC.RCTL, KC.JD_y,  KC.NO, KC.NO,
KC.TG(LAYER_JACKDAW), KC.NO, KC.NO, KC.MO(4), KC.JD_A, KC.JD_O,  KC.NO, KC.NO,      KC.JD_E, KC.JD_u, KC.MO(1), KC.NO, KC.NO, KC.NO,  KC.NO, KC.NO,
]
]

if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()


