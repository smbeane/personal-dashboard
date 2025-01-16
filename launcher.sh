#!/bin/sh
# launcer.sh
# navigate to home directory, then to this directory, then execute the python script

cd /
cd home/smbeane5235/spotify/testing
python ./dashboard.py --led-slowdown-gpio=4 -b=75
cd /

