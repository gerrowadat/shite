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
  def __init__(self):
    self._tpf = irishtides.TidePredictionFetcher()

  def _request_date(self, date):
    """Return a datetime.date for either today or the supplied date."""
    if not date:
      return datetime.date.today()

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

    return datetime.date(year, month, day)

  def _populate_station_info(self, station_name, station_id):
    """ One or the other of these is set. return both values."""
    global _ID_CACHE
    if not _ID_CACHE:
      cherrypy.log('Fetching Station List')
      _ID_CACHE = self._tpf.GetAllStations()

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

    return (station_name, station_id)

  def _try_cache(self, station_name, station_id, request_date):
    global _TIDE_CACHE
    # See if we have non-stale data to serve.
    cache_hits = [e for e in _TIDE_CACHE if e.station_id == station_id and e.date == request_date and not e.is_stale]
    if cache_hits:
      cherrypy.log('Cache hit for %s on %s' % (station_name, request_date))
      return cache_hits[0].tide_data
    return None

  @cherrypy.expose
  def index(self, station_name=None, station_id=None, date=None):
    global _DATA_CACHE
    global _ID_CACHE

    if station_name is None and station_id is None:
      return 'Must specify station_name or station_id'

    request_date = self._request_date(date)

    (station_name, station_id) = self._populate_station_info(station_name, station_id)

    tide_data = self._try_cache(station_name, station_id, request_date)

    if not tide_data:
      cherrypy.log('Backend hit for %s on %s' % (station_name, request_date))
      tide_data = self._tpf.GetTidePredictionForDate(request_date, station_id=station_id)

    # Populate cache
    tc = TideCacheEntry(station_name, station_id, request_date, tide_data)
    _TIDE_CACHE.append(tc)

    ret = ''
    for e in tide_data:
      ret += '%s: %s\n' % (e, tide_data[e])
    return ret
