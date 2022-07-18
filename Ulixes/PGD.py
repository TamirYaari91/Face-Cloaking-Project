import torch
import torch.nn as nn
import numpy as np
from facenet_pytorch.models.mtcnn import MTCNN
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from PIL import Image
from torch.autograd import grad

EPSILON = 0.0001
EMBEDDING_MODEL = InceptionResnetV1(pretrained="vggface2").eval()
filename_for_original_image_cropped = "cropped_original.jpg"
filename_for_perturbated_image_ulixes = "cloaked_cropped_ulixes.jpg" # TODO - need to be png?


def Ulixes(image, margin):
    cropped_image = crop_image(image, filename_for_original_image_cropped)
    noise_mask = pgd(cropped_image, margin) # PGD

    # TODO: un_comment those lines and understand how to take the (1,512) dimensions noise and turn it into (160, 160, 3) dimensions matrix
    # cropped_image_with_mask = add_noise_mask(cropped_image, noise_mask)
    # cloaked_image_array_normalized = normalize_cloaked_image_tensor(cropped_image_with_mask)
    #
    # cloaked_image_array_normalized = np.swapaxes(cloaked_image_array_normalized, 0, 1)  # [3, 160, 160] -> [160, 3, 160]
    # cloaked_image_array_normalized = np.swapaxes(cloaked_image_array_normalized, 1, 2)  # [160, 3, 160] -> [160, 160, 3]
    #
    # cloaked_image = Image.fromarray(np.array(cloaked_image_array_normalized).astype(np.uint8))
    # cloaked_image.save(filename_for_perturbated_image_ulixes)
    # return cloaked_image
    return


def crop_image(image, cropped_path):
    mtcnn_pt = MTCNN(device=torch.device("cpu"))
    image = Image.open(image).convert("RGB")
    image_cropped = mtcnn_pt(image, save_path=cropped_path)
    return image_cropped


def pgd(image, margin=1.6, alpha=0.01):
    # margin: set to 1.1 as default, can be between [0.2, 2] to change intensity of noise masks introduced

    anchor = image
    positive = image
    negative = add_epsilon_noise(image)

    adv_triplet_margin_loss = nn.TripletMarginLoss(margin)

    embedded_anchor = torch.autograd.Variable(get_embedding(anchor))
    embedded_negative = torch.autograd.Variable(get_embedding(negative), requires_grad=True)
    embedded_positive = torch.autograd.Variable(get_embedding(positive))

    threshold = 0.01
    epochs = 100

    noise_mask = 0

    for i in range(epochs):

        loss = adv_triplet_margin_loss(embedded_positive, embedded_anchor, embedded_negative)
        loss.backward()
        gradient = (- 1) * embedded_negative.grad  # After checking the loss gradient calculation I think we need this

        new_noise = scale(gradient[0], alpha)
        noise_mask += new_noise  # obtaining total noise added

        embedded_negative.grad.zero_()

        anchor = torch.add(embedded_anchor, new_noise)

        difference_of_prev_anchor_and_new_anchor = np.linalg.norm(anchor.data - embedded_anchor.data)
        if difference_of_prev_anchor_and_new_anchor < threshold:
            break

        anchor = np.clip(anchor.detach(), embedded_positive.detach() - 0.5, embedded_positive.detach() + 0.5)
        anchor = np.clip(anchor, -1, 1)

        embedded_anchor = anchor

        print(f"Epoch {i}/{epochs}: Loss: {loss}")

    anchor = torch.add(embedded_anchor, noise_mask)
    return noise_mask


def get_loss(anchor, positive, const_distance_positive_negative, margin):
    distance_anchor_positive = np.linalg.norm(anchor.detach() - positive.detach())
    return distance_anchor_positive - const_distance_positive_negative + margin


def add_epsilon_noise(image):
    image = torch.add(image, EPSILON)
    return image


def add_noise_mask(image, noise):
    image = torch.add(image, noise)
    return image


def get_embedding(image):
    return EMBEDDING_MODEL(image.unsqueeze(0))


def scale(vector, alpha):
    inf_norm = np.linalg.norm(vector, np.inf)
    return (vector.data / inf_norm).data * alpha


def normalize_cloaked_image_tensor(image):
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    return normalized_image


if __name__ == '__main__':
    Ulixes("C:\matt.jpg", 1.1)
