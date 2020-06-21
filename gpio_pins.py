# -*- coding: utf-8 -*-

# Python 2/3 compatibility imports
from __future__ import print_function
from six.moves import range

# local module imports
from blinker import signal
import gv
from pyA20.gpio import gpio
from pyA20.gpio import port

pins = [port.PA10, port.PA13, port.PA2, port.PA14]
gpio.init()
gv.platform = u"pi"

for pin in pins:
    gpio.setcfg(pin, gpio.OUTPUT)


zone_change = signal(u"zone_change")



global pin_rain_sense
global pin_relay


def set_output():
    """
    Activate pins according to gv.srvals.
    """

    with gv.output_srvals_lock:
        gv.output_srvals = gv.srvals
        if gv.sd[u"alr"]:
            gv.output_srvals = [
                1 - i for i in gv.output_srvals
            ]  #  invert logic of shift registers
        j = 0
        for pin in pins:
            if gv.output_srvals[j] == 1:
                gpio.output(pin, 0)
            else:
                gpio.output(pin, 1)

            j += 1
        zone_change.send()
