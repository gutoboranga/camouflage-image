import sys

from camouflage_image import ImageCamouflager
from file_handler import FileHandler
from file_picker import FilePicker
from image_resizer import ImageResizer

# 1. Open file picker to choose 2 images: Background and Overlay
file_picker = FilePicker()
file_handler = FileHandler()

# 2. Read the files chosen
background = file_handler.read(file_picker.background_path, colors=True)
overlay = file_handler.read(file_picker.overlay_path, alpha=True)

# 3. Open window for user to resize and position the Overlay on the Background
image_resizer = ImageResizer(background, overlay)
resized_overlay = image_resizer.resize()

# 4. Start the camouflage algorithm itself
camo = ImageCamouflager()
result = camo.camouflage(background, resized_overlay)

# 5. If a "save" parameter was provided, save the resulting image
if len(sys.argv) > 1:
    if sys.argv[1] == "save":
        file_handler.save(result)

print "Done!"

# 6. Show the result
file_handler.show(result)

