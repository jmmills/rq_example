#!/bin/bash

./redis-monitor.py --duration 10 &
./redis-live.py $*
