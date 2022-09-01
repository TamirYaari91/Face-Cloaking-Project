import os

from Testing.vggface_identification import identify_face
from Ulixes.ulixes_controller import cloak_image_with_ulixes

PATH_OF_DIRECTORY_OF_ORIGINAL_IMAGES = "OriginalImages"
PATH_OF_DIRECTORY_OF_CROPPED_IMAGES = "Testing number of iterations/CroppedImages"
PATH_OF_DIRECTORY_OF_CLOAKED_AND_CROPPED_IMAGES = "Testing number of iterations/CloakedAndCroppedImages"
PATH_OF_DIRECTORY_OF_FINAL_CLOAKED_IMAGES = "Testing number of iterations/Final cloaked images"
NUMBER_OF_EPOCHS_LIST = (100, 150, 200, 250, 300)


def generate_cloaked_images_from_original_images_dir():
    threshold = 0.01
    for epoch in NUMBER_OF_EPOCHS_LIST:
        for file_name in os.listdir(PATH_OF_DIRECTORY_OF_ORIGINAL_IMAGES):
            original_image_path = os.path.join(PATH_OF_DIRECTORY_OF_ORIGINAL_IMAGES, file_name)
            cropped_image_path = os.path.join(PATH_OF_DIRECTORY_OF_CROPPED_IMAGES, file_name)
            cloaked_and_cropped_image_path = os.path.join(PATH_OF_DIRECTORY_OF_CLOAKED_AND_CROPPED_IMAGES + str(epoch),
                                                          file_name)
            final_cloaked_image_path = os.path.join(PATH_OF_DIRECTORY_OF_FINAL_CLOAKED_IMAGES + str(epoch), file_name)

            cloak_image_with_ulixes(original_image_path, cropped_image_path, cloaked_and_cropped_image_path,
                                    final_cloaked_image_path, epoch, threshold)
        threshold -= 0.001


def identify_images(path, directory):
    """
    Path should be a path to a new .txt to which the identification results from vggface_identification will be written.
    Directory should either be PATH_OF_DIRECTORY_OF_ORIGINAL_IMAGES or PATH_OF_DIRECTORY_OF_FINAL_CLOAKED_IMAGES as we
    want to evaluate the results of identification before and after cloaking
    """
    results_of_images_identification_file = open(path, "w")
    for file_name in os.listdir(directory):
        path_of_face_to_identify = os.path.join(directory, file_name)
        results_of_images_identification_file.write(file_name + ": \n")
        results_of_images_identification_file.write(identify_face(path_of_face_to_identify))
        results_of_images_identification_file.write("\n ---------------------------------- \n")
    results_of_images_identification_file.close()


generate_cloaked_images_from_original_images_dir()
