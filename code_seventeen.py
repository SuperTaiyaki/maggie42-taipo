# Taro Hayashi On The 17
# https://github.com/Taro-Hayashi/qmk_firmware/blob/tarohayashi/keyboards/tarohayashi/_archive/onthe17/keyboard.json
import microcontroller
# The built-in RGB module has a bunch of crap sucking up memory, do it simple
import neopixel
px = neopixel.NeoPixel(pin = microcontroller.pin.GPIO15, n = 75, brightness = 0.05, auto_write = False)
px.fill((32, 32, 32))

px[66] = (0, 255, 0) # enter/backspace light up
px[67] = (255, 0, 0)
px[53] = (24, 24, 140) # Light the entire central column
px[52] = (24, 24, 140)
px[35] = (24, 24, 140)
px[34] = (24, 24, 140)

px[60] = (24, 24, 140)
px[27] = (24, 24, 140)
# presumably 0-10 are the underglow
px.show()

# Don't import board because this isn't a defined board

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

from kmk.utils import Debug
debug = Debug(__name__)


from synchronousscanner import SynchronousScanner

import digitalio

keyboard = KMKKeyboard()

keyboard.col_pins = (
        microcontroller.pin.GPIO29, microcontroller.pin.GPIO27, microcontroller.pin.GPIO23, microcontroller.pin.GPIO21, microcontroller.pin.GPIO14, microcontroller.pin.GPIO13, microcontroller.pin.GPIO12, microcontroller.pin.GPIO11, microcontroller.pin.GPIO10,
      microcontroller.pin.GPIO9, microcontroller.pin.GPIO8, microcontroller.pin.GPIO7, microcontroller.pin.GPIO6, microcontroller.pin.GPIO5, microcontroller.pin.GPIO4, microcontroller.pin.GPIO2, microcontroller.pin.GPIO1)
keyboard.row_pins = (
        microcontroller.pin.GPIO25, microcontroller.pin.GPIO20, microcontroller.pin.GPIO3, microcontroller.pin.GPIO0)
keyboard.diode_orientation = DiodeOrientation.COLUMNS
# MEMO: flip rows, not columns to minimize cycle time
keyboard.matrix = SynchronousScanner(keyboard.col_pins, keyboard.row_pins, reverse_matrix = True)

# 75 LEDs (ws28120) on GP15
# PWM3360 on SPI bus (CS=GP17, SCK=GP18, MISO=GP16, MOSI=GP19)

keyboard.modules.append(StickyKeys(release_after = 3000))
keyboard.modules.append(MouseKeys())
keyboard.modules.append(RapidFire())
from pwm3360 import PWM3360
keyboard.modules.append(PWM3360(cs = microcontroller.pin.GPIO17, sclk = microcontroller.pin.GPIO18, miso = microcontroller.pin.GPIO16, mosi = microcontroller.pin.GPIO19))

layers = Layers()
layers.tap_time = 150
keyboard.modules.append(layers)

from cykey import Cykey
keyboard.modules.append(Cykey())
from jackdaw import Jackdaw
keyboard.modules.append(Jackdaw(compact = True))

holdtap = HoldTap()
holdtap.tap_time = 150
keyboard.modules.append(holdtap)

