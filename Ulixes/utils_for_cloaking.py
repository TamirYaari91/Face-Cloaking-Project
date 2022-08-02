import numpy as np
import torch
from PIL import Image
from facenet_pytorch.models.mtcnn import MTCNN


def crop_image_with_mtcnn(image, path_for_cropped_image):
    mtcnn_pt = MTCNN()
    image = Image.open(image).convert("RGB")
    image_cropped = mtcnn_pt(image, save_path=path_for_cropped_image)
    return image_cropped


def generate_cloaked_cropped_image_from_noise_mask(cropped_image, noise_mask):

    # Add noise mask to the cropped face image, normalize its values and change the order of dimensions
    cloaked_cropped_image = add_noise_mask_to_image(cropped_image, noise_mask)
    cloaked_cropped_image_normalized = normalize_image_tensor(cloaked_cropped_image)
    cloaked_cropped_image_normalized_as_array = cloaked_cropped_image_normalized.detach().numpy()

    # [3, 160, 160] -> [160, 3, 160]
    cloaked_cropped_image_normalized_as_array = np.swapaxes(cloaked_cropped_image_normalized_as_array, 0, 1)

    # [160, 3, 160] -> [160, 160, 3]
    cloaked_cropped_image_normalized_as_array = np.swapaxes(cloaked_cropped_image_normalized_as_array, 1, 2)

    return cloaked_cropped_image_normalized_as_array


def add_noise_mask_to_image(image, noise):
    image = torch.add(image, noise)
    return image


def normalize_image_tensor(image):
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    return normalized_image
