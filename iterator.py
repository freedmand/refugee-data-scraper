import constants
import csv
import itertools
import os

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
  assert(date.startswith(prefix)), 'Invalid date format'


def readAllRows():
  for fn in os.listdir(constants.EXTRACTED_DIR):
    # Skip any non-CSV file.
    if not fn.endswith('.csv'): continue

    fullPath = os.path.join(constants.EXTRACTED_DIR, fn)
    with open(fullPath, 'rb') as csvfile:
      reader = csv.reader(csvfile, delimiter=',', quotechar='"')

      previousRow = None
      for row in reader:
        if row and row[0].startswith('From:'):
          if previousRow != None:
            yield previousRow
            previousRow = None
        else:
          previousRow = row

import csv
with open('combined_out.csv', 'wb') as csvfile:
  writer = csv.writer(csvfile, delimiter=',', quotechar='"')

  for i in readAllRows():
    writer.writerow(i)
