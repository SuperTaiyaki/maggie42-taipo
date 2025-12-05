# Copyright Jeremy Chin, 2025.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Uses code from https://github.com/user202729/plover-jackdaw-alt1 , hence the GPLv3.

# Keying memo:
"""
A C W N (XZ)    |    (zx) r l c t (tE)
S T H R (UO)    |    (ei) n g h s (y)
   (I) I E (A)     (A) o u (u)

    AO-eu
IE=OE  IO=AO  OA=AOEU

AI=AEU AU=AU
EA=AE EE=AOE
I=EU   IE=OE  IO=AO
OI=OEU OO=AOU OU=OU OA=AOEU
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
SS: NLS

T+TE -> TE
TE alone -> Y
(just for de-conflicting reasons)
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

RH: ST = NLT (alternate S)
    
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

from dvp import DVP
DVP = DVP()

# Block will be used for L/Vowels/R/special
class JackdawKey(Key):
    def __init__(self, code, block):
        self.code = code
        self.block = block
        super().__init__()


# JD_4 is an A key
# This is in steno order!

lh_keycodes = [
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
]

center_keycodes = [
'UO', # Because this is a modifier
'A',
'O',
'E',
'u',
]

rh_keycodes =  [
'x', # These are maybe special
'z',

'xQUOTE',

'r',
'n',
'l',
'g',
'c',
'h',
't',
's',

'dE', # Call this something else, the t breaks shit (generates Y or TE)
'e',
'y',

'xDOT',
'xCOMMA',

]

special_keycodes = [
'BS',
'SHIFT',
]

jd_keycodes = lh_keycodes + center_keycodes + rh_keycodes + special_keycodes
consonant_keycodes = lh_keycodes + rh_keycodes + special_keycodes

for key in jd_keycodes:
    make_key(names = ("JD_" + key,), constructor = JackdawKey, code = key, block = 0)

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
    "ei": 3441, <-- missing
    "ue": 2439, <-- missing
    "ua": 2205, <-- missing
    "au": 2136, <-- present?
    "ui": 1974,
    "oi": 1837, <-- present
V-- all missing
    "oa": 1692, <-- less than 10% (I added it in...)
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
"""

"""
rules_dict = {
... mostly deleted, only this part is slightly weird
        'ttE': 'te',
        'tEe': 'ey',
        'tE': 'y',
"""

# One thing to try: UO alone and the alternate to generate more vowel pairs
# and both together?
# IE is EI + flip
# UE/UA are missing, 
rules_vowels_raw = {
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

        }
rules_vowels_shifted_raw = {
        'AEu': 'ia',
        'Au': 'ua',
        'AE': 'ae',
        'AOE': 'ee',
        'Eu': 'ii',
        'OE': 'ei',
        'AO': 'oi',
        'OEu': 'io',
        'AOu': 'oo',
        'Ou': 'uo',
        'AOEu': 'ao',

        'Ou': 'uo',

        'A': 'ua',
        'O': 'uo',
        'E': 'ue',
        'u': 'ui',
        }

#rules = {x: list() for x in jd_keycodes}
#for rule in rules_dict.items():
#    rules[rule[0][0]].append(rule)

#for rule in rules:
#    rules[rule] = sorted(rules[rule], key = lambda x: -len(x[0]))

