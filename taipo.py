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

# no enum class in circuitpython! oh well
# Reverse mapping to get correct taipo keystrokes to come out in dvorak
# This should probably have done another way so it's switchable (i.e. reverse just by dropping KC back in)
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
        self.COLN = KC.COLN # uhhhh does this work? since it's a shifted key
        self.COMM = KC.W
        self.D = KC.H
        self.DEL = KC.DEL
        self.DLR = KC.DLR
        self.DOT = KC.E
        self.DOWN = KC.DOWN
        self.DQT = KC.DQT # doublequote - but it's shifted... TODO
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

# Can this be changed to bits? Should it be?
# l/r
# t/b -> finger (OR modifier.... actually that's kind of bad)
# might gain a tiny bit of performance over the current /10 and %10, but it's not massive (probably)

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
    'TP_TRP': 10,
    'TP_TRR': 11,
    'TP_TRM': 12,
    'TP_TRI': 13,
    'TP_BRP': 14,
    'TP_BRR': 15,
    'TP_BRM': 16,
    'TP_BRI': 17,
    'TP_RIT': 18,
    'TP_ROT': 19,
    'LAYER0': 20,
    'LAYER1': 21,
    'LAYER2': 22,
    'LAYER3': 23,
    'MOD_GA': 24, # GUI+ALT
    'MOD_GC': 25, # GUI + CTRL
    'MOD_GS': 26,
    'MOD_AC': 27,
    'MOD_AS': 28,
    'MOD_CS': 29,
    'MOD_GAC': 30,
    'MOD_GAS': 31,
    'MOD_GCS': 32,
    'MOD_ACS': 33,
    'MOD_GACS': 34, # etc.
};
taipo_mods = {
        taipo_keycodes['TP_LIT'],
        taipo_keycodes['TP_LOT'],
        taipo_keycodes['TP_RIT'],
        taipo_keycodes['TP_ROT'],
}

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

class KeyPress:
    keycode = KC.NO
    hold = False
    hold_handled = False
    
class State:
    combo = 0 # the main 8 keys
    mods = 0 # use it / ot
    timer = 0
    combo_executed = False # Whether a key has been output using combo (i.e. non-mod key has been pressed)
    # the clear_state method should be in here, not in Taipo

    releasing = False # whether this is the pressing or releasing part of the sequence
    # the first release after a series of presses triggers the key; the following releases do not

    # Anti-ghost (sort of) stuff. On quick presses the keyup may come after the keydown - wind time back
    last_combo = 0 # combo as of One step before
    last_keypress_timestamp = 0

    key = KeyPress()

class TaipoMeta:
    def __init__(self, code):
        self.taipo_code = code

# TODO: put taipo_code in here directly, don't need meta
class TaipoKey(Key):
    def __init__(self, meta):
        self.meta = meta
        super().__init__()
    
