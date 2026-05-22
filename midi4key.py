# https://github.com/Sillabix/MIDI4TEXT-sistema-ortosillabico-per-tastiera-midi--MIDI4TEXT-orthosllabic-system-for-midi-keyboard/tree/main/ENG
"""
Things changed from the original theory:
    - base keymap changed (single-key t and r, basically easier fingering for stuff I want more ofter)
    - 2nd-group S (X stroke) comes to the front, so PX- generates sp-
    - ea is a terminating group that does nothing, so Peap generates a terminating 'pp'
    - Even if a word has been terminated, single consonants from group 4 will attach to the end (not open a space)


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
        DONE works pretty well.
        Now, do I want to replace another useless character and generate a leading A?

ZC on the right generates ck, left does nothing so ST (since it opens up group 2)
    FS would also have been good, and maybe made more sense...
    although I'm using FS as a chord trigger for some stuff

Swap X and Z? Mainly so that -EX is less painful to stroke
at current it's an up-down-up-down
ez is rare, ex comes up occasionally
    this may be weird on a piano keyboard
    DONE

Swap the ending/non-ending vowel logic?
    so hold U for a continuation instead...
    may actually work better, since no-continuation usually has the right hand consonant open

AND THEN: allow U-modified vowels in group 2 for the E-thing, for non-ending and ending options there....
    but, does this conflict with other group-2 stuff?

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
          ('n', 'p', 'z', 'c', 'f', 's'),
          () # Empty group to cause a trailing !
          )
keycodes = [x for xs in groups for x in xs]

for i, block in enumerate(groups):
    for char in block:
        make_key(names = ("MT_" + char,), constructor = MTKey, code = char, block = i)

# FZNX       enzf
# SCPR IU ui apcs
dictionary = {
        'FP!': 'v', 'pf': 'v',
        'CP!': 'sh', 'pc': 'sh',
        'S!': 's', 's': 's',
        'F!': 'f', 'f': 'f',
        'Z!': 'r', 'z': 'r',
        'SCN!': 'l', 'ncs': 'l',
        'P!': 'p', 'p': 'p',
        'SZP!': 'z', 'pzs' :'z',
        'N!': 'n', 'n': 'n',
        'FCP!': 'b', 'pcf': 'b',
        'SCP!': 'd', 'pcs': 'd',
        'SZN!': 'm', 'nzs': 'm',
        'ZP!': 'g', 'pz' :'g',
        'ZN!': 'y', 'nz': 'y',
        'CN!': 'w', 'nc': 'w',

        'C!': 't', 'c': 't',
        'FZ!': 'th', 'zf': 'th',
        'SZ!': 'k', 'zs': 'k',

        'FC!': 'h', # head
        'zcf!': 'h', # tail
        'cf!': 'st',

        'FCN!': 'x', 'ncf': 'x',
        'SC!': 'c', 'cs': 'c',
        'SP!': 'ch', 'ps': 'ch',
        'FZP!': 'gh', 'pzf' :'gh',
        'FN!': 'ind', 'nf': 'nd', # and more in combos
        'SN!': 'inc', 'ns': 'ng', # blend? and sometimes ^ing?
        'FZN!': 'int', 'nzf' :'nt',
        'zc!': 'ck',
        'ZC!': 'st',

        # Not in the theory (white/black together) but useful
        # J
        # Q
        # L and D are one key apart so merge thing
        'npcs!': 'ld',
        # Same with R (my modified R)
        'pzcs!': 'rd',
        # These could be used for something else on the left
        # Useful, not available on keyboard
        'pcfs!': 'dd',
        'ncfs!': 'll',
        'npcfs!': 'll', # easier to stroke
        'fs!': 'ss',
        'nzc!': 'rt', # zcs is shift, zcf is H, 
        'nzcs!': 'rl', 
        # -ort and -ert are maybe more common than -urt and -art (easier to stroke)
        'CNP!': 'wh', # Extra

        # 2nd series
        'R!': 'r',
        'X!': 's',
        'I!': 'i',
        'RI!': 'l',
        'XI!': 'w',
        'U!': 'u', # and backspace
        #'RU': 'm', # Never used?
        'RU!': 'y',
        'XU!': 'n', # for 'know'
        'IU!': 'h', # Used to be p/b
        'RIU!': 't', # Kind of useless with the S flip
        'XIU!': 'c', # and k/g
        'XR!': 'e',
        'XRI!': 'o',
        # extra, but not useful any more
        'XRIU!': 'k',

        # Alternate 2nd (mirrored vowels for terminating e) are in the other dictionary

        # 3rd series
        'a!': 'a',
        'e!': 'e',
        'i!': 'i',
        'ie!': 'o',
        'u!': 'u',

        # 3rd series terminators
        'ua!': '$a',
        'ue!': '$e',
        'ui!': '$i',
        'uie!': '$o',
        'uia!': '$u',

        # 1st+2nd specials
        'FSC!R!': 'str', # SCR blocks 'ha_e'. 
        'FC!RI!': 'spl',
        'FC!IU!': 'spr',
        'FC!XIU!': 'scr',
        'FC!XIU!': 'sch',
        'FZ!XIU!': 'sk',
        'FS!X!': 'sci', # SX conflicts with [s][e]
        'ZN!I!': 'j', # weird because it doesn't exist in the phonetic version?
        'CP!XIU!': 'qu', # no standalone q!

        'U!u!': 'au',
        'I!i!': 'ai',
        'I!ui!': '$ai',
        'I!ie!': 'io',
        'I!uie!': '$io', # aie is not useful
        'U!ua!': '$ua', # Mostly for 'usual' - I don't need aual. Come to think of it, do these even need special cases? U left, whatever right...
        'U!ui!': '$ui',# for 'build'
        'U!ue!': '$ue', # for -ue (continue)
        'U!uia!': '$au', # for 'laugh' - this is in the document. Not sure if it's meant to be terminating
        #'apzc': 'ae',
        #'uapzc': 'ae', # TODO: terminator
        'ia!': '$ou',
        #'ea': 'ea', # This is implicit!
        'iea!': '$ea', # not uea? hrm. They both work!
        # oh, uea is impossible on a proper Michela device

        # XI magic: after p,w,r,g it becomes H
        #'PXI': 'ph',
        #'CNXI': 'wh',
        #'FCNXI': 'rh',
        #'ZPXI': 'gh' ,# is this necessary...?
        # Removed since IU generates this anyway

        'ui!nz!': '$y',

        # TODO: apostrophe should force-connect to the left
        '!!iea!': '$\'',# Should this be terminating? Maybe it shouldn't count as 3rd group
        # Terminating is better since other consonants can still be tacked on
        # except for 're and 've and .....
        # quote on its own -> not terminating?
        # Another idea: Including this pushes to the front, other letters generate as usual. Then you can have one full stroke behind the apostrophe
        # AND! it's just easier to stroke sometimes (can use left hand s and whatever)
        # but then, how to terminate...
        # MAYBE todo: use some impossible post-apostrophe consonants for the e
        # 'f is impossible... 
        '!!iea!f!': '$\'e',# Should this be terminating? Maybe it shouldn't count as 3rd group

        # Alt 3rd group, for empty 2nd group
        '!ea!': '$',
        'uiea!': '$\'', # Should this be terminating? Maybe it shouldn't count as 3rd group
        # Terminating and non-terminating versions would be nice...
        # ia not used right now

        }

# Applies when 3rd group is empmty
dictionary_2nd = (
        # mirrored vowels for trailing-e
        ('R!', 'a'),
        ('XI!', 'o'),
        ('X!', 'e'),
        ('U!', 'u'),
        ('I!', 'i'),
        ('XR!', 'ea'),
        ('RI!', 'ou'),
        # idea: combine these with ea or some other unused combo, for a non-terminating version?
)
# TODO: attach may not be useful any more
class OutputStroke():
    def __init__(self, keycode, end_sentence = False, attach_left = False, attach_right = False, ignore_shift = True):
        self.keycode = keycode
        self.end_sentence = end_sentence
        self.attach_left = attach_left
        self.attach_right = attach_right
        self.ignore_shift = ignore_shift

specials = {
    # For briefs and things
    # These use the entire chord so no need for the dividers

    'IUep': OutputStroke(DVP['DOT'], attach_left = True, end_sentence = True),
    'IUec': OutputStroke(DVP['COMM'], attach_left = True, end_sentence = False),
    'IUzc': OutputStroke(DVP['EXLM'], attach_left = True, end_sentence = True),

    'IUpcf': OutputStroke(DVP['QUOT'], attach_left = True, attach_right = False), # Left single quote
    'IUepc': OutputStroke(DVP['QUOT'], attach_left = False, attach_right = True), # Right single quote

    'IUfs': OutputStroke(KC.LSFT(DVP['QUOT']), attach_left = True, attach_right = False), # Left dquote
    'IUea': OutputStroke(KC.LSFT(DVP['QUOT']), attach_left = False, attach_right = True), # Right dquote

    # a +
    #   \ ; `
    # a ? - =
    'IUaf': KC.GRV,
    'IUaz': OutputStroke(DVP['SCLN'], attach_left = True),
    'IUan': DVP['BSLS'],

    'IUas': DVP['EQL'],
    'IUac': OutputStroke(KC.QUOT, attach_left = True, attach_right = True), # Still weird (-)
    'IUap': OutputStroke(DVP['QUES'], attach_left = True, end_sentence = True),

    # e + (same as above, with shift held
    # e | : ~
    #   X X X  <-- Xs are regular punctuation instead
    'IUef': KC.LSFT(KC.GRV),
    'IUez': OutputStroke(KC.LSFT(DVP['SCLN']), attach_left = True),
    'IUen': KC.LSFT(DVP['BSLS']),

    # Michela-style punctuation
    'NX': OutputStroke(DVP['DOT'], end_sentence = True, attach_left = True),
    'NXen': OutputStroke(DVP['COMM'], end_sentence = False, attach_left = True),

    # Briefs list
    'I': OutputStroke(KC.LSFT(DVP['I'])), # I = I
    'IU': 'you', # you = IU
    #'FN': OutputStroke((DVP['a'], DVP['n'], DVP['d'])), # and = FN
    'FN': 'and',
    'X': 'is',
    'SZX': 'the',
    # do I need 'the'?

    'ieapf': OutputStroke((DVP['QUOT'], DVP['V'], DVP['E']), end_sentence = False, attach_left = True),
    'Iieapf': OutputStroke((KC.LSFT(DVP['I']), DVP['QUOT'], DVP['V'], DVP['E'])),
    'IUieapf': 'you\'ve',
    'ieaz': OutputStroke((DVP['QUOT'], DVP['R'], DVP['E']), end_sentence = False, attach_left = True), # 're
    'ieancs': OutputStroke((DVP['QUOT'], DVP['L'], DVP['L']), end_sentence = False, attach_left = True), #'ll

    # Maybe I want a connected -ed here
    # so type 'roll' and still be able to extend it
    # 's' works fine because it's group 4 consonant only
    # -er as well?
    # -en
    # but not -end
    # The terminating version or non-terminating...?
    # Terminating might be better. '^ed$' and '^er$' are not so useful...
    # well, I use er. crap.
    # and if I want 'error' I need the er starter (non-terminating)
    # Use the mirrored 'e' instead...?
    # since ere and ede and ene aren't useful

# Samples from the PDF:
# for = FR
# I = I*
# new = NU
# few = FU
# did = SCPI
# he = FCX
# his = FCs
# self = SRIuef
# is = X*
# its = Xuipf
# can = CPR
# inside = NXuipcs
# session = SXuien
# can't = CPuanzf
# isn't = Xnzf
# design = SCPXuinf
# don't = SCPuienzf
# doesn't
# and = FN *
# sign = SIuinf
# have = FCcs
# ? = PSsp
# also = SCNXuie
# why = CNnz
# Auto^ = UApf
# don't = RIUuienzf

# Could add an extra thing that required that a space is buffered (or not) or the brief doesn't trigger
# Mostly to avoid collisions with non-brief things and open up the space a bit
        }

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
    def add(self, chars, space, shift):
        self.buffer_write += 1
        self.buffer_write %= self.BUFFER_SIZE
        self.buffer[self.buffer_write] = (chars, space, shift)
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
        self.space_buffered = False
        self.next_shift = False
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

        attach_left = False
        attach_right = True # maybe unused for now
        end_sentence = False

        blocks = ["".join([c for c in keys if self.chord[c]]) for keys in groups]
 
        # Alternate 2nd and 3rd blocks get enabled when the other block is empty
        alt_2nd = len(blocks[2]) == 0

        # Straight join for specials
        pressed = "".join(blocks)

        print(blocks)
        print(pressed)
        #print(f"Status: 2nd {alt_2nd}")

        if pressed == "":
            return ""
        elif pressed == "U":
            # backspace
            keys, self.space_buffered, self.next_shift = self.rewind.backspace()
            return [KC.BSPC] * keys
        elif pressed == "ea":
            # space
            self.space_buffered = False
            # TODO: rewind
            return [KC.SPC]
        elif pressed == "XRea":
            # Cancel space
            self.space_buffered = False
            return []
        elif pressed == "FZzf":
            # TODO: rewind
            self.space_buffered = False
            return [KC.ENTER] # TODO: set up a dictionary for this instead.
        elif pressed == "zcs":
            self.next_shift = True
            return ""
        elif pressed == "SZCzcs":
            self.next_shift = False
            return ""
        #elif pressed == "NX":
            # TODO: rewind
            # TODO: not useful
            # TODO: 
        #    self.next_shift = True
        #    return [DVP['DOT'], DVP['SPC']]
        elif pressed in specials:
            special = specials[pressed]
            if isinstance(special, OutputStroke):
                end_sentence = special.end_sentence
                attach_left = special.attach_left
                attach_right = special.attach_right # maybe unused
                space = not special.attach_right # Do this directly instead of attach_right
                if special.ignore_shift:
                    self.next_shift = False

                special = specials[pressed].keycode
            else:
                if isinstance(special, str):
                    space = True

            if isinstance(special, Key):
                block_output = [special]
            else:
                block_output = special
        else:
            pressed = "!".join(blocks)
            if blocks[1] == 'X' and not alt_2nd:
                # leading S
                blocks[1] = blocks[0]
                blocks[0] = 'X'
                pressed = "!".join(blocks)

        # The pdf has FZNX as indent, so it's available... but I'm not sure I want to flip my vowel block

            # TODO: unnecessary check
            if blocks[3] == "zcs":
                # Actually not next, it's this round
                self.next_shift = True
                blocks[3] = ''
                pressed = "!".join(blocks)

            # This part of the documentation is unclear. What's the actual trigger to end the word?
            # Maybe this logic is correct and the correct way is just to make sure the final stroke is [4] only?
            if len(blocks[0]) == 0 and len(blocks[1]) == 0 and len(blocks[2]) == 0 and len(blocks[3]) > 0:
                space = True
                # TODO: maybe continuous 4th-only blocks shouldn't trigger this (so -n/-n generates 'nn', not 'n n'
                # The only English single-letter words are vowels
                # Should  probably rework the auto spacing logic overall
                # something like self.space_buffered = False
                # More like, attach_right is true...?
                attach_left = True

            while idx < len(pressed):
                initial_idx = idx
                #print("Check: ", pressed[idx:])

                if alt_2nd:
                    generated = False
                    # I wonder if linear search through the whole word list is too slow
                    for stroke, out in dictionary_2nd:
                        # This duplicated check is dumb
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
                    char = pressed[idx]
                    if char != '!':
                        block_output += list(char)
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
                        # maybe this is a bit filthy
                        if len(target) > 0 and target[0] == '\'':
                            attach_left = True
                            # This is different from single quote (which may include a space)

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
                    char = pressed[idx]
                    if char != '!':
                        block_output += list(char)
                    idx += 1

        if add_e:
            block_output += 'e'
        keystrokes = [c if isinstance(c, Key) else DVP[c] for c in block_output]

        if (self.next_shift and
                not isinstance(keystrokes[0], ModifiedKey) and
                not isinstance(keystrokes[0], ModifierKey)):
            keystrokes[0] = KC.LSFT(keystrokes[0])

        if self.space_buffered and not attach_left:
            keystrokes = [KC.SPC] + keystrokes
        
        self.rewind.add(len(keystrokes), self.space_buffered, self.next_shift)

        self.space_buffered = end_sentence or space # (space and not attach_right)

        # wtf is k
        if self.word_caps:
            keystrokes = [KC.LSFT(k) if
                        (k != KC.SPC and
                        not isinstance(k, ModifiedKey) and
                        not isinstance(k, ModifierKey))
                        else k
                        for k in keystrokes]
            self.word_caps_tripped = True

        self.next_shift = end_sentence

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
            if self.pressing:
                output = self.chord.result()
                #print("Output: ", output)
                self.handle_output(output)
                #self.chord.reset()
                self.pressing = False
            self.chord.discard(code)


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