# Pre-generated out of jackdaw_map.rb to save memory
rules = {'r': [('rnlchts', 'lds'),('rnlchs', 'ld'),('rlchts', 'rlds'),('rnchts', 'wds'),('rnchs', 'wd'),('rnlcs', 'ples'),('rnlct', 'lp'),('rnlhs', 'lves'),('rnlgt', 'lk'),('rnlch', 'lch'),('rlghs', 'rld'),('rnlgc', 'lb'),('rnlgh', 'lm'),('rngh', 'rm'),('rght', 'wk'),('rnlt', 'rst'),('rnlg', 'dl'),('rnch', 'rv'),('rnlc', 'pl'),('rnlh', 'lv'),('rnht', 'wth'),('rht', 'rth'),('rng', 'gn'),('rnl', 'll'),('rlh', 'wl'),('rnh', 'wn'),('rh', 'w'),('r', 'r'),],'4': [('4SCTWNR', 'aggl'),('4CTWHNR', 'abl'),('4SCTHNR', 'affl'),('4SCTWH', 'abb'),('4CTWHN', 'aby'),('4SCTHR', 'affr'),('4CTWNR', 'addl'),('4SCTHN', 'aft'),('4CTHNR', 'afl'),('4SCWNR', 'appl'),('4SCTWN', 'adj'),('4SCWHN', 'asphy'),('4CWNR', 'apl'),('4SCWN', 'app'),('4CTHN', 'aff'),('4CTWN', 'adm'),('4CTWH', 'ab'),('4CTNR', 'acq'),('4TWHN', 'ackn'),('4THNR', 'athl'),('4SCTW', 'agg'),('4CHNR', 'accl'),('4SCWR', 'appr'),('4SNR', 'asl'),('4CHN', 'acc'),('4TWN', 'aj'),('4CWN', 'amm'),('4CTN', 'adv'),('4CTW', 'add'),('4CHR', 'accr'),('4WNR', 'all'),('4TWH', 'ak'),('4SR', 'arr'),('4TW', 'att'),('4SN', 'ann'),('4', 'a'),],'C': [('CTWHNR', 'bl'),('CTWHN', 'by'),('CTHNR', 'fl'),('CWHNR', 'phl'),('CTWH', 'b'),('CTWN', 'dem'),('CWHR', 'phr'),('CTWR', 'der'),('CTHN', 'dy'),('CTNR', 'del'),('CHNR', 'cry'),('CTN', 'dev'),('CTH', 'f'),('CHR', 'chr'),('CNR', 'cl'),('CT', 'd'),('CW', 'p'),('CN', 'z'),('C', 'c'),],'S': [('STWHN', 'xy'),('STWNR', 'serv'),('STWH', 'sk'),('STW', 'x'),('SHR', 'shr'),('SCT', 'g'),('SCN', 'ss'),('SR', 'ser'),('S', 's'),],'l': [('lgcts', 'ckles'),('lgch', 'lf'),('lgcs', 'bles'),('lgct', 'ckl'),('lghs', 'xes'),('lgh', 'x'),('lhs', 'zes'),('lht', 'lth'),('lgc', 'bl'),('lgy', 'logy'),('lgt', 'kl'),('lc', 'p'),('lh', 'z'),('l', 'l'),],'n': [('nlgch', 'mp'),('nlght', 'dth'),('nlgh', 'sm'),('nlhs', 'shes'),('ngct', 'bt'),('ngch', 'mb'),('nlgt', 'sk'),('nlct', 'nst'),('nght', 'ngth'),('nht', 'nth'),('nhs', 'ves'),('nlg', 'd'),('nlc', 'sp'),('ncs', 'nces'),('nct', 'tion'),('ngh', 'm'),('ngc', 'gg'),('nh', 'v'),('nl', 's'),('n', 'n'),],'c': [('chts', 'ds'),('cht', 'tch'),('chs', 'd'),('cte', 'cate'),('c', 'c'),],'T': [('TWNR', 'jer'),('THNR', 'try'),('THR', 'thr'),('TNR', 'q'),('TWR', 'qu'),('TWH', 'k'),('TWN', 'j'),('TN', 'v'),('T', 't'),],'g': [('gchs', 'dg'),('gtse', 'kes'),('gct', 'ck'),('ght', 'ght'),('gch', 'f'),('gt', 'k'),('gc', 'b'),('g', 'g'),],'t': [('tdE', 'te'),('tsy', 'ys'),('t', 't'),],'W': [('WHN', 'my'),('WN', 'm'),('W', 'w'),],'H': [('HNR', 'ly'),('HN', 'y'),('HR', 'rh'),('H', 'h'),],'d': [('dEe', 'ey'),('dE', 'y'),],'N': [('NR', 'l'),('N', 'n'),],'h': [('ht', 'th'),('h', 'h'),],'y': [('y', 'y'),],'R': [('R', 'r'),],'e': [('e', 'e'),],'s': [('s', 's'),],}

# Extended rules that I don't want in the generator. Must be sorted by length.
rules['x'] = [('xCOMMA', ','), ('xQUOTE', '\''), ('xDOT', '.'), ('x', '')]

rules_vowels = {x: list() for x in center_keycodes}
for rule in rules_vowels_raw.items():
    rules_vowels[rule[0][0]].append(rule)
    
