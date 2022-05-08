# SPDX-FileCopyrightText: 2022 @Skicka for Adafruit Industries / Hakcat
# Logging data to .CSV file on CircuitPython Disk
# SPDX-License-Identifier: MIT

## If you get a read-only filesystem error, you must add "storage.remount('/', False)" in boot.py to enable writing to disk
## Make sure you add a way to reverse this in boot.py! Otherwise your CP device won't show up via USB anymore 
## See example here: https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger

import os
import time
import random
import storage
import circuitpython_csv as csv

## Check if .CSV file is already present. If not, we write CSV headers.
all_files = os.listdir() ## List all files in directory
if "datelog.csv" not in all_files: 
    with open("datelog.csv", mode="w", encoding="utf-8") as writablefile:
        csvwriter = csv.writer(writablefile)
        csvwriter.writerow(["Year", "Month", "Day", "Hour", "Minute"])

## Now that the file exists (or already did) we create a random date & try to append it to the .CSV file
with open("datelog.csv", mode="a", encoding="utf-8") as writablefile:
    RandomDate = [random.randint(1999,2022), random.randint(1,12), random.randint(1,30), random.randint(0,23), random.randint(0,60)]
    csvwriter = csv.writer(writablefile)
    csvwriter.writerow(RandomDate)

## Finally, we try to read back the last line in the CSV file to make sure it wrote.
with open("datelog.csv", "r") as file:
    data = file.readlines()
    print(data[-1])
