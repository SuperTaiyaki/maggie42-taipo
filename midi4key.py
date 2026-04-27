# https://github.com/Sillabix/MIDI4TEXT-sistema-ortosillabico-per-tastiera-midi--MIDI4TEXT-orthosllabic-system-for-midi-keyboard/tree/main/ENG

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

I installed EA as a null terminal but it's actually in use - when 2nd group is in use, it generates ea
    ia for $ou as well
    and iea for $ea
    these will reduce the need for a null terminal...
    can use the impossible ones though - UIEA, UEA
    ea for $ with no 2nd group should be fine, it's just for forcing consonant blocks to terminate

wtf is the B for in the second slot? I can see it being useful for the phonetic version...
    I want a slot to split W/H, that's taking up space
    the dictionary has lots of bp and the like, but that's also useless
    SP-type stuff is about all of it... useless!
        let's put the h there instead
        P would be much better
    C is also a bit iffy
        again, SC... is about all
        heck, the only consonant that chains into other consonants like that is S
    This slot is mostly for the phonetic version anyway, can rethink it later
        hopefully not confuse myself too much in the process

    URGH some sort of inversion might be better - S on the second, something else in the first and they
    swap. That solves most of the problems!
        so like the trailing E, set up a leading S
    actually H in 2nd is useful - TH, CH, WH so don't put the S on UI
    X generates S, which is absolutely useless in second... flip that?

pose: PXIs
but the PH to generate 

ZC on the right generates ck, left does nothing so ST (since it opens up group 2)

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
        'ZC': 'st',

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
        'fs': 'ss',

        # 2nd series
        'R': 'r',
        'X': 's',
        'I': 'i',
        'RI': 'l',
        'XI': 'w', # and magic
        'U': 'u', # and backspace
        'RU': 'm',
        'XU': 'n',
        'IU': 'h', # Used to be p/b
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
        'Iuie': '$io', # aie is not useful
        'Uua': '$ua', # Mostly for 'usual' - I don't need aual
        'Uui': '$ui',# for 'build'
        'Uue': '$ue', # for -ue (continue)
        'Uuia': '$au', # for 'laugh' - this is in the document. Not sure if it's meant to be terminating
        #'apzc': 'ae',
        #'uapzc': 'ae', # TODO: terminator
        'ia': '$ou',
        #'ea': 'ea', # This is implicit!
        'iea': '$ea', # not uea? hrm. They both work!
        # oh, uea is impossible on a proper Michela device

        # XI magic: after p,w,r,g it becomes H
        #'PXI': 'ph',
        #'CNXI': 'wh',
        #'FCNXI': 'rh',
        #'ZPXI': 'gh' ,# is this necessary...?
        # Removed since IU generates this anyway

        }

# Applies when 3rd group is empmty
dictionary_2nd = (
        # mirrored vowels for trailing-e
        ('R', 'a'),
        ('XI', 'o'),
        ('X', 'e'),
        ('U', 'u'),
        ('I', 'i'),
)
# Applies when 2nd group is empty
dictionary_3rd = (
        ('ea', '$'),
        ('iea', '\''), # Should this be terminating? Maybe it shouldn't count as 3rd group
        # ia not used right now
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
 
        # Alternate 2nd and 3rd blocks get enabled when the other block is empty
        alt_2nd = len(blocks[2]) == 0
        alt_3rd = len(blocks[1]) == 0

        if blocks[1] == 'X':
            # leading S
            blocks[1] = blocks[0]
            blocks[0] = 'X'

        pressed = "".join(blocks)

        if pressed == "":
            return ""
        elif pressed == "U":
            # backspace
            keys, _, _ = self.rewind.backspace()
            return [KC.BSPC] * keys
        elif pressed == "ea":
            # space
            return [KC.SPC]
        elif pressed == "nsf":
            # TODO: rewird
            return [KC.ENTER] # TODO: set up a dictionary for this instead.
            # HRMMMM this is a bit annoying with end-space (would like to un-space it)
        elif pressed == "zcs":
            # Push the space forward, etc.
            # zcs for shift - can be current word, or trigger next word
            return ""
        elif pressed == "NX":
            # TODO: Push the shift forward
            # TODO: rewird
            return ". "
        # TODO: full dictionary

        print(blocks)
        print(pressed)

        # This part of the documentation is unclear. What's the actual trigger to end the word?
        # Maybe this logic is correct and the correct way is just to make sure the final stroke is [4] only?
        if len(blocks[0]) == 0 and len(blocks[1]) == 0 and len(blocks[2]) == 0 and len(blocks[3]) > 0:
            space = True

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
            if alt_3rd:
                generated = False
                for stroke, out in dictionary_3rd:
                    if pressed.startswith(stroke, idx):
                        if out[0] == '$':
                            out = out[1:]
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

                    block_output += list(target)
                    idx += len(c[0])
                    break

            # Guarantees no infinite loop
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
