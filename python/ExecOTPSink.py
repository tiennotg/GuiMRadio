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
from os import system

class ExecOTPSink(VirtualOTPSink):
    """
    docstring for block ExecOTPSink
    """
    def __init__(self, otp_type=T_OTP, otp_basetime=30, otp_startat=0, secret=None, cmd="echo OK", init_cmd="", close_cmd=""):
        gr.sync_block.__init__(self,
            name="ExecOTPSink",
            in_sig=[numpy.ubyte, ],
            out_sig=None)
        
        if not isinstance(cmd,str) or cmd == "":
            raise ValueError("Cmd must be a non-empty string.")
        
        self._cmd = cmd
        self._init_cmd = init_cmd
        self._close_cmd = close_cmd
        super().__init__(otp_type=otp_type, otp_basetime=otp_basetime, otp_startat=otp_startat, secret=secret)
    
    def _worker_init(self):
        if self._init_cmd:
            system(self._init_cmd)
    
    def _worker_run(self):
        system(self._cmd)
                
    def _worker_close(self):
        if self._close_cmd:
            system(self._close_cmd)
