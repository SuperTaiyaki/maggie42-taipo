# This file is from a GPL2 repository, hence the overall license.

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

class TaipoMacro(TaipoKey):
    def __init__(self, output): # Meta has apparently disappeared (kmk docs are old)
        self.output = output
        super().__init__('TP_MACRO')

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

    'LAYER1': 11, # actually having these not bound no either side isn't great...
    'LAYER2': 12, # this keyboard isn't for 2-handed use anyway (maybe)
    'LAYER3': 13,

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

    'MOD_N': 43, # Cykey-specific
    'MOD_N_LOCK': 45, # Cykey-specific
    'MOD_S': 47,
    'MOD_S_LOCK': 48,
    'MOD_SHIFT': 46,
    'MOD_CLEAR': 44,

};

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
        self.COLN = KC.LSFT(KC.Z) # uhhhh does this work? since it's a shifted key
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

        self.MINUS = KC.QUOT,
        self.EQUAL = KC.LSFT(KC.RBRACKET),
        #self.DOUBLE_QUOTE = KC.LSFT(KC.Q), # When I send one of these to the Taipo code it explodes. WHY.
        self.QUESTION = KC.LSFT(KC.LBRACKET),

# DV = KC # To get a straight QWERTY mappign. Maybe!
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
ut = 1 << 10
s1 = 1 << 11
s2 = 1 << 12
s3 = 1 << 13

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
# #Q [x] [x] [x] [x]_[x] # Removed
# Looks good! I guess

# 'er' is a high frequency digram, removing the overlap (swap R/P?) might be better
# ehhhh there are a lot of those in this keymap anywya... but er/re are high frequency so fixing them might be better
# Do it sooner than later!
# -> r is a-t so that it can roll to and from e

# Swap U and A since that's how taipo does it. A has much higher frequency than U;
# mostly for comfort. Will affect some digrams...
# Purely for familiarity, A on pinkie and U on pair feels closer to taipo
# Is there much benefit?
# A is on a strong pair...
# -> +1 keystroke of efficiency, may as well do it

# I don't like Q (full press), it's just awkward. Is there another open chord?
# Punctuation... swap with exclamation mark? That seems appropriate
# Actually that chord is quite nice, does something else need to be upgraded? maybe F? Not a huge difference, meh.
# But that was [Y]
# Q [X] [_] [X] [X]_[ ]
# ! [x] [x] [x] [x]_[x]
# This Q can't roll to U, though that's not a huge deaal

# C and R changed, to move R to the stronger side. Improves some transitions slightly.
# R is about twice is frequent
# C [X] [ ] [X] [ ] [ ]_[ ]
# R [ ] [ ] [X] [ ] [X]_[ ]

# Move enter ([C] to upper layer, cmd + middle-upper (I guess it doesn't have a name, but would be [O])

# Something else to try: swap B and D around
# with the C/R switch, it feels like the left side of the hand is a bit... light
# Come to think of it, G is prime real estate (the worst of the pairs). Upgrade ... F? and throw it there?
# G is higher according to wikipedia!
# OK, so just b/d
# No effects of note (I guess keep it...?)
# D is much more common!


# Can I do a dollar sign...?
# no, the shift switch drops the mode....
# also need a hard tab

class KeyPress:
    keycode = KC.NO
    hold = False
    hold_handled = False

LAYER_NORMAL = const(0)
LAYER_N = const(1) # numeric
LAYER_S = const(2) # symbol
LAYER_LOCK = const(1 << 20)
 
class State:
    combo = 0
    timer = 0

    releasing = False # whether this is the pressing or releasing part of the sequence
    # the first release after a series of presses triggers the key; the following releases do not

    # Anti-ghost (sort of) stuff. On quick presses the keyup may come after the keydown - wind time back
    last_combo = 0 # combo as of One step before
    last_keypress_timestamp = 0

    shifted = LAYER_NORMAL
    shift = 0

    key = KeyPress()


class Cykey(Module):
    # sticky_timeout is now configured in the stickykeys module, this is unused
    # TODO: take an RGB and use it to display the current shift mode
    def __init__(self, rgb = None, tap_timeout=600, sticky_timeout=1000, ghost_timeout=50):
        self.rgb = rgb
        self.tap_timeout = tap_timeout
        self.sticky_timeout=sticky_timeout
        self.ghost_timeout = ghost_timeout
        self.state = [State(), State()]

        self.send_next = []

