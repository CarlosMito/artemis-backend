import cv2
from pathlib import Path
from collections import defaultdict
import numpy as np

RESOURCE_FOLDER = Path("../images/outputs")
OUTPUT_FOLDER = Path("./outputs")


def change_saturation(image: np.ndarray, scale: float):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[..., 1] = np.clip(hsv_image[..., 1] * scale, 0, 255)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)


def change_value(image: np.ndarray, scale: float):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_image[..., 2] = np.clip(hsv_image[..., 2] * scale, 0, 255)
    return cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)


# def change_hue(image: np.ndarray, target_color: float):

#     # The hue range of [cv2.COLOR_BGR2HSV] is [0, 179] and [cv2.COLOR_BGR2HSV_FULL] is [0, 255]
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)

#     hue = hsv[..., 0]
#     sat = hsv[..., 1]
#     val = hsv[..., 2]

#     val_mask = (val > 30) & (val < 225)
#     sat_mask = sat > np.percentile(sat[val_mask].flatten(), [75])[0]

#     histogram, bins = np.histogram(hue[sat_mask & val_mask].flatten(), 256, [0, 256])

#     maximum = bins[np.argmax(histogram)]
#     difference = target_color - maximum

#     if difference < 0:
#         difference += 256

#     hsv[:, :, 0] = (hue + difference) % 256

#     return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)

def change_hue(image: np.ndarray, target_color: float):
    # The hue range of [cv2.COLOR_BGR2HSV] is [0, 179] and [cv2.COLOR_BGR2HSV_FULL] is [0, 255]
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    hsv[..., 0] = target_color
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR_FULL)


# def equalize(image):
#     B, G, R = cv2.split(image)

#     output1_B = cv2.equalizeHist(B)
#     output1_G = cv2.equalizeHist(G)
#     output1_R = cv2.equalizeHist(R)

#     return cv2.merge((output1_B, output1_G, output1_R))


# def equalize_rgb_2(image):
#     # Code at https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv
#     lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
#     l_channel, a, b = cv2.split(lab)
#     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
#     cl = clahe.apply(l_channel)
#     limg = cv2.merge((cl, a, b))
#     return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)


# def equalize_rgb(image):

#     intensity = 255
#     total = image.shape[0] * image.shape[1] * 3
#     mapping = defaultdict(lambda: 0)
#     probabilities = {}
#     accumulated = {}
#     auxiliar = 0

#     for row in image:
#         for pixel in row:
#             for channel in pixel:
#                 mapping[channel] += 1

#     for key, value in sorted(mapping.items()):
#         probabilities[key] = value / total
#         auxiliar += probabilities[key]
#         accumulated[key] = auxiliar

#     new_mapping = {}
#     step = 1 / intensity
#     limit = step

#     for index, value in sorted(accumulated.items()):

#         while value + step > limit:
#             limit += step

#         new_mapping[index] = limit

#     equalized = np.ones((image.shape[0], image.shape[1], image.shape[2]))

#     for i, row in enumerate(image):
#         for j, pixel in enumerate(row):
#             for k, channel in enumerate(pixel):
#                 equalized[i, j, k] = new_mapping[channel]

#     return (np.clip(equalized, 0, 1) * 255).astype(np.uint8)

if __name__ == "__main__":

    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    images = [
        "placeholder_0.jpg",
        "placeholder_1.jpeg",
        "placeholder_2.jpg",
        "placeholder_3.jpg",
        "placeholder_4.jpeg",
        "placeholder_5.jpg",
        "placeholder_11.jpg",
        "placeholder_10.jpg",
        "rs5cko635fhkfhqhh4f6o72sdi-1.png",
    ]

    for image in images:

        image_path = str(RESOURCE_FOLDER / image)
        processed_path = str(OUTPUT_FOLDER / f"processed-{image}")

        image = cv2.imread(image_path)
        assert image is not None, f"Couldn't load image at {image_path}"

        # OK
        # processed = change_saturation(image, scale=1.5)
        # processed = change_saturation(image, scale=0.7)
        # processed = change_value(image, scale=1.5)
        # processed = change_value(image, scale=0.7)
        processed = change_hue(image, 150)  # Blue

        # Stacking images side-by-side
        result = np.hstack((image, processed))

        cv2.imwrite(processed_path, result)
        cv2.waitKey(0)
