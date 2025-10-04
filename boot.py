import usb_midi
usb_midi.disable()

import usb_hid
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE, usb_hid.Device.CONSUMER_CONTROL))

import supervisor
supervisor.set_usb_identification(None, 'maggie42cs0-L')

import digitalio
import board
import storage
write = digitalio.DigitalInOut(board.GP14)
write.switch_to_output()

read = digitalio.DigitalInOut(board.GP5)
read.switch_to_input(pull = digitalio.Pull.UP)

write.value = 0
if read.value == True: # not pressed
    storage.disable_usb_drive()
    # LATER: Disable the serial console too
