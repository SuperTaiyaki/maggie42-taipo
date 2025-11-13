# Keying memo:
"""
A C W N (XZ)    |    (zx) r l c t (e)
S T H R (UO)    |    (ei) n g h s (y)
   (I) I E (A)     (A) o u (u)


F: CTH
_ * _ _
_ * * _
G: SCT
_ * _ _
* * _ _
J: TWN
_ _ * *
_ * _ _
K: TWH
_ _ * -
_ * * _
Q: TNR    QU: TWR
_ _ _ *      _ _ * _
_ * _ *      _ * _ *
V: TN
_ _ _ *
_ * _ _
X: STW
_ _ * _
* * _ _
Z: CN
_ * _ *
_ _ _ _

_ _ _ _
_ _ _ _
D: CHS
_ _ * _
_ _ * *
F: GCH
_ _ * _
_ * * _
K: GT
_ _ _ *
_ * _ _
M: NGH
_ _ _ _
* * * _
P: LC (same as left hand)



B=CTWH
D=CT
F=CTH
G=SCT
J=TWN
K=TWH
L=NR
M=WN
P=CW
Q=TNR
V=TN
X=STW
Y=HN
Z=CN

B=GC
D=NLG or CHS
F=GCH
K=GT
M=NGH
P=LC
S=NL or S
V=NH
X=LGH
Z=LH

sf <-- should be GH (scth)
"""


try:
    from typing import Optional, Tuple, Union
except ImportError:
    pass
from micropython import const

import kmk.handlers.stock as handlers
from kmk.keys import Key, KC, make_key
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules import Module
from kmk.utils import Debug
from supervisor import ticks_ms

