#!/bin/sh
xdotool search --name "mame" windowsize 541 406
PID=`pgrep mame`
ID=`xdotool search --pid $PID`
xdotool windowmove $ID 107 114
