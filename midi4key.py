# https://github.com/Sillabix/MIDI4TEXT-sistema-ortosillabico-per-tastiera-midi--MIDI4TEXT-orthosllabic-system-for-midi-keyboard/tree/main/ENG

"""
problems:
felt
-lt
should that merge?
not in the dictionary!
    there are no ~lt in the entire damn dictionary
    ... maybe it just doesn't generate?
        yep, just need to split

two
    T = FP
    W = CN
    FCNP
    Officially, FPXIuie
    AHHHH so the characters don't merge in each slot...?
    not true. FCPRIuianzf = blunt
    b-l-u$-n... zf? 
    ahhh nzf is nt (tail) (or int at the head)
    [t][w][o$] (CXIuo)

seem
s-e-e-m...
se would be s-xr, but sx is sci
SRX is apparently the better way?
    uhhh 
    so I was basically right
    seem and the like are basically the only problems...
    e in the second slot
    SRXue[m]

hand
    dictionary uses nf
        defined in the list!
            can I swap that with R or something?
        alias it or something if necessary

only
    nothing?
        brief it, I guess
        3 strokes, needs a brief

want
-nzf
    oh, just ned to remember FZN

earth
    how to terminate this?
    FCnzf is supposed to be terminal, not sure about the logic
    ear/th (RXa/c) is fine

have
    Dictionary says FCRcs. So, this just can't be briefed out...
        or requires some ever more annoying logic to block those if group 3 is dropped...?
    works now

tain (certain)
    Oh, use the Ii
        and no way to force a word break so split it into 3...?

join
    J is shitty, the end
        still, only 2 strokes

shout
    ARGH sh- and sw- are both feasible, the XI alone doesn't work...
        OH I have an SH!

board is a bit annoying
    boa- is fine
    rd$ is two strokes...
        ea does nothing, allow it to drop in in place of the vowel and create a word break?
            Given that I have no differentiation to deal with, that might be suitable
            (this is implemented)
            so [r][ea][d] should work

usual:
    no idea!
        the second u is a pain to stroke....
        any solo u is hard to stroke
        ua is not available
        so u/ doesn't work, us/u/ doesn't work... ????
        us/Uapcs
        oops delete was on the wrong side. Still sucks though!
            3 strokes
        the problem here is the -ual
        Uaul should work, but it gets caught as UUa[l] -> usaual
            but I want us[u][a$]l
                I can force that... Uua -> $ua?
                DONE
        maybe this is just too weird a case

build:
    tricky...
    bu/il/d works, but is that optimal?
    would gets a brief, CNuiapcs
    CN ->w
    uia -> final u
    pcs -> ???
    d = p c s
    l = n c s
    so it's wu$d... might be the only way

think
    ~nk, can that be optimized?
    drink is SCPRin/zs in the manual
        thin/k... probably the way. bah.

skill:
    2nd slot has C that gets shared with k/g, but that doesn't auto switch...
    just need to break, probably
    ZXIUuincs = skil
        from the 2nd group??
    Z = Z
    XIU = c (or alt)
        hrm, why not sk? just based on the phonetic version?
    honestly, the doubled L is annoying enough to be worth the double tap

afraid
    the -raid part is doable enough, but can I merge in a terminator?
    -ai is Ii
    dictionary: Iui
    riid?
    why not 

nue (continue)
    I want u + e$, but the Uu takes priority. Is that suitable?
        It generates a useless ue, so probably not...
        so those should be group 2/3 exact matches
""" 