# ARGH time to swap this back into cykey (maybe. someday.)
class DVP():
    def __init__(self):
        self.keys = {
            'A': KC.A,
            'AMPR': KC.AMPR,
            'ASTR': KC.ASTR,
            'AT': KC.AT,
            'AUDIO_VOL_DOWN': KC.AUDIO_VOL_DOWN,
            'AUDIO_VOL_UP': KC.AUDIO_VOL_UP,
            'B': KC.N,
            'BRIGHTNESS_DOWN': KC.BRIGHTNESS_DOWN,
            'BRIGHTNESS_UP': KC.BRIGHTNESS_UP,
            'BSLS': KC.BSLS,
            'BSPC': KC.BSPC,
            'C': KC.I,
            'CIRC': KC.CIRC, # ^
            'COLN': KC.LSFT(KC.Z), # uhhhh does this work? since it's a shifted key
            'COMM': KC.W,
            'D': KC.H,
            'DEL': KC.DEL,
            'DLR': KC.DLR,
            'DOT': KC.E,
            'DOWN': KC.DOWN,
            'DQT': KC.LSFT(KC.Q),# doublequote - but it's shifted... TODO
            'E': KC.D,
            'END': KC.END,
            'ENTER': KC.ENTER,
            'EQL': KC.RBRACKET,
            'ESC': KC.ESC,
            'EXLM': KC.EXLM, # ? 
            'F': KC.Y,
            'F1': KC.F1,
            'F10': KC.F10,
            'F11': KC.F11,
            'F12': KC.F12,
            'F2': KC.F2,
            'F3': KC.F3,
            'F4': KC.F4,
            'F5': KC.F5,
            'F6': KC.F6,
            'F7': KC.F7,
            'F8': KC.F8,
            'F9': KC.F9,
            'G': KC.U,
            'GRV': KC.GRV,
            'H': KC.J,
            'HASH': KC.HASH,
            'HOME': KC.HOME,
            'I': KC.G,
            'INS': KC.INS,
            'J': KC.C,
            'K': KC.V,
            'L': KC.P,
            'LABK': KC.LABK,
            'LALT': KC.LALT,
            'LAYER0': KC.LAYER0,
            'LAYER1': KC.LAYER1,
            'LAYER2': KC.LAYER2,
            'LAYER3': KC.LAYER3,
            'LBRC': KC.LBRC,
            'LCBR': KC.LCBR,
            'LCTL': KC.LCTL,
            'LEFT': KC.LEFT,
            'LGUI': KC.LGUI,
            'LPRN': KC.LPRN,
            'LSFT': KC.LSFT,
            'M': KC.M,
            'MINS': KC.QUOTE, # minus
            'MOD_AC': KC.MOD_AC, # ARGH this isn't defined yet
            'MOD_ACS': KC.MOD_ACS,
            'MOD_AS': KC.MOD_AS,
            'MOD_CS': KC.MOD_CS,
            'MOD_GA': KC.MOD_GA,
            'MOD_GAC': KC.MOD_GAC,
            'MOD_GACS': KC.MOD_GACS,
            'MOD_GAS': KC.MOD_GAS,
            'MOD_GC': KC.MOD_GC,
            'MOD_GCS': KC.MOD_GCS,
            'MOD_GS': KC.MOD_GS,
            'N': KC.L,
            'N0': KC.N0,
            'N1': KC.N1,
            'N2': KC.N2,
            'N3': KC.N3,
            'N4': KC.N4,
            'N5': KC.N5,
            'N6': KC.N6,
            'N7': KC.N7,
            'N8': KC.N8,
            'N9': KC.N9,
            'NO': KC.NO,
            'O': KC.S,
            # '.OS(mod': KC.OS(mod,
            'P': KC.R,
            'PERC': KC.PERC,
            'PGDN': KC.PGDN,
            'PGUP': KC.PGUP,
            'PIPE': KC.PIPE,
            'PLUS': KC.PLUS, # shifted TODO
            'PRINT_SCREEN': KC.PRINT_SCREEN,
            'Q': KC.X,
            'QUES': KC.LSFT(KC.LBRACKET), # shifted. It puts out a capital Z, so it should be ... 
            'QUOT': KC.Q,
            'R': KC.O,
            'RABK': KC.RABK,
            'RALT': KC.RALT,
            'RBRC': KC.RBRC,
            'RCBR': KC.RCBR,
            'RIGHT': KC.RIGHT,
            'RPRN': KC.RPRN, # right paren
            'S': KC.SCLN, # probably?
            'SCLN': KC.Z,
            'SLSH': KC.LBRACKET,
            'SPC': KC.SPC,
            'T': KC.K,
            'TAB': KC.TAB,
            'TILD': KC.TILD, # shifted
            'U': KC.F,
            'UNDS': KC.UNDS, # shifted
            'UP': KC.UP,
            'V': KC.DOT,
            'W': KC.COMMA, # wut, not used in the main map?
            'X': KC.B,
            'Y': KC.T,
            'Z': KC.SLASH,
            ' ': KC.SPC,
                 }
    def __getitem__(self, name):
        return self.keys[name.upper()]
DVP = DVP()

class JackdawKey(Key):
    def __init__(self, code):
        self.code = code
        super().__init__()


# Oh wtf I have no punctuation!
# Can do it outside Jackdaw, I guess...
# Design some chords ...?
# What needs to be layer, what can be under CMD?
# Got 3 spare keys under each hand (ZXC), but they're hard to reach
# the UO/EI keys are good for comboing
# is EI used for anything?
# actually standalone, they would make good space
# Top centers (T/Y) for asterisk joiner key, below that for.... something


# JD_4 is an A key
# This is in steno order! Need to be more careful...
jd_keycodes = [
'4',
'S',
'C',
'T',
'W',
'H',
'N',
'R',
'X',
'Z',

'I',
'UO',
'E',
'A',

'a',
'o',
'ei',
'u',

'x', # These are maybe special
'z',

'r',
'n',
'l',
'g',
'c',
'h',
't',
's',

'e', # special right-hand ones (special logic isn't applied yet)
'y',
'BS'
]

