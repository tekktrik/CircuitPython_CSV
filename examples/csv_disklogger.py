# SPDX-FileCopyrightText: 2022 @Skicka for Adafruit Industries / Hakcat
# Logging data to .CSV file on CircuitPython Disk
# SPDX-License-Identifier: MIT

# If you get a read-only filesystem error, add "storage.remount('/', False)" in boot.py
# Make sure you add a way to reverse this in boot.py or your CP device won't show up via USB
# See example below: 
# https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/data-logger

import os
import random
import circuitpython_csv as csv

# Check if .CSV file is already present. If not, we write CSV headers.
all_files = os.listdir() ## List all files in directory
if "datelog.csv" not in all_files: 
    with open("datelog.csv", mode="w", encoding="utf-8") as writablefile:
        csvwriter = csv.writer(writablefile)
        csvwriter.writerow(["Year", "Month", "Day", "Hour", "Minute"])

# Now that the file exists (or already did) we make a random date 
year = random.randint(1999,2022); month = random.randint(1,12)
day = random.randint(1,30); hour = random.randint(0,23); minute = random.randint(0,60)

# We append this to the .CSV file
with open("datelog.csv", mode="a", encoding="utf-8") as writablefile:
    csvwriter = csv.writer(writablefile)
    csvwriter.writerow([year, month, day, hour, minute])

# Finally, we try to read back the last line in the CSV file to make sure it wrote.
with open("datelog.csv", "r", encoding="utf-8") as file:
    data = file.readlines()
    print(data[-1])
