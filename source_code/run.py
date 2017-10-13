import sys

from camouflage_image import ImageCamouflager


camo = ImageCamouflager()
camo.camouflage(sys.argv[1], sys.argv[2])
