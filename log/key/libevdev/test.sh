#!/bin/bash

DEVICE="/dev/input/event0"

sleep 5
evemu-event $DEVICE  --type EV_KEY --code KEY_R --value 1 --sync
sleep 2
evemu-event $DEVICE --type EV_KEY --code KEY_R --value 0 --sync
