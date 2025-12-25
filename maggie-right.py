import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
#from kmk.modules.split import Split, SplitSide
from thicksplit import ThickSplit, SplitSide
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
# Mouse stuff
from kmk.modules.rapidfire import RapidFire

from kmk.extensions.rgb import RGB

from synchronousscanner import SynchronousScanner

from kmk.utils import Debug
debug = Debug(__name__)

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP10,board.GP9,board.GP8,board.GP7,board.GP6,board.GP5,)
keyboard.row_pins = (board.GP27,board.GP26,board.GP15,board.GP14,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.matrix = SynchronousScanner(keyboard.col_pins, keyboard.row_pins)

split = ThickSplit(data_pin = board.GP0, use_pio = False, split_flip = False)
keyboard.modules.append(split)

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(RapidFire())

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

# The RP2040s have a neopixel-ish thing, light it up
rgb = RGB(pixel_pin = board.NEOPIXEL, num_pixels = 1, hue_default = 176, sat_default = 30, val_default = 128, val_limit = 128,)
keyboard.extensions.append(rgb)

#from cykey import Cykey
#keyboard.modules.append(Cykey(rgb))

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

keyboard.keymap = [
        # Normal layer
       [
KC.ESCAPE,   KC.Q,KC.W,KC.E,KC.R,KC.T,         KC.Y, KC.U, KC.UP, KC.O, KC.P, KC.BACKSPACE,
       KC.LCTRL, KC.A, KC.S, KC.D, KC.F, KC.G,     KC.H, KC.LEFT, KC.DOWN, KC.RIGHT, KC.SEMICOLON, KC.QUOTE,
       KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V, KC.B,        KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLASH, KC.RSHIFT,
       KC.NO, KC.NO, KC.NO, KC.LT(LAYER_BROWSER, KC.ESCAPE), KC.LT(LAYER_RAISED, KC.BSPACE), KC.SPACE,       KC.ENTER, KC.LT(LAYER_LOWERED, KC.SPACE), KC.HT(KC.ESCAPE, KC.LGUI), KC.NO, KC.NO, KC.NO
       ],
       # That top right backspace is maybe unnecessary
       

    # Browser layer
    # empty spaces can be used for non-browser convenience stuff
    # mixing this with UI layer might be nice
    [
        KC.RELOAD, KC.LGUI(KC.N1), KC.LGUI(KC.N2), KC.LGUI(KC.N3), KC.LGUI(KC.N4), KC.LGUI(KC.N5),  KC.LGUI(KC.N6), KC.LGUI(KC.N7), KC.LGUI(KC.N8), KC.LGUI(KC.N9), KC.LGUI(KC.N0), KC.NO, 
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
                   ]

if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()

# Slightly annoying thing: HT causes a bit of lag. Layer switch doesn't (but that's a bit different....)
# a HT-ish thing that triggers on release is maybe closer to what I want
# Oh, there's a lot going on with HT so that's a bit hard

