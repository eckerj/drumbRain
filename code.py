import board
import digitalio
import analogio
import usb_hid
import adafruit_hid
import time
import struct

FLOOR_SAMPLES=100
FLOOR_SAMPLE_INTERVAL=0.001 # in seconds
FLOOR_SAMPLE_DURATION=3 # in seconds

debug=True

# s0 thru s3 are multiplexer address pins.
# s0-3 = 0,0,0,0 => multiplexer pin 0
# s0-3 = 0,0,1,1 => multiplexer pin 3
# etc
s0=digitalio.DigitalInOut(board.GP18)
s1=digitalio.DigitalInOut(board.GP19)
s2=digitalio.DigitalInOut(board.GP20)
s3=digitalio.DigitalInOut(board.GP21)

s0.direction=Direction.OUTPUT
s1.direction=Direction.OUTPUT
s2.direction=Direction.OUTPUT
s3.direction=Direction.OUTPUT

# for debug purposes, we're only going to test out pin 3 (fourth input pin)
s0.value=True
s1.value=True
s2.value=False
s3.value=False

#from drumbRain import DrumbRain

drumbRain = adafruit_hid.find_device(usb_hid.devices, usage_page=0x1, usage=0x5)
padin = analogio.AnalogIn(board.A0)

if debug: print("drumbRain device:",drumbRain)

def send_drumbRain_report(button_state):
    report = bytearray(2)  ## must be same size as specified in HID Report Descriptor in boot.py
    #report_id = 4  ## must match what's in HID Report Descriptor in boot.py
    struct.pack_into(
        "<H",      # little endian, one 2-byte value
        report,
        0,
        button_state
    )
    if debug: print(["%02x" % x for x in report])
    try:
        drumbRain.send_report(report)
    except:
        if debug: print("Cant send report at this time")

# utility to help us set & clear bits in the button_state
def set_bit(v,i):
    v |= (1 << i)
    return v

def clr_bit(v,i):
    v &= ~(1 << i)
    return v

button_state = 0x00  # holds the state of our buttons
button_num = 0 # which button are we current toggling

def find_analog_floor(input):
    # grab 100 samples and find the max
    maxval = 0
    start_time=time.time()
    curr_time=start_time
    while (curr_time - start_time) <= FLOOR_SAMPLE_DURATION:
        val = input.value
        if val > maxval: maxval=val
#        time.sleep(FLOOR_SAMPLE_INTERVAL)
        curr_time=time.time()
    return maxval

def main_loop():
    while True:
        if debug: print("pushing button ", (button_num+1))  # human buttons start at one not zero

        # push button
        button_state = set_bit(button_state, button_num)

        send_drumbRain_report(button_state)
        time.sleep(1)

        if debug: print("releasing button ", (button_num+1))  # human buttons start at one not zero

        # release button
        button_state = clr_bit(button_state, button_num)
        send_drumbRain_report(button_state)
        
            
        time.sleep(1)

        # go to next button
        button_num = (button_num+1) % 16

#main_loop()