# One thing I want to work on: enter ([C] for carriage return) is not safe! It's too close to backspace, liable to do it accidentally
# Will be better once I remember K...

# Will want left/right for text editing
# could sneak them into the top layer but it has something...
# [F] and [K], but they're not write for modern systems
# oh hey [H] and [L] are in the right places (and only one key apart)
# [P] and [H] are also mode switches, a bit hard to reach


        keymap_main = { # KEYMAP_START
            it: KC.MOD_SHIFT, # Next char is capital
            ot: DV.SPC, # is this a permanent...?
            it | e | o: DV.TAB, # [T]
            # These two are also in the punctuation mode...?
            # (and space)
            e | o | a: DV.COMM,
            e | t | o: DV.DOT,
            # Wasn't there one or two more...?
            it | t | o: KC.MOD_N,  # [Y]/[N]
           #it | n | s: KC.MOD_N_LOCK, # This is here because shift logic swaps the rows around - can't double tap [N] otherwise
            it | t | a: KC.MOD_S, # [C]/[M] mod_s layer: left/right brackets, easily accessible arrow keys...

            a | it: KC.ESC, # [H] for escape (or [A], either way)

            ot | e: DV.I,
            ot | e | a: DV.L,
            a | o: DV.G,
            ot | o | a: DV.J,
            e | o: DV.T,
            a | ot: DV.H,
            e: DV.E,
            t: DV.O,
            o: DV.S,
            a: DV.A,
            e | t: DV.U,
            t | o: DV.N,
            ot | e | o: DV.V,
            ot | o: DV.K,
            ot | e | t | o: DV.F,
            e | t | o | a: DV.Z,
            ot | e | t: DV.B,
            t | o | a: DV.D,
            ot | t: DV.R,
            t | a: DV.C,
            e | a: DV.P,
            ot | t | o: DV.Y,
            ot | t | o | a: DV.X,
            ot | e | o | a: DV.W,
            ot | t | a: DV.M,
            e | t | a: DV.Q,

            # Non-permanent punctuation
            #e | t | a: KC.QUOT, # DV.MINUS, DV.MINUS doesn't work!
            ot | e | t | a: DV.QUOT,
            ot | e | t | o | a: KC.EXCLAIM,

            # Experimental bigram macros
            # TODO: simplify these
            # [T] -> TH, [H] -> HE (escape needs to go somewhere else), [I] for IN...?
            # [R] for ER is possible but hard to catch. Maybe leave that as-is
            it | o | e: TaipoMacro([DV.T, DV.H]), # actually these probably shouldn't be descended from TaipoKey
            it | a | e: TaipoMacro([DV.H, DV.E]),
            it | o | t | e: TaipoMacro([DV.I, DV.N]),
            it | t | e: TaipoMacro([DV.E, DV.R]),

        }

        keymap_numbers = {
            it | t | o: KC.MOD_N_LOCK,  # [Y]/[N]

            # Not in the original layout, but since I have more keys...
            # This is mostly useful because they can be shifted for symbols
            e: DV.N1,
            e | ot: DV.N2,
            e | ot | t: DV.N3,
            e | ot | t | o: DV.N4,
            e | ot | t | o | a: DV.N5,
            a: DV.N6,
            a | o: DV.N7,
            a | o | t: DV.N8,
            a | o | t | e: DV.N9,
            t: DV.N0,

            ot | a | o | e: DV.COLN,
            ot | o | e: DV.SCLN,
            ot | o | a: DV.EQUAL, # "J"ust the same
            a | t: KC.LEFT_PAREN,
            t | ot: KC.RIGHT_PAREN,
            ot | a: KC.QUOT, # DV.MINUS, # Don't know why this doesn't work via DV.

            # LSFTing stuff doesn't work in here - need to use the constructor directly.
            t | o: KC.LSFT(KC.Q), # DOUBLE_QUOTE
            e | t | a: KC.EXCLAIM, # Wasn't this in the top layer...? (all five)
            ot | t | o:  KC.LSFT(KC.LBRACKET), # QUESTION,
            ot | o: DV.BSLS, # re-slanted because left hand
            a | e: DV.SLSH,
            # TODO: need an escape key somewhere (or just a hardware escape...
        } # KEYMAP_END

        keymap_permanent = {
            # Shifted commands
            # These seem to be permanents in Microwriter
            it | o: DV.BSPC,
            #it | t: DV.ENTER, # [C] Carriage return
            it | n: DV.ENTER, # [C] Carriage return
            # Want an escape here just in case I happen to be vim-ing for some reason...
            it | i: DV.ESC, # [E] for escape (level shifted up)

            it | ot: KC.MOD_CLEAR,
            s1: KC.MOD_CLEAR, # Since mashing thumbs together on this board is an annoying reach
            s2: KC.MOD_N,
            s3: KC.MOD_S,
            s1 | s2 | s3: DV.ENTER,
            s1 | s2 | o: DV.ENTER, # since the mapping changed ugh

            # Taipo arrow keys since they don't clash
            ot | t | n : DV.UP,
            ot | o | s : DV.DOWN,
            ot | a | r : DV.LEFT,
            ot | e | i : DV.RIGHT, # why is this not DV? oh well

            # Taipo modifier block since it works well
            t | n : DV.LCTL,
            o | s : DV.LALT,
            a | r : DV.LGUI,
            e | i : KC.LSFT, # why is this not DV? oh well
            r | a | s | o: KC.MOD_GA,
            r | a | n | t: KC.MOD_GC,
            r | a | i | e: KC.MOD_GS,
            s | o | n | t: KC.MOD_AC,
            s | o | i | e: KC.MOD_AS,
            n | t | i | e: KC.MOD_CS,
            r | a | s | o | n | t: KC.MOD_GAC,
            r | a | s | o | i | e: KC.MOD_GAS,
            r | a | n | t | i | e: KC.MOD_GCS,
            s | o | n | t | i | e: KC.MOD_ACS,
        }

        keymap_extra = {
            it | t | a: KC.MOD_S_LOCK, # [C]/[M] mod_s layer: left/right brackets, easily accessible arrow keys...
            # delete, insert, home, end, pgup, pgdn... where's my tilde?
            # F keys?

            a | t: KC.MINUS, # [
            t | ot: KC.EQUAL, # ]
            a | o: KC.LSFT(KC.MINUS), # {
            e | ot: KC.LSFT(KC.EQUAL), # }
            # <
            # >
            # T -> ~ ?

            # And then fill this layer with other things that might be useful without having to shift-number or whatever

            # Maybe put F keys in the top row - they're not frequently used to a stretch is fine
        }

        # inspired by reddit: common word macros
        # macro shift - w looks like 'the', d looks like 'and'
        # that, with, at least four letters
        # non-macro layer, command buttons would be better... otherwise efficiency sucks. is [D] used for anything?
        # [X]/[D] for and
        # [W]/[,] for the
        # Even better, can start typing and as long as I don't press the thumb first can switch to macro partway through
        # OR: TH/HE as commands instead. Not a huge improvement... but common enough to be useful?
        # IN/ER would be next
        # I think they're all available...
        # I guess .... just record them straight into the table?
        # Logic needs to be smart enough to shift only the first character

        def bitswap(val):
            high = val & 0xF0
            low = val & 0x0F
            mods = val & 0xFF00 # Actually there are only 2 bits
            return mods | high >> 4 | low << 4

        # Might be better to define this as main set, number set, then merge them as number set bitswapped
        # So I can keep merged layers for other stuff
        self.keymap = keymap_permanent | keymap_main | {bitswap(combo): result for combo, result in keymap_numbers.items()}
        self.keymap_layer1 = keymap_permanent | keymap_numbers | {bitswap(combo): result for combo, result in keymap_main.items()}
        self.keymap_layer2 = keymap_permanent | keymap_extra | {bitswap(combo): result for combo, result in keymap_main.items()}

        # Standard modes are U (upper), N (numeric), P (extended printable)
        # TODO: maybe auto generate this by flipping the main keymap and have real layers
        # Since layer 3 is going to be something else entirely
        # ALSO: Pull in layer 3 chars from quirkey, they look reasonable
        # In theory I have <, > since they're on , and . but hard to remember...
        # Have B/D, R/C, maybe s/e to use as directionals


    def rgb_neutral(self):
        if self.rgb:
            self.rgb.set_hsv_fill(176, 140, 90)
            self.rgb.show()
        pass
    def rgb_moden(self):
        if self.rgb:
            self.rgb.set_hsv_fill(30, 200, 180)
            self.rgb.show()
        pass

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

                self.state[side].key.keycode = self.determine_key(combo, self.state[side].shifted)
                # If it's not a mod, keep it...?
                # Can shift-4 using the lock but this breaks it. Being able to go in either order would be nice...
                # so hold the shift lock here instead, can add a KC_LSHIFT inside the determine_key (maybe)
                # Shift kind of isn't a real modifier layer - it doesn't replace the others (so just another flag?)
                # Otherwise I need to fight with KC.SK
                # The original MW4 didn't really have a concept of shift, it's just another character map (I guess)
                # i.e. shifting a number is meaningless... maybe
                # I want to see the Quinkey manual...
                # Quirkey seems to do it that way
                #if self.state[side].key.keycode != KC.NO and self.state[side].shifted & LAYER_LOCK == 0:
                #    self.state[side].shifted = LAYER_NORMAL
                #    self.rgb_neutral()

            # Combo key that has never triggered a combo does create a keystroke
            # Combo key that was part of a combo and is released at the end won't trigger a keystroke
            self.handle_key(keyboard, side)

            # At some point I need logic to one-shot the mode shifts
            # But for now I have multiple rows to use so it doesn't actually matter
            self.state[side].combo &= ~(1 << (key.taipo_code & 0xF)) # Remove the released key from the combo block

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

        if isinstance(key.keycode, TaipoMacro):
            keyboard.tap_key(key.keycode.output[0])
            remain = key.keycode.output[1:]
            remain.reverse()
            self.send_next = remain
            return

        if key.keycode == KC.NO:
            return
        elif key.keycode == KC.MOD_N:
            self.state[side].shifted = LAYER_N
            self.rgb_moden()
            return
        # unfortunately the shifted state has been lost by here - this code does nothing
        elif key.keycode == KC.MOD_N_LOCK:
            self.state[side].shifted = LAYER_N | LAYER_LOCK
            return
        elif key.keycode == KC.MOD_S:
            self.state[side].shifted = LAYER_S
            self.rgb_moden() # TODO
            return
        elif key.keycode == KC.MOD_S_LOCK:
            self.state[side].shifted = LAYER_S | LAYER_LOCK
            return
        elif key.keycode == KC.MOD_CLEAR:
            self.state[side].shifted = LAYER_NORMAL
            self.state[side].shift = 0
            self.rgb_neutral()
            return
        elif key.keycode == KC.MOD_SHIFT:
            if self.state[side].shift == LAYER_S:
                self.state[side].shift = LAYER_S | LAYER_LOCK
            else:
                self.state[side].shift = LAYER_S
            return
            # guess we don't need to clear the shift state here

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
            # Oh hey this is maybe not good, the remove_key may not match
            code = key.keycode if self.state[side].shift == 0 else KC.RSFT(key.keycode)
            if self.state[side].shift & LAYER_LOCK == 0:
                self.state[side].shift = 0

            if self.state[side].shifted & LAYER_LOCK == 0:
                if self.state[side].shifted > 0:
                    print("Cancelled layer")
                    # AH FUCK on the release it passes through here...
                self.state[side].shifted = LAYER_NORMAL
                self.rgb_neutral()

            if key.hold_handled:
                keyboard.remove_key(code)
            elif key.hold:
                keyboard.add_key(code)
                self.state[side].key.hold_handled = True
            else:
                keyboard.tap_key(code)

    def determine_key(self, val, shifted = False):
        keymap = self.keymap
        if shifted & LAYER_N != 0:
            keymap = self.keymap_layer1
        elif shifted & LAYER_S != 0:
            keymap = self.keymap_layer2

        if val in keymap:
            return keymap[val]
        else:
            return KC.NO
       
    def before_hid_send(self, keyboard):
        if len(self.send_next) > 0:
            keyboard.tap_key(self.send_next.pop())

    def after_hid_send(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass

# Some stuff to do:
# Separate the keymaps into different files
# Try building a web app (touchscreen) to practice on this?
# Heck, even a web emulated MicroWriter!
