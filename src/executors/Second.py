"""
    Rotates two images with the same settings.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response_second
from components.Package.src.utils.rotation import get_rotation_params, rotate
from components.Package.src.models.PackageModel import PackageModel


class Second(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        configs = self.request.model.configs.executor.value.value.configs
        self.angle, self.scale, self.keep_side = get_rotation_params(configs.rotateMode)
        self.image = self.request.get_param("inputImage")
        self.image2 = self.request.get_param("inputImage2")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def rotate_frame(self, image):
        img = Image.get_frame(img=image, redis_db=self.redis_db)
        img.value = rotate(img.value, self.angle, self.scale, self.keep_side)
        return Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)

    def run(self):
        self.image = self.rotate_frame(self.image)
        self.image2 = self.rotate_frame(self.image2)
        packageModel = build_response_second(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
