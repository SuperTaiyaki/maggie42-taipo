# Taro Hayashi On The 17
# https://github.com/Taro-Hayashi/qmk_firmware/blob/tarohayashi/keyboards/tarohayashi/_archive/onthe17/keyboard.json
import microcontroller

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
#from jackdaw import Jackdaw
#keyboard.modules.append(Jackdaw(compact = True))
from midi4key import MidiKey
keyboard.modules.append(MidiKey())

holdtap = HoldTap()
holdtap.tap_time = 1000
keyboard.modules.append(holdtap)

# How does holdtap work?

from rgb_seventeen import Onthe17RGB
keyboard.extensions.append(Onthe17RGB())

# Layer IDs
JD = 1
CY = 2
NUM = 3
CMD = 4

keyboard.keymap = [
        # HHKB-inspired... I guess?
        # Can't have a number row because space (thumbs) ends up in an uncomfortable spot
        # As usual, want a shifted desktop flip/browser layer
        #       Probably merged with the HHKB control layer...?
        # Need F keys too, somewhere (can't merge with HHKB because up is on the top row)

        # going one to the right to get more clearance away from the trackball would be nice, but
        # then I lose the brackets in the corner and have to pull them into the middle like the ergodash
        # which isn't bad, really. Let's do it
        # Brackets are opposite from the ergodash (up rather than down)

        # Numbers in the middle row, lifted row for shifted... works pretty well!


[KC.TB_MOD, KC.HT(KC.A, KC.B),
 KC.NO,  KC.TAB,     KC.Q, KC.W, KC.E, KC.R, KC.T,   KC.HT(KC.ESC, KC.LGUI), KC.LT(CMD, KC.GRAVE),      KC.Y, KC.U, KC.I, KC.O, KC.P, KC.LBRACKET,
KC.TB_RMB, KC.TB_LMB,
 KC.TB_MMB, KC.LCTL,    KC.A, KC.S, KC.D, KC.F, KC.G,    KC.MINUS, KC.EQUAL,      KC.H, KC.J, KC.K, KC.L, KC.SCLN, KC.QUOT,
KC.NO, KC.NO,
 KC.TB_SCROLL,   KC.LSFT,    KC.Z, KC.X, KC.C, KC.V, KC.B,       KC.RBRC, KC.BSLS,   KC.N, KC.M, KC.COMM, KC.DOT, KC.SLASH, KC.RSFT,
KC.NO, KC.NO,
 KC.TB_LMB,      KC.LM(NUM, KC.LGUI),   KC.LGUI, KC.LALT, KC.MO(CMD), KC.MO(NUM), KC.SPC,   KC.BSPC, KC.ENTER,   KC.SPC, KC.MO(NUM), KC.MO(CMD), KC.RALT, KC.RGUI, KC.RCTL,

 # HT for space/shift doesn't work well, end up with too many shifts sticking to other characters
 # Need to figure out the alt/GUI stuff too, bah
 ],

# Midi4Key
[ # JD
KC.TRNS, KC.TRNS, KC.TRNS,   KC.TRNS, KC.MT_F, KC.MT_Z, KC.MT_N, KC.MT_X, KC.NO,     KC.TRNS, KC.TRNS,    KC.NO, KC.MT_e, KC.MT_n, KC.MT_z, KC.MT_f, KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS,   KC.TRNS, KC.MT_F, KC.MT_Z, KC.MT_N, KC.MT_X, KC.NO,     KC.TRNS, KC.TRNS,    KC.NO, KC.MT_e, KC.MT_n, KC.MT_z, KC.MT_f, KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS,  KC.MT_S, KC.MT_C, KC.MT_P, KC.MT_R, KC.NO,     KC.TRNS, KC.TRNS,    KC.NO, KC.MT_a, KC.MT_p, KC.MT_c, KC.MT_s, KC.TRNS,
 #KC.TRNS, KC.TRNS, KC.TRNS,  KC.LSFT, KC.LCTL, KC.LGUI, KC.LALT, KC.NO, KC.NO,      KC.TRNS, KC.TRNS,    KC.NO, KC.NO, KC.RALT, KC.RGUI, KC.RCTL, KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS,  KC.TRNS, KC.TRNS, KC.TRNS, KC.MO(NUM), KC.MT_I, KC.MT_U,    KC.NO, KC.NO,    KC.MT_u, KC.MT_i, KC.MO(NUM), KC.TRNS, KC.TRNS, KC.TG(JD)
],

# Cykey!
[ # CY
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TP_TLP, KC.TP_TLR, KC.TP_TLM, KC.TP_TLI, KC.N5,    KC.TRNS, KC.TRNS,   KC.TRNS, KC.TP_TRI, KC.TP_TRM, KC.TP_TRR, KC.TP_TRP, KC.MINUS,
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TP_BLP, KC.TP_BLR, KC.TP_BLM, KC.TP_BLI, KC.TRNS,  KC.TRNS, KC.TRNS,   KC.TRNS, KC.TP_BRI, KC.TP_BRM, KC.TP_BRR, KC.TP_BRP, KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.N7, KC.N8, KC.N9, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TP_LIT, KC.TP_LOT, KC.TRNS, KC.TRNS, KC.TP_ROT, KC.TP_RIT, KC.TRNS, KC.TRNS, KC.TRNS, KC.TG(CY),
 ],


# numbers and minor fun stuff layer
# Middle row is straight up numbers, upper row is shifted numbers, bottom row is alternate numbers (mirrored)
[ # NUM
KC.TRNS, KC.TRNS, KC.TRNS, KC.ESCAPE, KC.LSFT(KC.N1), KC.LSFT(KC.N2), KC.LSFT(KC.N3), KC.LSFT(KC.N4), KC.LSFT(KC.N5),    KC.TRNS, KC.TRNS,    KC.LSFT(KC.N6), KC.LSFT(KC.N7), KC.LSFT(KC.N8), KC.LSFT(KC.N9), KC.LSFT(KC.N0), KC.BSPC, 
KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,   KC.N1, KC.N2, KC.N3 ,KC.N4, KC.N5,    KC.TRNS, KC.TRNS,     KC.N6, KC.N7, KC.N8, KC.N9, KC.N0, KC.ENTER,
 # almost! but I want to have shifted middle chars in here too, the doubled grave is a bit in the way
KC.NO, KC.NO, KC.TRNS, KC.TRNS,   KC.GRAVE, KC.LSFT(KC.GRAVE), KC.LSFT(KC.MINUS), KC.MINUS, KC.BSLS, KC.TRNS, KC.TRNS,   KC.LSFT(KC.BSLS), KC.EQUAL, KC.LSFT(KC.EQUAL), KC.LSFT(KC.RBRC), KC.RBRC, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS,   KC.TRNS, KC.N0, KC.TRNS, KC.TRNS, KC.LSFT,      KC.TRNS, KC.TRNS,    KC.LSFT,KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
 ],
# 5 keys in the middle - on a normal keyboard minus, equal, right brace, backslash, backtick
# on this layout that's left brace, right brace, equal, backslash, grave
# on a normal layout the grave is on the left, so put them there....
# almost want backslash on the main layer, but there's no space
# ` ~ { [ \ | ] } = +

# for ardux based symbol layer...
# braces paired off is nice
# mix with vim/shell/whatever ^$ to pair?
# and #* are also paired
# leaving... !@&%
# replace the middle braces with shifts to hit that symbol layer
# Right hand already has () where they mosty should be (on the number layer)

# HHKB shifted layer + browser controls
[ # CMD
KC.TG(JD), KC.TRNS, KC.TRNS, KC.GRAVE, KC.F1, KC.F2, KC.F3, KC.F4, KC.F5,    KC.F11, KC.F12,    KC.F6, KC.F7, KC.F8, KC.F9, KC.F10, KC.DELETE,
KC.TG(CY), KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.LCTL(KC.LSFT(KC.TAB)), KC.TRNS, KC.LCTL(KC.TAB), KC.TRNS,   KC.TRNS, KC.TRNS,   KC.HOME, KC.PGUP, KC.LEFT, KC.UP,   KC.RIGHT, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,    KC.TRNS, KC.TRNS,   KC.END, KC.PGDN, KC.LEFT, KC.DOWN, KC.RIGHT, KC.TRNS,
KC.NO, KC.NO, KC.TRNS, KC.TRNS,  KC.NO, KC.NO, KC.NO, KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS,   KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS, KC.TRNS,
 ],


]

if __name__ == '__main__':
    debug.enabled = False
    keyboard.go()
