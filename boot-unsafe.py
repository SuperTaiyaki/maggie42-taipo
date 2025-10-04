import usb_midi
usb_midi.disable()

import usb_hid
usb_hid.enable((usb_hid.Device.KEYBOARD, usb_hid.Device.MOUSE, usb_hid.Device.CONSUMER_CONTROL))

import supervisor
supervisor.set_usb_identification(None, 'WriterBoard')

