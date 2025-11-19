# TODO: remove unused layers, it's maybe slowing down the response. How fast does this go if nothing but Jackdaw is running?
# Keying memo:
"""
A C W N (XZ)    |    (zx) r l c t (e)
S T H R (UO)    |    (ei) n g h s (y)
   (I) I E (A)     (A) o u (u)

    AO-eu
AI=AEU AU=AU
EA=AE EE=AOE
I=EU   IE=OE  IO=AO
OI=OEU OO=AOU OU=OU OA=AOEU?
Ux=


G: SCT
_ * _ _
* * _ _
J: TWN
_ _ * *
_ * _ _
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

B: GC
_ _ * _
_ * _ _
D: CHS or NLG
_ _ * _   _ * _ _
_ _ * *   * * _ _
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
V: NH
_ _ _ _
* _ * _
W: RH
* _ _ _
_ _ * _
X: LGH
_ * _ _
_ * * _
Z: LH
_ * _ _
_ _ * _
LL: RNL
CK: GCT
ST: NLT


_ _ _ _
_ _ _ _

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
W=RH
X=LGH
Z=LH

sf <-- should be GH (scth)
RH: ST = NLT (alternate S)

Stuff to fix:
    MP is a lot more common than PM, override the ordering (right hand)
    (this is in the patent, actually)
    

Customization: single characters don't auto-space!
    need a combo for that... 

wtf: CL on the left doesn't work?
    I'm getting ZR instead
    .... this is why the patent has the full chart defined

"""

"""
This vowel reaching sucks

I think this is based on an ae-ou layout
no its not consistent
ao eu


AI=AEU AU=AU
EA=AE  EE=AOE
I=EU   IE=OE  IO=AO
OI=OEU OO=AOU OU=OU
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


# Cross to -S->-E and -T-> -Y are basically impossible, relocating the Y is an option (down, as per the Plover wiki page)
# TODO: JD_BS + something for single backspace


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

#'I',
#'UO',
#'E',
#'A',

#'a',
#'o',
#'ei',
#'u',
'A',
'O',
'E',
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
'BS',
'SHIFT',
]

for key in jd_keycodes:
    make_key(names = ("JD_" + key,), constructor = JackdawKey, code = key)

class State:
    combo = 0

""" Vowel silliness
AO - EU is reasonable...
    That's the steno order
    The patent order is ei-a-ou
A
O
E
U
ao
ae
au
oe
ou
eu

aoe
aou
aeu
oeu

aoeu

Hey the jackdaw chart can't generate EU, that's kind of annoying
in order:
    ou
    ea

SO the existent 2-chars are:
    ARGH there are ordering issues too, eu and ue both exist...
    so 5*5, 25 combinations!
aa
ae*
ai*
ao*
au*

ea**
ee**
ei**
eo
eu*

ia* trial
ie** field
ii
io** prior
iu?

oa* boar
oe?
oi* toil
oo**
ou**

ua
ue* fuel
ui?
uo 
uu
at least 16 combinations in use

Maybe take a reasonable set and just let the rest break strokes up...?
    "ou": 17457,
    "ea": 13361,
    "io": 12278,
    "ee": 7446,
    "ai": 6880,
    "ie": 6832,
    "oo": 4910,
    "ia": 4867,
    "ei": 3441,
    "ue": 2439,
    "ua": 2205,
    "au": 2136,
    "ui": 1974,
    "oi": 1837,

    "oa": 1692, <-- less than 10%
    "eo": 1497,
    "oe": 734,
    "eu": 340,
    "ae": 266,
    "iu": 221,

    "uo": 150, < -- less than 1%
    "ao": 75,
    "ii": 57,
    "aa": 53,
    "uu": 11,

roughly, ao - ie looks reasonable
ao doesn't exist, so that's fine for u
but then we can't generate ou...
    that's crucial enough that I want it top-layer
    ao - eu lets that generate easily enough. Maybe why it's there?
    use ae to generate ea... (or just outright swap them)
        uo doesn't exist so auto-swap that?
ou: ou
ea: ae
io: ao is fine (super low occurence)
ee: aoe is fine?
ai: aeu
ie: oe (same logic as ea?)
oo: aou
ia: ao
ei: no generation???
ue, ua, : nothing
au: why???
ui: nothing!
oi: oeu (this one exists)

oa: nothing


Ah. So the missing OA is a <10%
    all-4 for that?

One thought: breaking a stroke in the middle isn't much of a penalty
    in which case, fucking break everything...?

ue$ (and any other e$) can be generated using the rightmost e

I'm missing ei quite a lot (it's in the top 100 words)
and it's in the top 100 list
so I should probably exchange it into the set somewhere
    I have space for one more button (thumb rear), use it for vowel swap...?
        the vowel double would be handy, then I can unlock a few combos
            That alone might help (only 2 combos though - ee, oo)
            AO is super not useful, so make that also generate I and then with the swap we can get any vowel pair!


