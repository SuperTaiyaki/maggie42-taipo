# This file is from a GPL2 repository, hence the overall license.

# Actually this file is no longer Taipo, it's a (modified) CyKey layout

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

debug = Debug(__name__)
# Define keys first so they can be used below in DVP
class TaipoKey(Key):
    def __init__(self, code): # Meta has apparently disappeared (kmk docs are old)
        self.taipo_code = code
        super().__init__()

# Can this be changed to bits? Should it be?
# l/r
# t/b -> finger (OR modifier.... actually that's kind of bad)
# might gain a tiny bit of performance over the current /10 and %10, but it's not massive (probably)
# 133mhz core, I don't think we need it

taipo_keycodes = {
    'TP_TLP': 0, # = top row, left, pinkie
    'TP_TLR': 1, # ring
    'TP_TLM': 2, # middle
    'TP_TLI': 3, # index?
    'TP_BLP': 4,
    'TP_BLR': 5,
    'TP_BLM': 6,
    'TP_BLI': 7,
    'TP_LIT': 8, # inner thumb
    'TP_LOT': 9, # outer thumb (and I have one more thumb, amongst other stuff)
    'TP_LUT': 10, # upper thumb

    'TP_TRP': 16,
    'TP_TRR': 17,
    'TP_TRM': 18,
    'TP_TRI': 19,
    'TP_BRP': 20,
    'TP_BRR': 21,
    'TP_BRM': 22,
    'TP_BRI': 23,
    'TP_RIT': 24,
    'TP_ROT': 25,
    'TP_RUT': 26,

    # If you assign any of these the logic will break
    'LAYER0': 42, # the actual order doesn't matter
    'LAYER1': 27,
    'LAYER2': 28,
    'LAYER3': 29,
    'MOD_GA': 30, # GUI+ALT
    'MOD_GC': 31, # GUI + CTRL
    'MOD_GS':  33,
    'MOD_AC':  34,
    'MOD_AS':  35,
    'MOD_CS':  36,
    'MOD_GAC': 37,
    'MOD_GAS': 38,
    'MOD_GCS': 39,
    'MOD_ACS': 40,
    'MOD_GACS': 41, # etc.
};

# This should probably happen outside the module instead - this is a bit late
for key, code in taipo_keycodes.items():
    make_key(names=(key,), constructor=TaipoKey, code=code)


