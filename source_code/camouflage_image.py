#import Tkinter as tk
#import numpy as np
import cv2

from image_processor import ImageProcessor
from file_handler import FileHandler


class ImageCamouflager():
    
    file_handler = FileHandler()
    image_processor = ImageProcessor()
    
    quantizationLevels = [0,85,170,255]
    
    
    def camouflage(self, background_path, overlay_path):
        self.background, self.overlay = self.read_inputs(background_path, overlay_path)
        
        proccessed_background = self.proccess_background()
        proccessed_overlay = self.proccess_overlay()
        
        textures = self.create_textures(self.background, proccessed_background, proccessed_overlay)
        textures = self.correct_empty_textures(textures)
        
        texturized_overlay = self.apply_textures(proccessed_overlay, textures)
        
        output = self.image_processor.overlapImages(self.background, texturized_overlay)
        
        print "done"
        
        self.file_handler.show(output)
        
    def read_inputs(self, background_path, overlay_path):
        print "> reading inputs"

        background = self.file_handler.read(background_path, colors=True)
        overlay = self.file_handler.read(overlay_path, alpha=True)
        
        return background, overlay
        
    def proccess_background(self):
        print "> proccessing background image"
        
        proccessed_background = self.image_processor.luminanceNoAlpha(self.background)
        proccessed_background = self.image_processor.quantizationNoAlpha(proccessed_background, 4)
        
        return proccessed_background
        
    def proccess_overlay(self):
        print "> proccessing overlay image"
        
        proccessed_overlay = self.image_processor.luminance(self.overlay)
        proccessed_overlay = self.adjust_brightness(self.background, proccessed_overlay)
        proccessed_overlay = self.image_processor.quantization(proccessed_overlay, 4)
        
        return proccessed_overlay
        
    def adjust_brightness(self, reference, image_to_be_adjusted):
        print "> adjusting brightness"
        
        bright_factors = self.calculate_brightness_diff(reference, image_to_be_adjusted)
        bright_difference = bright_factors[0] - bright_factors[1]
        
        return self.image_processor.brightness(image_to_be_adjusted, bright_difference)
        
    def calculate_brightness_diff(self, background, overlay):
        height, width, channels = overlay.shape
        back = []
        over = []
        for row in range(0,height):
            for column in range(0,width - 1):
                if self.pixelIsValid(overlay[row, column]):
                    back.append(background[row, column][0])
                    over.append(overlay[row, column][0])
        return [sum(back)/len(back), sum(over)/len(over)]
        

    def create_textures(self, image, quantizatedImage, region):
        print "> collecting textures"
        
        height, width, channels = region.shape
        textures = [[],[],[],[]]

        for row in range(0,height):
            for column in range(0,width - 1):

                if self.pixelIsValid(region[row, column]):
                    backQuantPixel = quantizatedImage[row, column]
                    i = 0
                    found = False
                    # Check to which level of quantization the pixel belongs: 0, 85, 170 or 255
                    while i < 4 and not found:
                        # print i, pixel[0], quantizationLevels[i]
                        if backQuantPixel[0] == self.quantizationLevels[i]:
                            backRealPixel = image[row, column]
                            textures[i].append([backRealPixel[0], backRealPixel[1], backRealPixel[2], 1])
                            found = True
                        i = i + 1

        return textures

    def correct_empty_textures(self, textures):
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
