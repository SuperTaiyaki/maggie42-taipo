# TODO: remove unused layers, it's maybe slowing down the response. How fast does this go if nothing but Jackdaw is running?
# Keying memo:
"""
A C W N (XZ)    |    (zx) r l c t (tE)
S T H R (UO)    |    (ei) n g h s (y)
   (I) I E (A)     (A) o u (u)

    AO-eu
AI=AEU AU=AU
EA=AE EE=AOE
I=EU   IE=OE  IO=AO
OI=OEU OO=AOU OU=OU OA=AOEU?
Ux=
# Hey I have an open slot for AOEU-reverse

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

sf <-- should be GH (scth)
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

'r',
'n',
'l',
'g',
'c',
'h',
't',
's',

'tE',
'e', # special right-hand ones (special logic isn't applied yet)
'y',

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

Generating -e and a- are less important for lower-frequency combinations because the board corners can kind of make up....
    IE is the only one anyway

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

I have the doublers, should I eliminate OO and EE...?
"""

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
		'TWR': 'qu', # maybe the only thing not in the patent (other than the vowel blocks)
		'TN': 'v',
		'STW': 'x',
		'HN': 'y',
		'CN': 'z',

        # override because they don't work right
        'CNR': 'cl',
        'CWNR': 'pl',

        'STWH': 'sk',

# AI=AEU AU=AU
# EA=AE  EE=AOE
# I=EU   IE=OE  IO=AO
# OI=OEU OO=AOU OU=OU

# Nothing generates OA?
# What's still open?
# ARGH I want something that can be figured out using heuristics...

# UNrelated: Maybe I can shift this over one to the right - right hand needs to stretch right anyway

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

        'ttE': 'te',
        'tEe': 'ey',
        'tE': 'y',

		'lh': 'z',
        'nl': 's',  # in the patent

        # right hand extra
       'ht': 'th',
       'rnl': 'll', # in the patent!
       'gct': 'ck',

       'ght': 'ght', # These tend to generate other things (the k takes priority)
       'ghs': 'ghs',
       'rnlchs': 'ld', # really??
       'rnlct': 'lp',
       'rnlc': 'pl',

       'nlgch': 'mp', # reversed
       'rnh': 'wn',
       'rnch': 'rv', # rnh generates WN instead
       'nht': 'nth',
       'nght': 'ngth',
