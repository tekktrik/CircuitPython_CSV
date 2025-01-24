# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Alec Delaney
#
# SPDX-License-Identifier: MIT

"""Example file for working with CSV files one CIrcuitPython boards.

This example assumes that an SD storage device is connected to the CircuitPython board.
"""

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
