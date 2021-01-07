import datetime
import cherrypy

from astral import LocationInfo
from astral.sun import sun
from astral import moon


class Error(Exception):
  pass


class SunBlob(object):

  @cherrypy.expose
  def index(self):
    city = LocationInfo(
        "Dublin",
        "Ireland",
        latitude=53.427,
        longitude=-6.25,
        timezone='Europe/Dublin')
    s = sun(city.observer, datetime.date.today())

    ret = 'Sunrise: %s<br/>\n' % (s['sunrise'].strftime('%H:%M'))
    ret += 'Sunset: %s<br/>\n' % (s['sunset'].strftime('%H:%M'))

    phasenum = moon.phase(datetime.date.today())

    if 14 < phasenum < 15:
      ret += 'Full moon'

    return ret
