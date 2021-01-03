import os
import cherrypy

class Root(object):
  @cherrypy.expose
  def index(self):
      return "Hello World!"

class CardBlobIndex(object):
  @cherrypy.expose
  def index(self):
    return "So many card blobs."

class TidesIndex(object):
  @cherrypy.expose
  def index(self):
    return 'tides go in and out and such.'

class BusIndex(object):
  @cherrypy.expose
  def index(self):
    return 'bus stuff goes here (if we ever get a bus again)'


def main():
  cf = os.path.join(os.path.dirname(__file__), 'cherrypy.conf')

  root = Root()
  root.cardblobs = CardBlobIndex()
  root.cardblobs.tides = TidesIndex()
  root.cardblobs.bus = BusIndex()

  cherrypy.quickstart(root, config=cf)

main()
