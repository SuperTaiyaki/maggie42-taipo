# The license on this repository is GPL2 becasue of taipo.py . This file is BSD.

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
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire

from kmk.extensions.rgb import RGB

from kmk.utils import Debug
debug = Debug(__name__)

from jackdaw import Jackdaw
from geminipr import Gemini

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP10,board.GP9,board.GP8,board.GP7,board.GP6,board.GP5,)
keyboard.row_pins = (board.GP27,board.GP26,board.GP15,board.GP14,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

split = ThickSplit(data_pin = board.GP0, use_pio = False, split_flip = False)
keyboard.modules.append(split)

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

# The RP2040s have a neopixel-ish thing, light it up
rgb = RGB(pixel_pin = board.NEOPIXEL, num_pixels = 1, hue_default = 176, sat_default = 30, val_default = 128, val_limit = 128,)
keyboard.extensions.append(rgb)

from cykey import Cykey
keyboard.modules.append(Cykey(rgb))

#from taipo import Taipo
#keyboard.modules.append(Taipo())

keyboard.modules.append(Jackdaw())
keyboard.modules.append(Gemini())



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

MWUP = KC.RF(KC.MW_UP, interval = 800, timeout = 20)
MWDOWN = KC.RF(KC.MW_DOWN, interval = 800, timeout = 20)

keyboard.keymap = [
# Jackdaw
[
       KC.BSPACE, KC.JD_4, KC.JD_C, KC.JD_W, KC.JD_N, KC.JD_X,       KC.JD_z, KC.JD_r, KC.JD_l, KC.JD_c, KC.JD_t, KC.JD_dE, # y/TE
   KC.JD_SHIFT,  KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_R, KC.JD_UO,       KC.JD_F, KC.JD_n, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_e, 
KC.NO, KC.JD_xQUOTE, KC.JD_xCOMMA, KC.JD_xDOT, KC.JD_UO, KC.JD_UO,      KC.JD_UO, KC.JD_UO, KC.NO, KC.E, KC.JD_SHIFT, KC.JD_y, 
KC.TG(LAYER_JACKDAW), KC.NO, KC.NO, KC.MO(4), KC.JD_A, KC.JD_O,        KC.JD_E, KC.JD_u, KC.MO(1), KC.NO, KC.NO, KC.NO, 
    ],

# Taipo
        [
        KC.TG(1), KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,  MWUP,          KC.TG(LAYER_GAME), KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.TG(1), 
        KC.NO, KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, MWDOWN,         KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.TG(LAYER_GEMINI), 
        KC.NO, KC.TP_BLP, KC.TP_BLR, KC.LAYER2, KC.TP_LIT, KC.TP_LOT,      KC.TP_ROT, KC.TP_RIT, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, 
        KC.NO, KC.NO, KC.NO, KC.SK(KC.MO(LAYER_BROWSER)), KC.TP_LIT, KC.TP_LOT,       KC.TP_RIT, KC.TP_ROT, KC.MO(1), KC.NO, KC.NO, KC.NO, 
        ],

# Most everything after this is unused

# TP but Cykey
#       [
#       KC.NO, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,  MWUP,          KC.TG(LAYER_GAME), KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_BRP, KC.TG(LAYER_JACKDAW), 
#       KC.NO, KC.TP_TLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, MWDOWN,         KC.NO, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TG(LAYER_GEMINI), 
#       KC.NO, KC.TP_BLP, KC.TP_BLR, KC.LAYER2, KC.LAYER1, KC.TP_LUT,      KC.NO, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, 
#       KC.NO, KC.NO, KC.NO, KC.SK(KC.MO(LAYER_BROWSER)), KC.TP_LOT, KC.TP_LIT,       KC.TP_RIT, KC.TP_ROT, KC.MO(1), KC.NO, KC.NO, KC.NO, 
#       ],
        # bottom-left should probably change to a oneshot since it's a pain to reach
        # Taipo macro layer - useful browser stuff
        # tab left/right
        # spawn tab, kill tab
       # scroll up, scroll down
        # flip desktops
        # ctrl+l to focus address bar would be handy (maybe)
        [
        KC.TRNS, KC.LGUI(KC.N1), KC.LGUI(KC.N2), KC.LGUI(KC.N3), KC.LGUI(KC.N4), KC.LGUI(KC.N5),  KC.LGUI(KC.N6), KC.LGUI(KC.N7), KC.LGUI(KC.N8), KC.LGUI(KC.N9), KC.LGUI(KC.N0), KC.NO, 
        KC.NO, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.NO,     KC.NO, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.NO, 
        KC.NO, KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,      KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.NO, 
        KC.NO, KC.NO, KC.NO, KC.TRIGGERL, KC.TP_LIT, KC.TP_LOT,       KC.TP_ROT, KC.TP_RIT, KC.TRIGGERR, KC.NO, KC.NO, KC.NO, 
        ],


        # Let's go with watchman, maybe
        # https://www.keyboard-layout-editor.com/#/gists/246772cb72fa2de02354d5cb1add6b2b

                   # for this layer:
                   # corner is escape (tap), GUI (hold)
                   # that can be done with holdtap, but I want to change the layer too
                   # oh wait I like tab... tab/GUI?
                   # then escape is a combo...
                   # thumb outermost should be FN

                   # what to do about shifted numbers, and escape, and the like?

        # Normal layer
       [KC.LT(LAYER_BROWSER, KC.TAB),   KC.Q,KC.W,KC.E,KC.R,KC.T,         KC.Y, KC.U, KC.I, KC.O, KC.P, KC.BACKSPACE,
       KC.LCTRL, KC.A, KC.S, KC.D, KC.F, KC.G,     KC.H, KC.J, KC.K, KC.L, KC.SEMICOLON, KC.QUOTE,
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
        NORMAL_OFF, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),    KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.INSERT, KC.DELETE, 
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
        NORMAL_OFF, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),    KC.TG(LAYER_GAME), KC.NO, KC.UP, KC.NO, KC.INSERT, KC.DELETE, 
        KC.TRNS, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,          KC.NO, KC.LEFT, KC.DOWN, KC.RIGHT, KC.GRAVE, KC.BSLASH, 
        KC.TRNS, KC.NO, KC.NO, KC.NO, KC.END, KC.NO,       KC.END, KC.PGDN, KC.LEFT, KC.I, KC.B, KC.SLASH, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,       KC.SLASH, KC.B, KC.I, KC.NO, KC.NO, KC.NO, 
    ],

