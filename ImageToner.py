#!/usr/bin/env python3

import argparse
import image
import os

parser = argparse.ArgumentParser()
parser.add_argument('filename')
# parser.add_argument('scheme', choices=['negative', 'greyscale'])
args = parser.parse_args()

image = image.FileImage(args.filename)
width = image.get_width()
height = image.get_height()

newImage = image.copy()

print("Processing...\t0%", end='')
lastPercent = 0
for row in range(height):
    for column in range(width):
        currentPixel = newImage.getPixel(column, row)
        greyscale = int(0.299 * currentPixel.red +
                        0.587 * currentPixel.green +
                        0.114 * currentPixel.blue)
        currentPixel.red = greyscale
        currentPixel.green = greyscale
        currentPixel.blue = greyscale
        newImage.setPixel(column, row, currentPixel)

    newPercent = row * 100 // height
    if newPercent > lastPercent:
        print("\rProcessing...\t", newPercent, "%", end='')
        lastPercent = newPercent

print("\rProcessing...\t100 %")

fileparts = os.path.splitext(args.filename)
newFileName = fileparts[0] + "_new" + fileparts[1]
print("Saving to '" + newFileName + "'...\t", end='')
newImage.save(newFileName)
print("OK")
