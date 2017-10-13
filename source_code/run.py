import sys

from camouflage_image import ImageCamouflager
from file_handler import FileHandler
from file_picker import FilePicker
from image_resizer import ImageResizer

file_picker = FilePicker()

file_handler = FileHandler()

background = file_handler.read(file_picker.background_path, colors=True)
overlay = file_handler.read(file_picker.overlay_path, alpha=True)

image_resizer = ImageResizer(background, overlay)

resized_overlay = image_resizer.resize()

camo = ImageCamouflager()
result = camo.camouflage(background, resized_overlay)

print "done!"

file_handler.show(result)
