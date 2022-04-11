#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2022 Guilhem Tiennot.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#
# This file is part of GuiMRadio gnuradio package.
# 
# GuiMRadio is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# GuiMRadio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GuiMRadio.  If not, see <https://www.gnu.org/licenses/>.
#


# Modes:
#   - Toggle
#   - Turn high (until untriggered)
#   - Turn low (until untriggered)
#   - Keep high (forever)
#   - Keep low (forever)


import numpy
from gnuradio import gr

TURN_HIGH=0
TURN_LOW=1
KEEP_HIGH=2
KEEP_LOW=3
TOGGLE=4

class RaspiGPIOSink(gr.sync_block):
    """
    docstring for block RaspiGPIOSink
    """
    
    def __init__(self, gpio_number=0, threshold=0, mode=TURN_HIGH, initial_state=False):
        gr.sync_block.__init__(self,
            name="RaspiGPIOSink",
            in_sig=[numpy.float32, ],
            out_sig=None)
        self.gpio_number = gpio_number
        self.threshold = threshold
        self.mode = mode
        
        # Choose the initial state, according to the mode
        if self.mode in (TURN_HIGH,KEEP_HIGH):
            self.state = False
        elif self.mode in (TURN_LOW,KEEP_LOW):
            self.state = True
        else:
            self.state = initial_state
        self._previous_trigger = initial_state
        
        # Init GPIO and apply initial state
        self._gpio_init()
        self._gpio_apply_state()
    
    def _gpio_init(self):
        pass
    
    def _gpio_apply_state(self):
        print(self.state)
    
    # Determine the new state to apply to GPIO, according to data and the chosen mode
    def _get_new_state(self,data):
        t = (max(data) > self.threshold)
        
        if self.mode == TURN_HIGH:
            return t
        elif self.mode == TURN_LOW:
            return not t
        elif self.mode == KEEP_HIGH:
            return (self.state or t)
        elif self.mode == KEEP_LOW:
            return (self.state and not t)
        else:
            if t == self._previous_trigger:
                return self.state
            else:
                self._previous_trigger = t
                if t:
                    return not self.state
                else:
                    return self.state
        
    def work(self, input_items, output_items):
        in0 = input_items[0]
        new_state = self._get_new_state(in0)
        
        # No need to apply the new state if it's the same than the previous
        if new_state != self.state:
            self.state = new_state
            self._gpio_apply_state()
        return len(input_items[0])