class Taipo(Module):
    # sticky_timeout is now configured in the stickykeys module, this is unused
    def __init__(self, tap_timeout=300, sticky_timeout=1000, ghost_timeout=100):
        self.tap_timeout = tap_timeout
        self.sticky_timeout=sticky_timeout
        self.state = [State(), State()]
        # This should probably happen outside the module instead - this is a bit late
        for key, code in taipo_keycodes.items():
            make_key( names=(key,), constructor=TaipoKey, meta=TaipoMeta(code))

        self.keymap = {
            t: DV.T,
            t | e: DV.H,
            it: DV.BSPC,
            ot: DV.SPC,
            r: DV.R,
            r | ot: KC.LSFT(DV.R),
            r | it: DV.RABK,
            r | ot | it: DV.PRINT_SCREEN, # ewwwww
            s: DV.S,
            s | ot: KC.LSFT(DV.S),
            s | it: DV.RCBR,
            # s | ot | it: DV.BRIGHTNESS_UP, # ewwww
            n: DV.N,
            n | ot: KC.LSFT(DV.N),
            n | it: DV.RBRC,
            #n | ot | it: DV.BRIGHTNESS_DOWN,
            i: DV.I,
            i | ot: KC.LSFT(DV.I),
            i | it: DV.RPRN,
            #i | ot | it: DV.MEDIA_PLAY_PAUSE,
            a: DV.A,
            a | ot: KC.LSFT(DV.A),
            a | it: DV.LABK,
            #a | ot | it: DV.MEDIA_NEXT_TRACK,
            o: DV.O,
            o | ot: KC.LSFT(DV.O),
            o | it: DV.LCBR,
            # o | ot | it: DV.AUDIO_VOL_UP, # ewww, and I don't want OT+IT combos
            t: DV.T,
            t | ot: KC.LSFT(DV.T),
            t | it: DV.LBRC,
            # t | ot | it: DV.AUDIO_VOL_DOWN, # lol these aren't documented either, just the creator's bonuses?
            e: DV.E,
            e | ot: KC.LSFT(DV.E),
            e | it: DV.LPRN,
            #e | ot | it: DV.MEDIA_PREV_TRACK, # More importantly, can these be re-coded or re-expressed to be less annoying? Maybe not... though being able to express shift without this would be nice
            # Yeah, change to dynamically generating this
            e | o: DV.C,
            e | o | ot: KC.LSFT(DV.C),
            e | o | it: DV.N1,
            e | o | ot | it: DV.F1, # on the other hand, this is kind of useful.... actually, I have 3 modifiers so I can go further
            t | o: DV.U,
            t | o | ot: KC.LSFT(DV.U),
            t | o | it: DV.N2,
            t | o | ot | it: DV.F2,
            t | a: DV.M,
            t | a | ot: KC.LSFT(DV.M),
            t | a | it: DV.N3,
            t | a | ot | it: DV.F3,
            o | a: DV.L,
            o | a | ot: KC.LSFT(DV.L),
            o | a | it: DV.N4,
            o | a | ot | it: DV.F4,
            i | n: DV.Y,
            i | n | ot: KC.LSFT(DV.Y),
            i | n | it: DV.N5,
            i | n | ot | it: DV.F5,
            i | s: DV.F,
            i | s | ot: KC.LSFT(DV.F),
            i | s | it: DV.N6,
            i | s | ot | it: DV.F6,
            n | s: DV.P,
            n | s | ot: KC.LSFT(DV.P),
            n | s | it: DV.N7,
            n | s | ot | it: DV.F7,
            n | r: DV.W,
            n | r | ot: KC.LSFT(DV.W),
            n | r | it: DV.N8,
            n | r | ot | it: DV.F8,
            s | r: DV.B,
            s | r | ot: KC.LSFT(DV.B),
            s | r | it: DV.N9,
            s | r | ot | it: DV.F9,
            e | t: DV.H,
            e | t | ot: KC.LSFT(DV.H),
            e | t | it: DV.N0,
            e | t | ot | it: DV.F10,
            e | a: DV.D,
            e | a | ot: KC.LSFT(DV.D),
            e | a | it: DV.AT,
            e | a | ot | it: DV.F11,
            i | r: DV.G,
            i | r | ot: KC.LSFT(DV.G),
            i | r | it: DV.HASH,
            i | r | ot | it: DV.F12,
            t | r: DV.X,
            t | r | ot: KC.LSFT(DV.X),
            t | r | it: DV.CIRC,
            #t | r | ot | it: DV.LCTL(DV.X),
            i | o: DV.K,
            i | o | ot: KC.LSFT(DV.K),
            i | o | it: DV.PLUS,
            #i | o | ot | it: DV.LCTL(DV.C),
            e | s: DV.V,
            e | s | ot: KC.LSFT(DV.V),
            e | s | it: DV.ASTR,
            #e | s | ot | it: DV.LCTL(DV.V),
            n | a: DV.J,
            n | a | ot: KC.LSFT(DV.J),
            n | a | it: DV.EQL,
            #n | a | ot | it: DV.LCTL(DV.Z),
            e | r: DV.Z, # changed
            e | r | ot: KC.LSFT(DV.Z),
            e | r | it: DV.DLR,
            # e | r | ot | it: DV.NO,
            i | a: DV.Z,
            i | a | ot: KC.LSFT(DV.Z),
            i | a | it: DV.AMPR,
            # i | a | ot | it: DV.NO,
            t | s: DV.SLSH,
            t | s | ot: DV.BSLS,
            t | s | it: DV.PIPE,
            # t | s | ot | it: DV.NO,
            n | o: DV.MINS,
            n | o | ot: DV.UNDS,
            n | o | it: DV.PERC,
            # n | o | ot | it: DV.NO,
            i | t: DV.QUES,
            i | t | ot: DV.EXLM,
            # i | t | it: DV.NO,
            # i | t | ot | it: DV.NO,
            e | n: DV.COMM,
            e | n | ot: DV.DOT,
            # e | o | a: DV.DOT,
            e | n | it: DV.TILD,
            # e | n | ot | it: DV.NO,
            o | r: DV.SCLN,
            #t | o | a: DV.SCLN, # wait 2 semicolons? I guess for some languages this one isn't bad
            o | r | ot: DV.COLN,
            t | o | a | ot: DV.COLN,
            # o | r | it: DV.NO,
            # t | o | a | it: DV.NO,
            # o | r | ot | it: DV.NO,
            # t | o | a | ot | it: DV.NO,
            s | a: DV.QUOT,
            #n | s | r: DV.QUOT,
            s | a | ot: DV.DQT,
            n | s | r | ot: DV.DQT,
            s | a | it: DV.GRV,
            n | s | r | it: DV.GRV,
            # s | a | ot | it: DV.NO,
            # n | s | r | ot | it: DV.NO,
            i | n | s: DV.TAB,
            i | n | s | ot: DV.DEL,
            i | n | s | it: DV.INS,
            # i | n | s | ot | it: DV.NO,
            e | t | o: DV.ENTER,
            e | t | o | ot: DV.ESC,
            e | t | o | it: DV.RALT,
            # e | t | o | ot | it: DV.NO,
            a | r: DV.LGUI,
            a | r | ot: DV.RIGHT,
            a | r | it: DV.PGUP,
            a | r | ot | it: DV.LAYER3,
            o | s: DV.LALT,
            o | s | ot: DV.DOWN,
            o | s | it: DV.HOME,
            o | s | ot | it: DV.LAYER2,
            t | n: DV.LCTL,
            t | n | ot: DV.UP,
            t | n | it: DV.END,
            t | n | ot | it: DV.LAYER1,
            e | i: KC.LSFT, # AHHH these aren't kmk oneshots, they're taipo builtins
            e | i | ot: DV.LEFT,
            e | i | it: DV.PGDN,
            e | i | ot | it: DV.LAYER0,
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
            r | a | s | o | n | t | i | e: KC.MOD_GACS,
            e | t | a | o: DV.SPC, # Borrowed from Ardux, just to let my space finger float
            s | r | n | i: DV.BSPC, # Borrowed from Ardux, just to let my space finger float

            # experimental block
            r | s | n: DV.J, # up/down not vi style (K is more common, this is more comfortable)
            a | o | t: DV.K, # plus shift

            r | s | i: DV.X, # V points down
            a | o | e: DV.V, # middle finger up

            r | n | i: DV.Q, # ring finger gap
            a | t | e: DV.Z, # Q comes first so it's up on top
        }

    # Changes from stock:
    # * swap m/w
    # * move DOT to unshifted (probably swap with semicolon)
    # * add Ardux space/backspace 4-fingers
    # - use the... Z and Q (sn/at) with M and W, since I don't like those big diagonals
    #   I like the flat chords better so use them for higher frequency stuff

    # Remove the cross-level keys entirely for letters!
    # aot, aoe, ate * 2 levels = exactly the amount of missing chars
    # otherwise I would have to eat the enter, not good
    # J/K, V/X, Q/Z
    # just by feeling: KJV are more important
    # AH CRAP I was using those for quote and semicolon
    # but I guess some other codes open, so..

    def during_bootup(self, keyboard):
        pass

    def before_matrix_scan(self, keyboard):
        for side in [0, 1]:
            # SO: if it's timed out (300ms) send the key
            # BUT that's when hold becomes true, and we need to hit the hold point in order to reach the combo logic
            if self.state[side].timer != 0 and ticks_ms() > self.state[side].timer:
                self.state[side].key.keycode = self.determine_key(self.state[side].combo | self.state[side].mods)
                self.state[side].key.hold = True
                self.handle_key(keyboard, side)
                self.state[side].timer = 0

    def after_matrix_scan(self, keyboard):
        pass

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not isinstance(key, TaipoKey):
            return key

        # with the TaipoKey check above this if is maybe unnecessary
        if hasattr(key.meta, 'taipo_code'):
            side = 1 if key.meta.taipo_code / 10 >= 1 else 0 # taipo_code & 0x1 would be better, fix that later
            code = key.meta.taipo_code
            if is_pressed:
                if self.state[side].key.keycode != KC.NO:
                    self.handle_key(keyboard, side)
                    self.clear_state(side)

                self.state[side].last_combo = self.state[side].combo
                self.state[side].last_keypress_timestamp = ticks_ms()

                # And if the current state is clear (no key determined yet) it gets added to the combo and the timer starts

                if key.meta.taipo_code in taipo_mods:
                    self.state[side].mods |= 1 << (key.meta.taipo_code % 10)
                else:
                    self.state[side].combo |= 1 << (key.meta.taipo_code % 10) # mod 10? ahhhh since the first digit is the side, this pushes to l/r...
                    self.state[side].timer = ticks_ms() + self.tap_timeout
                    self.state[side].releasing = False
            else:
                # Going to need to mess with this logic - keyup _kills the timer_
                # but it does that!
                if not self.state[side].key.hold and not self.state[side].releasing:
                    # Key was not pressed long enough to trigger 'hold'

                    # TODO: make this tunable
                    # TODO: formatting
                    # TODO: maybe keycode should be changed in a moment...? I don't know what that affects
                    #combo = self.state[side].last_combo if self.state[side].last_keypress_timestamp > ticks_ms() - 100 else self.state[side].combo
                    combo = self.state[side].combo
                    if self.state[side].last_keypress_timestamp > ticks_ms() - 100:
                        last_keypress_timestamp = 0
                        # OH HEY this needs to stick past the clear_state at the end
                        # but I thought the rolling fix did that?
                        # rolling combos not implemented on here yet???

                    self.state[side].key.keycode = self.determine_key(combo | self.state[side].mods)

                    # If we trip a fast-keystroke thing releasing has to be reset to _false_

                # Combo key that has never triggered a combo does create a keystroke
                # Combo key that was part of a combo and is released at the end won't trigger a keystroke
                if self.state[side].combo != 0 or self.state[side].combo_executed == False:
                    self.handle_key(keyboard, side)
                    self.state[side].combo_executed = True

                if key.meta.taipo_code in taipo_mods:
                    self.state[side].mods &= ~(1 << (key.meta.taipo_code % 10))
                else:
                    self.state[side].combo &= ~(1 << (key.meta.taipo_code % 10))
                self.state[side].releasing = True

                self.clear_state(side)
        else:
            return key # AHHHH so anything that's not taipo-mapped gets passed straight through. Handy.

    def clear_state(self, side):
        # why does this not work?
        # self.state[side] = State()
        # Actually we don't want that any more, mods persists beyond the reset
        # mods is _not reset_
        #self.state[side].combo = 0
        self.state[side].timer = 0
        self.state[side].key.keycode = KC.NO
        self.state[side].key.hold = False
        self.state[side].key.hold_handled = False
        if self.state[side].mods == 0:
            self.state[side].combo_executed = False 
        
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
        if val in self.keymap:
            return self.keymap[val]
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

