import torch
import torch.nn as nn
import numpy as np
from PIL import Image


def pgd(model, input, margin=1.1, alpha=2/255, iters=40):
    """
    :param input: the image uploaded
    :param margin: set to 1.1 as default, can be between [0.2, 2] to change intensity of noise masks introduced
    """
    anchor = positive = input
    negative = base_epsilon_noise(input)
    triplet_loss = nn.TripletMarginLoss(margin)

    DSSIM_diff_upper_bound = 1.242
    threshold = 0.01

    for i in range(iters):
        images.requires_grad = True
        outputs = model(images)

        model.zero_grad()
        cost = loss(outputs, labels).to(device)
        cost.backward()

        adv_images = images + alpha * images.grad.sign()
        eta = torch.clamp(adv_images - ori_images, min=-eps, max=eps)
        images = torch.clamp(ori_images + eta, min=0, max=1).detach_()

    return images


def base_epsilon_noise(image):
    epsilon = 0.00001

    for i in range(image.shape(0)):
        for j in range(image.shape(1)):
            image[i][j][0] += epsilon
            image[i][j][1] += epsilon

    return image
