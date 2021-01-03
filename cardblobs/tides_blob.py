import time
import datetime
import cherrypy

import irishtides


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


class TidesBlob(object):
  @cherrypy.expose
  def index(self, station_name=None, station_id=None, date=None):
    global _DATA_CACHE
    global _ID_CACHE

    if station_name is None and station_id is None:
      return 'Must specify station_name or station_id'

    if date:
      # Use the one true date format
      try: 
        (year, month, day) = date.split('-')
      except ValueError:
        return 'Specify date in YYYY-MM-DD or omit for today'

      if len(year) != 4 or len(month) != 2 or len(day) != 2:
        return 'Specify date in YYYY-MM-DD or omit for today'

      for elem in (year, month, day):
        if not elem.isnumeric():
          return 'Specify date in YYYY-MM-DD or omit for today'

      request_date = datetime.date(year, month, day)
    else:
      request_date = datetime.date.today()

    tpf = irishtides.TidePredictionFetcher()

    if not _ID_CACHE:
      cherrypy.log('Fetching Station List')
      _ID_CACHE = tpf.GetAllStations()

    # We alreadyknow that one of station_name or station_id are specified.
    if station_name:
      if station_name not in _ID_CACHE:
        return 'Unknown station %s. Stations Available: %s' % (station_name, [x for x in _ID_CACHE.keys()])
      if not station_id:
        station_id = _ID_CACHE[station_name]
    else:
      if station_id not in _ID_CACHE.values():
        return 'Unknown station %s.\n Stations Available: %s' % (
                station_name, ['%s: %s' % (x, _ID_CACHE[x]) for x in _ID_CACHE.keys()])
      if not station_name:
        station_name = [s_n for s_n in _ID_CACHE.keys() if _ID_CACHE[s_n] == station_name][0]


    # See if we have non-stale data to serve.
    cache_hits = [e for e in _TIDE_CACHE if e.station_id == station_id and e.date == request_date and not e.is_stale]
    if cache_hits:
      cherrypy.log('Cache hit for %s on %s' % (station_name, request_date))
      cache = cache_hits[0].tide_data
      ret = ''
      for e in cache:
        ret += '%s: %s\n' % (e, cache[e])
      return ret
        

    # No Cache hit, make the request
    cherrypy.log('Accessing marine.ie for Tides for %s on %s' % (station_name, request_date))

    tide_data = tpf.GetTidePredictionForDate(request_date, station_id=station_id)

    # Populate cache
    tc = TideCacheEntry(station_name, station_id, request_date, tide_data)
    _TIDE_CACHE.append(tc)

    cherrypy.log('Backend hit for %s on %s' % (station_name, request_date))
    ret = ''
    for e in tide_data:
      ret += '%s: %s\n' % (e, tide_data[e])
    return ret

