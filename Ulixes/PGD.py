import math
import os
from time import sleep

import torch
import torch.nn as nn
import numpy as np
from facenet_pytorch.models.mtcnn import MTCNN
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from PIL import Image
from torch import autograd

EPSILON = 0.0001
EMBEDDING_MODEL = InceptionResnetV1(pretrained="vggface2").eval()

filename_for_perturbated_image_ulixes = "cloaked_ulixes.jpg"


def normalize_cloaked_image_tensor(image):
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    return normalized_image


def Ulixes(image, margin):
    cropped_image = crop_image(image, "cropped_image_ulixes.jpg")

    cloaked_image_tensor = pgd(cropped_image, margin)
    cloaked_image_array_normalized = normalize_cloaked_image_tensor(cloaked_image_tensor).detach().numpy()

    cloaked_image_array_normalized = np.swapaxes(cloaked_image_array_normalized, 0, 1)  # [3, 160, 160] -> [160, 3, 160]
    cloaked_image_array_normalized = np.swapaxes(cloaked_image_array_normalized, 1, 2)  # [160, 3, 160] -> [160, 160, 3]

    cloaked_image = Image.fromarray(cloaked_image_array_normalized.astype(np.uint8))

    # cloaked_image.save("cloaked_image.png")
    cloaked_image.save(filename_for_perturbated_image_ulixes)
    return cloaked_image


def crop_image(image, cropped_path):
    mtcnn_pt = MTCNN(device=torch.device("cpu"))
    image = Image.open(image).convert("RGB")
    image_cropped = mtcnn_pt(image, save_path=cropped_path)
    return image_cropped


def get_embedding(image):
    return EMBEDDING_MODEL(image.unsqueeze(0))


def pgd(image, margin=1.1, alpha=0.01):
    # margin: set to 1.1 as default, can be between [0.2, 2] to change intensity of noise masks introduced
    anchor = positive = image
    negative = add_epsilon_noise(image)
    negative.requires_grad_()
    positive.requires_grad_()
    triplet_loss = nn.TripletMarginLoss(margin=margin, p=2)
    embedded_positive = get_embedding(positive)

    threshold = 0.01

    while True:
        anchor.requires_grad_()
        loss = triplet_loss(anchor, negative, positive)
        g = autograd.grad(loss, loss)
        with torch.no_grad():
            anchor = torch.add(anchor, scale(g, alpha))
        embedded_anchor = get_embedding(anchor)
        difference_of_anchor_and_positive = embedded_anchor - embedded_positive
        if math.copysign(1, g[0]) != 1 or np.linalg.norm(difference_of_anchor_and_positive.detach(),
                                                         axis=1) < threshold:
            break
        anchor = np.clip(anchor, positive - EPSILON, positive + EPSILON)
    anchor = np.clip(anchor, -1, 1)
    return anchor


def add_epsilon_noise(image):
    image = torch.add(image, EPSILON)
    return image


def scale(vector, alpha):
    inf_norm = np.linalg.norm(vector, np.inf)
    print(vector[0].item() / inf_norm)
    return alpha * (vector[0].detach() / inf_norm)


if __name__ == '__main__':
    # Ulixes("C:\matt.jpg", 1.1)
    Ulixes("/Users/tamiryaari/Desktop/UNI/Year3/Workshop/Face-Cloaking-Project/server/original.jpg", 1.1)
