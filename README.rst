Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-veml6075/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/veml6075/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_VEML6075.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_VEML6075
    :alt: Build Status

CircuitPython library to support VEML6075 UVA & UVB sensor.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

.. code-block:: python

	import time
	import board
	import busio
	import adafruit_veml6075

	i2c = busio.I2C(board.SCL, board.SDA)

	veml = adafruit_veml6075.VEML6075(i2c, integration_time=100)

	while True:
	    print(veml.uv_index)
	    time.sleep(1)

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_VEML6075/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
