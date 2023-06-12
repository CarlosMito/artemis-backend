import numpy as np
import colorsys
import cv2


def change_saturation(image: np.ndarray, scale: float):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[..., 1] = np.clip(hsv_image[..., 1] * scale, 0, 255)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)


def change_value(image: np.ndarray, scale: float):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[..., 2] = np.clip(hsv_image[..., 2] * scale, 0, 255)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)


def change_hue(image: np.ndarray, target_color: int):
    # The hue range of [cv2.COLOR_BGR2HSV] is [0, 179] and [cv2.COLOR_BGR2HSV_FULL] is [0, 255]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    hsv[..., 0] = target_color
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)


def argb_to_hsv(argb: int):
    """
    [argb]: The integer representation of the ARGB color.
    """
    red = (argb >> 16) & 0xFF
    green = (argb >> 8) & 0xFF
    blue = argb & 0xFF

    normalized_red = red / 255.0
    normalized_green = green / 255.0
    normalized_blue = blue / 255.0

    return colorsys.rgb_to_hsv(normalized_red, normalized_green, normalized_blue)


# processed = change_saturation(image, scale=1.5)
# processed = change_saturation(image, scale=0.7)
# processed = change_value(image, scale=1.5)
# processed = change_value(image, scale=0.7)
# processed = change_hue(image, 150)  # Blue
