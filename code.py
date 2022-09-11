import time
import board
import digitalio
import rotaryio
import neopixel
import math
from richbutton import RichButton
from rainbowio import colorwheel

#from adafruit_circuitplayground import cp
# if use this, need to use cp.pixels.brightness

'''
For animations:
https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-neopixel
'''

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            pixels[i] = colorwheel(rc_index & 255)
        pixels.show()
        time.sleep(wait)


def rainbow(wait):
    for j in range(255):
        for i in range(len(pixels)):
            idx = int(i + j)
            pixels[i] = colorwheel(idx & 255)
        pixels.show()
        time.sleep(wait)

def wheel(pos): # Input a value 0 to 255 to get a color value.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    elif pos < 85:
        return(int(pos * 3), int(255 - pos*3), 0)
    elif pos < 170:
        pos -= 85
        return(int(255 - pos*3), 0, int(pos * 3))
    else:
        pos -= 170
        return(0, int(pos * 3), int(255 - pos*3))

NUM_PIXELS = 10
MIN_BRIGHTNESS = 1   # Minimum LED brightness as a percentage (0 to 100)
MAX_BRIGHTNESS = 25 # Maximum LED brighrness as a percentage (0 to 100)

# Set initial brightness and speed to center values
BRIGHTNESS = (MIN_BRIGHTNESS + MAX_BRIGHTNESS) // 2
LEVEL = BRIGHTNESS * 0.01 # Integer brightness percentage to 0.0-1.0 coeff.
LEVEL = 0.3

pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=LEVEL, auto_write=False)
#pixels = neopixel.NeoPixel(board.NEOPIXEL, NUM_PIXELS, brightness=LEVEL, auto_write=True)
pixels.fill(0)
pixels.show()

# WOrking to get colors from easy int loop
'''
wait = 0.05
for i in range(255):
    pixels.fill(wheel(i))
    pixels.show()
    time.sleep(wait)
'''

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
print("Entering rotary encoder loop")

#can check RichButton.TAP, *.DOUBLE_TAP, *.HOLD, *.RELEASE
ENCODER_BUTTON = RichButton(board.A5)

ENCODER = rotaryio.IncrementalEncoder(board.A2, board.A3)
LAST_POSITION = ENCODER.position

# How quickly turning the knob changes colors
TURN_SPEED = 3

# Variable to track if currently in animations
IS_ANIMATING = False
CURRENT_COLOR_TUPLE = (0,0,0)

while True:
    POSITION = ENCODER.position
    if POSITION != LAST_POSITION:
        MOVE = POSITION - LAST_POSITION
        COLOR_POSITION = POSITION % 255
        print("current position = " + str(POSITION))
        print("current COLOR position = " + str(COLOR_POSITION))
        print("COLOR POSITION * TURN SPEED = " + str(COLOR_POSITION * TURN_SPEED))
        VAL_FOR_WHEEL = (COLOR_POSITION * TURN_SPEED) % 255
        print("(COLOR_POSITION * TURN_SPEED) % 255 = " + str(VAL_FOR_WHEEL))
        CURRENT_COLOR_TUPLE = wheel(VAL_FOR_WHEEL)
        print("CURRENT COLOR TUPLE = " + str(CURRENT_COLOR_TUPLE))
        #pixels.fill(wheel(VAL_FOR_WHEEL))
        pixels.fill(CURRENT_COLOR_TUPLE)
        pixels.show()
        LAST_POSITION = POSITION
    ACTION = ENCODER_BUTTON.action()
    if ACTION is RichButton.TAP:
        print("button tap")
        LEVEL += 0.1
        ROUND_LEVEL = round(LEVEL,2)
        NEW_BRIGHTNESS = round(ROUND_LEVEL % 1, 2)
        if NEW_BRIGHTNESS < 0.1:
            NEW_BRIGHTNESS = 0.1
            LEVEL = 0.1
        print("Setting brightness = " + str(NEW_BRIGHTNESS))
        LEVEL = NEW_BRIGHTNESS
        pixels.brightness = NEW_BRIGHTNESS
        pixels.show()
    if ACTION is RichButton.DOUBLE_TAP:
        print("button double tap")
        # add animations here?
        print("started animation")
        rainbow_cycle(0.05)
        print("animation done")
        pixels.fill(CURRENT_COLOR_TUPLE)
        pixels.show()

