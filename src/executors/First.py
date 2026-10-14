"""
    It is one of the preprocessing components in which the image is rotated.
"""

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_response_first
from components.Package.src.utils.rotation import get_rotation_params, rotate
from components.Package.src.models.PackageModel import PackageModel


class First(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        configs = self.request.model.configs.executor.value.value.configs
        self.angle, self.scale, self.keep_side = get_rotation_params(configs.rotateMode)
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = rotate(img.value, self.angle, self.scale, self.keep_side)
        self.image = Image.set_frame(img=img, package_uID=self.uID, redis_db=self.redis_db)
        packageModel = build_response_first(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
