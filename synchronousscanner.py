import board
import digitalio
import keypad

from kmk.scanners import Scanner

""" Straight up python matrix scanner, that hopefully won't desync like
the built-in keypad scanner. Only supports standard diode layouts.
"""

class SynchronousScanner(Scanner):
    def __init__(self, col_pins, row_pins):
        self.cols = [digitalio.DigitalInOut(x) for x in col_pins]
        self.rows = [digitalio.DigitalInOut(x) for x in row_pins]
        for r in self.rows:
            r.pull = digitalio.Pull.DOWN

        # Public-ish?
        self.matrix = [False] * (len(self.cols) * len(self.rows))

        self.event_queue = [(0, 0)] * 64
        self.queue_head = 0
        self.queue_tail = 0

    @property
    def key_count(self):
        return len(self.cols) * len(self.rows)

    def scan_for_changes(self):
        rowlength = len(self.cols)
        for c in range(len(self.cols)):
            self.cols[c].switch_to_output(value = True)
            #time.sleep(0.000_01)

            for r in range(len(self.rows)):
                # TODO: queue keydowns before keyups, for better chording
                address = c + r * rowlength
                value = self.rows[r].value
                if self.matrix[address] != value:
                    self.matrix[address] = value
                    self.add_event(address, value)

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

