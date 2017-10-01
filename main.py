import datetime
import os

import helpers
import scraper

if __name__ == '__main__':
  # Grab the current date.
  date = datetime.datetime.now()
  day = datetime.timedelta(days=1)

  # Start from yesterday in case all data for today has yet to be processed.
  date -= day

  # The number of files skipped because they have already been extracted.
  skipped = 0

  while date.year >= 2002:
    # Iterate from yesterday back in time day-by-day until 1/1/2002 (when the
    # refugee dataset starts).
    americanDate = helpers.americanDateFormat(date)
    # Set date to the day before for the next iteration.
    date -= day

    if os.path.exists(helpers.getCsvFnFromAmericanDate(americanDate)):
      # Skip files that have already been extracted.
      skipped += 1
      continue

    if skipped > 0:
      print 'Skipped %d files' % skipped
      skipped = 0

    scraper.grabDate(americanDate)
