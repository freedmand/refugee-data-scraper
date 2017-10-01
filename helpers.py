"""Provides helper methods for extracting data and writing it to files."""

import json
import re
from bs4 import BeautifulSoup

import constants


def getNewData(response):
  """Extracts hidden input data from a response, returning a data dictionary.

  Extracts hidden input data from a response body, returning a dictionary of
  key-value pairs representing data to send to subsequent requests.

  Args:
      response: The Python requests response object, typically corresponding to
                a simple GET request on the main refugee explorer page.

  Returns:
      A dictionary with key-value pairs representing the data.
  """
  b = BeautifulSoup(response.text, 'html5lib')
  inputs = b.findAll('input', type='hidden')
  newdata = {elem.get('name'): elem.get('value') for elem in inputs}
  return newdata


def getKeepAlive(response):
  """Extracts and returns the keep alive token from the response.

  Extracts and returns the actual keep-alive token from within the response;
  this token enables subsequent requests for CSV data.

  Args:
      response: The Python requests response object, typically corresponding to
                a simple GET request on the main refugee explorer page.

  Returns:
      A keep-alive token which is used to validate subsequent requests.

  Raises:
      AssertionError: Could not extract a single keep-alive token from the page.
  """
  controlId = re.findall('ControlID=([a-fA-F0-9]+)"', response.text)
  assert len(controlId) == 1, 'Multiple or no tokens should not happen'
  return controlId[0]


def getDownloadUrl(response):
  """Extracts a URL from a response that can be used to download CSV results.

  After requesting a refugee search and passing in the proper validation, the
  subsequent response body will contain a download URL that can be used to get
  the actual contents in CSV format.

  Args:
      response: The Python requests response object corresponding to a validated
                request for data.

  Returns:
      The URL to download the requested data in CSV format, or an empty string
      if no download URL was found in the page.

  Raises:
      AssertionError: Extracted more than one download URL.
  """
  newUrl = re.findall('"ExportUrlBase":("[^"]+")', response.text)
  if len(newUrl) == 0: return ''
  assert len(newUrl) == 1, 'Multiple download URLs should not happen'
  return constants.HOST_URL + json.loads(newUrl[0]) + 'CSV'


def writeToFile(response, fn):
  """Writes the given response body to the specified file name.

  Writes the response body text (from the Python library `requests`) to the
  specified file name.

  Args:
      response: The Python requests response object.
      fn: The name of the file to write to.
  """
  with open(fn, 'w') as f:
    f.write(response.text.encode('utf8'))


def writeDataToFile(data, fn):
  """Writes the specified post data to the specified file name.

  Each item in the data dictionary is listed as a separate line with format:
    key: value

  Args:
      data: A dictionary of key-value pairs representing the data.
      fn: The name of the file to write to.
  """
  with open(fn, 'w') as f:
    for (key, value) in data.iteritems():
      f.write('%s: %s\n' % (key, value))


def americanDateFormat(date):
  """Formats the specified datetime object as an American date (m/d/yyyy).

  Args:
      date: A datetime object.

  Returns:
      A string of the form m/d/yyyy that represents the specified date, e.g.
      5/2/2012, or 12/25/2008.
  """
  return '{d.month}/{d.day}/{d.year}'.format(d = date)


def getCsvFnFromAmericanDate(date):
  """Returns the CSV file corresponding to the American-style date string.

  Args:
      date: A date in American format (m/d/yyyy).

  Returns:
      A path to the expected CSV file in the extracted/ directory for the
      specified date.
  """
  return '%s/%s.csv' % (constants.EXTRACTED_DIR, date.replace('/', '-'))
