import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
# Mouse stuff
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire

from kmk.utils import Debug
debug = Debug(__name__)

from jackdaw import Jackdaw
from geminipr import Gemini

keyboard = KMKKeyboard()


keyboard.col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7)
keyboard.row_pins = (board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP16)
keyboard.diode_orientation = DiodeOrientation.COLUMNS

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

#from cykey import Cykey
#keyboard.modules.append(Cykey())

#from taipo import Taipo
#keyboard.modules.append(Taipo())
from cykey import Cykey
keyboard.modules.append(Cykey())

keyboard.modules.append(Jackdaw(compact = True))
keyboard.modules.append(Gemini())

holdtap = HoldTap()
holdtap.tap_time = 150
keyboard.modules.append(holdtap)

MWUP = KC.RF(KC.MW_UP, interval = 800, timeout = 20)
MWDOWN = KC.RF(KC.MW_DOWN, interval = 800, timeout = 20)

LAYER_BROWSER = 3
LAYER_GAME = 6

keyboard.keymap = [
# Jackdaw
[
KC.JD_4, KC.JD_C, KC.JD_W, KC.JD_N,      KC.JD_X,    KC.JD_r, KC.JD_l, KC.JD_c, KC.JD_t, KC.JD_dE,
KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_R,      KC.JD_z,    KC.JD_n, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_e, 
KC.JD_xQUOTE, KC.JD_xCOMMA, KC.JD_xDOT, KC.JD_UO,     KC.JD_x,    KC.JD_UO,  KC.JD_u, KC.TG(4), KC.TG(3), KC.JD_y,
                        KC.NO , KC.JD_A, KC.JD_O, KC.JD_E, KC.JD_u,    KC.ENTER # thumb row
],

# GeminiPR steno
[
KC.G_S1, KC.G_LT, KC.G_LP, KC.G_LH, KC.G_ST1,   KC.G_RF, KC.G_RP, KC.G_RL, KC.G_RT, KC.G_RD,
KC.G_S2, KC.G_LK, KC.G_LW, KC.G_LR, KC.G_ST2,   KC.G_RR, KC.G_RB, KC.G_RG, KC.G_RS, KC.G_RZ, 
KC.NO, KC.NO, KC.SPC, KC.G_LA, KC.G_LO,         KC.G_RE, KC.G_RU,   KC.ENTER, KC.NO, KC.NO,
],

# Taipo
[
KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,  MWUP,          KC.TG(3), KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_BRP,
KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, MWDOWN,         KC.NO, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR,
KC.TP_BLP, KC.TP_BLR, KC.LAYER2, KC.TP_LIT, KC.TP_LOT,      KC.TP_LIT, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR,
KC.NO , KC.TP_LIT, KC.TP_LOT, KC.JD_E, KC.JD_u, KC.JD_C # thumb row
],

# Cykey
[
KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI,     MWUP,          KC.TG(3), KC.TP_TRI, KC.TP_TRM, KC.TP_TRR,       KC.TP_BRP,
KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI,     MWDOWN,         KC.NO, KC.TP_BRI, KC.TP_BRI, KC.TP_BRM, KC.     TP_BRR,
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


