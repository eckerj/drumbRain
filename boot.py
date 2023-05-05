import usb_hid
import usb_midi
import time

# inputs
# 1  start
# 2  select
# 3  up
# 4  down
# 5  left
# 6  right
# 7  kick 1
# 8  kick 2
# 9  pad  1 red
# 10 pad  2 yellow
# 11 pad  3 blue
# 12 pad  4 green
# 13 pad  5 yellowcym
# 14 pad  6 bluecymbal
# 15 pad  7 greencymbal
# ?? hi-hat pedal
# ?? additional pads

# Short term:
# 0   7     6     5        4       3       2     1         0
# 1   kick2 kick1 right    left    down    up    select    start
#
# Long term:
# 0   7     6     5        4       3       2     1         0
# 1   kick2 kick1 right    left    down    up    select    start
# 2   pad8? pad7  pad6     pad5    pad4    pad3  pad2      pad1
# 3   pad1 velocity
# 4   pad1 velocity
# 5   pad2 velocity
# 6   pad2 velocity
# 7   pad3 velocity
# 8   pad3 velocity
# 9   pad4 velocity
# 10   pad4 velocity
# 11   pad5 velocity
# 12   pad5 velocity
# 13   pad6 velocity
# 14   pad6 velocity
# 15   pad7 velocity
# 16   pad7 velocity
# 17   pad8 velocity
# 18   pad8 velocity
# 19   kick1 velocity
# 20   kick1 velocity
# 21   kick2 velocity
# 22   kick3 velocity

DRUMBRAIN_REPORT_DESCRIPTOR = bytes((
    0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09, 0x05,  # Usage (Game Pad)
    0xA1, 0x01,  # Collection (Application)
    0x85, 0x04,  #     Report ID (1)
    0x05, 0x09,  #     Usage Page (Button)
    0x19, 0x01,  #     Usage Minimum (Button 1)
    0x29, 0x10,  #     Usage Maximum (0x10), 16 buttons
    0x15, 0x00,  #     Logical Minimum (0)
    0x25, 0x01,  #     Logical Maximum (1)
    0x75, 0x01,  #     Report Size (1)
    0x95, 0x10,  #     Report Count (16) ## 2 bytes
    0x81, 0x02,  #     Input (Cnst,Var,Abs)
    0xC0,        # End Collection
))

drumbRain = usb_hid.Device(
    report_descriptor=DRUMBRAIN_REPORT_DESCRIPTOR,
    usage_page=0x01,           # Generic Desktop Control
    usage=0x05,                # Gamepad
    report_ids=(4,),           # Descriptor uses report ID 1.
    in_report_lengths=(2,),    # This gamepad sends 2 bytes in its report.
    out_report_lengths=(0,),   # It does not receive any reports.
)

usb_midi.disable()

usb_hid.enable(
    (drumbRain,)
)
# This does all sorts of funky keyboard stuff
#usb_hid.enable(
#    (usb_hid.Device.KEYBOARD,
#     usb_hid.Device.MOUSE,
#     usb_hid.Device.CONSUMER_CONTROL,
#     drumbRain)
#)

