Introduction
============


.. image:: https://readthedocs.org/projects/circuitpython-circuitpython-csv/badge/?version=latest
    :target: https://circuitpython-csv.readthedocs.io/
    :alt: Documentation Status


.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/tekktrik/Circuitpython_CircuitPython_CSV/workflows/Build%20CI/badge.svg
    :target: https://github.com/tekktrik/Circuitpython_CircuitPython_CSV/actions
    :alt: Build Status


.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Code Style: Black

CircuitPython helper library for working with CSV files


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install csv

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code-block:: python

    import board
    import sdcardio
    import storage
    import circuitpython_csv as csv

    # Initialize SD card
    spi = board.SPI()
    sdcard = sdcardio.SDCard(spi, board.D10)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")

    # Write the CSV file!
    with open("/sd/testwrite.csv", mode="w", encoding="utf-8") as writablefile:
        csvwriter = csv.writer(writablefile)
        csvwriter.writerow(["I", "love", "CircuitPython", "!"])
        csvwriter.writerow(["Spam"] * 3)


Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/tekktrik/Circuitpython_CircuitPython_CSV/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
