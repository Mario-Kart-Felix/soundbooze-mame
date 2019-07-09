#!/bin/sh

sleep 2 
xterm -fn 9x15 +sb -geometry 400x400+800+600 -hold -e python ~/soundbooze-mame/sf2ce/obsolete/feed/log.py & 
python ~/soundbooze-mame/sf2ce/obsolete/feed/player1.py | python ~/soundbooze-mame/sf2ce/obsolete/resume.py