"""
# Somehow crams everything into 10 keys - no external consonants, no extra thumbs. How???
# Nice and regular, for the most part... but maybe more magic required
    More magic because it's really hard to generate beyond one syllable in one stroke
    but mental load is good! This is a proper speed layout
# Base grid:
#
# FZNX       enzf
# SCPR IU ui apcs
Vowel rules:
including the -u, ending vowel -> terminate word (trigger next space)
    does it need to be buffered?

    There's no way to squish the terminating vowels into Jackdaw...
    would need to crush the consonants into the sides and open more vowels
        not impossible
        I guess that's the trick with this system
        so this is going to have worse stroke efficiency, probably.
        key in -> key out efficiency is almost certainly worse since common
            chars have more keys
        SH instead of C for a single stroke is pretty crazy


using the left hand vowels instead (a -> R) -> terminate + add ending e
    so this requires some planning
    BUT on the observation that all words have to be memorized anyway that's fine
        composing with this is quite a bit harder, by the looks of it

Maybe more natural voiced/unvoiced variations
    oh, maybe not

I don't know if this follows the steno priority rules...

Magic: XI generates W, but H after a (p, w, r) but also f/v in special cases
    'swung' is SXIiuans, but shuck is.... oh, Ciua...
ah, 'divi' is special (SCPXIi
    .... maybe this is the level of magic I want?

Hesitation:
FCe/Si/FPa/FPIuien

Oh hey there's a sample: 'jail' doesn't generate in one stroke
ZNIa/uincs
    The J requires the I so break the stroke

should call this something other than midi4text, bah

How do I terminate a word without a vowel...?
standalone 4th block is also terminating...? HRM.
    so the logic is pretty similar to my jackdaw, lol
    I guess if you need to drop more in you use non-4th consonants?

^STR is easy enough (FCR), but ST is... S from the first block, T/D from the second block
ah, RIU

P31, lesson V: ending E
    Is the rule for group 2 without group 3? Or vowels specifically?
P45, lesson X: AU/AI (Uu/Ii) combinations
P56, lesson XV: uo mix ('ground' using ia)
p57, "" - consonant clusters
    I don't get why contexts gets a space on the FPs
    maybe it doesn't and the manual space gets used?

So, this is a proper steno-ish thing that uses plenty of briefs (or can...)
    is that better than jackdaw? IDK
        my conclusions about jackdaw... probably not

so ll$ and gg$ and the like are just... stroke again?
    group 3 has basically no consonants, so probably
    BUT you get less movement and maybe less vowel thinking....

Ok, it feels like it's meant to be one chord per group (with a few blends), no steno-ish
merging stuff inside one cluster

in that case: Maybe move M and R to somewhere less annoying
swap R and Z?
    DONE works nicely

standard: 3 keys * 2 positions = 26 basic combinations
        Need to map out what's not in use (and drop the J in there, maybe)
        28 in the table, probably done!
    allow double and we get 3 positions, 32 combinations

Is there any reason why I can't rework the whole damn table? No need to follow the Michela sensibilities
    The 2nd and 3rd groups have some smart stuff though
    and they don't chain or anything... there's just a few blends
    priorities:
        t sucks
ETAOINS RHLDCUM
TNS RHL DCM
swap T and C?
    lol C ends up like cykey
    This frequency graph doesn't quite apply!
    T and P? P isn't that high frequency...
        but P needs to blend with the next key a bit, less awkward is good
    DONE: C-> T, FP -> C

Q and J: Left hand vertical pairs aren't used, so do that
blends that clash: same thing, change them to FS which is not used in the original theory

On the right hand, FZ to add some more useful stuff...
    I want an ~ll (NSFS?)
    and a -dd (PSFZ?)
        lol same logic as jackdaw
        DONE

Since I have the C/K problem in group 2, use one of the open slots to deal with it?
    XIU -> C
    The missing one was... RXU RXIU
        RXIU -> K looks reasonable
        DONE

The dictionary has a bunch of useless shit, why?
    158k lines ughhh
    "boae"
"""

from kmk.keys import Key, KC, make_key, ModifierKey, ModifiedKey
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules import Module
from kmk.utils import Debug

from dvp import DVP
DVP = DVP()

class MTKey(Key):
    def __init__(self, code, block):
        self.code = code
        self.block = block
        super().__init__()

groups = (('F', 'S', 'Z', 'C', 'N', 'P'),
          ('X', 'R', 'I', 'U'),
          ('u', 'i', 'e', 'a'),
          ('n', 'p', 'z', 'c', 'f', 's')
          )
keycodes = [x for xs in groups for x in xs]

for i, block in enumerate(groups):
    for char in block:
        make_key(names = ("MT_" + char,), constructor = MTKey, code = char, block = i)

