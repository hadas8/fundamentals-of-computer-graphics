from PIL import Image
import numpy as np


def get_image(image):
    return Image.fromarray(np.uint8(image)).convert('RGB')


def normalize_image(image):
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    image = get_image(normalized_image)
    return image



