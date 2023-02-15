# SPDX-FileCopyrightText: 2023 Jos D. Montoya
# Reading data from a .CSV file on CircuitPython Disk
# SPDX-License-Identifier: MIT

import time
import sdcardio
import storage
import board
import displayio
from adafruit_displayio_layout.widgets.cartesian import Cartesian
import circuitpython_csv as csv

print("Setting up SD Card")
spi = board.SPI()
sdcard = sdcardio.SDCard(spi, board.SD_CS)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Data is a copy of the version could be found in
# https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=30682
# Title: THUNDER BAY ONTARIO Daily weather

weather_file = "/sd/en_climate_daily_ON_6048268_2023_P1D.csv"
raw_data = []
data = []

print("Reading the csv file contents. This could take some time")

# We use the library reader to get the values from the weather file
with open(weather_file, "r") as csvfile:
    row = csv.reader(csvfile)
    for item in row:
        raw_data.append(item[11])
raw_data = raw_data[1:40]

# We convert the values to something that we can plot
for i, item in enumerate(raw_data):
    data.append((i, int(float(item[-4:]))))

print("Done reading")

# create the display on the PyPortal or Clue or PyBadge(for example)
display = board.DISPLAY
print("Now we will display the data")

# Create a Cartesian widget
my_plane = Cartesian(
    x=30,  # x position for the plane
    y=10,  # y plane position
    width=140,  # display width
    height=105,  # display height
    xrange=(0, 50),  # x range
    yrange=(0, 50),  # y range
)

my_group = displayio.Group()
my_group.append(my_plane)
display.show(my_group)  # add high level Group to the display

for x, y in data:
    my_plane.add_plot_line(x, y)
    time.sleep(0.2)

while True:
    pass
