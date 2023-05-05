import board
import digitalio
import analogio
import usb_hid
import adafruit_hid
import time
import struct

#from drumbRain import DrumbRain

drumbRain2 = adafruit_hid.find_device(usb_hid.devices, usage_page=0x1, usage=0x5)

print("drumbRain device:",drumbRain2)

def send_drumbRain_report(button_state):
    report = bytearray(2)  ## must be same size as specified in HID Report Descriptor in boot.py
    #report_id = 4  ## must match what's in HID Report Descriptor in boot.py
    struct.pack_into(
        "<H",      # little endian, one 2-byte value
        report,
        0,
        button_state
    )
    print(["%02x" % x for x in report])
    try:
        drumbRain2.send_report(report)
    except:
        print("Cant send report at this time")

# utility to help us set & clear bits in the button_state
def set_bit(v,i):
    v |= (1 << i)
    return v

def clr_bit(v,i):
    v &= ~(1 << i)
    return v

button_state = 0x00  # holds the state of our buttons
button_num = 0 # which button are we current toggling

def main_loop():
    while True:
        print("pushing button ", (button_num+1))  # human buttons start at one not zero

        # push button
        button_state = set_bit(button_state, button_num)

        send_drumbRain_report(button_state)
        time.sleep(1)

        print("releasing button ", (button_num+1))  # human buttons start at one not zero

        # release button
        button_state = clr_bit(button_state, button_num)
        send_drumbRain_report(button_state)
        
            
        time.sleep(1)

        # go to next button
        button_num = (button_num+1) % 16

#main_loop()
