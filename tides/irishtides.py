#!/usr/bin/python3

# Scrape marine.ie for tide forecasts for a given station and year.
# See the form at the URL below for the list of stations.

import requests
import datetime
from bs4 import BeautifulSoup


class Error(Exception):
  pass


class TidePredictionUsageError(Error):
  pass


class TidePredictionBackendError(Error):
  pass


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
      raise TidePredictionUsageError('unknown station <%s>' % (station_name, ))
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
        data[d_td[0].text] = float(d_td[1].text)

    return data


def main():
  tpf = TidePredictionFetcher()
  tides = tpf.GetTidePredictionForToday(station_name='Dublin Port')
  for t in tides:
    print('%s: %s' % (t, tides[t]))


if __name__ == '__main__':
  main()
