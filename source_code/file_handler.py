import cv2
import error


class FileHandler():
    
    def read(self, path, colors=None, alpha=None):
        if colors:
            image = cv2.imread(path, 1)
        
        elif alpha:
            image = cv2.imread(path, -1)
        
        else:
            image = cv2.imread(path, 0)
        
        if image is None:
            print("{} {}".format(error.NO_SUCH_FILE, path))
            exit(1)
        
        return image
    
    
    def show(self, image):
        cv2.imshow("Result", image)
        cv2.waitKey(0)
        
    def save(self, image):
        cv2.imwrite("result.png", image)
        