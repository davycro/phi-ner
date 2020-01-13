#!/usr/bin/env python3
#
#


import sys
import os
from pymediainfo import MediaInfo
from PIL import Image
import tempfile
import subprocess
import shutil
from pathlib import Path

import hanlp
recognizer = hanlp.load(hanlp.pretrained.ner.CONLL03_NER_BERT_BASE_UNCASED_EN)

def is_image(path):
  try:
    Image.open(path)
  except IOError:
    return False
  return True

def is_video(filepath):
  media_info = MediaInfo.parse(filepath)
  for track in media_info.tracks:
    if track.track_type == 'Video':
      return True

  return False


def tesseract_media(filepath):
  print(filepath)
  if is_video(filepath):
    print("is a video")
    p = subprocess.run(['sh', './parse_video.sh', filepath], capture_output=True)
  elif is_image(filepath):
    print("is an image")
    p = subprocess.run(['sh', './parse_image.sh', filepath], capture_output=True)
  else:
    print("invalid file")
    return False
  text = p.stdout.decode('utf-8')
  # Path(filepath).with_name(Path(filepath).name+'.txt').write_text(text)
  return text


def has_a_person(words):
  output = recognizer(words)
  print(output)
  for i in output:
    if i[1]=="PER":
      return True
  return False


inputDir = "{}/input".format(os.getcwd())
outputDir = "./output"

if os.path.exists(outputDir):
  shutil.rmtree(outputDir)

os.mkdir(outputDir)

os.mkdir(outputDir + '/true')
os.mkdir(outputDir + '/false')


for filename in os.listdir(inputDir):
  sourceFile = inputDir + '/' + filename

  if is_video(sourceFile) or is_image(sourceFile):

    logfiletext = []
    has_phi = False

    text = tesseract_media(sourceFile)
    logfiletext.append("Tesseract output: ")
    logfiletext.append(text)

    for word in text.split():
      logfiletext.append(word)
      if len(word)>3:
        output = recognizer([word])
        logfiletext.append("recognizer: {} = {}".format(word, output))
        for i in output:
          if i[1]=="PER":
            has_phi = True

    # check for text with a comma
    s = text.split(",")
    if len(s)>=2:
      last = s[0].split().pop()
      first = s[1].split()[0]
      output = recognizer(["{} {}".format(first, last)])
      logfiletext.append("recognizer: {} = {}".format(word, output))
      for i in output:
        if i[1]=="PER":
          has_phi = True



    logfiletext.append("HAS PHI? {}".format(has_phi))

    if has_phi:
      targetFile = "{}/true/{}".format(outputDir, filename)
    else:
      targetFile = "{}/false/{}".format(outputDir, filename)

    logfilePath = Path(targetFile).with_name(Path(targetFile).name+'.txt')
    logfilePath.write_text("\n".join(logfiletext))

    shutil.copy2(sourceFile, targetFile)