# FZNX       enzf
# SCPR IU ui apcs
dictionary = {
        'FP': 'c', 'pf': 'c',
        'CP': 'sh', 'pc': 'sh',
        'S': 's', 's': 's',
        'F': 'f', 'f': 'f',
        'Z': 'r', 'z': 'r',
        'SCN': 'l', 'ncs': 'l',
        'P': 'p', 'p': 'p',
        'SZP': 'm', 'pzs' :'m',
        'n': 'n', 'n': 'n',
        'FCP': 'b', 'pcf': 'b',
        'SCP': 'd', 'pcs': 'd',
        'SZN': 'x', 'nzs': 'x',
        'ZP': 'g', 'pz' :'g',
        'ZN': 'y', 'nz': 'y',
        'CN': 'w', 'nc': 'w',

        'C': 't', 'c': 't',
        'FZ': 'th', 'zf': 'th',
        'SZ': 'k', 'zs': 'k',

        'FC': 'h', # head
        'cf': 'st',
        'zcf': 'h', # tail

        'FCN': 'z', 'ncf': 'z',
        'SC': 'v', 'cs': 'v',
        'SP': 'ch', 'ps': 'ch',
        'FZP': 'gh', 'pzf' :'gh',
        'FN': 'ind', 'nf': 'nd', # and more in combos
        'SN': 'inc', 'ns': 'ng', # blend? and sometimes ^ing?
        'FZN': 'int', 'nzf' :'nt',
        'zc': 'ck',

        # Not in the theory (white/black together) but useful
        # J
        # Q
        # L and D are one key apart so merge thing
        'npcs': 'ld',
        # Same with R (my modified R)
        'pzcs': 'rd',
        # These could be used for something else on the left
        # Useful, not available on keyboard
        'pcfs': 'dd',
        'ncfs': 'll',

        # 2nd series
        'R': 'r',
        'X': 's',
        'I': 'i',
        'RI': 'l',
        'XI': 'w', # and magic
        'U': 'u', # and backspace
        'RU': 'm',
        'XU': 'n',
        'IU': 'b', # and b
        'RIU': 't',
        'XIU': 'c', # and k/g
        'XR': 'e',
        'XRI': 'o',
        # extra
        'XRIU': 'k',

        # Alternate 2nd (mirrored vowels for terminating e) are in the other dictionary

        # 3rd series
        'a': 'a',
        'e': 'e',
        'i': 'i',
        'ie': 'o',
        'u': 'u',
        'ea': '$',

        # 3rd series terminators
        'ua': '$a',
        'ue': '$e',
        'ui': '$i',
        'uie': '$o',
        'uia': '$u',

        # 1st+2nd specials
        'FSCR': 'str', # SCR blocks 'ha_e'. 
        'FCRI': 'spl',
        'FCIU': 'spr',
        'FCXIU': 'scr',
        'CXIU': 'sch',
        'ZXIU': 'sk',
        'FSX': 'sci', # SX conflicts with [s][e]
        'ZNI': 'j', # weird because it doesn't exist in the phonetic version?
        'CPXIU': 'qu', # no standalone q!

        'Uu': 'au',
        'Ii': 'ai',
        'Iui': '$ai',
        'Uua': '$ua', # Mostly for 'usual' - I don't need aual
        'Uui': '$ui',# for 'build'
        'Uue': '$ue', # for -ue (continue)
        # TODO: Missing: ia/ea/iea specials
        'apzc': 'ae',
        'uapzc': 'ae', # TODO: terminator

        # XI magic: after p,w,r,g it becomes H
        'PXI': 'ph',
        'CNXI': 'wh',
        'FCNXI': 'rh',
        'ZPXI': 'gh' ,# is this necessary...?

        }

dictionary_2nd = (
        # mirrored vowels for trailing-e
        ('R', 'a'),
        ('XI', 'o'),
        ('X', 'e'),
        ('U', 'u'),
        ('I', 'i'),
)

# special markers: $ for terminators
# ! for terminator + ending E

rules = {}
for k, v in dictionary.items():
    leader = k[0]
    if leader not in rules:
        rules[leader] = []
    rules[leader].append((k, v))

for combos in rules.values():
    combos.sort(key = lambda x: len(x[0]) * -1)

