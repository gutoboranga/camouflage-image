from camouflage_image import ImageCamouflager
from file_handler import FileHandler
from file_picker import FilePicker


file_picker = FilePicker()

file_handler = FileHandler()

background = file_handler.read(file_picker.background_path, colors=True)
overlay = file_handler.read(file_picker.overlay_path, alpha=True)

camo = ImageCamouflager()
result = camo.camouflage(background, overlay)

print "done!"

file_handler.show(result)
