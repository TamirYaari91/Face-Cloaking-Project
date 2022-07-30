import numpy as np
from PIL import Image
from matplotlib import pyplot
from mtcnn import MTCNN


def bounding_box_detector(path):
    # load image from file
    pixels = pyplot.imread(path)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    merge_perturbated_image_with_original_image("/Users/yarden.benbassat/Desktop/Images-for-face-cloaking/Ben Stiller cloaked cropped.jpg", path, x1, y1, width, height)


def merge_perturbated_image_with_original_image(perturbated_path, original_image_path, x1, y1, width, height):
    perturbated_image = Image.fromarray(pyplot.imread(perturbated_path).astype(np.uint8))
    perturbated_image_resized = perturbated_image.resize((width, height))
    x2, y2 = x1 + width, y1 + height
    original_image = Image.fromarray(pyplot.imread(original_image_path).astype(np.uint8))
    original_image_array = np.asarray(original_image)
    original_image_array[y1:y2, x1:x2] = np.asarray(perturbated_image_resized)

    # For Debug
    # normalized_original_image_array = normalize_cloaked_image_tensor(original_image_array)
    image = Image.fromarray(original_image_array.astype(np.uint8))
    # face_array = Image.fromarray(image).astype(np.uint8)
    image.save("/Users/yarden.benbassat/Desktop/Images-for-face-cloaking/Ben Stiller final result.jpeg")

    return original_image



bounding_box_detector("/Users/yarden.benbassat/Desktop/Images-for-face-cloaking/Ben Stiller.jpeg")