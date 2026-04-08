# The license on this repository is GPL2 becasue of taipo.py . This file is BSD.

import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from thicksplit import ThickSplit, SplitSide
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
# Mouse stuff
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire

# Not using KMK RGB because it does a bunch of useless stuff (and wastes my memory)
from neopixel import NeoPixel

from kmk.utils import Debug
debug = Debug(__name__)

from jackdaw import Jackdaw

from synchronousscanner import SynchronousScanner

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP10,board.GP9,board.GP8,board.GP7,board.GP6,board.GP5,)
keyboard.row_pins = (board.GP27,board.GP26,board.GP15,board.GP14,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.matrix = SynchronousScanner(keyboard.col_pins, keyboard.row_pins)

split = ThickSplit(data_pin = board.GP0, use_pio = False, split_flip = False)
keyboard.modules.append(split)

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

# The RP2040s have a neopixel-ish thing, light it up
rgb = NeoPixel(board.NEOPIXEL, 1, brightness = 0.5, auto_write = False)

keyboard.modules.append(Jackdaw(rgb = rgb))
from cykey import Cykey
keyboard.modules.append(Cykey())

LAYER_NORMAL = 2
LAYER_BROWSER = 3
LAYER_RAISED = 4
LAYER_LOWERED = 5
LAYER_GAME = 6
LAYER_JACKDAW = 7
LAYER_GEMINI = 8

holdtap = HoldTap()
holdtap.tap_time = 150
keyboard.modules.append(holdtap)

MWUP = KC.RF(KC.MW_UP, interval = 800, timeout = 20)
MWDOWN = KC.RF(KC.MW_DOWN, interval = 800, timeout = 20)

keyboard.keymap = [
# Jackdaw
[
       KC.JD_1, KC.JD_4, KC.JD_C, KC.JD_W, KC.JD_N, KC.JD_X,       KC.JD_z, KC.JD_r, KC.JD_l, KC.JD_c, KC.JD_t, KC.JD_d, # y/TE
   KC.JD_3,  KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_R, KC.NO,       KC.NO, KC.JD_n, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_e, 
KC.LSFT, KC.LCTL, KC.LGUI, KC.LALT, KC.JD_M, KC.JD_Q,      KC.JD_Q, KC.JD_F, KC.RALT, KC.RGUI, KC.RCTL, KC.JD_y, 
KC.TG(LAYER_JACKDAW), KC.NO, KC.NO, KC.MO(4), KC.JD_A, KC.JD_O,        KC.JD_E, KC.JD_u, KC.MO(1), KC.NO, KC.NO, KC.NO, 
    ],

    # Browser layer
    # empty spaces can be used for non-browser convenience stuff
    # mixing this with UI layer might be nice
    [
        KC.RELOAD, KC.LGUI(KC.N1), KC.LGUI(KC.N2), KC.LGUI(KC.N3), KC.LGUI(KC.N4), KC.LGUI(KC.N5),  KC.LGUI(KC.N6), KC.LGUI(KC.N7), KC.LGUI(KC.N8), KC.LGUI(KC.N9), KC.LGUI(KC.N0), KC.TG(5), 
        KC.TRNS, KC.LCTRL(KC.LSFT(KC.TAB)), KC.LCTRL(KC.K) , KC.LCTRL(KC.TAB), KC.NO, KC.NO,     KC.NO, KC.NO, KC.NO, KC.LGUI(KC.P), KC.NO, KC.NO, 
        KC.RESET, KC.LCTRL(KC.P), KC.LCTRL(KC.COMMA) , KC.LGUI(KC.C), KC.LGUI(KC.V), KC.NO,      KC.NO, KC.LGUI(KC.J), KC.NO, KC.NO, KC.NO, KC.NO, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,       KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, 
        ],
    
    # Raised layer
    [
        KC.NO, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),  KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.LSFT(KC.N0), KC.LBRACKET, 
        KC.TRNS, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,          KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.RBRACKET, 
        # Grave is on the right because that's the HHKB layout
        # Pipe should probably be somewhere so it's not hiding under the backspace + shift
        # Splitting backtick and tilde like this is liable to break my brain
        KC.TRNS, KC.LSHIFT(KC.GRAVE), KC.NO, KC.LSHIFT(KC.MINUS), KC.MINUS, KC.NO,      KC.NO, KC.EQUAL, KC.LSHIFT(KC.EQUAL), KC.NO, KC.GRAVE, KC.TRNS, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,       KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, 
        ],
        # outside the brackets, angle brackets

    
    # Lowered layer
    # HHKB-based
    [
        KC.NO, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),    KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.INSERT, KC.DELETE, 
        KC.TRNS, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,          KC.HOME, KC.PGUP, KC.N8, KC.UP, KC.GRAVE, KC.BSLASH, 
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.END, KC.NO,       KC.END, KC.PGDN, KC.LEFT, KC.DOWN, KC.RIGHT, KC.TRNS, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,       KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, 
        ],


# Need to do something about modifiers so they stick between the layer switch
# ctrl/alt/gui, at minimum
# also, the backspace hold thing is a bit annoying - can't hold backspace through words!

# why does ctrl++ not trigger alacritty scaling? 
# Extra layer: Gaming layout
# arrow keys, z, x, and the like hanging out nearby
    [
        KC.NO, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),    KC.TG(LAYER_GAME), KC.NO, KC.UP, KC.NO, KC.INSERT, KC.DELETE, 
        KC.TRNS, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,          KC.NO, KC.LEFT, KC.DOWN, KC.RIGHT, KC.GRAVE, KC.BSLASH, 
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.END, KC.NO,       KC.END, KC.PGDN, KC.LEFT, KC.I, KC.B, KC.SLASH, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,       KC.SLASH, KC.B, KC.I, KC.NO, KC.NO, KC.NO, 
    ],

# Maybe lower middle fingers should be shifts, that get applied to the far side...?
# Numbers, symbols, etc. Same style as Cykey

    [

KC.TRNS, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.NO,    KC.NO, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.TG(5),
KC.TRNS, KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,    KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.TRNS,
KC.TRNS, KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,    KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.TRNS,

        KC.NO, KC.NO, KC.NO, KC.NO, KC.TP_LIT, KC.TP_LOT,       KC.TP_ROT, KC.TP_RIT, KC.NO, KC.NO, KC.NO, KC.NO, 
    ],


                   ]

if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()

# Slightly annoying thing: HT causes a bit of lag. Layer switch doesn't (but that's a bit different....)
# a HT-ish thing that triggers on release is maybe closer to what I want
# Oh, there's a lot going on with HT so that's a bit hard


# Ok, how to make this keyboard more useful generally?
# full QWERTY layout is pretty much impossible
# double cykey maybe gets close...
# Add more supporting stuff around jackdaw so I can operate it like a normal keyboard?
# What's the actual problem, anyway?
# Mostly that if I want to type normally it's kind of annoying

