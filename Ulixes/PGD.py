import math
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


def Ulixes(image, margin):
    cropped_image = crop_image(image, "cropped_image.png")
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


def pgd(image, margin=1.6, alpha=0.01):
    # margin: set to 1.1 as default, can be between [0.2, 2] to change intensity of noise masks introduced
    anchor = positive = image
    negative = add_epsilon_noise(image)
    negative.requires_grad_()
    positive.requires_grad_()
    embedded_negative = get_embedding(negative)
    embedded_positive = get_embedding(positive)
    distance_positive_negative = np.linalg.norm(embedded_positive.detach() - embedded_negative.detach())
    #triplet_loss = nn.TripletMarginLoss(margin=margin, p=2)
    threshold = 0.001
    count = 0

    while True:
        # print(count)
        anchor.requires_grad_()
        embedded_anchor = get_embedding(anchor)
        loss_number = get_loss(embedded_anchor, embedded_positive, distance_positive_negative, margin)
        loss = torch.as_tensor(loss_number)
        loss.requires_grad_()
        # print(f"loss is: {loss_number}")
        g = autograd.grad(loss, loss)
        prev_anchor = anchor
        anchor = torch.add(anchor, scale(g, alpha))
        difference_of_prev_anchor_and_new_anchor = np.linalg.norm(get_embedding(anchor).detach() - get_embedding(prev_anchor).detach())
        # print(f"new noise is: {difference_of_prev_anchor_and_new_anchor}")
        #if math.copysign(1, np.linalg.norm(loss.detach().numpy(), np.inf)) != 1 or difference_of_prev_anchor_and_new_anchor < threshold:
        if difference_of_prev_anchor_and_new_anchor < threshold or count == 100:
            break
        anchor = np.clip(anchor.detach(), positive.detach() - 0.5, positive.detach() + 0.5)
        anchor = np.clip(anchor.detach(), -1, 1)
        count += 1
    return anchor


def get_loss(anchor, positive, const_distance_positive_negative, margin):
    distance_anchor_positive = np.linalg.norm(anchor.detach() - positive.detach())
    return distance_anchor_positive - const_distance_positive_negative + margin
def add_epsilon_noise(image):
    image = torch.add(image, EPSILON)
    return image


def get_embedding(image):
    return EMBEDDING_MODEL(image.unsqueeze(0))


def scale(vector, alpha):
    inf_norm = np.linalg.norm(vector, np.inf)
    #print(vector[0].item() / inf_norm)
    return alpha * (vector[0].detach() / inf_norm)


def normalize_cloaked_image_tensor(image):
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    return normalized_image


if __name__ == '__main__':
    Ulixes("C:\matt.jpg", 0.8)
