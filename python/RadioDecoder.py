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

import numpy
from gnuradio import gr
from bitstring import BitArray

STANDARD=0
INVERTED=1
MANCHESTER=2
INVERTED_MANCHESTER=3

CHUNK_SIZE=4096

class SchmittTrigger():
    def __init__(self, thres1, thres2, initial_state=False):
        self._t1, self._t2, self._state, self._initial = thres1, thres2, initial_state, initial_state

    def compare(self, value):
        if self._state:
            if value < self._t1:
                self._state = False
        else:
            if value > self._t2:
                self._state = True
        return self._state

    def reset(self):
        self._state = self._initial

class RadioDecoder(gr.basic_block):
    """
    docstring for block RadioDecoder
    """
    def __init__(self, sample_rate=48000, baud_rate=2000, encoding=STANDARD, offset=0, threshold=0.2):
        gr.basic_block.__init__(self,
            name="RadioDecoder",
            in_sig=[numpy.float32, ],
            out_sig=[numpy.ubyte, ])
        self.sample_rate = sample_rate
        self.period = 1/baud_rate
        self.offset = offset
        
        if encoding == STANDARD:
            self.decode = self.decode_standard
        elif encoding == INVERTED:
            self.decode = self.decode_inverted
        elif encoding == MANCHESTER:
            self.decode = self.decode_manchester
        elif encoding == INVERTED_MANCHESTER:
            self.decode = self.decode_inverted_manchester
        else:
            raise ValueError("Incorrect encoding value")
        
        self._init_data()
        self.trigger = SchmittTrigger(0,threshold)

    def decode_standard(self,high="1",low="0"):
        res = ""
        for b in self.data:
            if b[0]:
                new_bit=high
            else:
                new_bit=low
            if b[1] < 10*self.period:
                res += new_bit*round(b[1]/self.period)
        return self._str_to_bytes(res)
    
    def decode_inverted(self):
        return self.decode_standard(high="0",low="1")
    
    # algo :
    # comparer j et j+1 pour savoir si front descendant ou front montant
    # puis, j += 1 si durée de j+1 == T, j+=2 si durée de j+1 == T/2
    def decode_manchester(self,rising="0",falling="1"):
        res=""
        j=0
        while j < len(self.data)-1:
            if j > 0 and (not self.data[j][0]) and self.data[j][1] > 10*self.period:
                break # End of message
            elif self.data[j][0] and not self.data[j+1][0]:
                res += falling
            elif not self.data[j][0] and self.data[j+1][0]:
                res += rising
            if self.data[j+1][1] > self.period/1.7:
                j+=1
            else:
                j+=2
        return self._str_to_bytes(res)
    
    def decode_inverted_manchester(self):
        return self.decode_manchester(rising="1",falling="0")
    
    def _init_data(self):
        self.data = [[False,0],]
    
    def _str_to_bytes(self,strin):
        return BitArray(bin=strin).tobytes()
    
    def forecast(self, noutput_items, ninputs):
        # ninputs is the number of input connections
        # setup size of input_items[i] for work call
        # the required number of input items is returned
        #   in a list where each element represents the 
        #   number of required items for each input
        ninput_items_required = [noutput_items] * ninputs
        return ninput_items_required

    def general_work(self, input_items, output_items):
        nout=0
        for x in input_items[0]:
            state = self.trigger.compare(x+self.offset)
            if state == self.data[-1][0]:
                self.data[-1][1] += 1/self.sample_rate
            else:
                self.data.append([state,1/self.sample_rate])
        
        if len(self.data) > 1 and self.data[-1][1] > 10*self.period:
            message = self.decode()
            nout = len(message)
            for i in range(nout):
                output_items[0][i] = int(message[i])
            print("Decoded: {}".format(message))
            self._init_data()
        
        self.consume(0,len(input_items[0]))
        return nout

