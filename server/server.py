import http
import os
import threading
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO
import connect_to_uni as ctu
from Ulixes import PGD

# Set up Flask:
app = Flask(__name__)

# Set up Flask to bypass CORS:
cors = CORS(app)


def get_image_base64_string_from_data(data):
    image_json = data[0]
    im_b64 = list(image_json.values())[0]
    im_b64 = im_b64[im_b64.find(",") + 1:]
    return im_b64


def image_base64_string_to_pil_image(im_b64):
    img_string = base64.b64decode(im_b64)
    img = Image.open(BytesIO(img_string))
    return img


def image_base64_string_to_jpeg(im_b64, filename):
    decoder = open(filename, 'wb')
    decoder.write(base64.b64decode(im_b64))
    decoder.close()


def pil_image_to_image_base64_string(img, image_format):
    buffered = BytesIO()
    img.save(buffered, format=image_format)
    img_str = str(base64.b64encode(buffered.getvalue()), 'utf-8')
    return img_str


def delete_all_images_from_server():
    for file in os.listdir("."):
        if file.endswith(".jpg") or file.endswith(".png"):
            os.remove(file)


def calc_dssim_original():
    command = "dssim " + ctu.filename_for_original_image + " " + ctu.filename_for_original_image
    output = os.popen(command).read()
    output = [val.strip() for val in output.split('\t')]
    return output[0]


def calc_dssim_faceoff():
    command = "dssim " + ctu.filename_for_original_image + " " + ctu.filename_for_perturbated_image_faceoff
    output = os.popen(command).read()
    output = [val.strip() for val in output.split('\t')]
    return output[0]


def calc_dssim_ulixes():
    command = "dssim " + PGD.filename_for_original_image_cropped + " " + PGD.filename_for_perturbated_image_ulixes
    output = os.popen(command).read()
    output = [val.strip() for val in output.split('\t')]
    return output[0]


# TODO - Faceoff calculates DSSIM on entire image, Ulixes only on cropped face - change to entire image when possible


@app.route("/image_receiver", methods=["POST"])
def image_handler():
    data = request.get_json()
    if len(data[0].keys()) == 0:  # no image uploaded
        return jsonify(success=True)  # probably needs to be different

    # convert imb64 to jpeg:
    img_original_b64 = get_image_base64_string_from_data(data)
    image_base64_string_to_jpeg(img_original_b64, ctu.filename_for_original_image)

    # Create threads to run the different algorithms:
    faceoff_thread = threading.Thread(target=ctu.faceoff_wrapper)
    ulixes_thread = threading.Thread(target=PGD.Ulixes, args=ctu.filename_for_original_image)

    # Start the threads:
    faceoff_thread.start()
    ulixes_thread.start()

    # Wait for the threads to finish:
    faceoff_thread.join()
    ulixes_thread.join()

    img_faceoff = Image.open(os.getcwd() + '/' + ctu.filename_for_perturbated_image_faceoff)
    img_ulixes = Image.open(os.getcwd() + '/' + PGD.filename_for_perturbated_image_ulixes)

    img_faceoff_b64 = pil_image_to_image_base64_string(img_faceoff, "jpeg")
    img_ulixes_b64 = pil_image_to_image_base64_string(img_ulixes, "jpeg")

    cloaked_images_b64 = dict()
    cloaked_images_b64["original_image"] = img_original_b64
    cloaked_images_b64["faceoff_image"] = img_faceoff_b64
    cloaked_images_b64["ulixes_image"] = img_ulixes_b64
    cloaked_images_b64["original_dssim"] = calc_dssim_original()
    cloaked_images_b64["faceoff_dssim"] = calc_dssim_faceoff()
    cloaked_images_b64["ulixes_dssim"] = calc_dssim_ulixes()
    cloaked_images_b64["success"] = True

    # sleep(3)  # imitates faceoff waiting time

    res = jsonify(cloaked_images_b64)
    delete_all_images_from_server()
    return res


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
