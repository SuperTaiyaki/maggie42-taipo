import board
import microcontroller

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
from kmk.modules.encoder import EncoderHandler


from kmk.utils import Debug
debug = Debug(__name__)

from jackdaw import Jackdaw
from geminipr import Gemini

keyboard = KMKKeyboard()

"""
  "matrix_pins": {
    "cols": ["F4", "F5", "F6", "F7", "B1"],
    "rows": ["B6", "B2", "B3", "B5", "B4", "E6"]
  },
  "dynamic_keymap": {
    "layer_count": 6
  },
  "diode_direction": "ROW2COL",
  "encoder": {
    "enabled": true,
    "rotary": [
      { "pin_a": "D2", "pin_b": "D1", "resolution": 4 },
      { "pin_a": "D0", "pin_b": "D4", "resolution": 4 },
      { "pin_a": "C6", "pin_b": "D7", "resolution": 4 }
    ]
  },

  F4 = A3
  F5 = A2
  F6 = A1
  F7 = A0
  B1 = D15 = 22

  B6 = D10/A10 = 21
  B2 = D16 = 23
  B3 = D14 = 20
  B5 = D9 = 9
  B4 = D8 = 8
  E6 = D7 = 7

  D2 = D2
  D1 = GPIO0 = D0?
  D0 = GPIO1 = D1?
  D4 = D4
  C6 = D5
  D7 = D7 (isn't that E6? Yep, they overlap!)


  board.A0 board.D26 (GPIO26)
board.A1 board.D27 (GPIO27)
board.A2 board.D28 (GPIO28)
board.A3 board.D29 (GPIO29)
board.D0 board.TX (GPIO0)
board.D1 board.RX (GPIO1)
board.D2 (GPIO2)
board.D20 board.MISO (GPIO20)
board.D21 (GPIO21)
board.D22 board.SCK (GPIO22)
board.D23 board.MOSI (GPIO23)
board.D3 (GPIO3)
board.D4 (GPIO4)
board.D5 (GPIO5)
board.D6 (GPIO6)
board.D7 (GPIO7)
board.D8 (GPIO8)
board.D9 (GPIO9)
board.NEOPIXEL (GPIO25)
board.SCL (GPIO17)
board.SDA (GPIO16)


  """

""" Weird stickiness with this board...
I thought it was limited to the encoders but sharp taps on the keys can get missed too
Why?
Debounce settings?
Even changing the MCU it's happening, so...
capacitance or bad layout?
nature of these switches?

Small matrix, maybe I can increase the scan speed
"""
keyboard.col_pins = (board.A3, board.A2, board.A1, board.A0, board.D22)
keyboard.row_pins = (board.D21, board.D23, board.D20, board.D9, board.D8, board.D7)
keyboard.diode_orientation = DiodeOrientation.ROWS

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())

encoder_handler = EncoderHandler()
encoder_handler.pins = [
        (board.D1, board.D2, None),
        (board.D3, board.D4, None),
        (board.D5, board.D6, None)
        ]
encoder_handler.map = [
        ((KC.N1, KC.N2), (KC.N3, KC.N4), (KC.N5, KC.N6))
        ]
keyboard.modules.append(encoder_handler)

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

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

keyboard.keymap = [
        [
            KC.LGUI(KC.N1), KC.LGUI(KC.N2), KC.LGUI(KC.N3), KC.LGUI(KC.N4), KC.LGUI(KC.N5),
            KC.N6, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.N0,
            KC.TP_BLP, KC.N7, KC.N8, KC.N9, KC.N9, # 2 and 4 -> encoder clicks
            KC.LSFT, KC.N7, KC.N8, KC.N9, KC.N9, # 5 -> encoder click
            KC.LSFT, KC.N7, KC.N8, KC.TP_LIT, KC.TP_LOT,
            KC.Z, KC.NO, KC.C, KC.NO, KC.B, # 0 -> thumb up, 5 -> thumb down, 3 -> thumb click

        ],
        [
            KC.N1, KC.N2, KC.N3, KC.N4, KC.N5,
            KC.N6, KC.N7, KC.N8, KC.N9, KC.N0,
            KC.TAB, KC.N7, KC.N8, KC.N9, KC.N9, # 2 and 4 -> encoder clicks
            KC.LSFT, KC.N7, KC.N8, KC.N9, KC.N9, # 5 -> encoder click
            KC.LSFT, KC.N7, KC.N8, KC.N9, KC.N9,
            KC.Z, KC.NO, KC.C, KC.NO, KC.B, # 0 -> thumb up, 5 -> thumb down, 3 -> thumb click

        ]
]
if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()


