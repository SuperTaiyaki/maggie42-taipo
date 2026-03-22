# The license on this repository is GPL2 becasue of taipo.py . This file is BSD.

import board

# board is the RPi Pico

from kmk.kmk_keyboard import KMKKeyboard

from kmk.keys import KC, Key, make_key
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.sticky_keys import StickyKeys # requirement for Taipo (formerly oneshot, KC.OS)
from kmk.modules.holdtap import HoldTap
# Mouse stuff
from kmk.modules.mouse_keys import MouseKeys
from kmk.modules.rapidfire import RapidFire


from kmk.extensions.rgb import RGB

from cykey import Cykey

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP13, board.GP9,board.GP10,board.GP12,board.GP15, board.GP14,)
keyboard.row_pins = (board.GP0,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(RapidFire())

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

keyboard.modules.append(Cykey(None))

LAYER_NORMAL = 2
LAYER_BROWSER = 3
LAYER_RAISED = 4
LAYER_LOWERED = 5
LAYER_GAME = 6

holdtap = HoldTap()
holdtap.tap_time = 150
keyboard.modules.append(holdtap)

keyboard.keymap = [
        [
KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.TP_LIT, KC.TP_LOT
]
                  ]

if __name__ == '__main__':
    keyboard.go()

