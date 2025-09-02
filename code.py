import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide

from kmk.extensions.rgb import RGB

from taipo import Taipo

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP10,board.GP9,board.GP8,board.GP7,board.GP6,board.GP5,)
keyboard.row_pins = (board.GP27,board.GP26,board.GP15,board.GP14,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

split = Split(data_pin = board.GP0, use_pio = True, split_flip = False)
keyboard.modules.append(split)

keyboard.modules.append(Layers())
keyboard.modules.append(Taipo())

#keyboard.keymap = [
#    [KC.Q,KC.W,KC.E,KC.R,KC.T,KC.Y,
#    KC.A, KC.S, KC.D, KC.F, KC.G, KC.H,
#     KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N,
#     KC.NO, KC.NO, KC.NO, KC.N1, KC.N2, KC.N3
#     ]
#]

keyboard.keymap = [[
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,          KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, 
        KC.NO, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.NO,     KC.NO, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.NO, 
        KC.TG(1), KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,      KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.NO, 
        KC.NO, KC.NO, KC.NO, KC.NO, KC.TP_LIT, KC.TP_LOT,       KC.TP_ROT, KC.TP_RIT, KC.NO, KC.NO, KC.NO, KC.NO, 
        ],

                   [KC.TAB,   KC.Q,KC.W,KC.E,KC.R,KC.T,         KC.Y, KC.U, KC.C, KC.O, KC.P, KC.BACKSPACE,
                   KC.CTRL  , KC.A, KC.S, KC.D, KC.F, KC.G,     KC.H, KC.J, KC.K, KC.L, KC.ENTER, # can maybe do something better than enter
                   ####KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V, KC.B,
                   KC.LSHIFT, KC.Z, KC.X, KC.C, KC.V, KC.B,        KC.N, KC.M, KC.COMMA, KC.DOT, KC.SLASH, KC.RSHIFT,
                   KC.NO, KC.NO, KC.NO, KC.BSPACE, KC.ENTER, KC.SPACE,       KC.ENTER, KC.SPACE, KC.TG(1), KC.NO, KC.NO, KC.NO
                   ]
                   ]

# Slightly annoying: The right side goes from the inner side, it's not a 100% flip
# or maybe it is....? hrm.
# not that it matters

rgb = RGB(pixel_pin = board.NEOPIXEL, num_pixels = 1, hue_default = 176, sat_default = 30, val_default = 128, val_limit = 128,)
keyboard.extensions.append(rgb)

if __name__ == '__main__':
    keyboard.go()

