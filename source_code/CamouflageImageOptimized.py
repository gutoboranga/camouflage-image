#import Tkinter as tk
#import numpy as np
import ImageProcessor as ip
import time
import cv2
import sys
#from Tkinter import Tk, Frame, BOTH

#####################################
# C A M O U F L A G E     I M A G E #
# by                                #
#                                   #
# Augusto Boranga                   #
# Nicolas Pessutto                  #
#####################################

### Functions ###

def correctEmptyTextures(textures):
    for i in range(0,4):
        if len(textures[i]) == 0:
            if i < 3:
                if len(textures[i + 1]) > 0:
                    textures[i] = textures[i + 1]
                else:
                    sys.exit("> Error: Image too difficult to camouflage. Sorry :(")
            else:
                if len(textures[i - 1]) > 0:
                    textures[i] = textures[i - 1]
                else:
                    sys.exit("> Error: Image too difficult to camouflage. Sorry :(")
    return textures

start_time = time.time()

# Open images
background = cv2.imread(sys.argv[1], 1)
overlay = cv2.imread(sys.argv[2], -1)

# Image processing
bg = background
processedOverlay = overlay

backBrightness = []
overBrightness = []
textures = [[],[],[],[]]
quantizationLevels = [0,85,170,255]
height, width, channels = background.shape

print "> 1st iteration"
# 1st iteration
for row in range(0,height):
    for column in range(0,width - 1):
        overPixel = overlay[row, column]

        if overPixel[3] !=0:
            l = 0.299 * overPixel[0] + 0.587 * overPixel[1] + 0.114 * overPixel[2]
            processedOverlay[row, column] = [l,l,l,overPixel[3]]
            backBrightness.append(background[row, column][0])
            overBrightness.append(overlay[row, column][0])

        backPixel = background[row, column]
        l = 0.299 * backPixel[0] + 0.587 * backPixel[1] + 0.114 * backPixel[2]
        bg[row, column] = [l,l,l]

brightnessDiff = sum(backBrightness)/len(backBrightness) - sum(overBrightness)/len(overBrightness)

background = cv2.imread(sys.argv[1], 1)

print "> 2nd iteration"
# 2nd iteration
for row in range(0,height):
    for column in range(0,width - 1):
        backPixel = bg[row, column]
        # check in which interval the pixel is
        if backPixel[0] < 191:
            if backPixel[0] < 127:
                if backPixel[0] < 63:
                    bg[row, column] = [0, 0, 0]
                else:
                    bg[row, column] = [85, 85, 85]
            else:
                bg[row, column] = [170, 170, 170]
        else:
            bg[row, column] = [255, 255, 255]

        overPixel = processedOverlay[row, column]
        if overPixel[3] !=0:
            # Apply brightness adjust
            for c in range(0,channels):
                color = processedOverlay.item(row,column,c)
                newValue = (color + brightnessDiff)
                if newValue <= 255:
                    if newValue >= 0:
                        processedOverlay.itemset((row,column,c), newValue)
                    else:
                        processedOverlay.itemset((row,column,c), 0)
                else:
                    processedOverlay.itemset((row,column,c), 255)

            # Quantize
            if overPixel[0] < 191:
                if overPixel[0] < 127:
                    if overPixel[0] < 63:
                        processedOverlay[row, column] = [0, 0, 0, 1]
                    else:
                        processedOverlay[row, column] = [85, 85, 85, 1]
                else:
                    processedOverlay[row, column] = [170, 170, 170, 1]
            else:
                processedOverlay[row, column] = [255, 255, 255, 1]

            # Create textures
            backQuantPixel = bg[row, column]
            i = 0
            found = False
            # Check to which level of quantization the pixel belongs: 0, 85, 170 or 255
            while i < 4 and not found:
                # print i, pixel[0], quantizationLevels[i]
                if backQuantPixel[0] == quantizationLevels[i]:
                    backRealPixel = background[row, column]
                    textures[i].append([backRealPixel[0], backRealPixel[1], backRealPixel[2], 1])
                    found = True
                i = i + 1

textures = correctEmptyTextures(textures)
texturePointers = [0,0,0,0]
output = background

print "> 3rd iteration"
# 3rd iteration
for row in range(0,height):
    for column in range(0,width - 1):
        overPixel = processedOverlay[row, column]
        if overPixel[3] !=0:
            i = 0
            found = False
            while i < 4 and not found:
                if overPixel[0] == quantizationLevels[i]:
                    if len(textures[i]) <= texturePointers[i]:
                        texturePointers[i] = 0
                    newPixel = textures[i][texturePointers[i]]
                    processedOverlay[row, column] = newPixel
                    texturePointers[i] = texturePointers[i] + 1
                    found = True
                i = i + 1
            texturizedPixel = processedOverlay[row, column]
            output[row, column] = [texturizedPixel[0], texturizedPixel[1], texturizedPixel[2]]
        else:
            # pixel from brackground
            output[row, column] = background[row, column]

elapsed_time = time.time() - start_time
print "Time: "
print elapsed_time

# Save final output
cv2.imwrite("result.png", output)

# Show result
# print "\nCamouflage concluded with success!"
cv2.imshow("Result", output)
cv2.waitKey(0)
