# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Alec Delaney
#
# SPDX-License-Identifier: MIT
"""
`circuitpython_csv`
================================================================================

CircuitPython helper library for working with CSV files


* Author(s): Alec Delaney

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s).
  Use unordered list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies
  based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tekktrik/Circuitpython_CircuitPython_CSV.git"

import io
import re
import os

try:
    from typing import List
except ImportError:
    pass

class reader:

    def __init__(self, file_iterator: io.TextIOWrapper, delimiter: str = ',', quotechar: str = '"'):

        self.file_interator = file_iterator
        self.delimiter = delimiter
        self.quotechar = quotechar
        self._re_exp = '(\\' + quotechar + '.+?\\' + quotechar + ')|([^' + delimiter + ']+)'

    def __iter__(self):
        return self

    def __next__(self):
        csv_value_list = []
        pre_regex_string = self.file_interator.__next__()

        while len(pre_regex_string) != 0: # while length of string is not zero
            if pre_regex_string.startswith(self.delimiter): # if string starts with delimiter, add element and remove
                csv_value_list.append('')
                pre_regex_string = pre_regex_string[1:]
                continue

            next_match = re.match(self._re_exp, pre_regex_string) # get text match, and add to list
            matches = next_match.groups()
            if matches[0] == None:
                latest_match = matches[1].strip('\r\n').strip('\n')
                csv_value_list.append(latest_match)
            else:
                latest_match = matches[0].strip('\r\n').strip('\n')
                csv_value_list.append(latest_match[1:-1])

            if len(pre_regex_string) != 0: # If anything is left in the list...
                pre_regex_string = pre_regex_string[len(latest_match):] # Remove the element just grabbed
                if pre_regex_string == self.delimiter: # if all that's left is a trailing delimiter, remove and append element to list
                    csv_value_list.append('')
                    pre_regex_string = pre_regex_string[1:]
                elif pre_regex_string == '\r\n' or pre_regex_string == 'n': # if it's just a newline, remove it and leave as empty string
                    pre_regex_string=''
                pre_regex_string = pre_regex_string[1:] # remove the delimiter


        return csv_value_list

        return csv_value_list