"""

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

        # override because they don't work right
        'CNR': 'cl',
        'CWNR': 'pl',

# AI=AEU AU=AU
# EA=AE  EE=AOE
# I=EU   IE=OE  IO=AO
# OI=OEU OO=AOU OU=OU

# Nothing generates OA?
# What's still open?
# ARGH I want something that can be figured out using heuristics...

# UNrelated: Maybe I can shift this over one to the right - right hand needs to stretch right anyway

        # E is right-hand, it's uppercased so it doesn't conflict with far-right e
        # AO-eu
        'AEu': 'ai',
        'Au': 'au',
        'AE': 'ea',
        'AOE': 'ee',
        'Eu': 'i',
        'OE': 'ie',
        'AO': 'io',
        'OEu': 'oi',
        'AOu': 'oo',
        'Ou': 'ou',
        'AOEu': 'oa',

        'A': 'a',
        'O': 'o',
        'E': 'e',
        'u': 'u',


####     # Left vowels
####	'I': 'i',
####    #'IE': 'u',
####    #'IA': 'u', # For my triangle thumb cluster
####    'IUO': 'u',
####    'UOE': 'o',
####	'E': 'e',
####    #'EA': 'o',
####	'A': 'a',

####    # right hand
####	'a': 'a',
####    #'ao': 'e',
####	'o': 'o',
####    'oei': 'e',
####    'eiu': 'i',
####    #'ou': 'i',
####    #'au': 'i',
####	'u': 'u',

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
        # Y is a hard key
		'lh': 'z',
        'nl': 's',  # in the patent

        # right hand extra
        'ht': 'th',
        'rnl': 'll', # in the patent!
        'gct': 'ck',
         }

# Oh hey in the patent keymap LL is available (RNL)
rules = sorted(rules_dict.items(), key = lambda x: -len(x[0]))

class Chord():
    def __init__(self, compact):
        self.compact = compact
        self.reset()

    def reset(self):
        self.chord = {x: False for x in jd_keycodes}

    def add(self, key):
        self.chord[key] = True

    def result(self):

        pressed = "".join([c for c in jd_keycodes if self.chord[c]])
        # Otherwise backspace causes trouble
        if len(pressed) == 0:
            return ""

        print("Chord: ", pressed)

        if pressed == "S" and self.compact:
            return [KC.BSPACE]

        stripped = pressed
        for x in ['x', 'X', 'z', 'Z']:
            stripped = stripped.replace(x, '')

        add_space = (pressed != stripped)
        shifted = stripped.endswith('SHIFT')
        if shifted:
            # TODO: this is tail replace
            stripped = stripped.replace('SHIFT', '')
        
        #if pressed != stripped and stripped == "":
        #if pressed == stripped:
            # HRM not working...

            # This is actually backwards. It should be for joining, not for unjoining
            #stripped = " " + stripped
            #stripped = " " # for now

        for x in rules:
            if (x[0] != x[1]):
                stripped = stripped.replace(x[0], x[1])

        if len(stripped) == 0: # At current, only space and shift
            if add_space:
                return [KC.SPC]
            elif shifted:
                return [KC.BSPACE]
            else:
                return ""


        keys = ([KC.LSFT(DVP[stripped[0]]) if shifted else DVP[stripped[0]]] +
                [DVP[c] for c in stripped[1:]])

        # TODO: cleaner expression of this
        return keys + [KC.SPC] if add_space else keys


## Compact mode: left S tapped alone is backspace
# Also the IE -> O, OU -> E chords are enabled (because the board has no space for UO and EI buttons)
class Jackdaw(Module):
    def __init__(self, compact = False):
        self.chord = Chord(compact)
        self.compact = compact
        self.last_stroke = 1

        self.held = set()

        # Stream the output
        self.send_next = []
        # Try to work around the tap_key weirdness
        self.now_pressed = None



    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, JackdawKey):
            return key

        code = key.code

        if is_pressed:
            self.held.add(code)
            if code == 'BS':
                self.send_next = [KC.BSPACE] * self.last_stroke
                self.chord.reset()
                self.last_stroke = 1
            else:
                self.chord.add(code)
        else:
            self.held.remove(code)
            # keys_pressed is the USB report; coordkeys is real keys (kmk internal)
            if len(keyboard._coordkeys_pressed) == 0:

                # OH HEY this isn't just JD keys
                result = self.chord.result()
                if result == [KC.BSPACE]:
                    result *= self.last_stroke
                    self.last_stroke = 1
                else:
                    self.last_stroke = len(result)
                self.handle_chord(result)
                self.chord.reset()
        print("Held: ", self.held)

    def handle_chord(self, chord):
        if chord == "":
            return

        # SO. Chord should be ordered like that
        # And then.... just execute every replace?
        # And then spit out the remainder?
        # print(chord)
        out = [c for c in list(chord)]
        out.reverse()

        # TODO: need to lead with a space, probably
        # Unless one of the XYZs is included...?
        self.send_next = out

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        # ARGH this is kind of buggy on KMK. The upstrokes can get lost...?
        if self.now_pressed != None:
            keyboard.remove_key(self.now_pressed)
            self.now_pressed = None
        elif len(self.send_next) > 0:
            key = self.send_next.pop()
            keyboard.add_key(key)
            self.now_pressed = key

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass


# In the end this is a lot closer to the original Shelton patent than the Jackdaw theory
