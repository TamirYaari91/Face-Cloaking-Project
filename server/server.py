import os
from time import sleep

from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
from io import BytesIO
import connect_to_uni

# Set up Flask:
app = Flask(__name__)

# Set up Flask to bypass CORS:
cors = CORS(app)


@app.route("/params_receiver", methods=["POST"])
def params_handler():
    data = request.get_json()
    data = inc_all_fields_by_one(data)
    header = data.headers
    header['Access-Control-Allow-Origin'] = '*'
    return data


def inc_all_fields_by_one(data):
    inputs_json = data[0]
    for key in inputs_json.keys():
        inputs_json[key] += 1
    output = [inputs_json]
    res = jsonify(output)
    return res


def get_image_base64_string_from_data(data):
    image_json = data[0]
    im_b64 = list(image_json.values())[0]
    im_b64 = im_b64[im_b64.find(",") + 1:]
    return im_b64


def get_image_base64_string_from_jpeg(filepath, filename):
    with open(filepath + filename, "rb") as image_file:
        im_b64 = base64.b64encode(image_file.read())
        return im_b64


def image_base64_string_to_pil_image(im_b64):
    img_string = base64.b64decode(im_b64)
    img = Image.open(BytesIO(img_string))
    return img


def image_base64_string_to_jpeg(im_b64, filename):
    decoder = open(filename, 'wb')
    decoder.write(base64.b64decode(im_b64))
    decoder.close()


def pil_image_make_grayscale(img):
    return img.convert("L")


def pil_image_to_image_base64_string(img, image_format):
    buffered = BytesIO()
    img.save(buffered, format=image_format)
    img_str = str(base64.b64encode(buffered.getvalue()), 'utf-8')
    return img_str


@app.route("/image_receiver", methods=["POST"])
def image_handler():
    data = request.get_json()
    if len(data[0].keys()) == 0:  # no image uploaded
        return jsonify(success=True)  # probably needs to be different

    im_b64 = get_image_base64_string_from_data(data)
    image_base64_string_to_jpeg(im_b64, connect_to_uni.filename_for_original_image)

    img = image_base64_string_to_pil_image(im_b64)
    img_grayscale = pil_image_make_grayscale(img)
    img_grayscale_b64 = pil_image_to_image_base64_string(img_grayscale, "jpeg")

    # Perform Face-Off
    # connect_to_uni.face_off_wrapper()
    # img_faceoff_b64 = get_image_base64_string_from_jpeg(os.getcwd(), connect_to_uni.filename_for_perturbated_image)

    cloaked_images_b64 = dict()
    cloaked_images_b64["grayscale"] = img_grayscale_b64
    # cloaked_images_b64["face-off"] = img_faceoff_b64
    cloaked_images_b64["success"] = True

    # img.show()
    sleep(3)  # TODO - imitates faceoff waiting time

    return jsonify(cloaked_images_b64)


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
