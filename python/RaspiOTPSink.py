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
import RPi.GPIO as GPIO

RASPI_GPIO_MAX=27

class RaspiOTPSink(VirtualOTPSink):
    """
    docstring for block RaspiOTPSink
    """
    def __init__(self, otp_type=T_OTP, otp_basetime=30, otp_startat=0, secret=None, gpio_number=0):
        gr.sync_block.__init__(self,
            name="RaspiOTPSink",
            in_sig=[numpy.ubyte, ],
            out_sig=None)
        super().__init__(otp_type=otp_type, otp_basetime=otp_basetime, otp_startat=otp_startat, secret=secret)
        
        if gpio_number < 0 or gpio_number > RASPI_GPIO_MAX:
            raise ValueError("GPIO number must be between 0 and {}.".format(RASPI_GPIO_MAX))
        self._gpio_number = gpio_number
    
    def _worker_init(self):
        GPIO.setup(self._gpio_number,GPIO.OUT,initial=GPIO.LOW)
    
    def _worker_run(self):
        GPIO.output(self._gpio_number, not GPIO.input(self._gpio_number))
                
    def _worker_close(self):
        GPIO.cleanup()
