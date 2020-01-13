#!/bin/sh

convert $1 -gravity north -crop 100x20% +repage - | tesseract stdin "t" &> /dev/null
cat "t.txt"
rm t.txt


