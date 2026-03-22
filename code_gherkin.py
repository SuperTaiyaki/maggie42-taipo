import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
# Mouse stuff
#from kmk.modules.mouse_keys import MouseKeys
#from kmk.modules.rapidfire import RapidFire

from kmk.utils import Debug
debug = Debug(__name__)

from jackdaw import Jackdaw

from synchronousscanner import SynchronousScanner

import digitalio
led= digitalio.DigitalInOut(board.LED)
led.switch_to_output()
led.value = 1

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7)
keyboard.row_pins = (board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP16)
keyboard.diode_orientation = DiodeOrientation.COLUMNS
keyboard.matrix = SynchronousScanner(keyboard.col_pins, keyboard.row_pins)

keyboard.modules.append(StickyKeys(release_after = 3000))

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

from cykey import Cykey
keyboard.modules.append(Cykey())

keyboard.modules.append(Jackdaw(compact = True))

holdtap = HoldTap()
holdtap.tap_time = 150
keyboard.modules.append(holdtap)

keyboard.keymap = [
# Jackdaw
[
KC.JD_4, KC.JD_C, KC.JD_W, KC.JD_N,      KC.JD_X,    KC.JD_r, KC.JD_l, KC.JD_c, KC.JD_t, KC.JD_d,
KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_R,      KC.JD_z,    KC.JD_n, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_e, 
KC.JD_3, KC.LGUI, KC.LALT, KC.JD_Q,     KC.JD_M,    KC.JD_Q,  KC.JD_u, KC.TG(4), KC.TG(3), KC.JD_y,
KC.NO,                  KC.JD_A, KC.JD_O, KC.JD_E, KC.JD_u,    KC.JD_F# thumb row
],
# Terrible hack, center key to flip to taipo since symbols and stuff work

# Taipo (unused)
[
KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,  KC.NO,          KC.TG(3), KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_BRP,
KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,         KC.NO, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR,
KC.TP_BLP, KC.TP_BLR, KC.LAYER2, KC.TP_LIT, KC.TP_LOT,      KC.TP_LIT, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR,
KC.NO , KC.TP_LIT, KC.TP_LOT, KC.JD_E, KC.JD_u, KC.JD_C # thumb row
],

# Cykey
[
KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,     KC.NO,          KC.TG(3), KC.TP_TRI, KC.TP_TRM, KC.TP_TRR,       KC.TP_BRP,
KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI,     KC.NO,         KC.NO, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.     TP_BRR,
KC.TP_BLP, KC.TP_BLR, KC.LAYER2, KC.TP_LIT,     KC.TP_LOT,      KC.TP_LIT, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM,     KC.TP_BRR,
KC.NO , KC.TP_LIT, KC.TP_LIT, KC.TP_LOT, KC.TP_LOT, KC.JD_C # thumb row
],


# Something resembling a normal layout. This will require tuning!
    [
        KC.Q,    KC.W,    KC.E,    KC.R,   KC.T,     KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.A,    KC.S,    KC.D,    KC.F,   KC.G,     KC.H,    KC.J,    KC.K,    KC.L,    KC.SCLN,
KC.HT(KC.Z, KC.LSFT),    KC.X,    KC.C,    KC.V,   KC.B,     KC.N,    KC.M,    KC.COMMA,    KC.DOT,    KC.SLASH,
KC.NO,      KC.MO(5), KC.SPACE, KC.SPACE, KC.ENTER, KC.LT(6, KC.BSPACE),
    ],

[
  KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4),   KC.LSFT(KC.N5),  KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.LSFT(KC.N0),
        KC.N1,    KC.N2,    KC.N3,    KC.N4,   KC.N5,     KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,
        # Drop symbols into the next row
KC.LSFT,    KC.GRAVE,    KC.QUOTE,    KC.MINUS,        KC.B,         KC.EQUAL,    KC.LBRC,    KC.RBRC,    KC.EQUAL,    KC.BSLASH,
KC.NO,      KC.NO, KC.SPACE, KC.LCTRL, KC.ENTER, KC.LGUI
    ],
# Layer 6: browser layer and layer switches
[
  KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4),   KC.LSFT(KC.N5),  KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.TO(0),
        KC.N1,    KC.N2,    KC.N3,    KC.N4,   KC.N5,     KC.N6,    KC.N7,    KC.N8,    KC.N9,    KC.N0,
        # Drop symbols into the next row
KC.LSFT,    KC.GRAVE,    KC.QUOTE,    KC.MINUS,        KC.B,         KC.EQUAL,    KC.LBRC,    KC.RBRC,    KC.EQUAL,    KC.BSLASH,
KC.NO,      KC.NO, KC.SPACE, KC.LCTRL, KC.ENTER, KC.LGUI
    ],
]
# Oops can't ctrl-C

# bottom leftmost -> layer shift

# Combo design:
# SPACER + something -> enter
# Shift.... semicolon (shift) and z hold? (maybe not Z, put the right hand side elsewhere)
# Based on kkga's layout (https://keymapdb.com/keymaps/kkga/)
# W + S -> escape
# s + x -> tab?

#combos = [
#        Chord((KC.W, KC.S), KC.ESCAPE),
#        Chord((KC.S, KC.X), KC.TAB),
#        ]
        


# How to build a sane layout onto this...
# top left are punctuation anyway, so
# a+' -> escape?
# o + , -> ?
# e + # -> ?
# a + ; -> ?
# shift... on space?
# enter -> double right thumb
# outer right thumb -> fn
# outer left thumb -> also fn?
# ; hold -> ctrl
# q hold -> cmd? bit weird, maybe
# Don't want to cause too much confusion with my ergodash, may need to merge the layouts later
# and probably don't even try to merge the maggie, leave it for crazier stuff
# Would be nice if the layer setup merged with cykey so I can choose my key layer and then drop stuff on top

# What would I ever need a normal layout for, on a chorded/jackdaw/whatever keyboard?
# WM controls
# browser controls? (99% browser + cykey though)
# super minor console stuff (tab, vim, a bit more)
# .... throw all that stuff on the Handyman, and use the gherkin and maggie purely for typing?

if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()

