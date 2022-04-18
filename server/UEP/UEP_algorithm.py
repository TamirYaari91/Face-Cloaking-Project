import torch
from PIL import Image
from facenet_pytorch.models.inception_resnet_v1 import InceptionResnetV1
from facenet_pytorch.models.mtcnn import MTCNN

from server.classification_models import classification_models


def classification_using_faceNet(img_path, cropped_path, model_name):
    """

    :param img_path: path of image to calculate classification probability vector for.
    :param cropped_path: path to save a cropped image containing just the face, sized 160 X 160.
    :param model_name: the name of the pretrained model to be used
    :return: A classification probability vector of the image in img_path.
    """
    # Returns a pretrained network that returns images cropped to include the face only
    mtcnn_pt = MTCNN(device=torch.device('cpu'))

    # Opens the image using PIL and converts it to RGB
    image = Image.open(img_path).convert('RGB')

    # Crops the image using the MTCNN network to a default size of 160 x 160
    img_cropped = mtcnn_pt(image, save_path=cropped_path)

    # Instantiate pretrained vggface2 as a classifier
    model = InceptionResnetV1(pretrained=model_name).eval()

    # Compute classification probability vector using the model.
    img_probs = model(img_cropped.unsqueeze(0))

    print(img_probs)
    return img_probs


if __name__ == "__main__":
    classification_using_faceNet(
        "/Users/yarden.benbassat/PycharmProjects/Face-Cloaking-Project/resources/test_images/angelina_jolie.png",
        "/Users/yarden.benbassat/PycharmProjects/Face-Cloaking-Project/resources/test_images_cropped/angelina_jolie.png",
        classification_models.casia_webface.value)

