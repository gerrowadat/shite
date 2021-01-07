Home Assistant integrations make me angry so I'm just going to serve these internally via webpage embed cards in lovelace.

`docker run -d  -p 54332:54332 gerrowadat/cardblobs:latest`

Then look at:

  http://myhost:54332/cardblobs/...

    .../tides/ -- For Irish tide forecasts (not fully implemented yet). See code for options.

    .../sun/ -- Shows the sunrise and sunset times for today in Dublin, Ireland.

    .../bus/ -- Not implemented yet, wil be Next Dublin Bus from your local stop.


