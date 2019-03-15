import sys
import os
import binascii

from tornado.web import RequestHandler

sys.path.insert(0, "../camouflage")
from camouflage_image import ImageCamouflager
from file_handler import save2 as save_image
from image_processor import data_uri_to_cv2_img as make_image

BASE_URL = "http://localhost:5000"
RESULTS_PATH = "results"

class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin, X-Requested-With, Content-Type, Accept, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        self.set_status(204)
        self.finish()


class WakeUpHandler(BaseHandler):

    def initialize(self):
        pass

    def get(self):
        self.write("I'm awake now")


class ResultHandler(BaseHandler):

    def make_path(self, hash):
        return "{}/{}.jpg".format(RESULTS_PATH, hash)

    def get(self, id):
        path = self.make_path(id)
        print(path)

        if os.path.isfile(path):
            self.write("Ok")
        else:
            self.write("Not found")


class CreateHandler(BaseHandler):

    def initialize(self):
        pass

    def make_path(self, hash):
        return "{}/{}.jpg".format(RESULTS_PATH, hash)

    def make_url(self, hash):
        return "{}/result/{}.jpg".format(BASE_URL, hash)

    def post(self):

        print("> will try to camouflage")

        try:
            background_body = self.request.arguments['background']
            overlay_body = self.request.arguments['overlay']

            background = make_image(background_body[0])
            overlay = make_image(overlay_body[0], flag=-1)

            # proccess the images
            camo = ImageCamouflager()
            result = camo.run(background, overlay)

            # save the image and generate an url
            hash = binascii.hexlify(os.urandom(6))
            path = self.make_path(hash)

            save_image(result, path)

            print("> Done! Image {} saved.".format(hash))

            self.write(self.make_url(hash))

        except Exception as e:
            print("[ERRO]", e)
            self.write("error")
