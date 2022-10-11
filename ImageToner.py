#!/usr/bin/env python3

import argparse
import image
import os

def grayscale(currentPixel):
    grayscale = int(0.299 * currentPixel.red +
                    0.587 * currentPixel.green +
                    0.114 * currentPixel.blue)
    return image.Pixel(grayscale, grayscale, grayscale)

def stub(currentPixel):
    return currentPixel

def chooseAlgorithm(name):
    for algorithm in algorithms:
        if algorithm[0] == name:
            return algorithm[1]

    return stub

algorithms = (('grayscale', grayscale), )

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('scheme', choices=['grayscale'])
args = parser.parse_args()

algorithm = chooseAlgorithm('grayscale')
newImage = image.FileImage(args.filename)
width = newImage.get_width()
height = newImage.get_height()

imageCopy = newImage.copy()

print("Processing...\t0%", end='')
lastPercent = 0
for row in range(height):
    for column in range(width):
        currentPixel = algorithm(imageCopy.getPixel(column, row))
        imageCopy.setPixel(column, row, currentPixel)

    newPercent = row * 100 // height
    if newPercent > lastPercent:
        print("\rProcessing...\t", newPercent, "%", end='')
        lastPercent = newPercent

print("\rProcessing...\t100 %")

fileparts = os.path.splitext(args.filename)
newFileName = fileparts[0] + "_new" + fileparts[1]
print("Saving to '" + newFileName + "'...\t", end='')
imageCopy.save(newFileName)
print("OK")
