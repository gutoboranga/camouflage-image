import cv2


class FileHandler():
    
    def read(self, path, colors=None, alpha=None):
        if colors:
            return cv2.imread(path, 1)
        
        if alpha:
            return cv2.imread(path, -1)
        
        return cv2.imread(path, 0)
    
    def show(self, image):
        cv2.imshow("Result", image)
        cv2.waitKey(0)
        
    def save(self, image):
        cv2.imwrite("result.png", image)
        