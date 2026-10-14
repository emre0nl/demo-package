
import cv2


def get_rotation_params(rotate_mode):
    """
        Returns (angle, scale, keep_side) for the option selected in RotateMode.
    """
    option = rotate_mode.value
    if option.name == "Manual":
        return option.degree.value, 1.0, option.keepSide.value.value
    return option.presetAngle.value.value, option.scale.value, True


def rotate(image, angle, scale, keep_side):
    height, width = image.shape[:2]
    image_center = (width / 2, height / 2)
    rotation_arr = cv2.getRotationMatrix2D(image_center, angle, scale)

    if not keep_side:
        return cv2.warpAffine(image, rotation_arr, (width, height))

    abs_cos = abs(rotation_arr[0, 0])
    abs_sin = abs(rotation_arr[0, 1])
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)
    rotation_arr[0, 2] += bound_w / 2 - image_center[0]
    rotation_arr[1, 2] += bound_h / 2 - image_center[1]
    return cv2.warpAffine(image, rotation_arr, (bound_w, bound_h))