# no enum class in circuitpython! oh well
# Reverse mapping to get correct taipo keystrokes to come out in dvorak
# This should probably have done another way so it's switchable (i.e. reverse just by dropping KC back in)
# Can replace the DV = below with KC, maybe
class DVP():
    def __init__(self):
        self.A = KC.A
        self.AMPR = KC.AMPR
        self.ASTR = KC.ASTR
        self.AT = KC.AT
        self.AUDIO_VOL_DOWN = KC.AUDIO_VOL_DOWN
        self.AUDIO_VOL_UP = KC.AUDIO_VOL_UP
        self.B = KC.N
        self.BRIGHTNESS_DOWN = KC.BRIGHTNESS_DOWN
        self.BRIGHTNESS_UP = KC.BRIGHTNESS_UP
        self.BSLS = KC.BSLS
        self.BSPC = KC.BSPC
        self.C = KC.I
        self.CIRC = KC.CIRC # ^
        self.COLN = KC.Z # uhhhh does this work? since it's a shifted key
        self.COMM = KC.W
        self.D = KC.H
        self.DEL = KC.DEL
        self.DLR = KC.DLR
        self.DOT = KC.E
        self.DOWN = KC.DOWN
        self.DQT = KC.LSFT(KC.Q)# doublequote - but it's shifted... TODO
        self.E = KC.D
        self.END = KC.END
        self.ENTER = KC.ENTER
        self.EQL = KC.RBRACKET
        self.ESC = KC.ESC
        self.EXLM = KC.EXLM # ? 
        self.F = KC.Y
        self.F1 = KC.F1
        self.F10 = KC.F10
        self.F11 = KC.F11
        self.F12 = KC.F12
        self.F2 = KC.F2
        self.F3 = KC.F3
        self.F4 = KC.F4
        self.F5 = KC.F5
        self.F6 = KC.F6
        self.F7 = KC.F7
        self.F8 = KC.F8
        self.F9 = KC.F9
        self.G = KC.U
        self.GRV = KC.GRV
        self.H = KC.J
        self.HASH = KC.HASH
        self.HOME = KC.HOME
        self.I = KC.G
        self.INS = KC.INS
        self.J = KC.C
        self.K = KC.V
        self.L = KC.P
        self.LABK = KC.LABK
        self.LALT = KC.LALT
        self.LAYER0 = KC.LAYER0
        self.LAYER1 = KC.LAYER1
        self.LAYER2 = KC.LAYER2
        self.LAYER3 = KC.LAYER3
        self.LBRC = KC.LBRC
        self.LCBR = KC.LCBR
        self.LCTL = KC.LCTL
        self.LEFT = KC.LEFT
        self.LGUI = KC.LGUI
        self.LPRN = KC.LPRN
        self.LSFT = KC.LSFT
        self.M = KC.M
        self.MINS = KC.QUOTE # minus
        self.MOD_AC = KC.MOD_AC # ARGH this isn't defined yet
        self.MOD_ACS = KC.MOD_ACS
        self.MOD_AS = KC.MOD_AS
        self.MOD_CS = KC.MOD_CS
        self.MOD_GA = KC.MOD_GA
        self.MOD_GAC = KC.MOD_GAC
        self.MOD_GACS = KC.MOD_GACS
        self.MOD_GAS = KC.MOD_GAS
        self.MOD_GC = KC.MOD_GC
        self.MOD_GCS = KC.MOD_GCS
        self.MOD_GS = KC.MOD_GS
        self.N = KC.L
        self.N0 = KC.N0
        self.N1 = KC.N1
        self.N2 = KC.N2
        self.N3 = KC.N3
        self.N4 = KC.N4
        self.N5 = KC.N5
        self.N6 = KC.N6
        self.N7 = KC.N7
        self.N8 = KC.N8
        self.N9 = KC.N9
        self.NO = KC.NO
        self.O = KC.S
        #self.OS(mod = KC.OS(mod
        self.P = KC.R
        self.PERC = KC.PERC
        self.PGDN = KC.PGDN
        self.PGUP = KC.PGUP
        self.PIPE = KC.PIPE
        self.PLUS = KC.PLUS # shifted TODO
        self.PRINT_SCREEN = KC.PRINT_SCREEN
        self.Q = KC.X
        self.QUES = KC.LSFT(KC.LBRACKET) # shifted. It puts out a capital Z, so it should be ... 
        self.QUOT = KC.Q
        self.R = KC.O
        self.RABK = KC.RABK
        self.RALT = KC.RALT
        self.RBRC = KC.RBRC
        self.RCBR = KC.RCBR
        self.RIGHT = KC.RIGHT
        self.RPRN = KC.RPRN # right paren
        self.S = KC.SCLN # probably?
        self.SCLN = KC.Z
        self.SLSH = KC.LBRACKET
        self.SPC = KC.SPC
        self.T = KC.K
        self.TAB = KC.TAB
        self.TILD = KC.TILD # shifted
        self.U = KC.F
        self.UNDS = KC.UNDS # shifted
        self.UP = KC.UP
        self.V = KC.DOT
        self.W = KC.COMMA # wut, not used in the main map?
        self.X = KC.B
        self.Y = KC.T
        self.Z = KC.SLASH
DV = DVP()


# These are taipo key names, they don't make much sense for Cykey
r = 1 << 0 # ahhhh, these are the stock single-finger character codes
s = 1 << 1 # un-mirroring each hand will be a bit tricky like this... (if I want smarter hjkl layout)
n = 1 << 2
i = 1 << 3
a = 1 << 4
o = 1 << 5
t = 1 << 6
e = 1 << 7
it = 1 << 8
ot = 1 << 9

# Changes to make to the layout:
# P is a pain, swap it with something less useful (maybe P/Z)
# Apart from that.... nothing, really?
# M and R are also not great (4 fingers for M, 3 for R). What's open?
# There are only 31 combinations available, there's not much open...
# Oh what the hell punctuation get 3 characters!
# Punctuation beats VKXJQZ
# Q is taking up a damn valuable slot!
# So, drop m? into the Q slot? or R?
# Don't forget that Q leads into U
# V is also damn low, put R in there
# and then put M into Q
# Don't want to touch K because it's an important command
# J is useless, use that for M?
# Z is easy to type too


# and then R-M-V
# But need to bring in another low-utility character...

# For left hand
# P [x] [ ] [ ] [x]_[ ]
# M [x] [ ] [x] [ ]_[x]
# V [ ] [x] [ ] [x]_[x]
# Z [x] [x] [x] [x]_[ ]

# AH CRAP I meant to reassign P
# Swap P and Q because it's easier to remember
# R [x] [ ] [x] [ ]_[ ]
# Q [x] [x] [x] [x]_[x]
# Looks good! I guess

# 'er' is a high frequency diagram, removing the overlap (swap R/P?) might be better
# ehhhh there are a lot of those in this keymap anywya... but er/re are high frequency so fixing them might be better
# Do it sooner than later!

class KeyPress:
    keycode = KC.NO
    hold = False
    hold_handled = False
    
