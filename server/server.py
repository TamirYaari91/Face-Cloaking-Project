import base64
import http
import os
import threading
from io import BytesIO
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
sys.path.append("..")

import connect_to_uni as ctu
from Ulixes.ulixes_controller import cloak_image_with_ulixes

filename_for_original_image_cropped = "cropped.jpg"
filename_for_perturbated_image_faceoff = "faceoff_perturbated.jpg"
filename_for_perturbated_cropped_image_ulixes = "ulixes_perturbated_cropped.jpg"
filename_for_perturbated_image_ulixes = "ulixes_perturbated.jpg"
list_of_extensions_to_remove = (".jpg", ".jpeg", ".png")

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
        for extension in list_of_extensions_to_remove:
            if file.endswith(extension):
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
    command = "dssim " + ctu.filename_for_original_image + " " + filename_for_perturbated_image_ulixes
    output = os.popen(command).read()
    output = [val.strip() for val in output.split('\t')]
    return output[0]


def set_ulixes_parameters(input_param):
    # input param is in range of [1,5] and ulixes epochs needs to be in [100,300], threshold needs to be in [0.006,0.01]
    parameters = [(100, 0.01), (150, 0.009), (200, 0.008), (250, 0.007), (300, 0.006)]
    return parameters[input_param - 1]


input_params = dict()
data_for_results_page = dict()


@app.route("/params_receiver", methods=["POST"])
def params_handler():
    data = request.get_json()
    inputs_json = data[0]
    ulixes_input_param = int(inputs_json["prefValue"])

    data_for_results_page["range_bar_level"] = ulixes_input_param
    input_params["ulixes_params"] = set_ulixes_parameters(ulixes_input_param)
    input_params["should_run_ulixes"] = inputs_json["runUlixes"]
    input_params["should_run_faceoff"] = inputs_json["runFaceOff"]

    return '', http.HTTPStatus.OK


@app.route("/image_receiver", methods=["POST"])
def image_handler():
    data = request.get_json()
    if len(data[0].keys()) == 0:  # no image uploaded
        return jsonify(success=True)

    ulixes_epochs = input_params["ulixes_params"][0]
    ulixes_threshold = input_params["ulixes_params"][1]
    should_run_ulixes = input_params["should_run_ulixes"]
    should_run_faceoff = input_params["should_run_faceoff"]

    # convert imb64 to jpeg:
    img_original_b64 = get_image_base64_string_from_data(data)
    image_base64_string_to_jpeg(img_original_b64, ctu.filename_for_original_image)

    # Create threads to run the different algorithms:
    faceoff_thread = threading.Thread(target=ctu.faceoff_wrapper)
    ulixes_thread = threading.Thread(target=cloak_image_with_ulixes,
                                     args=(ctu.filename_for_original_image, filename_for_original_image_cropped,
                                           filename_for_perturbated_cropped_image_ulixes,
                                           filename_for_perturbated_image_ulixes, ulixes_epochs, ulixes_threshold))

    data_for_results_page["original_image"] = img_original_b64

    # Start the threads:
    if should_run_ulixes:
        ulixes_thread.start()
    if should_run_faceoff:
        faceoff_thread.start()

    # Wait for the threads to finish:
    if should_run_ulixes:
        ulixes_thread.join()
    if should_run_faceoff:
        faceoff_thread.join()

    if should_run_ulixes:
        img_ulixes = Image.open(os.getcwd() + '/' + filename_for_perturbated_image_ulixes)
        img_ulixes_b64 = pil_image_to_image_base64_string(img_ulixes, "jpeg")
        data_for_results_page["ulixes_image"] = img_ulixes_b64
        data_for_results_page["ulixes_dssim"] = calc_dssim_ulixes()

    if should_run_faceoff:
        img_faceoff = Image.open(os.getcwd() + '/' + ctu.filename_for_perturbated_image_faceoff)
        img_faceoff_b64 = pil_image_to_image_base64_string(img_faceoff, "jpeg")
        data_for_results_page["faceoff_image"] = img_faceoff_b64
        data_for_results_page["faceoff_dssim"] = calc_dssim_faceoff()

    data_for_results_page["success"] = True

    res = jsonify(data_for_results_page)
    delete_all_images_from_server()
    return res


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
