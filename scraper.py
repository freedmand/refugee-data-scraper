import requests

import constants
import helpers

def grabDate(date):
  """Grabs the refugee data for the specified date for all countries as a CSV.

  Requests the refugee immigration data to every state in America from every
  country in the world for the specified date, writing the results to a file in
  the extracted/ directory with the name set to the data. If no download URL is
  found, nothing happens.

  Args:
      date: The date as a string in the American m/d/yyyy form, e.g. 3/22/2015
            or 12/1/2008.
  """
  print 'Grabbing %s' % date
  # Initialize a session that persists state.
  requester = requests.session()

  # Grab the site URL in a GET request to start a session.
  r = requester.get(constants.URL)
  print 'Ran initial request'

  # Extract the keep-alive token and new data parameters.
  keepAlive = helpers.getKeepAlive(r)
  data = helpers.getNewData(r)
  data.update(constants.UPDATE_DATA)
  # Set the data for the date parameters to the date specified in the function
  # argument.
  for key in constants.DATA_UPDATE_KEYS:
    data[key] = date

  # Post to the keep-alive URL to start a session (this is different from the
  # cookies that are automatically tracked with requests.session).
  updatedKeepAliveUrl = constants.KEEP_ALIVE_URL % keepAlive
  r = requester.post(updatedKeepAliveUrl)
  print r.text

  # Make another request with the updated data to retrieve the download URL.
  r = requester.post(constants.URL, data = data)
  print 'Made secondary request'
  downloadUrl = helpers.getDownloadUrl(r)
  if downloadUrl == '':
    print 'No download URL found; assuming empty'
    return
  print 'Download URL: %s' % downloadUrl

  r = requester.get(downloadUrl)
  helpers.writeToFile(r, helpers.getCsvFnFromAmericanDate(date))
  print 'Finished'
