'''Enables splitting keyboards wirelessly or wired'''

# HORRIBLE SILLINESS: kmk_keyboard.py checks for kmk.modules.split by name, that will fail
# if using this module that needs to be patched

import board
import busio
from micropython import const
from supervisor import runtime, ticks_ms

from keypad import Event as KeyEvent
from storage import getmount

from kmk.hid import HIDModes
from kmk.kmktime import check_deadline
from kmk.modules import Module
from kmk.utils import Debug

import math

debug = Debug(__name__)

# With top parity bit
hamming = [
    0,
    135,
    153,
    30,
    170,
    45,
    51,
    180,
    75,
    204,
    210,
    85,
    225,
    102,
    120,
    255
]

class SplitSide:
    LEFT = const(1)
    RIGHT = const(2)

class ThickSplit(Module):
    '''Enables splitting keyboards wirelessly, or wired'''

    def __init__(
        self,
        split_flip=True,
        split_side=None,
        split_target_left=True,
        uart_interval=20,
        data_pin=None,
        data_pin2=None,
        uart_flip=True,
        use_pio=False,
    ):
        self._is_target = True
        self.split_flip = split_flip
        self.split_side = split_side
        self.split_target_left = split_target_left
        self.split_offset = None
        self.data_pin = data_pin
        self.data_pin2 = data_pin2
        self.uart_flip = uart_flip
        self._use_pio = use_pio
        self._uart = None
        self._uart_interval = uart_interval
        self.uart_header = bytearray([0b1111_0100])  # Something way outside hamming correction
        self.matrix = None
        self.report_size = 0 # one-sided
        self.far_matrix = None
        self.events = []
        self.receive_buffer = []
        self.refresh = 100

        if self._use_pio:
            from kmk.transports.pio_uart import PIO_UART

            self.PIO_UART = PIO_UART

    def during_bootup(self, keyboard):
        # Set up name for target side detection and BLE advertisment
        name = str(getmount('/').label)
        # Try to guess data pins if not supplied
        if not self.data_pin:
            self.data_pin = keyboard.data_pin

        # if split side was given, find target from split_side.
        if self.split_side == SplitSide.LEFT:
            self._is_target = bool(self.split_target_left)
        elif self.split_side == SplitSide.RIGHT:
            self._is_target = not bool(self.split_target_left)
        else:
            # Detect split side from name
            self._is_target = runtime.usb_connected

            if name.endswith('L'):
                self.split_side = SplitSide.LEFT
            elif name.endswith('R'):
                self.split_side = SplitSide.RIGHT

        #self._is_target = False
        if not self._is_target:
            keyboard._hid_send_enabled = False

        if self.split_offset is None:
            self.split_offset = keyboard.matrix[-1].coord_mapping[-1] + 1

        if self.data_pin is not None:
            if self._is_target or not self.uart_flip:
                if self._use_pio:
                    # Overclocking this goes badly
                    self._uart = self.PIO_UART(tx=self.data_pin2, rx=self.data_pin, baudrate = 4800)
                else:
                    # TODO: don't hardcode this
                    self._uart = busio.UART(
                        tx=None, rx=board.GP1, timeout=self._uart_interval, baudrate = 125_000
                    )
            else:
                if self._use_pio:
                    # at 2400 there are no errors
                    # at 4800 errors start creeping in
                    # ARGH FUCKING NEXT PLAN
                    #GP1/GP0 are the UART ports anyway so bridge them and stop using PIO UART

                    self._uart = self.PIO_UART(tx=self.data_pin, rx=self.data_pin2, baudrate = 4800)
                else:
                    self._uart = busio.UART(
                        tx=board.GP0, rx=None, timeout=self._uart_interval, baudrate = 125_000
                    )

        # Attempt to sanely guess a coord_mapping if one is not provided.
        if not keyboard.coord_mapping and keyboard.row_pins and keyboard.col_pins:
            cm = []

            rows_to_calc = len(keyboard.row_pins)
            cols_to_calc = len(keyboard.col_pins)

            # Flips the col order if PCB is the same but flipped on right
            cols_rhs = list(range(cols_to_calc))
            if self.split_flip:
                cols_rhs = list(reversed(cols_rhs))

            for ridx in range(rows_to_calc):
                for cidx in range(cols_to_calc):
                    cm.append(cols_to_calc * ridx + cidx)
                for cidx in cols_rhs:
                    cm.append(cols_to_calc * (rows_to_calc + ridx) + cidx)

            keyboard.coord_mapping = tuple(cm)
        # ARGH silly offset stuff....
        self.matrix = [False] * (len(keyboard.row_pins) * len(keyboard.col_pins))
        self.far_matrix = [False] * (len(keyboard.row_pins) * len(keyboard.col_pins))
        self.report_size = math.ceil(len(self.matrix) / 8)

        if not keyboard.coord_mapping and debug.enabled:
            debug('Error: please provide coord_mapping for custom scanner')

        if self.split_side == SplitSide.RIGHT:
            offset = self.split_offset
            for matrix in keyboard.matrix:
                matrix.offset = offset
                offset += matrix.key_count

    def before_matrix_scan(self, keyboard):
        if self._is_target or self.data_pin2:
            self._receive_uart(keyboard)
        return

    def after_matrix_scan(self, keyboard):
        # actually this does nothing, this will only ever get called with 1 update
        if not self._is_target:
            refresh = False

            if keyboard.matrix_update:
                event = keyboard.matrix_update
                self.matrix[event.key_number - self.split_offset] = event.pressed
                refresh = True

            # reduce the number of updates
            if keyboard.matrix_update_queue and all([event.pressed == keyboard.matrix_update_queue[0].pressed for event in keyboard.matrix_update_queue]):
                refresh = False
                self.refresh -= 20

            if refresh or self.refresh < 0:
                if not self._is_target or self.data_pin2:
                    self._send_uart(self._encode_matrix())
                else:
                    #print(self._encode_matrix())
                    pass  # explicit pass just for dev sanity...

                self.refresh = 100
            self.refresh -= 1
        return

    def _encode_matrix(self):
        # TODO: recycle this (instance variable it)
        cells = bytearray(self.report_size)
        for x in range(len(self.matrix)):
            if self.matrix[x]:
                cells[x // 8] |= 1 << (x % 8)
        return cells

    def _decode_matrix(self, compressed):
        if compressed is None:
            return None
        return [compressed[x // 8] & (1 << (x % 8)) != 0 for x in range(len(self.matrix))]

    def before_hid_send(self, keyboard):
        if not self._is_target:
            keyboard.hid_pending = False
        return

    def after_hid_send(self, keyboard):
        return

    def on_powersave_enable(self, keyboard):
        pass
    def on_powersave_disable(self, keyboard):
        pass

    def _check_all_connections(self, keyboard):
        pass

    def _serialize_update(self, update):
        buffer = bytearray(2)
        buffer[0] = update.key_number
        buffer[1] = update.pressed
        return buffer

    def _deserialize_update(self, update):
        kevent = KeyEvent(key_number=update[0], pressed=update[1])
        return kevent

    # 4 bits in, 8 bits (7 bits) out
    def _hamming(self, word):
        global hamming
        return hamming[word]

    # Funkiness: B- is always corrected!
    # It's sending some junk data...
    # Now 178 is being received (consistently!) but it's not in the table
    # And some others.... is the serial transmission really that flaky?
    # Where's my white cable...
    # WTF? 178 means the top bit got set
    # LOL FUCK 178 is a desync (it's the marker). Should use something else, like 0xff
    # 0xFE is probably better because of the parity error

    # TODO next: 8,4 with a full parity bit

    # 7 bits in, 8 bits out
    def _dehamming(self, word):
        def isbit(b, i):
            return 0 if b & (1 << i) == 0 else 1

        parity_error = sum([isbit(word, i) for i in range(8)]) & 1
        if parity_error:
            print("Parity error")
            return None

        error1 = isbit(word, 0) + isbit(word, 2) + isbit(word, 4) + isbit(word, 6)
        error2 = isbit(word, 1) + isbit(word, 2) + isbit(word, 5) + isbit(word, 6)
        error3 = isbit(word, 3) + isbit(word, 4) + isbit(word, 5) + isbit(word, 6)
        error = (error1 % 2) + (error2 % 2) << 1 + (error3 % 2) << 2
        if error != 0:
            if parity_error == 0:
                print("Uncorrectable") # 2-bit error
                return None
            print("Corrected: val ", word,"with error ", error)
            word ^= 1 << (error - 1)
        result = isbit(word, 2) | isbit(word, 4) << 1 | isbit(word, 5) << 2 | isbit(word, 6) << 3
        return result

    def _encode(self, update):
        output = bytearray(len(update) * 2)
        for i in range(len(update) * 2):
            block = (update[i // 2] if i % 2 == 0 else (update[i // 2] >> 4)) & 0xF
            output[i] = self._hamming(block)
        return output

    def _decode(self, encoded):
        output = bytearray(len(encoded) // 2)
        for i in range(len(encoded)):
            word = self._dehamming(encoded[i])
            if word is None:
                return None
            if i % 2 == 1:
                output[i // 2] |= word << 4
            else:
                output[i // 2] = word
        return output


    def _send_uart(self, update):
        if self._uart is not None:
            #update = self._serialize_update(update)
            self._uart.write(self.uart_header)
            self._uart.write(self._encode(update))
            #self._uart.write(self._checksum(update))

    def _receive_uart(self, keyboard):
        if self._uart is not None and self._uart.in_waiting > 0:
            self.receive_buffer += self._uart.read(self._uart.in_waiting)

        # ARGH smells like the whole damn communication is desyncing
        while self.receive_buffer and self.receive_buffer[0] != self.uart_header[0]:
            print("Walk")
            del self.receive_buffer[0]

        while len(self.receive_buffer) >= 1 + self.report_size * 2: # *2 for the error correction
            if self.receive_buffer: # Not actually doing anything
                new_matrix = self._decode_matrix(self._decode(self.receive_buffer[1:self.report_size *2 + 1]))
                del self.receive_buffer[0:self.report_size*2 + 1]
                #print(new_matrix)
                #print(self.far_matrix)
                if new_matrix != None:
                    for i in range(len(self.matrix)):
                        # Kind of bad: debounce this?
                        if self.far_matrix[i] != new_matrix[i]:
                            # split_offset is only for right side!
                            key_number = i + self.split_offset if self.split_side == SplitSide.LEFT else i
                            self.events.append(KeyEvent(key_number = key_number, pressed = new_matrix[i]))

                    self.far_matrix = new_matrix
                else:
                    print("Discarded incoming matrix due to error")

        if self.events:
            keyboard.secondary_matrix_update = self.events.pop(0)

