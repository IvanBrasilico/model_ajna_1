import numpy as np
import os
from PIL import Image


def prepare_images(filenames, path, size):
    #images = np.zeros((len(filenames), size[1], size[0], 3))
    images = []
    for ind, filename in enumerate(filenames):
        image = Image.open(os.path.join(path, filename))
        image = image.resize(size, Image.LANCZOS)
        image_array = np.array(image) / 255
        # images[ind, :, :, :] = image_array
        images.append(image_array.tolist())
    return images