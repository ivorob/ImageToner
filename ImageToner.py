#!/usr/bin/env python3

import argparse
import image
import os


# Algorithms
# Grayscale
def grayscale(currentPixel):
    grayscale = int(0.299 * currentPixel.red +
                    0.587 * currentPixel.green +
                    0.114 * currentPixel.blue)
    return image.Pixel(grayscale, grayscale, grayscale)


def sepia(currentPixel):
    newRed = int(0.393 * currentPixel.red +
                 0.769 * currentPixel.green +
                 0.189 * currentPixel.blue)
    newGreen = int(0.349 * currentPixel.red +
                   0.686 * currentPixel.green +
                   0.168 * currentPixel.blue)
    newBlue = int(0.272 * currentPixel.red +
                  0.534 * currentPixel.green +
                  0.131 * currentPixel.blue)

    return image.Pixel(
                min(newRed, 255),
                min(newGreen, 255),
                min(newBlue, 255))


def negative(currentPixel):
    return image.Pixel(
                255 - currentPixel.red,
                255 - currentPixel.green,
                255 - currentPixel.blue)


# Do nothing
def stub(currentPixel):
    return currentPixel


def chooseAlgorithm(name):
    for algorithm in algorithms:
        if algorithm[0] == name:
            return algorithm[1]

    return stub


# Supported algorithms
algorithms = (('grayscale', grayscale),
              ('sepia', sepia),
              ('negative', negative))


def makeAlgorithmNames():
    choices = []
    for algorithm in algorithms:
        choices.append(algorithm[0])

    return choices


parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('scheme', choices=makeAlgorithmNames())
args = parser.parse_args()

algorithm = chooseAlgorithm(args.scheme)
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
newFileName = "{}_{}{}".format(fileparts[0], args.scheme, fileparts[1])
print("Saving to '" + newFileName + "'...\t", end='')
imageCopy.save(newFileName)
print("OK")
