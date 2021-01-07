import datetime
import cherrypy

from astral import LocationInfo
from astral.sun import sun
from astral import moon


class Error(Exception):
  pass


class SunBlob(object):

  @cherrypy.expose
  def index(self, latitude=None, longitude=None):
    if latitude:
      try:
        latitude = float(latitude)
      except ValueError:
        return 'latitude must be a floating point number'

    if longitude:
      try:
        longitude = float(longitude)
      except ValueError:
        return 'longitude must be a floating point number'

    # Default to Dublin, Ireland
    city = LocationInfo(latitude=(latitude or 53.427), longitude=(longitude or -6.25))
    s = sun(city.observer, datetime.date.today())

    ret = 'Sunrise: %s<br/>\n' % (s['sunrise'].strftime('%H:%M'))
    ret += 'Sunset: %s<br/>\n' % (s['sunset'].strftime('%H:%M'))

    phasenum = moon.phase(datetime.date.today())

    if 14 < phasenum < 15:
      ret += 'Full moon'

    return ret
