#!/bin/sh

tmpfile="./tmp.png"
rm -f $tmpfile
ffmpeg -v warning -i $1 -vframes 1 -y $tmpfile
convert $tmpfile -gravity north -crop 100x20% -negate +repage - | tesseract stdin "t" &> /dev/null
cat "t.txt"
rm t.txt
rm $tmpfile

