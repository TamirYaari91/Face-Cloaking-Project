import torch
import torch.nn as nn
import numpy as np
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1

EPSILON = 0.0001
EMBEDDING_MODEL = InceptionResnetV1(pretrained="vggface2").eval()


def pgd(image, margin, epochs=150, threshold=0.01, alpha=8 / 255):
    anchor = image
    positive = image
    negative = add_epsilon_noise(image)
    adv_triplet_margin_loss = nn.TripletMarginLoss(margin=margin)

    noise_mask = 0.0

    for i in range(int(epochs)):

        anchor.requires_grad = True
        loss = adv_triplet_margin_loss(get_embedding(positive), get_embedding(anchor), get_embedding(negative))
        loss.backward()
        gradient = anchor.grad

        new_noise = scale(gradient, alpha)
        noise_mask += new_noise  # obtaining total noise added

        prev_anchor = anchor
        anchor = torch.add(anchor, new_noise)

        difference_of_prev_anchor_and_new_anchor = np.linalg.norm(
            get_embedding(anchor).detach() - get_embedding(prev_anchor).detach())
        print(f"new noise: {difference_of_prev_anchor_and_new_anchor}")
        if difference_of_prev_anchor_and_new_anchor < threshold:
            break

        anchor = np.clip(anchor.detach(), positive.detach() - 0.5, positive.detach() + 0.5)
        anchor = np.clip(anchor, -1, 1)

        print(f"Epoch {i}/{epochs}: Loss: {loss}")

    return noise_mask


def add_epsilon_noise(image):
    image = torch.add(image, EPSILON)
    return image


def get_embedding(image):
    return EMBEDDING_MODEL(image.unsqueeze(0))


def scale(matrix, alpha):
    abs_matrix = torch.abs(matrix)
    inf_norm = torch.max(torch.linalg.matrix_norm(abs_matrix, ord=2))
    return torch.mul(torch.div(matrix, inf_norm), alpha)
