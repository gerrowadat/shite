Because there's no official image (as far as I know).

Plant gateway: https://github.com/ChristianKuehnel/plantgateway

Place plantgw.yaml (without the . at the start) in your directory, and map it to /config -- the log will appear there also.

```docker run -v /path/to/configdir:/root --privileged --net=host gerrowadat/plant-gateway```
