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
import pyotp

T_OTP=0
H_OTP=1

# Virtual class. Inherited class must define _worker_init(), _worker_run() and _worker_close() methods.
# The first one is called in the __init__ method, the second one when a valid OTP is received,
# and the third one in the __del__ function.

class VirtualOTPSink(gr.sync_block):
    """
    docstring for block RaspiOTPSink
    """
    def __init__(self, otp_type=T_OTP, otp_basetime=30, otp_startat=0, secret=None):
        if (not isinstance(secret,str)) or secret == "":
            raise ValueError("Secret must be a non-empty string!")
        if not otp_type in (T_OTP,H_OTP):
            raise ValueError("otp_type must be in ({},{}) values.".format(T_OTP,H_OTP))
        if otp_basetime <= 0 or not isinstance(otp_basetime,int):
            raise ValueError("otp_basetime must be a not-null positive integer.")
        if otp_startat < 0 or not isinstance(otp_startat,int):
            raise ValueError("otp_startat must be a positive integer.")
        self._otp_type=otp_type
        if otp_type==H_OTP:
            self._otp = pyotp.HOTP(secret)
            self._index = otp_startat
        else:
            self._otp = pyotp.TOTP(secret,interval=otp_basetime)
        self._worker_init()

    def _look_for_otp(self,data,length=6):
        if len(data) == 0:
            return None
        for i in range(len(data)):
            if data[i] in range(0x30,0x40):
                if i+length > len(data):
                    return None
                for j in range(i,i+length):
                    if not data[j] in range(0x30,0x40):
                        return None
                return data[i:i+length]
    
    def _array_to_str(self,a):
        res=''
        for c in a:
            res+=chr(c)
        return res
                
    def work(self, input_items, output_items):
        in0 = input_items[0]
        otp = self._look_for_otp(in0)
        try:
            if len(otp) > 0:
                if self._otp_type == T_OTP:
                    if self._otp.verify(self._array_to_str(otp)):
                        print("OTP valid!")
                        self._worker_run()
                else:
                    if self._otp.verify(self._array_to_str(otp),counter=self._index):
                        print("OTP valid!")
                        self._worker_run()
                        self._index+=1
        except TypeError as e:
            pass
        finally:
            return len(input_items[0])
    
    def __del__(self):
        self._worker_close()