# Maybe lower middle fingers should be shifts, that get applied to the far side...?
# Numbers, symbols, etc. Same style as Cykey

# Gemini steno
[
                   KC.BSPACE, KC.G_S1, KC.G_LT, KC.G_LP, KC.G_LH, KC.G_ST1,       KC.G_ST3, KC.G_RF, KC.G_RP, KC.G_RL, KC.G_RT, KC.G_RD,
                   KC.BSPACE, KC.G_S2, KC.G_LK, KC.G_LW, KC.G_LR, KC.G_ST2,       KC.G_ST4, KC.G_RR, KC.G_RB, KC.G_RG, KC.G_RS, KC.G_RZ, 
        KC.TG(LAYER_GEMINI), KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_I, KC.G_LA,       KC.G_RU, KC.JD_u, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_y, 
        KC.TG(LAYER_JACKDAW), KC.NO, KC.NO, KC.SPC, KC.G_LA, KC.G_LO,            KC.G_RE, KC.G_RU, KC.ENTER, KC.NO, KC.NO, KC.NO, 
    ],


                   ]

if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()

# Slightly annoying thing: HT causes a bit of lag. Layer switch doesn't (but that's a bit different....)
# a HT-ish thing that triggers on release is maybe closer to what I want
# Oh, there's a lot going on with HT so that's a bit hard

