#!/bin/sh
DATE=`date +"%Y-%m-%d-%H-%M-%S"`
ffmpeg -video_size 541x406 -framerate 25 -f x11grab -i :0.0+107,114 $DATE".mp4"
