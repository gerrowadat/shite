import os
import cherrypy

import tides_blob

class Root(object):
  @cherrypy.expose
  def index(self):
      return "Hello World!"

class CardBlobIndex(object):
  @cherrypy.expose
  def index(self):
    return "So many card blobs."

class BusBlob(object):
  @cherrypy.expose
  def index(self):
    return 'bus stuff goes here (if we ever get a bus again)'


def main():
  cf = os.path.join(os.path.dirname(__file__), 'cherrypy.conf')

  root = Root()
  root.cardblobs = CardBlobIndex()
  root.cardblobs.tides = tides_blob.TidesBlob()
  root.cardblobs.bus = BusBlob()

  cherrypy.quickstart(root, config=cf)

main()
