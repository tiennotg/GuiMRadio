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
from GuiMRadio.OTPSink import VirtualOTPSink,T_OTP,H_OTP
import serial

class SerialOTPSink(VirtualOTPSink):
    """
    docstring for block SerialOTPSink
    """
    def __init__(self, otp_type=T_OTP, otp_basetime=30, otp_startat=0, secret=None, data="", sfile="/dev/ttyS0", baudrate=9600, bits=8, stopbits=1, parity=serial.PARITY_NONE):
        gr.sync_block.__init__(self,
            name="SerialOTPSink",
            in_sig=[numpy.ubyte, ],
            out_sig=None)
        
        self._serial = serial.Serial()
        self._serial.baudrate = baudrate
        self._serial.port = sfile
        self._serial.bytesize = bits
        self._serial.parity = parity
        self._serial.stopbits = stopbits
        self._data_to_send = data
        super().__init__(otp_type=otp_type, otp_basetime=otp_basetime, otp_startat=otp_startat, secret=secret)
    
    def _worker_init(self):
        self._serial.open()
    
    def _worker_run(self):
        self._serial.write(self._data_to_send.encode("latin1"))
                
    def _worker_close(self):
        self._serial.close()
