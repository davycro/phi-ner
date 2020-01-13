#!/bin/sh

tmpfile="./tmp/tmp.png"
rm -f $tmpfile
ffmpeg -v warning -i $1 -vframes 1 -y $tmpfile
convert $tmpfile -gravity north -crop 100x20% +repage - | tesseract stdin "t" &> /dev/null
cat "t.txt"
rm t.txt


