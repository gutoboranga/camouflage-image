#import Tkinter as tk
#import numpy as np
import ImageProcessor as ip
import cv2
import sys
import time
#from Tkinter import Tk, Frame, BOTH

#####################################
# C A M O U F L A G E     I M A G E #
# by                                #
#                                   #
# Augusto Boranga                   #
# Nicolas Pessutto                  #
#####################################

### Constants ###

quantizationLevels = [0,85,170,255]

### Functions ###

def calculateBrightnessDiff(background, overlay):
    height, width, channels = overlay.shape
    back = []
    over = []
    for row in range(0,height):
        for column in range(0,width - 1):
            if pixelIsValid(overlay[row, column]):
                back.append(background[row, column][0])
                over.append(overlay[row, column][0])
    return [sum(back)/len(back), sum(over)/len(over)]

def adjustBrightness(background, overlay):
    brightFactors = calculateBrightnessDiff(bg, overlay)
    brightDifference = brightFactors[0] - brightFactors[1]
    return ip.brightness(processedOverlay, brightDifference)

def createTextures(image, quantizatedImage, region):
    height, width, channels = region.shape
    textures = [[],[],[],[]]

    for row in range(0,height):
        for column in range(0,width - 1):

            if pixelIsValid(region[row, column]):
                backQuantPixel = quantizatedImage[row, column]
                i = 0
                found = False
                # Check to which level of quantization the pixel belongs: 0, 85, 170 or 255
                while i < 4 and not found:
                    # print i, pixel[0], quantizationLevels[i]
                    if backQuantPixel[0] == quantizationLevels[i]:
                        backRealPixel = image[row, column]
                        textures[i].append([backRealPixel[0], backRealPixel[1], backRealPixel[2], 1])
                        found = True
                    i = i + 1

    return textures

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

def applyTextures(image, textures):
    height, width, channels = image.shape
    texturePointers = [0,0,0,0]

    for row in range(0,height):
        for column in range(0,width - 1):
            pixel = image[row, column]

            if pixelIsValid(pixel):

                i = 0
                found = False
                while i < 4 and not found:
                    if pixel[0] == quantizationLevels[i]:
                        if len(textures[i]) <= texturePointers[i]:
                            texturePointers[i] = 0
                        newPixel = textures[i][texturePointers[i]]
                        image[row, column] = newPixel
                        texturePointers[i] = texturePointers[i] + 1
                        found = True
                    i = i + 1
    return image

def pixelIsValid(pixel):
    return pixel[3] > 0

### Main ###

start_time = time.time()

# Open images
print "> reading input"
background = cv2.imread(sys.argv[1], 1)
overlay = cv2.imread(sys.argv[2], -1)
# partial = ip.overlapImages(background, overlay)
# cv2.destroyAllWindows()
# cv2.imshow("Result", partial)

# Image processing
bg = background

print "> applying luminance"
bg = ip.luminanceNoAlpha(bg)
processedOverlay = ip.luminance(overlay)
# partial = ip.overlapImages(bg, processedOverlay)
# cv2.destroyAllWindows()
# cv2.imshow("Result", partial)

print "> applying quantization"
bg = ip.quantizationNoAlpha(bg, 4)
# 3 iterations

print "> adjusting brightness"
processedOverlay = adjustBrightness(bg, processedOverlay)
# 5 iterations

# partial = ip.overlapImages(bg, processedOverlay)
# cv2.destroyAllWindows()
# cv2.imshow("Result", partial)

processedOverlay = ip.quantization(processedOverlay, 4)
# partial = ip.overlapImages(bg, processedOverlay)
# cv2.destroyAllWindows()
# cv2.imshow("Result", partial)

background = cv2.imread(sys.argv[1], 1)

# Handle textures
print "> creating textures"
textures = createTextures(background, bg, processedOverlay)
textures = correctEmptyTextures(textures)

print "> applying textures"
processedOverlay = applyTextures(processedOverlay, textures)

# Overlap the images
print "> overlapping images"
output = ip.overlapImages(background, processedOverlay)

elapsed_time = time.time() - start_time
print "Time: "
print elapsed_time


# Save final output
# print "> exporting final image"
cv2.imwrite("result.png", output)

# Show result
# print "\nCamouflage concluded with success!"
cv2.imshow("Result", output)
cv2.waitKey(0)