keyboard.keymap = [
        # HHKB-inspired... I guess?
        # With a Thinkpad-style arrow key block
        # Can't have a number row because space (thumbs) ends up in an uncomfortable spot
        # As usual, want a shifted desktop flip/browser layer
        #       Probably merged with the HHKB control layer...?
        # Need F keys too, somewhere (can't merge with HHKB because up is on the top row)

        # going one to the right to get more clearance away from the trackball would be nice, but
        # then I lose the brackets in the corner and have to pull them into the middle like the ergodash
        # which isn't bad, really. Let's do it
        # Brackets are opposite from the ergodash (up rather than down)


        # If there's a problem with this so far, it's that the numbers need a shift and it's hard to remember
        # and I need symbols quite often! A proper symbol layer may be better
        # Numbers in the middle row, lifted row for shifted...?
[KC.TB_MOD, KC.NO, KC.NO,  KC.TAB,     KC.Q, KC.W, KC.E, KC.R, KC.T,   KC.LM(2, KC.ESC), KC.GRAVE,      KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRACKET,
KC.TB_RMB, KC.TB_LMB, KC.NO, KC.LCTL,    KC.A, KC.S, KC.D, KC.F, KC.G,    KC.MINUS, KC.EQUAL,      KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT,
KC.NO, KC.NO, KC.TB_SCROLL,   KC.LSFT,    KC.Z, KC.X, KC.C, KC.V, KC.B,       KC.BSLS, KC.RBRC,   KC.N, KC.M, KC.COMM, KC.DOT, KC.SLASH, KC.RSFT,
KC.NO, KC.NO, KC.TB_LMB,      KC.LM(1, KC.LGUI),   KC.LGUI, KC.LALT, KC.MO(2), KC.MO(1), KC.SPC,   KC.BSPC, KC.ENTER,   KC.SPC, KC.MO(1), KC.MO(2), KC.RALT, KC.RGUI, KC.RCTL,
 # HT for space/shift doesn't work well, end up with too many shifts sticking to other characters
 # Need to figure out the alt/GUI stuff too, bah
 # Do I need a numbers + shift key too...? or just let modifiers stack?
 ],
# numbers and minor fun stuff layer
# Middle row is straight up numbers, upper row is shifted numbers, bottom row is alternate numbers (mirrored)
[
KC.TRNS, KC.TRNS, KC.TRNS, KC.ESCAPE, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),    KC.TRNS, KC.TRNS,    KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.LSFT(KC.N0), KC.MINUS, 
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.N1, KC.N2, KC.N3 ,KC.N4, KC.N5,    KC.TRNS, KC.TRNS,     KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS,       KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.TRNS, KC.TRNS,   KC.N1, KC.N2, KC.N3, KC.N4, KC.N5, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS, KC.TRNS, KC.N0, KC.TRNS, KC.TRNS, KC.LSFT,      KC.TRNS, KC.TRNS,    KC.LSFT,KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
 ],


# HHKB shifted layer + browser controls
[
KC.TG(3), KC.TRNS, KC.TRNS, KC.GRAVE, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5,    KC.F11, KC.F12,    KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.DELETE,
KC.TG(4), KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS,   KC.HOME, KC.PGUP, KC.LEFT, KC.UP,   KC.RIGHT, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS,   KC.END, KC.PGDN, KC.LEFT, KC.DOWN, KC.RIGHT, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS,  KC.NO, KC.NO, KC.NO, KC.MO(1), KC.TRNS,   KC.TRNS, KC.TRNS,   KC.TRNS, KC.MO(1), KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
# TODO: what browser controls? Left hand is not busy
 ],

# Jackdaw
[
KC.TRNS, KC.TRNS, KC.TRNS,   KC.JD_1, KC.JD_4, KC.JD_C, KC.JD_W, KC.JD_N, KC.JD_X,     KC.TRNS, KC.TRNS,    KC.JD_z, KC.JD_r, KC.JD_l, KC.JD_c, KC.JD_t, KC.JD_d,
KC.TRNS, KC.TRNS, KC.TRNS,  KC.JD_3,  KC.JD_S, KC.JD_T, KC.JD_H, KC.JD_R, KC.JD_X,     KC.TRNS, KC.TRNS,    KC.JD_z, KC.JD_n, KC.JD_g, KC.JD_h, KC.JD_s, KC.JD_e,
KC.TRNS, KC.TRNS, KC.TRNS,  KC.LSFT, KC.LCTL, KC.LGUI, KC.LALT, KC.JD_M, KC.JD_Q,      KC.TRNS, KC.TRNS,    KC.JD_Q, KC.JD_F, KC.RALT, KC.RGUI, KC.RCTL, KC.JD_y,
KC.TRNS, KC.TRNS, KC.TRNS,  KC.TG(3), KC.TRNS, KC.TRNS, KC.MO(4), KC.JD_A, KC.JD_O,    KC.TRNS, KC.TRNS,    KC.JD_E, KC.JD_u, KC.MO(1), KC.TRNS, KC.TRNS, KC.TG(3)
],

# Cykey!
[
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.N5,    KC.TRNS, KC.TRNS,   KC.TRNS, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.MINUS,
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.TRNS,  KC.TRNS, KC.TRNS,   KC.TRNS, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.N7, KC.N8, KC.N9, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TP_LIT, KC.TP_LOT, KC.TP_LIT,   KC.TRNS, KC.TRNS,    KC.TP_RIT, KC.TP_ROT, KC.TP_RIT, KC.TRNS, KC.TRNS, KC.TG(4),
 ]

]

if __name__ == '__main__':
    #debug.enabled = False
    keyboard.go()


