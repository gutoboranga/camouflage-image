import numpy as np
import Tkinter as tk
from Tkinter import Tk, Frame, BOTH
import cv2


class ImageProcessor():
    def overlapImages(self, back, overlay):
        height, width, channels = back.shape
        result = np.zeros([height,width,channels],dtype=np.uint8)
        for row in range(0,height):
            for column in range(0,width):
                overPixel = overlay[row, column]

                # if pixel in overlay is not transparent (alpha > 0)
                if overPixel[3] > 0:
                    # pixel from overlay
                    result[row, column] = [overPixel[0], overPixel[1], overPixel[2]]
                else:
                    # pixel from brackground
                    result[row, column] = back[row, column]
        return result

    def luminance(self, image):
        height, width, channels = image.shape
        result = np.zeros([height,width,channels],dtype=np.uint8)
        
        for row in range(0,height):
            for column in range(0,width - 1):
                color = image[row, column]
        
                if color[3] !=0:
                    l = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
                    result[row, column] = [l,l,l,color[3]]
                    
        
        return result

    def luminanceNoAlpha(self, image):
        height, width, channels = image.shape
        result = np.zeros([height,width,channels],dtype=np.uint8)
        
        for row in range(0,height):
            for column in range(0,width - 1):
                color = image[row, column]
                l = 0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]
                result[row, column] = [l,l,l]
                
        return result

    def quantization(self, image, tonesQuantity):
        height, width, channels = image.shape
        result = np.zeros([height,width,channels],dtype=np.uint8)
        
        for row in range(0,height):
            for column in range(0,width - 1):
                pixel = image[row, column]

                # if alpha is positive
                if pixel[3] > 0:

                    # check in which interval the pixel is
                    if pixel[0] < 191:
                        if pixel[0] < 127:
                            if pixel[0] < 63:
                                result[row, column] = [0, 0, 0, 1]
                            else:
                                result[row, column] = [85, 85, 85, 1]
                        else:
                            result[row, column] = [170, 170, 170, 1]
                    else:
                        result[row, column] = [255, 255, 255, 1]
        return result

    def quantizationNoAlpha(self, image, tonesQuantity):
        height, width, channels = image.shape
        result = np.zeros([height,width,channels],dtype=np.uint8)
        
        for row in range(0,height):
            for column in range(0,width - 1):
                pixel = image[row, column]
                # check in which interval the pixel is
                if pixel[0] < 191:
                    if pixel[0] < 127:
                        if pixel[0] < 63:
                            result[row, column] = [0, 0, 0]
                        else:
                            result[row, column] = [85, 85, 85]
                    else:
                        result[row, column] = [170, 170, 170]
                else:
                    result[row, column] = [255, 255, 255]
        return result

    def brightness(self, image, value):
        height, width, channels = image.shape
        result = np.zeros([height,width,channels],dtype=np.uint8)
        
        for row in range(0,height):
            for column in range(0,width):
                pixel = image[row, column]
                if pixel[3] !=0:
                    for c in range(0,channels):
                        color = image.item(row,column,c)
                        newValue = (color + value)
                        if newValue <= 255:
                            if newValue >= 0:
                                result.itemset((row,column,c), newValue)
                            else:
                                result.itemset((row,column,c), 0)
                        else:
                            result.itemset((row,column,c), 255)
        return result
