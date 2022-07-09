from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image

# If required, create a face detection pipeline using MTCNN:
mtcnn = MTCNN(device=torch.device("cpu"))

# Create an inception resnet (in eval mode):
resnet = InceptionResnetV1(pretrained='vggface2').eval()

img = Image.open("matt_damon.jpg")
img_cropped = mtcnn(img, save_path="matt_damon_cropped.jpg")


resnet.classify = True
img_probs = resnet(img_cropped.unsqueeze(0))

img_probs_sorted = torch.sort(img_probs)
print(img_probs_sorted)


# help(InceptionResnetV1)