class RewindBuffer():
    BUFFER_SIZE = 10
    def __init__(self):
        self.buffer = [(1, False, False)] * self.BUFFER_SIZE
        self.buffer_write = 0
        self.reversed = 0 # For tracking single-char removals
    def add(self, chars, suppress_space, shift):
        self.buffer_write += 1
        self.buffer_write %= self.BUFFER_SIZE
        self.buffer[self.buffer_write] = (chars, suppress_space, shift)
    def backspace(self):
        # Return the entire state
        ret = self.buffer[self.buffer_write]
        self.buffer[self.buffer_write] = (1, False, False)
        self.buffer_write -= 1
        self.buffer_write %= self.BUFFER_SIZE
        return ret


class Chord():
    def __init__(self):
        self.chord = {x: False for x in keycodes}

        self.rewind = RewindBuffer()

        # Things that flow into the next chord
        self.next_shift = False
        self.suppress_space = True
        self.word_caps = False
        self.word_caps_tripped = False

    def reset(self):
        for x in self.chord:
            self.chord[x] = False

    def add(self, key):
        self.chord[key] = True
    def discard(self, key):
        self.chord[key] = False

    def result(self):
        block_output = []
        idx = 0
        space = False
        add_e = False

        blocks = ["".join([c for c in keys if self.chord[c]]) for keys in groups]
        pressed = "".join(blocks)

        if pressed == "":
            return ""

        if pressed == "U":
            # backspace
            keys, _, _ = self.rewind.backspace()
            return [KC.BSPC] * keys
        elif pressed == "ea":
            # space
            return [KC.SPC]
        # zcs for shift - can be current word, or trigger next word

        print(blocks)

        # This part of the documentation is unclear. What's the actual trigger to end the word?
        # Maybe this logic is correct and the correct way is just to make sure the final stroke is [4] only?
        if len(blocks[0]) == 0 and len(blocks[1]) == 0 and len(blocks[2]) == 0 and len(blocks[3]) > 0:
            space = True
        
        # Enable the alternate vowel block only if block 3 is empty (for terminating Es)
        alt_2nd = len(blocks[2]) == 0

        while idx < len(pressed):
            initial_idx = idx

            if alt_2nd:
                generated = False
                # I wonder if linear search through the whole word list is too slow
                for stroke, out in dictionary_2nd:
                    if pressed.startswith(stroke, idx):
                        add_e = True
                        space = True
                        generated = True
                        block_output += list(out)
                        idx += len(stroke)
                        break
                if generated:
                    continue

            if pressed[idx] not in rules:
                block_output += list(pressed[idx])
                idx += 1
                continue

            candidates = rules[pressed[idx]]
            for c in candidates:
                if pressed.startswith(c[0], idx):
                    target = c[1]
                    if target[0] == '$':
                        # buffer the space
                        space = True
                        target = target[1:]
                    #elif target[0] == '!':
                    #    # buffer the space
                    #    if len(blocks[1]) == 0:
                    #        space = True
                    #        add_e = True
                    #    target = target[1:]

                    print("gen: ", target)
                    block_output += list(target)
                    idx += len(c[0])
                    break

            # Guarantees no infinite loop
            # .... does this still do something?
            if idx == initial_idx:
                block_output += list(pressed[idx])
                idx += 1

        if add_e:
            block_output += 'e'
        if space:
            block_output += ' '
        keystrokes = [c if isinstance(c, Key) else DVP[c] for c in block_output]
        self.rewind.add(len(keystrokes), False, False)

        return keystrokes


class MidiKey(Module):
    def __init__(self):
        self.chord = Chord()

        self.held = set()
        self.pressing = True # press/release edge

        # Stream the output
        self.send_next = []
        # Try to work around the tap_key weirdness
        self.now_pressed = None
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, MTKey):
            return key

        code = key.code

        if is_pressed:
            self.chord.add(code)
            self.pressing = True
        else:
            # oops should wait until everything is up
            output = self.chord.result()
            print("Output: ", output)
            self.handle_output(output)
            self.chord.reset()
            self.pressing = False
            # Nothing important to do on the transition to auto_space, probably


    def handle_output(self, chars):
        if chars == "":
            return
        out = [c for c in list(chars)]
        out.reverse()

        self.send_next += out

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

"""
# Briefs required:
only (on/l/y or on/ly/$)

"""
