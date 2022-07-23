import cv2
import torch
import torch.nn as nn
import numpy as np
from facenet_pytorch.models.mtcnn import MTCNN
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from PIL import Image

EPSILON = 0.0001
EMBEDDING_MODEL = InceptionResnetV1(pretrained="vggface2").eval()
filename_for_original_image_cropped = "original_cropped.jpg"
filename_for_perturbated_image_ulixes = "ulixes_perturbated.jpg"  # TODO - need to be png?


def Ulixes(image, margin=1.1):
    cropped_image = crop_image(image, filename_for_original_image_cropped)
    noise_mask = pgd(cropped_image, margin)  # PGD

    # Add noise mask to the cropped face image, normalize its values and change the order of dimensions
    cropped_image_with_mask = add_noise_mask(cropped_image, noise_mask)
    cloaked_image_normalized = normalize_cloaked_image_tensor(cropped_image_with_mask)
    cloaked_image_array_normalized = cloaked_image_normalized.detach().numpy()
    cloaked_image_array_normalized = np.swapaxes(cloaked_image_array_normalized, 0, 1)  # [3, 160, 160] -> [160, 3, 160]
    cloaked_image_array_normalized = np.swapaxes(cloaked_image_array_normalized, 1, 2)  # [160, 3, 160] -> [160, 160, 3]

    # TODO: CALL BOUNDING_BOX CODE AND PUT THE CLOAKED FACE IN THE RIGHT PLACE

    # Save image
    cloaked_image = Image.fromarray(cloaked_image_array_normalized.astype(np.uint8))
    cloaked_image.save(filename_for_perturbated_image_ulixes)
    return cloaked_image


def crop_image(image, cropped_path):
    mtcnn_pt = MTCNN()
    image = Image.open(image).convert("RGB")
    image_cropped = mtcnn_pt(image, save_path=cropped_path)
    return image_cropped


def pgd(image, margin=1.1, alpha=8 / 255):
    # margin: set to 1.1 as default, can be between [0.2, 2] to change intensity of noise masks introduced

    anchor = image
    positive = image
    negative = add_epsilon_noise(image)
    adv_triplet_margin_loss = nn.TripletMarginLoss(margin=margin)

    threshold = 0.01
    epochs = 150
    noise_mask = 0.0

    for i in range(epochs):

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


def add_noise_mask(image, noise):
    image = torch.add(image, noise)
    return image


def get_embedding(image):
    return EMBEDDING_MODEL(image.unsqueeze(0))


def scale(matrix, alpha):
    abs_matrix = torch.abs(matrix)
    inf_norm = torch.max(torch.linalg.matrix_norm(abs_matrix, ord=2))
    return torch.mul(torch.div(matrix, inf_norm), alpha)


def normalize_cloaked_image_tensor(image):
    min_img = image.min()
    max_img = image.max()
    normalized_image = (image - min_img) / (max_img - min_img)
    normalized_image *= 255.0
    return normalized_image


# if __name__ == '__main__':
#     Ulixes("C:\ImagesForTesting\matt.jpg", 2)
