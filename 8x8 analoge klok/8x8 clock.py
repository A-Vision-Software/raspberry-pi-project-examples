# Installation: https://luma-led-matrix.readthedocs.io/en/latest/install.html
import time
import datetime

import Adafruit_ADS1x15

from luma.led_matrix.device import max7219
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.interface.serial import spi, noop

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0, rotate=0, blocks_arranged_in_reverse_order=False)

virtual = viewport(device, width=device.width, height=device.height)    

adc = Adafruit_ADS1x15.ADS1015()

def zero(draw,small=False):
    if small:
        draw.line((4, 4, 6, 4), fill="white")
    else:
        draw.line((4, 4, 7, 4), fill="white")
def one(draw,small=False):
    if small:
        draw.line((4, 4, 6, 5), fill="white")
    else:
        draw.line((4, 4, 7, 6), fill="white")
def two(draw,small=False):
    if small:
        draw.line((4, 4, 5, 6), fill="white")
    else:
        draw.line((4, 4, 6, 7), fill="white")
def three(draw,small=False):
    if small:
        draw.line((4, 4, 4, 6), fill="white")
    else:
        draw.line((4, 4, 4, 7), fill="white")
def four(draw,small=False):
    if small:
        draw.line((4, 4, 3, 6), fill="white")
    else:
        draw.line((4, 4, 2, 7), fill="white")
def five(draw,small=False):
    if small:
        draw.line((4, 4, 2, 5), fill="white")
    else:
        draw.line((4, 4, 1, 6), fill="white")
def six(draw,small=False):
    if small:
        draw.line((4, 4, 2, 4), fill="white")
    else:
        draw.line((4, 4, 1, 4), fill="white")
def seven(draw,small=False):
    if small:
        draw.line((4, 4, 2, 3), fill="white")
    else:
        draw.line((4, 4, 1, 2), fill="white")
def eight(draw,small=False):
    if small:
        draw.line((4, 4, 3, 2), fill="white")
    else:
        draw.line((4, 4, 2, 1), fill="white")
def nine(draw,small=False):
    if small:
        draw.line((4, 4, 4, 2), fill="white")
    else:
        draw.line((4, 4, 4, 1), fill="white")
def ten(draw,small=False):
    if small:
        draw.line((4, 4, 5, 2), fill="white")
    else:
        draw.line((4, 4, 6, 1), fill="white")
def eleven(draw,small=False):
    if small:
        draw.line((4, 4, 6, 3), fill="white")
    else:
        draw.line((4, 4, 7, 2), fill="white")
def twelve(draw,small=False):
    zero(draw,small)

def number(draw, n=0, small=False):
    if n == 0:
        zero(draw,small)
    if n == 1:
        one(draw,small)
    if n == 2:
        two(draw,small)
    if n == 3:
        three(draw,small)
    if n == 4:
        four(draw,small)
    if n == 5:
        five(draw,small)
    if n == 6:
        six(draw,small)
    if n == 7:
        seven(draw,small)
    if n == 8:
        eight(draw,small)
    if n == 9:
        nine(draw,small)
    if n == 10:
        ten(draw,small)
    if n == 11:
        eleven(draw,small)
    if n == 12:
        twelve(draw,small)

def small_hand(draw):
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second    
    if h >= 12:
        h = h - 12
    number(draw, round(h + m/60), True)

def big_hand(draw):
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    s = now.second    
    number(draw, round(m/5))
    if (s % 2) == 0:
        draw.point((0, 0), fill="black")
    if (s % 2) == 1:
        draw.point((0, 0), fill="white")

def brightness():
    light = adc.read_adc(0, gain=1)
    if light >= 512:
        light = 512
    b = (16 - round(light/16))*16
    if b >= 256:
        b = 255
    if b < 0:
        b = 0
    device.contrast(b)

while True:
    brightness()

    """ Full clock cycle test (place a # in fron of line to enable)
    if not 'h' in locals():
        h = 0
    if not 'm' in locals():
        m = 0
    with canvas(virtual) as draw:
        number(draw, h, True)
        number(draw, m)
        time.sleep(0.125)
        m = m + 1
        if (m==12):
            h = h+1
            m = 0
            if (h==12):
                h = 0
    """
    
    with canvas(virtual) as draw:
        small_hand(draw) # hour
        big_hand(draw) # minute (each 5 minutes)

    time.sleep(0.25)
    #"""
    