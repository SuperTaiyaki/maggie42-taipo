import board
import digitalio
import keypad
import time

from kmk.scanners import Scanner

""" Straight up python matrix scanner, that hopefully won't desync like
the built-in keypad scanner. Only supports standard diode layouts.

The debounce algorithm is lifted from CircuitPython
"""

class SynchronousScanner(Scanner):
    # I didn't want debounce, crappy Kailh switches keep flaking out on me
    DEBOUNCE = 10 # TODO: verify the scan rate, this should be expressed in time rather than cycles
    def __init__(self, col_pins, row_pins):
        self.cols = [digitalio.DigitalInOut(x) for x in col_pins]
        self.rows = [digitalio.DigitalInOut(x) for x in row_pins]
        for r in self.rows:
            r.pull = digitalio.Pull.DOWN

        # Public-ish?
        self.matrix = [- self.DEBOUNCE] * (len(self.cols) * len(self.rows))

        self.event_queue = [(0, 0)] * 64
        self.queue_head = 0
        self.queue_tail = 0

    @property
    def key_count(self):
        return len(self.cols) * len(self.rows)

#    @property
#    def matrix(self):
#        return [k == DEBOUNCE for k in self.matrix]

    def scan_for_changes(self):
        rowlength = len(self.cols)
        for c in range(len(self.cols)):
            self.cols[c].switch_to_output(value = True)
            # May need a more serious debounce
            time.sleep(0.000_01)

            for r in range(len(self.rows)):
                # TODO: queue keydowns before keyups, for better chording
                address = c + r * rowlength
                value = self.rows[r].value
                if value:
                    if self.matrix[address] < self.DEBOUNCE:
                        self.matrix[address] += 1
                        if self.matrix[address] >= 0:
                            self.matrix[address] = self.DEBOUNCE
                            self.add_event(address, value)
                else:
                    if self.matrix[address] > - self.DEBOUNCE:
                        self.matrix[address] -= 1
                        if self.matrix[address] <= 0:
                            self.matrix[address] = - self.DEBOUNCE
                            self.add_event(address, value)

                #if self.matrix[address] != value:
                #    self.matrix[address] = value
                #    self.add_event(address, value)

            self.cols[c].switch_to_input()
        return self.get_event()

    def add_event(self, address, value):
        self.queue_head += 1
        self.queue_head %= 64
        self.event_queue[self.queue_head] = (address, value)

    def get_event(self):
        if self.queue_tail != self.queue_head:
            self.queue_tail += 1
            self.queue_tail %= 64
            event = keypad.Event(self.event_queue[self.queue_tail][0], self.event_queue[self.queue_tail][1])
            return event
        else:
            return None

# Just a memo about the circuitpython issue...
# One input behind = number of entries in the queue has desynced from the queue contents
# read and write are in separate threads, so the update of one gets stomped by the other...?

