#
# Copyright 2008,2009 Free Software Foundation, Inc.
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


# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio GUIMRADIO module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the GuiMRadio namespace
try:
    # this might fail if the module is python-only
    from .GuiMRadio_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .RadioDecoder import RadioDecoder

try:
    from .RaspiGPIOSink import RaspiGPIOSink
    from .RaspiOTPSink import RaspiOTPSink
except ModuleNotFoundError as e:
    if "RPi" in e.__str__():
        print("Warning: Module RPi.GPIO not found. If you're running this module on a Raspberry Pi, please consider to install it. Otherwire, you can ignore it.")
    else:
        raise e

from .ExecOTPSink import ExecOTPSink
from .SerialOTPSink import SerialOTPSink
#