class State:
    combo = 0
    timer = 0

    releasing = False # whether this is the pressing or releasing part of the sequence
    # the first release after a series of presses triggers the key; the following releases do not

    # Anti-ghost (sort of) stuff. On quick presses the keyup may come after the keydown - wind time back
    last_combo = 0 # combo as of One step before
    last_keypress_timestamp = 0

    key = KeyPress()

# Alternate no-lift keymap stuff:
# ot alone is a modifier (next is shift)
# Ah crap the various modes don't exist...
# Let's just implement this and try. If ot is pressed, shift the keymap up 4 (forget it and ot for now)

# Early confusion: Wow this is nice
# Now, how to make the shift and various other modes work?
# space tap for space, space tap for caps... wait wut
# ahhhh it's command not space
# so that's it (uh oh), 


class Taipo(Module):
    # sticky_timeout is now configured in the stickykeys module, this is unused
    def __init__(self, tap_timeout=600, sticky_timeout=1000, ghost_timeout=50):
        self.tap_timeout = tap_timeout
        self.sticky_timeout=sticky_timeout
        self.ghost_timeout = ghost_timeout
        self.state = [State(), State()]

# One thing I want to work on: enter is not safe! It's too close to backspace, liable to do it accidentally
# Will be better once I remember K...

# Will want left/right for text editing
# could sneak them into the top layer but it has something...
# [F] and [K], but they're not write for modern systems
# oh hey [H] and [L] are in the right places (and only one key apart)
# [P] and [H] are also mode switches, a bit hard to reach

        self.keymap = { # KEYMAP_START
            it: DV.LSFT, # Next char is capital
            ot: DV.SPC,
            
            ot | e: DV.I,
            ot | e | a: DV.L,
            a | o: DV.G,
            ot | o | a: DV.J,
            e | o: DV.T,
            a | ot: DV.H,
            e: DV.E,
            t: DV.O,
            o: DV.S,
            a: DV.U,
            e | t: DV.A,
            t | o: DV.N,
            ot | e | o: DV.V,
            ot | o: DV.K,
            ot | e | t | o: DV.F,
            e | t | o | a: DV.Z,
            ot | e | t: DV.D,
            t | o | a: DV.B,
            ot | t: DV.C,
            t | a: DV.R,
            ot | e | t | o | a: DV.Q,
            e | a: DV.P,
            ot | t | o: DV.Y,
            ot | t | o | a: DV.X,
            ot | e | o | a: DV.W,
            ot | t | a: DV.M,

            # These two are also in the punctuation mode...?
            # (and space)
            e | o | a: DV.COMM,
            e | t | o: DV.DOT,

            # Not in the original layout, but since I have more keys...
            i: DV.N1,
            i | ot: DV.N2,
            i | ot | n: DV.N3,
            i | ot | n | s: DV.N4,
            i | ot | n | s | r: DV.N5,
            r: DV.N6,
            r | s: DV.N7,
            r | s | t: DV.N8,
            r | s | t | i: DV.N9,
            n: DV.N0,
            # And then add their shifted symbols on top with... uhh.... the same shift logic! so hold IT or replace OT with IT

            # Shifted commands
            it | o: DV.BSPC, # [K] bacK
            it | t: DV.ENTER, # [C] Carriage return

            # These are not from the official layout
            it | a: DV.LEFT, # H
            it | a | e: DV.RIGHT, # L


        } # KEYMAP_END

        self.keymap_symbol = {
            ot | e | o | a: KC.LSFT(DV.SCLN),
            ot | e | o: DV.SCLN,
            #ot | t | a: DV.PERCENT, # TODO
            # uh oh, maybe I should put weird symbols onto numbers?
            # And there are a few symbols missing, maybe expand the layout for those
            # upper row for numbers...?

            }

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        for side in [0, 1]:
            # SO: if it's timed out (300ms) send the key
            # BUT that's when hold becomes true, and we need to hit the hold point in order to reach the combo logic
            if self.state[side].timer != 0 and ticks_ms() > self.state[side].timer:
                self.state[side].key.keycode = self.determine_key(self.state[side].combo)
                self.state[side].key.hold = True
                self.handle_key(keyboard, side)
                self.state[side].timer = 0

    def after_matrix_scan(self, keyboard):
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, TaipoKey):
            return key

        side = 1 if key.taipo_code & 0x10 != 0 else 0
        code = key.taipo_code # Forgot to use this?
        if is_pressed:
            if self.state[side].key.keycode != KC.NO:
                self.handle_key(keyboard, side)
                self.clear_state(side)

            self.state[side].last_combo = self.state[side].combo
            self.state[side].last_keypress_timestamp = ticks_ms()

            # And if the current state is clear (no key determined yet) it gets added to the combo and the timer starts

            self.state[side].combo |= 1 << (key.taipo_code & 0xF)
            self.state[side].timer = ticks_ms() + self.tap_timeout

            self.state[side].releasing = False
        else:

            anti_ghost = False

            if not self.state[side].key.hold and not self.state[side].releasing:
                # Key was not pressed long enough to trigger 'hold'

                combo = self.state[side].combo
                if (self.state[side].last_keypress_timestamp > ticks_ms() - self.ghost_timeout and
                    self.state[side].last_combo != 0):
                    combo = self.state[side].last_combo
                    self.state[side].last_keypress_timestamp = 0
                    anti_ghost = True

                self.state[side].key.keycode = self.determine_key(combo)

            # Combo key that has never triggered a combo does create a keystroke
            # Combo key that was part of a combo and is released at the end won't trigger a keystroke
            self.handle_key(keyboard, side)

            self.state[side].combo &= ~(1 << (key.taipo_code & 0xF))

            if anti_ghost:
                self.state[side].releasing = False
            else:
                self.state[side].releasing = True

            self.clear_state(side)

    def clear_state(self, side):
        # why does this not work?
        # self.state[side] = State()
        #self.state[side].combo = 0
        self.state[side].timer = 0
        self.state[side].key.keycode = KC.NO
        self.state[side].key.hold = False
        self.state[side].key.hold_handled = False
        
    def handle_key(self, keyboard, side):
        key = self.state[side].key
        mods = []

        # Should these be KC?
        if key.keycode in [ DV.LGUI, DV.LALT, DV.RALT, DV.LCTL, DV.LSFT ]:
            mods = [key.keycode]
        elif key.keycode == KC.MOD_GA:
            mods = [KC.LGUI, KC.LALT]
        elif key.keycode == KC.MOD_GC:
            mods = [KC.LGUI,KC.LCTL]
        elif key.keycode == KC.MOD_GS:
            mods = [KC.LGUI,KC.LSFT]
        elif key.keycode == KC.MOD_AC:
            mods = [KC.LALT,KC.LSFT]
        elif key.keycode == KC.MOD_AS:
            mods = [KC.LALT,KC.LSFT]
        elif key.keycode == KC.MOD_CS:
            mods = [KC.LCTL,KC.LSFT]
        elif key.keycode == KC.MOD_GAC:
            mods = [KC.LGUI,KC.LALT,KC.LSFT]
        elif key.keycode == KC.MOD_GAS:
            mods = [KC.LGUI,KC.LALT,KC.LSFT]
        elif key.keycode == KC.MOD_GCS:
            mods = [KC.LGUI,KC.LCTL,KC.LSFT]
        elif key.keycode == KC.MOD_ACS:
            mods = [KC.LALT,KC.LCTL,KC.LSFT]
        elif key.keycode == KC.MOD_GACS:
            mods = [KC.LGUI,KC.LALT,KC.LCTL,KC.LSFT]

        if len(mods) > 0:
            for mod in mods:
                if key.hold_handled:
                    keyboard.remove_key(mod)
                elif key.hold:
                    keyboard.add_key(mod)
                    self.state[side].key.hold_handled = True
                else:
                    keyboard.tap_key(KC.SK(mod, defer_release = True))
                    # defer_release is needed to hold the ctrl until the taipo key code is emitted
                    # without that it would release the key as soon as a physical key is emitted, which is wrong
        else:
            if key.hold_handled:
                keyboard.remove_key(key.keycode)
            elif key.hold:
                keyboard.add_key(key.keycode)
                self.state[side].key.hold_handled = True
            else:
                keyboard.tap_key(key.keycode)
        
    def determine_key(self, val):
        # LUT/RUT aren't used in combos, they just trigger combos
        actual_val = val & ~(1 << 10)
        if actual_val in self.keymap:
            return self.keymap[actual_val]
        else:
            return KC.NO
       
    def before_hid_send(self, keyboard):
        pass

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

# I think the reason I dislike pinkie-high combos is
# To make the pinkie reach I raise my whole hand, and then crunch everything else back down
# that movement in particular is bad
# tenting helps a lot with that
# ahhhhh the raised wrist thing
# Need tenting if I'm using a wide grip, normal tight keyboard grip my wrists can roll around

# Where'd my comments go, about designing a fresh layout...
# So, no diagonals!
# it feels like j/k should have higher priority than m/w
# K is actually really low! 
# K/W are about even, actually
# At the tail end we have:
# worst: Z/Q
# Then: V/X
# Then: J/K
# Then the normal stuff
# They're all so low that it doesn't matter, but the sequences matter...
# Bigram chart! See Norvig (https://norvig.com/mayzner.html)
# THE is important, not being able to roll that is annoying
#   Some special behaviour for this (slow roll?) might help
# Ideally I'd like E to be in the dvorak location, since muscle memory
# t/h/e/r being on the same row would maybe help efficiency? But then other stuff goes weird
# So it feels like the level switch is slowing me down (compared to dvorak...) but is that the biggest problem?
# I want full homing dots on one row...

