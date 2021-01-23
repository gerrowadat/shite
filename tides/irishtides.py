#!/usr/bin/python3

# Scrape marine.ie for tide forecasts for a given station and year.
# See the form at the URL below for the list of stations.

import datetime
import logging
import requests
from bs4 import BeautifulSoup


class Error(Exception):
  pass


class TideRequestError(Error):
  pass


class TidePredictionUsageError(Error):
  pass


class TidePredictionBackendError(Error):
  pass


# List of TideCacheEntry
_TIDE_CACHE = []

# {station id (int) : station name (str)}
_ID_CACHE = {}


class TideCacheEntry(object):
  def __init__(self, station_name, station_id, date, tide_data):
    self._station_name = station_name
    self._station_id = station_id
    self._date = date
    self._tide_data = tide_data
    self._last_access = datetime.datetime.now()

  @property
  def station_id(self):
    return self._station_id

  @property
  def date(self):
    return self._date

  @property
  def is_stale(self):
    td = datetime.timedelta(days=3)
    return (datetime.datetime.now() - self._last_access) > td

  @property
  def tide_data(self):
    self._last_access = datetime.datetime.now()
    return self._tide_data


class Tides(object):
  """Convenience object for a server seving tide data."""
  def __init__(self, logger=None):
    self._logger = logger or logging.getLogger('irishtides')
    self._tpf = TidePredictionFetcher()

  def request_date_or_today(self, date):
    """Return a datetime.date for either today or the supplied date."""
    if not date:
      return datetime.date.today()

    error = None

    # Use the one true date format
    try:
      (year, month, day) = date.split('-')
    except ValueError:
      error = 'Specify date in YYYY-MM-DD or omit for today'

    if len(year) != 4 or len(month) != 2 or len(day) != 2:
      error = 'Specify date in YYYY-MM-DD or omit for today'

    for elem in (year, month, day):
      if not elem.isnumeric():
        error = 'Specify date in YYYY-MM-DD or omit for today'

    if error:
      raise TideRequestError(error)

    return datetime.date(year, month, day)

  def _populate_station_info(self, station_name, station_id):
    """ One or the other of these is set. return both values."""
    global _ID_CACHE
    if not _ID_CACHE:
      self._logger.debug('Fetching Station List')
      _ID_CACHE = self._tpf.GetAllStations()

    if station_name:
      if station_name not in _ID_CACHE:
        raise TideRequestError('Unknown station %s. Stations Available: %s' % (
            station_name, [x for x in _ID_CACHE.keys()]))
      if not station_id:
        station_id = _ID_CACHE[station_name]
    else:
      if station_id not in _ID_CACHE.values():
        raise TideRequestError('Unknown station %s.\n Stations Available: %s' % (
            station_name, ['%s: %s' % (x, _ID_CACHE[x]) for x in _ID_CACHE.keys()]))
      if not station_name:
        station_name = [s_n for s_n in _ID_CACHE.keys() if _ID_CACHE[s_n] == station_id][0]

    return (station_name, station_id)

  def _try_cache(self, station_name, station_id, request_date):
    global _TIDE_CACHE
    # See if we have non-stale data to serve.
    cache_hits = [e for e in _TIDE_CACHE if e.station_id == station_id and e.date == request_date and not e.is_stale]
    if cache_hits:
      self._logger.debug('Cache hit for %s on %s' % (station_name, request_date))
      return cache_hits[0].tide_data
    return None

  def get_tide_data(self, station_name, station_id, request_date):
    global _TIDE_CACHE
    if station_name is None and station_id is None:
      raise TideRequestError('Must specify station_name or station_id')

    (station_name, station_id) = self._populate_station_info(station_name, station_id)

    tide_data = self._try_cache(station_name, station_id, request_date)

    if not tide_data:
      self._logger.debug('Backend hit for %s on %s' % (station_name, request_date))
      tide_data = self._tpf.GetTidePredictionForDate(request_date, station_id=station_id)

    # Populate cache
    tc = TideCacheEntry(station_name, station_id, request_date, tide_data)
    _TIDE_CACHE.append(tc)

    return tide_data


class TidePredictionFetcher(object):
  def __init__(self):
    self._url = 'http://webapps.marine.ie/IrishTidesChartingApplication/TidePredictions.aspx'
    # 'station name': ID
    self._stations = None

  def GetAllStations(self):
    if self._stations:
      return self._stations

    rep = requests.get(self._url)
    soup = BeautifulSoup(rep.text, features='html.parser')
    form = soup.find('form')
    opts = form.find_all('option')
    if not opts or len(opts) == 0:
      raise TidePredictionBackendError('malformed response from marine.ie')
    stations = {}
    for o in opts:
      stations[o.text] = o['value']
    self._stations = stations
    return self._stations

  def GetStationID(self, station_name):
    """Given a full name of a station form the form, return its ID."""
    stations = self.GetAllStations()
    if station_name not in stations:
      raise TidePredictionUsageError('unknown station <%s>' % (station_name, ))
    return stations[station_name]

  def GetStationName(self, station_id):
    """Given a Station Id, return its full name."""
    stations = self.GetAllStations()
    if station_id not in stations.values():
      raise TidePredictionUsageError('unknown station <%s>' % (station_id, ))
    all_ids = [x for x in stations.keys() if stations[x] == station_id]
    if len(all_ids) != 1:
      raise TidePredictionBackendError('got %d results for station id %d!' % (len(all_ids), station_id))
    return all_ids[0]

  def GetTidePredictionForToday(self, station_name=None, station_id=None):
    return self.GetTidePredictionForDate(
        datetime.date.today(), station_name=station_name, station_id=station_id)

  def GetTidePredictionForDate(self, dt, station_name=None, station_id=None):
    """Retun tide predictions for 6 days surrounding the date specified.

    This is the amount of data returned by marine.ie by default.

    dt is a datetime.date object.

    Returns a dict of { timestamp (str) : waterlevel (float) }
    """
    if station_id is None:
      if station_name is None:
        raise TidePredictionUsageError(
            'must specify station_name or station_id to GetTidePredictionForDate')
      else:
        station_id = self.GetStationID(station_name)

    rep = requests.get(self._url)

    soup = BeautifulSoup(rep.text, features='html.parser')
    form = soup.find('form')
    inputs = form.find_all('input')

    post_data = {}

    for i in inputs:
      post_data[i['name']] = i['value']

    post_data['lstSites'] = station_id
    post_data['SelectedDateTime'] = '%s/%s/%s' % (dt.day, dt.month, dt.year)

    rep = requests.post(self._url, data=post_data)

    soup = BeautifulSoup(rep.text, features='html.parser')

    dp = soup.find(id='DataPanel')

    d_tbl = dp.find('table')

    d_rows = d_tbl.find_all('tr')

    data = {}

    for row in d_rows:
      d_td = row.find_all('td')
      if d_td:
        # Website does dates as DD/MM/YYYY which can get in the sea (so to speak).
        stupid_date = d_td[0].text
        actual_date = datetime.datetime.strptime(stupid_date, '%d/%m/%Y %H:%M:%S')
        data[actual_date.strftime('%Y-%m-%d %H:%M:%S')] = float(d_td[1].text)

    return data


def main():
  tpf = TidePredictionFetcher()
  tides = tpf.GetTidePredictionForToday(station_name='Dublin Port')
  for t in tides:
    print('%s: %s' % (t, tides[t]))


if __name__ == '__main__':
  main()
