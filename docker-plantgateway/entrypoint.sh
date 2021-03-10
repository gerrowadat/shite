#!/bin/bash
set -e

# Time in minutes between updates
PLANT_INTERVAL=60

PLANT_INTERVAL_SECS=$(($PLANT_INTERVAL * 60))

while true
do
	"$@"
	RUN_DATE=`date`
	echo "$RUN_DATE: Sleeping $PLANT_INTERVAL_SECS secs..."
        sleep $PLANT_INTERVAL_SECS	

done

