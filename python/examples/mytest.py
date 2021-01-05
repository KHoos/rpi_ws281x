#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
#
# Functions added by Koos van den Hout (koos+github@idefix.net)

import time
from rpi_ws281x import *
import argparse

# LED strip configuration:
LED_COUNT      = 120      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def theaterChase2(strip, color, color2, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color2)
            strip.show()

def theaterChase3(strip, color, color2, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(6):
            for i in range(0, strip.numPixels(), 6):
                strip.setPixelColor(i+q, color)
            for i in range(0, strip.numPixels(), 6):
                strip.setPixelColor(i+q+3, color2)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def fadeon(strip, wait_ms=50):
    """Attempt at fade on"""
    for level in range(0,256,4):
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i,Color(level,level,level))
        strip.show()
        time.sleep(wait_ms/1000.0)

def fadeout(strip, wait_ms=50):
    """Attempt at fade out"""
    for level in range(255,0,-4):
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i,Color(level,level,level))
        strip.show()
        time.sleep(wait_ms/1000.0)

def blink(strip, color, wait_ms=250):
    """blink on and off"""
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()
    time.sleep(wait_ms/1000.0)
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, 0)
    strip.show()
    time.sleep(wait_ms/1000.0)

def walk(strip, color, wait_ms=5):
    """walk a pixel"""
    for i in range(0, strip.numPixels()):
        for j in range(0, strip.numPixels()):
            if i == j:
                strip.setPixelColor(j, color)
            else:
                strip.setPixelColor(j, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)

def walkback(strip, color, wait_ms=5):
    """walk a pixel"""
    for i in range(strip.numPixels()-1,-1,-1):
        for j in range(0, strip.numPixels()):
            if i == j:
                strip.setPixelColor(j, color)
            else:
                strip.setPixelColor(j, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Dictionary representing the morse code chart 
MORSE_CODE_DICT = { 'A':'.-', 'B':'-...', 
                    'C':'-.-.', 'D':'-..', 'E':'.', 
                    'F':'..-.', 'G':'--.', 'H':'....', 
                    'I':'..', 'J':'.---', 'K':'-.-', 
                    'L':'.-..', 'M':'--', 'N':'-.', 
                    'O':'---', 'P':'.--.', 'Q':'--.-', 
                    'R':'.-.', 'S':'...', 'T':'-', 
                    'U':'..-', 'V':'...-', 'W':'.--', 
                    'X':'-..-', 'Y':'-.--', 'Z':'--..', 
                    '1':'.----', '2':'..---', '3':'...--', 
                    '4':'....-', '5':'.....', '6':'-....', 
                    '7':'--...', '8':'---..', '9':'----.', 
                    '0':'-----', ', ':'--..--', '.':'.-.-.-', 
                    '?':'..--..', '/':'-..-.', '-':'-....-', 
                    '(':'-.--.', ')':'-.--.-'} 

def lookupmorse(letter):
    if letter != ' ':
        return MORSE_CODE_DICT[letter]
    else:
        return ' '

# I want to generate morse with the right spacing!
# space between parts of a letter: 1 dit
# space between 2 letters in a word: 3 dits
# space between 2 words: 7 dits
def fillarray(inputstring):
    bitlist = []
    for letter in inputstring:
        morsecode = lookupmorse(letter)
        for code in morsecode:
            # space between words: 7 dits of nothing. 5 here, rest below
            if code == ' ':
                bitlist.append(0)
                bitlist.append(0)
                bitlist.append(0)
                bitlist.append(0)
                bitlist.append(0)
            # dit or dah
            else:
                if code == '.':
                    bitlist.append(1)
                    bitlist.append(0)
                elif code == '-':
                    bitlist.append(1)
                    bitlist.append(1)
                    bitlist.append(1)
                    bitlist.append(0)
        # end of a letter, and match with the rest
        bitlist.append(0)
        bitlist.append(0)
    return bitlist

def morseloop(strip,oncolor,morsestring,wait_ms=250):
    """ morse code """
    mylist = fillarray(morsestring)
    for j in range(strip.numPixels()+len(mylist)-1):
        for i in range(strip.numPixels()):
            if i > j:
                strip.setPixelColor(i, 0)
            elif j-i+1 > len(mylist):
                strip.setPixelColor(i, 0)
            else:
                if mylist[j-i] == 1:
                    strip.setPixelColor(i, oncolor)
                else:
                    strip.setPixelColor(i, 0)
        strip.show()
        time.sleep(wait_ms/1000.0)

def morseblink(strip,oncolor,morsestring,wait_ms=250):
    mylist = fillarray(morsestring)
    for i in range(len(mylist)):
        for j in range(strip.numPixels()):
            if mylist[i] == 1:
                strip.setPixelColor(j, oncolor)
            else:
                strip.setPixelColor(j,0)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:

        while True:
#            print ('Color wipe animations.')
#            colorWipe(strip, Color(127,127,127), 5) # White wipe
#            colorWipe(strip, Color(127,127, 0), 5)  # Yellow wipe
#            colorWipe(strip, Color(0, 255, 0), 5)  # Green wipe
#            colorWipe(strip, Color(255, 0, 0), 5)  # Red wipe
#            colorWipe(strip, Color(0, 0, 255), 5)  # Blue wipe
            print ('Theater chase animations.')
#            theaterChase(strip, Color(127, 127, 127))  # White theater chase
#            theaterChase(strip, Color(127, 127,   0))  # Yellow theater chase
#            theaterChase(strip, Color(25,   0,   0),100)  # Red theater chase
#            theaterChase(strip, Color(  0, 127,   0))  # Green theater chase
#            theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
#            theaterChase2(strip, Color(25,  0,   0), Color(0,25,0), 100)
#            theaterChase2(strip, Color(0,  0,   127), Color(127,127,0), 100)
#            theaterChase3(strip, Color(25,  0,   0), Color(0,25,0), 200)
            theaterChase3(strip, Color(90,  0,   0), Color(0,90,0), 200)
#            print ('Rainbow animations.')
#            rainbow(strip)
#            rainbowCycle(strip)
#            theaterChaseRainbow(strip)
#            print ('Fade.')
#            fadeon(strip,10)
#            fadeout(strip,10)
#            print ('Blink.')
#            blink(strip,Color(127,0,0))
#            blink(strip,Color(0,127,0))
#            blink(strip,Color(127,127,0))
#            for level in range(0,255,5):
#                print(level)
#                blink(strip,Color(0,level,level))
#            print ('Walk.')
#            walk(strip,Color(0,127,0))
#            walkback(strip,Color(0,127,0))
#            walk(strip,Color(90,0,0))
#            walkback(strip,Color(90,0,0))
#            walk(strip,Color(0,0,127))
#            walk(strip,Color(90,90,90))
#            walk(strip,Color(70,70,70),10)
#            walk(strip,Color(50,50,50),15)
#            walk(strip,Color(120,120,120),2)
#            walkback(strip,Color(120,120,120),2)
#           ^ fast walks make my cat chase the light
            print ('Morse code')
            morseloop(strip,Color(127,0,0),'MERRY CHRISTMAS',50)
            print ('Blink.')
            blink(strip,Color(90,0,0))
            blink(strip,Color(0,90,0))
#            blink(strip,Color(127,127,0))

    except KeyboardInterrupt:
        if args.clear:
            colorWipe(strip, Color(0,0,0), 1)
            #blink(strip,Color(127,127,127),1)
