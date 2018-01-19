import constants
import csv
import itertools
import os
import datetime

class ImmigrationPatter(object):
  def __init__(self, day, originCountry, destState, destCounty, count):
    self.day = day
    self.originCountry = originCountry
    self.destState = destState
    self.destCounty = destCounty
    self.count = count

  def __repr__(self):
    return '(%s) %d refugee%s from %s to %s, %s' % (
      self.day.strftime('%Y-%m-%d'), self.count,
      '' if self.count == 1 else 's', self.originCountry, self.destCounty,
      self.destState
    )

def extractDate(date, prefix = "From: "):
  assert(date.startswith(prefix)), 'Invalid date format: %s' % date
  # Trim the prefix.
  date = date[len(prefix):]
  # Parse the date.
  return datetime.datetime.strptime(date, '%d %b %Y')

def cleanRow(row):
  day = extractDate(row[0])
  state = row[2]
  country = row[5]
  city = row[7]
  count = row[8]
  return [day, country, state, city, count]

def readAllRows():
  # Return the header row.
  yield ['Day', 'Country', 'State', 'City', 'Count']

  for fn in os.listdir(constants.EXTRACTED_DIR):
    # Skip any non-CSV file.
    if not fn.endswith('.csv'): continue

    fullPath = os.path.join(constants.EXTRACTED_DIR, fn)
    with open(fullPath, 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"')

      # Only return rows after finding a valid header.
      foundHeader = False
      for row in reader:
        if foundHeader:
          if row and row[0].startswith('From:'):
            yield cleanRow(row)
          else:
            # If the row is not valid, stop consuming rows after that.
            foundHeader = False
        # The valid header we're looking for in the data.
        if row == ['Textbox87','Textbox82','nat_definition4','region_name_3','textbox37','Category3','textbox39','Assur_DestinationCity1','Cases3','Cases4']:
          foundHeader = True

import csv
with open('combined_out.csv', 'wb') as csvfile:
  writer = csv.writer(csvfile, delimiter=',', quotechar='"')

  for i in readAllRows():
    writer.writerow(i)
