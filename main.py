#!/usr/bin/env python
import sys

from PIL import ImageFont

import inkyphat
import requests
import arrow

# Constants
SUNDAY = 6

START_OF_SERVICE_MON_TO_SAT = arrow.now().replace(hour=5, minute=14)
START_OF_SERVICE_SUN = arrow.now().replace(hour=6, minute=54)

START_OF_SERVICE = START_OF_SERVICE_SUN if arrow.now().weekday() == SUNDAY else START_OF_SERVICE_MON_TO_SAT
END_OF_SERVICE = arrow.now().replace(hour=23, minute=24)

NO_TRAINS_TIMETABLED = arrow.now() < START_OF_SERVICE or arrow.now() > END_OF_SERVICE

# Fonts
BOOKBOLD_MEDIUM = ImageFont.truetype('Lato2OFL/Lato-Bold.ttf', 16)#('NJFont-BookBold.otf', 16)
SIGNING_LARGE = ImageFont.truetype('Lato2OFL/Lato-Heavy.ttf', 40) #njfontsigning-medium.ttf', 40)
SIGNING_MEDIUM = ImageFont.truetype('Lato2OFL/Lato-Heavy.ttf', 16)#njfontsigning-medium.ttf', 16)
BOOK_MEDIUM = ImageFont.truetype('Lato2OFL/Lato-Regular.ttf', 16)#NJFont-Book.otf', 16)
BOOK_SMALL = ImageFont.truetype('Lato2OFL/Lato-Regular.ttf', 12)#NJFont-Book.otf', 12)

# URLs
BAKERLOO_STATUS = 'https://api.tfl.gov.uk/Line/bakerloo/Status'
OVERGROUND_STATUS = 'https://api.tfl.gov.uk/Line/london-overground/Status'

# Renamings
RENAMES = {
    'London Overground': 'Overground'
}

# Get next trains
r = requests.get('https://api.tfl.gov.uk/StopPoint/910GWATFDHS/Arrivals')

trains = []

for train in r.json():
    if train['destinationNaptanId'] == '910GEUSTON':
        train_time = arrow.get(train['expectedArrival']).to('Europe/London')
        train_mins = (train_time - arrow.now()).seconds / 60
        trains.append((train_time, train_mins))

trains = sorted(trains, key=lambda x: x[0])

TRAINS_DISRUPTED = trains[0][1] > 20

# Get line 1 status
r = requests.get(BAKERLOO_STATUS)

for status in r.json():
    line_1_name = status['name']
    line_1_status_text = status['lineStatuses'][0]['statusSeverityDescription']
    line_1_status_code = status['lineStatuses'][0]['statusSeverity']
    line_1_status_w, line_1_status_h = BOOK_MEDIUM.getsize(line_1_status_text)

if line_1_status_code != 10:
    TRAINS_DISRUPTED = True

# Get line 2 status
r = requests.get(OVERGROUND_STATUS)

for status in r.json():
    line_2_name = RENAMES.get(status['name'], status['name'])
    line_2_status_text = status['lineStatuses'][0]['statusSeverityDescription']
    line_2_status_code = status['lineStatuses'][0]['statusSeverity']
    line_2_status_w, line_2_status_h = BOOK_MEDIUM.getsize(line_1_status_text)

if line_1_status_code != 10:
    TRAINS_DISRUPTED = True


inkyphat.set_border(inkyphat.RED if TRAINS_DISRUPTED else inkyphat.WHITE)


inkyphat.set_rotation(180)

# Show the backdrop image

#inkyphat.set_image("resources/hello-badge.png")
#inkyphat.show()

# Add the text


station = 'Euston'

# Center the text and align it with the name strip

#x = (inkyphat.WIDTH / 2) - (w / 2)
#y = 12 - (h / 2)

train_1_w, train_1_h = SIGNING_LARGE.getsize('%d' % trains[0][1])
train_2_w, train_2_h = BOOKBOLD_MEDIUM.getsize('%d' % trains[1][1])
train_3_w, train_3_h = BOOKBOLD_MEDIUM.getsize('%d' % trains[2][1])

