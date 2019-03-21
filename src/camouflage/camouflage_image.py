#import Tkinter as tk
#import numpy as np
from sys import argv

from threading import Thread
import time

from image_processor import ImageProcessor
from file_handler import FileHandler
from file_picker import FilePicker
from image_resizer import ImageResizer

class ImageCamouflager():
    
    quantizationLevels = [0,85,170,255]

    image_processor = ImageProcessor(quantizationLevels=quantizationLevels)
    
    
    def camouflage(self, background, overlay):
        
        self.background = background
        self.overlay = overlay
        
        # 1. process both background and overlay images
        # processed_background = self.process_background()
        # processed_overlay = self.process_overlay()

        self.processed_background = background
        self.processed_overlay = overlay

        t1 = Thread(target=self.process_background)
        t2 = Thread(target=self.process_overlay)

        t1.start()
        t2.start()
        
        t1.join()
        t2.join()

        # 2. create the background textures and corrects them if some of the textures is empty
        textures = self.create_textures(self.background, self.processed_background, self.processed_overlay)
        textures = self.correct_empty_textures(textures)
        
        # 3. apply the texture to overlay image
        # texturized_overlay = self.apply_textures(processed_overlay, textures)
        
        # 4. overlap the original background image with the final (texturized) overlay
        # output = self.image_processor.overlapImages(self.background, texturized_overlay)

        output = self.image_processor.overlapImagesWithTextures(self.background, self.processed_overlay, textures)
        
        return output
        
    def process_background(self):
        print "> processing background image"
        result = self.image_processor.luminanceNoAlpha(self.background)
        result = self.image_processor.quantizationNoAlpha(result)
        
        self.processed_background = result
        
    def process_overlay(self):
        print "> processing overlay image"
        
        result = self.image_processor.luminance(self.overlay)
        result = self.adjust_brightness(self.background, result)
        result = self.image_processor.quantization(result, 4)
        
        self.processed_overlay = result
        
    def adjust_brightness(self, reference, image_to_be_adjusted):
        print "> adjusting brightness"
        
        bright_factors = self.calculate_brightness_factors(reference, image_to_be_adjusted)
        bright_difference = bright_factors[0] - bright_factors[1]
        
        return self.image_processor.brightness(image_to_be_adjusted, bright_difference)
        
    def calculate_brightness_factors(self, background, overlay):
        height, width, channels = overlay.shape
        
        back_sum = 0
        over_sum = 0
        
        back_count = 0
        over_count = 0
        
        for row in range(0,height):
            for column in range(0,width):
                if self.pixelIsValid(overlay[row, column]):
                    back_sum += background[row, column][0]
                    over_sum += overlay[row, column][0]
                    
                    back_count += 1
                    over_count += 1

        result = [back_sum/back_count, over_sum/over_count]
        print("> brightness factors: back={}, over={}".format(result[0], result[1]))
        
        return result
        

    def create_textures(self, image, quantizatedImage, region):
        print "> collecting textures"
        
        height, width, channels = region.shape
        textures = [[],[],[],[]]
        
        # import ipdb; ipdb.set_trace()
        quantDict = dict([(self.quantizationLevels[i],i) for i in range(0,len(self.quantizationLevels))])

        for row in range(0,height):
            for column in range(0,width - 1):

                if self.pixelIsValid(region[row, column]):
                    backQuantPixel = quantizatedImage[row, column]
                    quantLevel = backQuantPixel[0]
                    
                    index = quantDict[quantLevel]
                    
                    backRealPixel = image[row, column]
                    textures[index].append([backRealPixel[0], backRealPixel[1], backRealPixel[2], 1])
                    
                    # i = 0
                    # found = False
                    # Check to which level of quantization the pixel belongs: 0, 85, 170 or 255
                    # while i < 4 and not found:
                    #     # print i, pixel[0], quantizationLevels[i]
                    #     if backQuantPixel[0] == self.quantizationLevels[i]:
                    #         backRealPixel = image[row, column]
                    #         textures[i].append([backRealPixel[0], backRealPixel[1], backRealPixel[2], 1])
                    #         found = True
                    #     i = i + 1

        return textures

    def correct_empty_textures(self, textures):
        for i in range(0,4):
            if len(textures[i]) == 0:
                if i < 3:
                    if len(textures[i + 1]) > 0:
                        textures[i] = textures[i + 1]
                    else:
                        raise Exception("Image too difficult to camouflage. Sorry :(")
                else:
                    if len(textures[i - 1]) > 0:
                        textures[i] = textures[i - 1]
                    else:
                        raise Exception("Image too difficult to camouflage. Sorry :(")
        return textures

    def apply_textures(self, image, textures):
        print "> applying textures"
        
        height, width, channels = image.shape
        texturePointers = [0,0,0,0]

        for row in range(0,height):
            for column in range(0,width - 1):
                pixel = image[row, column]

                if self.pixelIsValid(pixel):

                    i = 0
                    found = False
                    while i < 4 and not found:
                        if pixel[0] == self.quantizationLevels[i]:
                            if len(textures[i]) <= texturePointers[i]:
                                texturePointers[i] = 0
                            newPixel = textures[i][texturePointers[i]]
                            image[row, column] = newPixel
                            texturePointers[i] = texturePointers[i] + 1
                            found = True
                        i = i + 1
        return image

    def pixelIsValid(self, pixel):
        return pixel[3] > 0

if __name__ == "__main__":
    file_handler = FileHandler()
    
    background = file_handler.read(argv[1], colors=True)
    overlay = file_handler.read(argv[2], alpha=True)
    
    camo = ImageCamouflager()
    
    result = camo.camouflage(background, overlay)
    file_handler.save(result)
    