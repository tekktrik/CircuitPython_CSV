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

None

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/tekktrik/Circuitpython_CircuitPython_CSV.git"

import re

try:
    from typing import List, Optional, Any, Dict
    import io
except ImportError:
    pass


class reader:  # pylint: disable=invalid-name
    def __init__(
        self, csvfile: io.TextIOWrapper, delimiter: str = ",", quotechar: str = '"'
    ):

        self.file_interator = csvfile
        self.delimiter = delimiter
        self.quotechar = quotechar
        self._re_exp = (
            "(\\" + quotechar + ".+?\\" + quotechar + ")|([^" + delimiter + "]+)"
        )

    def __iter__(self):
        return self

    def __next__(self):
        csv_value_list = []
        pre_regex_string = self.file_interator.__next__()

        while len(pre_regex_string) != 0:  # while length of string is not zero
            if pre_regex_string.startswith(
                self.delimiter
            ):  # if string starts with delimiter, add element and remove
                csv_value_list.append("")
                pre_regex_string = pre_regex_string[1:]
                continue

            next_match = re.match(
                self._re_exp, pre_regex_string
            )  # get text match, and add to list
            matches = next_match.groups()
            if matches[0] is None:
                latest_match = matches[1].strip("\r\n").strip("\n")
                csv_value_list.append(latest_match)
            else:
                latest_match = matches[0].strip("\r\n").strip("\n")
                csv_value_list.append(latest_match[1:-1])

            if len(pre_regex_string) != 0:  # If anything is left in the list...
                pre_regex_string = pre_regex_string[
                    len(latest_match) :
                ]  # Remove the element just grabbed
                if (
                    pre_regex_string == self.delimiter
                ):  # if all that's left is a trailing delimiter, remove and append element to list
                    csv_value_list.append("")
                    pre_regex_string = pre_regex_string[1:]
                elif (
                    pre_regex_string == "\r\n"  # pylint: disable=consider-using-in
                    or pre_regex_string == "n"  # pylint: disable=consider-using-in
                ):  # if it's just a newline, remove it and leave as empty string
                    pre_regex_string = ""
                pre_regex_string = pre_regex_string[1:]  # remove the delimiter

        return csv_value_list


class writer:  # pylint: disable=invalid-name
    def __init__(
        self, csvfile: io.TextIOWrapper, delimiter: str = ",", quoterchar: str = '"'
    ):

        self.file_iterator = csvfile
        self.delimiter = delimiter
        self.quotechar = quoterchar
        self.newlinechar = "\r\n"

    def writerow(self, seq):

        parsed_seq = [self._apply_quotes(entry) for entry in seq]
        parsed_str = (self.delimiter).join(parsed_seq)
        self.file_iterator.write(parsed_str + self.newlinechar)

    def writerows(self, rows: iter):
        for row in rows:
            self.writerow(row)

    def _apply_quotes(self, entry):

        return (
            (self.quotechar + entry + self.quotechar)
            if self.delimiter in entry
            else entry
        )


# Mostly copied from CPython's csv.py:
class DictReader:
    def __init__(
        self,
        f: io.TextIOWrapper,
        fieldnames: Optional[List] = None,
        restkey: Optional[str] = None,
        restval: Optional[Any] = None,
        **kwargs
    ):

        self.fieldnames = fieldnames
        self.restkey = restkey
        self.restval = restval
        self.reader = reader(f, **kwargs)
        self.line_num = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.line_num == 0:
            if self.fieldnames is None:
                self.fieldnames = next(self.reader)
        row = next(self.reader)

        row_dict = dict(zip(self.fieldnames, row))
        length_fn = len(self.fieldnames)
        length_row = len(row)
        if length_fn < length_row:
            row_dict[self.restkey] = row[length_fn:]
        elif length_fn > length_row:
            for key in self.fieldnames[length_row:]:
                row_dict[key] = self.restval
        self.line_num += 1
        return row_dict


# Copied from CPython's csv.py
class DictWriter:
    def __init__(
        self,
        f: io.TextIOWrapper,
        fieldnames: List,
        restval: str = "",
        extrasaction: str = "raise",
        **kwds
    ):
        self.fieldnames = fieldnames  # list of keys for the dict
        self.restval = restval  # for writing short dicts
        if extrasaction.lower() not in ("raise", "ignore"):
            raise ValueError(
                "extrasaction " "(%s)" " must be 'raise' or 'ignore'" % extrasaction
            )
        self.extrasaction = extrasaction
        self.writer = writer(f, **kwds)

    def writeheader(self):
        header = dict(zip(self.fieldnames, self.fieldnames))
        return self.writerow(header)

    def _dict_to_list(self, rowdict: Dict):
        if self.extrasaction == "raise":
            wrong_fields = rowdict.keys() - self.fieldnames
            if wrong_fields:
                raise ValueError(
                    "dict contains fields not in fieldnames: "
                    + ", ".join([repr(x) for x in wrong_fields])
                )
        return (rowdict.get(key, self.restval) for key in self.fieldnames)

    def writerow(self, rowdict: Dict):
        return self.writer.writerow(self._dict_to_list(rowdict))

    def writerows(self, rowdicts: iter):
        return self.writer.writerows(map(self._dict_to_list, rowdicts))
