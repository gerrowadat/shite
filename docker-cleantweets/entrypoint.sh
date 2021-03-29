#!/bin/bash
set -e

CONFIG_DIR=/config
CONFIG_FILE=$CONFIG_DIR/cleantweets.ini
DAYSTOKEEP=90

if [ ! -f $CONFIG_FILE ];
then
	echo "Cannot find config file $CONFIG_FILE, creating..."
	touch $CONFIG_FILE
fi

python3 "$@" --verbose --delete --unlike --days=$DAYSTOKEEP --config=$CONFIG_FILE

