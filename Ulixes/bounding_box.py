import numpy as np
from PIL import Image
from matplotlib import pyplot
from mtcnn import MTCNN


def get_bounding_box(path_of_original_image):
    # load image from file
    original_image = pyplot.imread(path_of_original_image)

    # create the detector, using default weights
    bounding_box_detector = MTCNN()

    # detect faces in the image
    results = bounding_box_detector.detect_faces(original_image)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']

    return x1, y1, width, height


def merge_perturbated_image_with_original_image(path_for_cloaked_and_cropped, path_of_original_image,
                                                path_for_cloaked_result, x1, y1, width, height):
    perturbated_image = Image.fromarray(pyplot.imread(path_for_cloaked_and_cropped).astype(np.uint8))
    perturbated_image_resized = perturbated_image.resize((width, height))
    x2, y2 = x1 + width, y1 + height
    original_image = Image.fromarray(pyplot.imread(path_of_original_image).astype(np.uint8))
    original_image_array = np.asarray(original_image.copy())
    original_image_array_copy = original_image_array.copy()
    original_image_array_copy[y1:y2, x1:x2] = np.asarray(perturbated_image_resized)

    # For Debug
    # normalized_original_image_array = normalize_cloaked_image_tensor(original_image_array)
    image = Image.fromarray(original_image_array_copy.astype(np.uint8))
    # face_array = Image.fromarray(image).astype(np.uint8)
    image.save(path_for_cloaked_result)

    return original_image
