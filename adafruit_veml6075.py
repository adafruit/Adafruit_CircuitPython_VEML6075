# The MIT License (MIT)
#
# Copyright (c) 2018 ladyada for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`Adafruit_VEML6075`
====================================================

CircuitPython library to support VEML6075 UVA & UVB sensor.

* Author(s): ladyada

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
  
* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_VEML6075.git"

from adafruit_bus_device.i2c_device import I2CDevice
from micropython import const

# pylint: disable=bad-whitespace
_VEML6075_ADDR = const(0x10)

_REG_CONF    = const(0x00)
_REG_UVA     = const(0x07)
#_REG_UVD     = const(0x08)  # Unused/reserved!
_REG_UVB     = const(0x09)
_REG_UVCOMP1 = const(0x0A)
_REG_UVCOMP2 = const(0x0B)
_REV_ID      = const(0x0C)

# Valid constants for UV Integration Time
_VEML6075_UV_IT = { 50:  0x00,
                    100: 0x01,
                    200: 0x02,
                    400: 0x03,
                    800: 0x04 }
# pylint: enable=bad-whitespace

class VEML6075:
    """
    Driver base for the VEML6075 UV Light Sensor
    :param i2c_bus: The `busio.I2C` object to use. This is the only required parameter.
    :param int integration_time: The integration time you'd like to set initially. Availble
                         options - each in milliseconds: 50, 100, 200, 400, 800.
                         The higher the '_x_' value, the more accurate
                         the reading is (at the cost of less samples per reading).
                         Defaults to 50ms if parameter not passed. To change
                         setting after intialization, use
                         ``[veml6075].integration_time = new_it_value``.
    """

    def __init__(self, i2c_bus, integration_time=50):
        self._i2c = I2CDevice(i2c_bus, _VEML6075_ADDR)
        self._buffer = bytearray(3)
        # read ID!
        veml_id = self._read_register(_REV_ID)[0]
        if veml_id != 0x26:
            raise RuntimeError("Incorrect VEML6075 ID 0x%02X" % veml_id)
        
        # Set integration time
        self.integration_time = integration_time


    @property
    def integration_time(self):
        key = (self._read_register(_REG_CONF)[0] >> 4) & 0x7
        for k,v in enumerate(_VEML6075_UV_IT):
            if key == k:
                return v

    @integration_time.setter
    def integration_time(self, val):
        if not val in _VEML6075_UV_IT.keys():
            raise RuntimeError("Invalid integration time")
        conf = self._read_register(_REG_CONF)[0]
        conf &= ~ 0b01110000 # mask off bits 4:6
        conf |= _VEML6075_UV_IT[val] << 4
        self._write_register(_REG_CONF, conf)

    def _read_register(self, register):
        self._buffer[0] = register
        with self._i2c as i2c:
            i2c.write_then_readinto(self._buffer, self._buffer,
                                    out_end=1, in_end=2, stop=False)
        return self._buffer

    def _write_register(self, register, value):
        self._buffer[0] = register
        self._buffer[1] = value
        self._buffer[2] = value >> 8
        with self._i2c as i2c:
            i2c.write(self._buffer)
