import constants
import os

# All CSV files should contain this text.
SUCCESSFUL_SCRAPE_MARKER = 'Data prior to 2002 was migrated into WRAPS from a legacy system therefore we are providing post-2002 data.'

if __name__ == '__main__':
  # Iterate through all extracted CSV files, finding those that do not contain
  # text indicating a successful scrape. The files with errors are reported and
  # deleted, so that they can be rescraped.
  errors = 0
  for fn in os.listdir(constants.EXTRACTED_DIR):
    # Skip any non-CSV file.
    if not fn.endswith('.csv'): continue

    fullPath = os.path.join(constants.EXTRACTED_DIR, fn)
    with open(fullPath) as f:
      contents = f.read()

    if SUCCESSFUL_SCRAPE_MARKER not in contents:
      # Log any error-laden CSV files and remove them.
      print 'Error: %s' % fn
      errors += 1
      os.remove(fullPath)

  print 'Total errors: %d' % errors