rules_vowels_shifted = {x: list() for x in center_keycodes}
for rule in rules_vowels_shifted_raw.items():
    rules_vowels_shifted[rule[0][0]].append(rule)

for v in center_keycodes:
    rules_vowels[v] = sorted(rules_vowels[v], key = lambda x: -len(x[0]))
    rules_vowels_shifted[v] = sorted(rules_vowels_shifted[v], key = lambda x: -len(x[0]))

class Chord():
    def __init__(self, compact):
        self.compact = compact
        self.reset()

    def reset(self):
        self.chord = {x: False for x in jd_keycodes}

    def add(self, key):
        self.chord[key] = True

    def result(self):
        blocks = ["".join([c for c in keys if self.chord[c]]) for keys in (center_keycodes, lh_keycodes, rh_keycodes, special_keycodes)]
        combined = blocks[1] + blocks[0] + blocks[2] + blocks[3]

        if len(combined) == 0:
            return ""
        # if combined == .... do something special (commands and whatever)
        # #. disable auto-space
        # #. something

        print("Chord: ", blocks)

        if combined == "S" and self.compact:
            return [KC.BSPACE]

        # stripped = pressed

        output_v = []
        vowel_shift = blocks[0].startswith("UO")
        vrules = rules_vowels_shifted if vowel_shift else rules_vowels
        idx = 2 if vowel_shift else 0
        while idx < len(blocks[0]):
            initial_idx = idx
            if blocks[0][idx] not in vrules:
                output_v += blocks[0][idx]
                idx += 1
                continue
            candidates = vrules[blocks[0][idx]]
            for c in candidates:
                if blocks[0].startswith(c[0], idx):
                    output_v += list(c[1])
                    idx += len(c[0])
                    break

            # TODO: just to stop the vowels from breaking
            if idx == initial_idx:
                output_v += blocks[0][idx]
                idx += 1

        add_space = False
        generated = []
        for block in range(1, 4):
            output = []
            idx = 0
            while idx < len(blocks[block]):

                # single x is used for things
                if blocks[block].startswith(('X', 'z', 'Z'), idx):
                    add_space = True
                    idx += 1
                    continue
                if blocks[block].startswith('SHIFT', idx):
                    idx += 5 # len('shift')
                    shifted = True
                    break # not continue because SHIFT is at the end

                initial_idx = idx

                if blocks[block][idx] not in rules:
                    output += list(blocks[block][idx])
                    idx += 1
                    continue

                candidates = rules[blocks[block][idx]]
                for c in candidates:
                    if blocks[block].startswith(c[0], idx):
                        output += list(c[1])
                        idx += len(c[0])
                        break

                # TODO: is this still useful?
                # Guarantees no infinite loop, at least
                if idx == initial_idx:
                    output += list(blocks[block][idx])
                    idx += 1
            generated.append(output)

        # print(output_v, generated)

        # Experiment:
        # if we finish with vowels, flip add_space
        # Since vowel combos suck
        #if len(output_v) > 0 and len(generated[1]) == 0 and len(generated[2]) == 0:
        #    add_space = not add_space
            # Too much mental load? Will have to try and see
            # -> Nope, too confusing

        output = generated[0] + output_v + generated[1] + generated[2]
        if len(output) == 0: # At current, only space and shift
            if add_space:
                return [KC.SPC]
            elif shifted:
                return [KC.BSPACE]
            else:
                return ""

        keys = ([KC.LSFT(DVP[output[0]]) if shifted else DVP[output[0]]] +
                [DVP[c] for c in output[1:]])

        # TODO: cleaner expression of this
        return keys + [KC.SPC] if not add_space else keys

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
            self.held.discard(code)
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

    # Not really chord, this is the output string
    def handle_chord(self, chord):
        if chord == "":
            return
        out = [c for c in list(chord)]
        out.reverse()

        self.send_next = out

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        pass
    def after_matrix_scan(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        was_pressed = self.now_pressed 
        if self.now_pressed != None:
            keyboard.remove_key(self.now_pressed)
            self.now_pressed = None
        # up/down in the same frame is possible unless it's the same key
        if len(self.send_next) > 0 and self.send_next[-1] != was_pressed:
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