# From the patent, the non-trivial combos
# .... which, unfortunately runs out of memory. CRAP.
# Probably more efficient to do it the same way as the arduino implementation. BAH.
         }
         """

# One thing to try: UO alone and the alternate to generate more vowel pairs
# and both together?
# IE is EI + flip
# UE/UA are missing, 
# both for UI
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

        'A': 'aa',
        'O': 'oo',
        'E': 'ee',
        'u': 'uu',
        }

#rules = {x: list() for x in jd_keycodes}
#for rule in rules_dict.items():
#    rules[rule[0][0]].append(rule)

#for rule in rules:
#    rules[rule] = sorted(rules[rule], key = lambda x: -len(x[0]))

# Pre-generated out of jackdaw_map.rb to save memory
rules = {'r': [('rnlchts', 'lds'),('rnlchs', 'ld'),('rlchts', 'rlds'),('rnchts', 'wds'),('rnchs', 'wd'),('rnlcs', 'ples'),('rnlct', 'lp'),('rnlhs', 'lves'),('rnlgt', 'lk'),('rnlch', 'lch'),('rlghs', 'rld'),('rnlgc', 'lb'),('rnlgh', 'lm'),('rngh', 'rm'),('rght', 'wk'),('rnlt', 'rst'),('rnlg', 'dl'),('rnch', 'rv'),('rnlc', 'pl'),('rnlh', 'lv'),('rnht', 'wth'),('rht', 'rth'),('rnl', 'll'),('rnh', 'wn'),('rlh', 'wl'),('rng', 'gn'),('rh', 'w'),('r', 'r'),],'4': [('4SCTWNR', 'aggl'),('4CTWHNR', 'abl'),('4SCTHNR', 'affl'),('4SCWNR', 'appl'),('4SCTHN', 'aft'),('4SCWHN', 'asphy'),('4CTHNR', 'afl'),('4CTWHN', 'aby'),('4CTWNR', 'addl'),('4SCTWH', 'abb'),('4SCTWN', 'adj'),('4SCTHR', 'affr'),('4CTHN', 'aff'),('4CHNR', 'accl'),('4SCTW', 'agg'),('4CTNR', 'acq'),('4CTWN', 'adm'),('4THNR', 'athl'),('4SCWR', 'appr'),('4CTWH', 'ab'),('4CWNR', 'apl'),('4SCWN', 'app'),('4TWHN', 'ackn'),('4CTW', 'add'),('4CHN', 'acc'),('4SNR', 'asl'),('4CWN', 'amm'),('4CHR', 'accr'),('4CTN', 'adv'),('4WNR', 'all'),('4TWH', 'ak'),('4TWN', 'aj'),('4SR', 'arr'),('4SN', 'ann'),('4TW', 'att'),('4', 'a'),],'C': [('CTWHNR', 'bl'),('CTWHN', 'by'),('CWHNR', 'phl'),('CTHNR', 'fl'),('CTWR', 'der'),('CTHN', 'dy'),('CTNR', 'del'),('CHNR', 'cry'),('CTWH', 'b'),('CTWN', 'dem'),('CWHR', 'phr'),('CTH', 'f'),('CTN', 'dev'),('CHR', 'chr'),('CNR', 'cl'),('CT', 'd'),('CN', 'z'),('CW', 'p'),('C', 'c'),],'S': [('STWNR', 'serv'),('STWHN', 'xy'),('STWH', 'sk'),('SHR', 'shr'),('SCT', 'g'),('STW', 'x'),('SCN', 'ss'),('SR', 'ser'),('S', 's'),],'l': [('lgcts', 'ckles'),('lgch', 'lf'),('lgcs', 'bles'),('lgct', 'ckl'),('lghs', 'xes'),('lgt', 'kl'),('lhs', 'zes'),('lgc', 'bl'),('lgh', 'x'),('lht', 'lth'),('lgy', 'logy'),('lc', 'p'),('lh', 'z'),('l', 'l'),],'n': [('nlgch', 'mp'),('nlght', 'dth'),('nlgh', 'sm'),('nlhs', 'shes'),('ngct', 'bt'),('ngch', 'mb'),('nlgt', 'sk'),('nlct', 'nst'),('nght', 'ngth'),('nct', 'tion'),('nht', 'nth'),('ngc', 'gg'),('nhs', 'ves'),('nlg', 'd'),('nlc', 'sp'),('ngh', 'm'),('ncs', 'nces'),('nh', 'v'),('nl', 's'),('n', 'n'),],'c': [('chts', 'ds'),('chs', 'd'),('cht', 'tch'),('cte', 'cate'),('c', 'c'),],'T': [('THNR', 'try'),('TWNR', 'jer'),('TWN', 'j'),('TNR', 'q'),('TWH', 'k'),('THR', 'thr'),('TN', 'v'),('T', 't'),],'g': [('gchs', 'dg'),('gtse', 'kes'),('gch', 'f'),('gct', 'ck'),('gc', 'b'),('gt', 'k'),('g', 'g'),],'t': [('tsy', 'ys'),('t', 't'),],'H': [('HNR', 'ly'),('HN', 'y'),('HR', 'rh'),('H', 'h'),],'W': [('WHN', 'my'),('WN', 'm'),('W', 'w'),],'h': [('ht', 'th'),('h', 'h'),],'N': [('NR', 'l'),('N', 'n'),],'y': [('y', 'y'),],'s': [('s', 's'),],'e': [('e', 'e'),],'R': [('R', 'r'),],}

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

        print("Chord: ", blocks)

        if combined == "S" and self.compact:
            return [KC.BSPACE]

        # stripped = pressed

        # TODO: not here
        shifted = blocks[3].endswith('SHIFT')

        output_v = []
        vowel_shift = blocks[0].startswith("UO")
        vrules = rules_vowels_shifted if vowel_shift else rules_vowels
        idx = 2 if vowel_shift else 0
        while idx < len(blocks[0]):
            initial_idx = idx
            if blocks[0][idx] not in rules:
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
                initial_idx = idx

                if blocks[block][idx] not in rules:
                    output += list(blocks[block][idx])
                    idx += 1
                    continue

                # TODO: can break up rules
                candidates = rules[blocks[block][idx]]
                if blocks[block].startswith(('x', 'X', 'z', 'Z'), idx):
                    add_space = True
                    idx += 1
                    continue
                if blocks[block].startswith('SHIFT', idx):
                    idx += 5 # len('shift')
                    break # not continue because SHIFT is at the end
                    # Flag is already set

                for c in candidates:
                    if blocks[block].startswith(c[0], idx):
                        output += list(c[1])
                        idx += len(c[0])
                        break

                # TODO: is this still useful?
                if idx == initial_idx:
                    output += list(blocks[block][idx])
                    idx += 1
            generated.append(output)

        print(output_v, generated)

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
