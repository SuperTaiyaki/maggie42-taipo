import board

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.split import Split, SplitSide
from kmk.modules.combos import Combos, Chord, Sequence
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.macros import Macros

from kmk.extensions.rgb import RGB

from taipo import Taipo

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP10,board.GP9,board.GP8,board.GP7,board.GP6,board.GP5,)
keyboard.row_pins = (board.GP27,board.GP26,board.GP15,board.GP14,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

split = Split(data_pin = board.GP0, use_pio = True, split_flip = False)
keyboard.modules.append(split)

layers = Layers()

keyboard.modules.append(Macros())
keyboard.modules.append(StickyKeys())
keyboard.modules.append(layers)
keyboard.modules.append(Taipo())

rgb = RGB(pixel_pin = board.NEOPIXEL, num_pixels = 1, hue_default = 176, sat_default = 30, val_default = 128, val_limit = 128,)
keyboard.extensions.append(rgb)

#keyboard.keymap = [
#    [KC.Q,KC.W,KC.E,KC.R,KC.T,KC.Y,
#    KC.A, KC.S, KC.D, KC.F, KC.G, KC.H,
#     KC.Z, KC.X, KC.C, KC.V, KC.B, KC.N,
#     KC.NO, KC.NO, KC.NO, KC.N1, KC.N2, KC.N3
#     ]
#]

LAYER_NORMAL = 2
LAYER_BROWSER = 3
LAYER_RAISED = 4

make_key(
    names=('TRIGGERL',),
    on_press=lambda *args: print('TRIGGERL'),
)
make_key(
    names=('TRIGGERR',),
    on_press=lambda *args: print('TRIGGERR'),
)

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
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,          KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, 
        KC.NO, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.NO,     KC.NO, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.NO, 
        KC.NO, KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,      KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.NO, 
        KC.NO, KC.NO, KC.NO, KC.TRIGGERL, KC.TP_LIT, KC.TP_LOT,       KC.TP_ROT, KC.TP_RIT, KC.TRIGGERR, KC.NO, KC.NO, KC.NO, 
        ],
        # Taipo macro layer - useful browser stuff
        # tab left/right
        # spawn tab, kill tab
       # scroll up, scroll down
        # flip desktops
        # ctrl+l to focus address bar would be handy (maybe)
        [
        KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO,          KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, KC.NO, 
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
       KC.NO, KC.NO, KC.NO, KC.ESCAPE, KC.LT(LAYER_RAISED, KC.BSPACE), KC.SPACE,       KC.ENTER, KC.SPACE, KC.TRIGGERR, KC.NO, KC.NO, KC.NO
       ],
    # Browser layer
    [
        KC.TRNS, KC.LGUI(KC.N1), KC.LGUI(KC.N2), KC.LGUI(KC.N3), KC.LGUI(KC.N4), KC.LGUI(KC.N5),  KC.LGUI(KC.N6), KC.LGUI(KC.N7), KC.LGUI(KC.N8), KC.LGUI(KC.N9), KC.LGUI(KC.N0), KC.NO, 
        KC.NO, KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.NO,     KC.NO, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.NO, 
        KC.NO, KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.NO,      KC.NO, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.NO, 
        KC.NO, KC.NO, KC.NO, KC.TRIGGERL, KC.TP_LIT, KC.TP_LOT,       KC.TP_ROT, KC.TP_RIT, KC.TRIGGERR, KC.NO, KC.NO, KC.NO, 
        ],
    # Raised layer
    [
        KC.NO, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),          KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.LSFT(KC.N0), KC.NO, 
        KC.TRNS, KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,          KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.BSLASH, 
        KC.TRNS, KC.NO, KC.NO, KC.LSHIFT(KC.MINUS), KC.MINUS, KC.NO,      KC.NO, KC.EQUAL, KC.LSHIFT(KC.EQUAL), KC.TP_BRR, KC.TP_BRP, KC.TRNS, 
        KC.NO, KC.NO, KC.NO, KC.TRIGGERL, KC.NO, KC.NO,       KC.NO, KC.NO, KC.TRIGGERR, KC.NO, KC.NO, KC.NO, 
        ],
    # That TRIGGERL should probably be alt or something

# Need to do something about modifiers so they stick between the layer switch
# ctrl/alt/gui, at minimum
# also, the backspace hold thing is a bit annoying - can't hold backspace through words!
                   ]

combos = Combos()
keyboard.modules.append(combos)
combos.combos = [
        Chord((KC.TRIGGERL, KC.TRIGGERR), NORMAL_ON),
        Chord((KC.BSPACE, KC.TRIGGERR), NORMAL_OFF),

    ]

if __name__ == '__main__':
    keyboard.go()

