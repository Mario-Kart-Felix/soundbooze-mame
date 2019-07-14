#!/bin/sh
xdotool search --name "mame" windowsize 800 600
PID=`pgrep mame`
ID=`xdotool search --pid $PID`
xdotool windowmove $ID 100 100
