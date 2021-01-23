import datetime
import cherrypy

import irishtides


class Error(Exception):
  pass


class TidesBlob(object):
  def __init__(self):
    self._t = irishtides.Tides()

  @cherrypy.expose
  def index(self):
    raise cherrypy.HTTPError(418)

  @cherrypy.expose
  def raw(self, station_name=None, station_id=None, date=None):
    try:
      request_date = self._t.request_date_or_today(date)
      tide_data = self._t.get_tide_data(station_name, station_id, request_date)
    except irishtides.TideRequestError as e:
      return 'Request error: %s' % (str(e))

    ret = ''
    for e in tide_data:
      ret += '%s: %s\n' % (e, tide_data[e])
    return ret

  @cherrypy.expose
  def today(self, station_name=None, station_id=None):
    request_date = datetime.date.today()

    try:
      tide_data = self._t.get_tide_data(station_name, station_id, request_date)
    except irishtides.TideRequestError as e:
      return 'Request error: %s' % (str(e))

    today_str = '%d-%02d-%02d' % (request_date.year, request_date.month, request_date.day)
    cherrypy.log('[/today] showing data for %s on %s' % (station_name, today_str))
    today_data = [d for d in tide_data.keys() if d.startswith(today_str)]

    ret = ''
    for e in today_data:
      ret += '%s: %s\n' % (e, tide_data[e])
    return ret
