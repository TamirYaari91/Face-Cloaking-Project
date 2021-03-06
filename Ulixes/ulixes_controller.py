import numpy as np
from PIL import Image

from Ulixes.PGD import pgd
from Ulixes.bounding_box import get_bounding_box, merge_perturbated_image_with_original_image
from Ulixes.utils_for_cloaking import crop_image_with_mtcnn, generate_cloaked_cropped_image_from_noise_mask


def cloak_image_with_ulixes(path_of_image_to_cloak, path_for_cropped_image, path_for_cloaked_and_cropped,
                            path_for_cloaked_result, margin=1.1):
    cropped_image = crop_image_with_mtcnn(path_of_image_to_cloak, path_for_cropped_image)

    noise_mask = pgd(cropped_image, margin)

    cloaked_cropped_image_normalized_as_array = generate_cloaked_cropped_image_from_noise_mask(cropped_image,
                                                                                               noise_mask)

    # Save image
    cloaked_cropped_image = Image.fromarray(cloaked_cropped_image_normalized_as_array.astype(np.uint8))
    cloaked_cropped_image.save(path_for_cloaked_and_cropped)

    # Get bounding box of face in image
    x1, y1, width, height = get_bounding_box(path_of_image_to_cloak)

    # Merge cloaked cropped image to original image we want to cloak
    cloaked_result = merge_perturbated_image_with_original_image(path_for_cloaked_and_cropped,
                                                                 path_of_image_to_cloak,
                                                                 path_for_cloaked_result, x1, y1, width, height)

    return cloaked_result

# cloak_image_with_ulixes("/Users/tamiryaari/Desktop/UNI/Year3/FCP/server/original.jpg",
#                         "/Users/tamiryaari/Desktop/UNI/Year3/FCP/server/cropped.jpg",
#                         "/Users/tamiryaari/Desktop/UNI/Year3/FCP/server/ulixes_perturbated_cropped.jpg",
#                         "/Users/tamiryaari/Desktop/UNI/Year3/FCP/server/ulixes_perturbated.jpg")
