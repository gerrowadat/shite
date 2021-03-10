Because there's no official image (as far as I know).

Plant gateway: https://github.com/ChristianKuehnel/plantgateway

Place plantgw.yaml (without the . at the start) in your cofig directory, and map it to /config -- the log will appear there also.

```docker run -v /path/to/configdir:/config -e PLANT_INTERVAL=60 --privileged --net=host gerrowadat/plant-gateway```

By default it updates hourly, set PLANT_INTERVAL to a number of minutes otherwise.
