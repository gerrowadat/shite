#!/bin/bash
set -e

CONFIG_DIR=/config

"$@" /shite/playerbot/playerbot.py --config_dir=$CONFIG_DIR

