import sys

import numpy as np
import cv2

from image_processor import ImageProcessor
from file_handler import FileHandler


class ImageResizer():
    
    ip = ImageProcessor()
    fh = FileHandler()

    MOVE_RATIO = 0.05
    RESIZE_RATIO = 0.05
    
    def __init__(self, background, overlay):
        self.background = background
        self.overlay = overlay
        
        output = overlay
    
    def resize(self):
        print "> resize the overlay image:\n\tw - up\n\ta - left\n\ts - down\n\td - right\n\n\tn - smaller\n\tm - bigger\n\n\tq - finish"
        
        height, width, channels = self.background.shape
        
        ammount_to_move = max(int(self.MOVE_RATIO * height), int(self.MOVE_RATIO * width))        
        ammount_to_resize = max(int(self.RESIZE_RATIO * height), int(self.RESIZE_RATIO * width))

        x_offset = 0
        y_offset = 0
        
        while(True):
            output = self.overlap(x_offset, y_offset)
            
            cv2.imshow("Result", output)
            ch = cv2.waitKey(0)

						# somente no linux (a principio):
            ch = ch % 2**16

            if ch == 110:
                self.overlay = self.smaller(self.overlay, ammount_to_resize)

            elif ch == 109:
                self.overlay = self.larger(self.overlay, ammount_to_resize)
                
            # left
            elif ch == 97:
                x_offset = x_offset - ammount_to_move
                print('aaaaa')
                
            # up
            elif ch == 119:
                y_offset = y_offset - ammount_to_move
                    
            # right
            elif ch == 100:
                x_offset = x_offset + ammount_to_move
                
            # down
            elif ch == 115:
                y_offset = y_offset + ammount_to_move
                
            elif ch == 113:
                output = self.create_resized_overlay(x_offset, y_offset)
                return output
                break
        
    def larger(self, image, ammount_to_enlarge):
        height, width, channels = image.shape
        
        result = cv2.resize(image,(width + ammount_to_enlarge, height + ammount_to_enlarge), interpolation = cv2.INTER_CUBIC)
        
        return result
    
    def smaller(self, image, ammount_to_diminish):
        height, width, channels = image.shape
        
        if height > 50 and width > 50:
            result = cv2.resize(image,(width - ammount_to_diminish, height - ammount_to_diminish), interpolation = cv2.INTER_CUBIC)
            
        return result
    
    def overlap(self, x_offset, y_offset):
        b_height, b_width, b_channels = self.background.shape
        o_height, o_width, o_channels = self.overlay.shape
        
        result = np.zeros([b_height,b_width,b_channels],dtype=np.uint8)
        
        for row in range(0,b_height):
            for column in range(0,b_width):
                if  row > y_offset and row < (o_height + y_offset) and column > x_offset and column < (o_width + x_offset):
                    
                    overPixel = self.overlay[row - y_offset, column - x_offset]

                    # if pixel in overlay is not transparent (alpha > 0)
                    if overPixel[3] > 0:
                        # pixel from overlay
                        result[row, column] = [overPixel[0], overPixel[1], overPixel[2]]
                    else:
                        # pixel from brackground
                        result[row, column] = self.background[row, column]
                else:
                    result[row, column] = self.background[row, column]
                    
        return result
    
    def create_resized_overlay(self, x_offset, y_offset):
        b_height, b_width, b_channels = self.background.shape
        o_height, o_width, o_channels = self.overlay.shape
        
        result = np.zeros([b_height,b_width,4],dtype=np.uint8)
        
        for row in range(0,b_height):
            for column in range(0,b_width):
                if  row > y_offset and row < (o_height + y_offset) and column > x_offset and column < (o_width + x_offset):
                    
                    overPixel = self.overlay[row - y_offset, column - x_offset]

                    # if pixel in overlay is not transparent (alpha > 0)
                    if overPixel[3] > 0:
                        # pixel from overlay
                        result[row, column] = overPixel
                    else:
                        # pixel from brackground
                        result[row, column] = [0,0,0,0]
                else:
                    result[row, column] = [0,0,0,0]
                    
        return result
        
