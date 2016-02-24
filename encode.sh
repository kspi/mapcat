#!/bin/bash -e

framedir=output/video_frames_sharp

if ! [ -d $framedir ]; then
    mkdir $framedir
    export MAGICK_THREAD_LIMIT=1
    parallel -j2 --eta "o=$framedir/{/}; test -f $o || convert -sharpen 5 {} $o" ::: output/video_frames/*.png
fi

ffmpeg \
    -r 60 -i "$framedir/%05d.png" \
    -i input/music.wav \
    -map 0:0 -map 1:0 \
    -vf 'crop=1920:1080:0:420' \
    -c:a libvorbis -qscale:a 8 -b:v 3.5M -shortest \
    -y -threads 2 \
    output/mapcat.webm