#inkyphat.rectangle((0,0,212,104), inkyphat.RED)

# Next Train
inkyphat.text((4, -4), station, inkyphat.BLACK, SIGNING_LARGE)
inkyphat.text((inkyphat.WIDTH - train_1_w, 0), '%d' % trains[0][1], inkyphat.BLACK, SIGNING_LARGE)

# Train 2
inkyphat.text((4, 40), 'EUS', inkyphat.BLACK, BOOKBOLD_MEDIUM)
inkyphat.text((((inkyphat.WIDTH - 20) / 2) - train_2_w, 40), '%d' % trains[1][1], inkyphat.BLACK, BOOKBOLD_MEDIUM)

# Train 3
inkyphat.text((((inkyphat.WIDTH + 20) / 2) + 4, 40), 'EUS', inkyphat.BLACK, BOOKBOLD_MEDIUM)
inkyphat.text((inkyphat.WIDTH - train_3_w, 40), '%d' % trains[2][1], inkyphat.BLACK, BOOKBOLD_MEDIUM)


#inkyphat.text((160, 14), str(trains[2][1]), inkyphat.BLACK, SIGNING_MEDIUM)


# inkyphat.text((120, 26), trains[0][0].format('HH:mm'), inkyphat.BLACK, BOOK_SMALL)
#inkyphat.text((184, 2), trains[1][0].format('HH:mm'), inkyphat.BLACK, BOOK_SMALL)
#inkyphat.text((184, 16), trains[2][0].format('HH:mm'), inkyphat.BLACK, BOOK_SMALL)


# Refresh the text strip
#
# Partial updates are snapped to 8 pixel boundaries vertically,
# so the name strip is carefully aligned to an 8 pixel grid
#
# Generally you should refresh only whole horizontal rows.
# Colours either side of the update area will be washed out!
#
# Your refreshed area may have a white border
# which could cut into surrounding colours.
#
# Remember:
# Art smartly to update partly!

inkyphat.set_partial_mode(0,64,0,inkyphat.WIDTH)
inkyphat.show()




if line_1_status_code != 10:
    inkyphat.rectangle((0, 0, 212, 104), inkyphat.RED)
    inkyphat.text((4, 60), line_1_name, inkyphat.WHITE, BOOKBOLD_MEDIUM)
    inkyphat.text((inkyphat.WIDTH - line_1_status_w, 60), line_1_status_text, inkyphat.WHITE, BOOK_MEDIUM)
else:
    inkyphat.rectangle((0,0,212,104), inkyphat.WHITE)
    inkyphat.text((4, 56), line_1_name, inkyphat.BLACK, BOOKBOLD_MEDIUM)
    inkyphat.text((inkyphat.WIDTH - line_1_status_w, 56), line_1_status_text, inkyphat.BLACK, BOOK_MEDIUM)

inkyphat.set_partial_mode(56,80,0,inkyphat.WIDTH)
inkyphat.show()



if line_2_status_code != 10:
    inkyphat.rectangle((0, 0, 212, 104), inkyphat.RED)
    inkyphat.text((4, 80), line_2_name, inkyphat.WHITE, BOOKBOLD_MEDIUM)
    inkyphat.text((inkyphat.WIDTH - line_2_status_w, 80), line_2_status_text, inkyphat.WHITE, BOOK_MEDIUM)
else:
    inkyphat.rectangle((0,0,212,104), inkyphat.WHITE)
    inkyphat.text((4, 80), line_2_name, inkyphat.BLACK, BOOKBOLD_MEDIUM)
    inkyphat.text((inkyphat.WIDTH - line_2_status_w, 80), line_2_status_text, inkyphat.BLACK, BOOK_MEDIUM)

inkyphat.set_partial_mode(80,104,0,inkyphat.WIDTH)
inkyphat.show()