for key in jd_keycodes:
    make_key(names = ("JD_" + key,), constructor = JackdawKey, code = key)

class State:
    combo = 0

rules_dict = {		# left hand obvious
		'4': 'a',
		'S': 's',
		'C': 'c',
		'T': 't',
		'W': 'w',
		'H': 'h',
		'N': 'n',
		'R': 'r',

		# left hand required
		'CTWH': 'b',
		'CT': 'd',
		'CTH': 'f',
		'SCT': 'g',
		'TWN': 'j',
		'TWH': 'k',
		'NR': 'l',
		'WN': 'm',
		'CW': 'p',
		'TNR': 'q',
		'TWR': 'qu',
		'TN': 'v',
		'STW': 'x',
		'HN': 'y',
		'CN': 'z',

         # Left vowels
		'I': 'i',
        #'IE': 'u',
        #'IA': 'u', # For my triangle thumb cluster
        'IUO': 'u',
        'UOE': 'o',
		'E': 'e',
        #'EA': 'o',
		'A': 'a',

        # right hand
		'a': 'a',
        #'ao': 'e',
		'o': 'o',
        'oei': 'e',
        'eiu': 'i',
        #'ou': 'i',
        #'au': 'i',
		'u': 'u',

        # right hand obvious
		'r': 'r',
		'n': 'n',
		'l': 'l',
		'g': 'g',
		'c': 'c',
		'h': 'h',
		't': 't',
		's': 's',
		'e': 'e',
		'y': 'y',

		# right hand required (to be fair, you can type this with the left hand anyway, but it takes another stroke)
		'gc': 'b',
		'nlg': 'd',
		'chs': 'd',
		'gch': 'f',
		'gt': 'k',
		'ngh': 'm',
		'lc': 'p',
		'nh': 'v',
		'rh': 'w',
		'lgh': 'x',
		'lh': 'z',
         }
rules = sorted(rules_dict.items(), key = lambda x: -len(x[0]))
print(rules)

class Chord():
    def __init__(self):
        self.reset()

    def reset(self):
        self.chord = {x: False for x in jd_keycodes}

    def add(self, key):
        self.chord[key] = True

    def result(self):
        pressed = "".join([c for c in jd_keycodes if self.chord[c]])

        stripped = pressed
        for x in ['x', 'X', 'z', 'Z']:
            stripped = stripped.replace(x, '')

        if pressed != stripped and stripped == "":
            #if pressed == stripped:
            # HRM not working...

            # This is actually backwards. It should be for joining, not for unjoining
            #stripped = " " + stripped
            stripped = " " # for now

        for x in rules:
            if (x[0] != x[1]):
                stripped = stripped.replace(x[0], x[1])

        return stripped


class Jackdaw(Module):
    def __init__(self):
        self.chord = Chord()
        self.send_next = []
        self.last_stroke = 1
        pass


    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, JackdawKey):
            return key

        code = key.code

        if is_pressed:
            if code == 'BS':
                self.send_next = [KC.BSPACE] * self.last_stroke
                self.chord.reset()
                self.last_stroke = 1
            else:
                self.chord.add(code)
        else:
            # keys_pressed is the USB report; coordkeys is real keys (kmk internal)
            if len(keyboard._coordkeys_pressed) == 0:
                self.handle_chord(self.chord.result())
                self.chord.reset()

    def handle_chord(self, chord):
        if chord == "":
            return

        # SO. Chord should be ordered like that
        # And then.... just execute every replace?
        # And then spit out the remainder?
        # print(chord)
        out = [DVP[c] for c in list(chord)]
        out.reverse()

        # TODO: need to lead with a space, probably
        # Unless one of the XYZs is included...?
        self.send_next = out
        self.last_stroke = len(out)

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        if len(self.send_next) > 0:
            keyboard.tap_key(self.send_next.pop())
            #keyboard.tap_key(KC[self.send_next.pop()])

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass


