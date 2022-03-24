from flask import Flask, request, jsonify
from flask_cors import CORS

# Set up Flask:
app = Flask(__name__)
# Set up Flask to bypass CORS:
cors = CORS(app)


# Create the receiver API POST endpoint:
@app.route("/params_receiver", methods=["POST"])
def paramsHandler():
    data = request.get_json()
    data = inc_all_fields_by_one(data)
    header = data.headers
    header['Access-Control-Allow-Origin'] = '*'
    return data


def inc_all_fields_by_one(data):
    print(data)
    inputs_json = data[0]
    for key in inputs_json.keys():
        print(type(inputs_json[key]))
        print(inputs_json[key])
        inputs_json[key] += 1
    output = [inputs_json]
    print(output)
    res = jsonify(output)
    return res


@app.route("/image_receiver", methods=["POST"])
def imageHandler():
    # data = request.get_json()
    print("received image!")
    data = request.get_json()
    image_json = data[0]
    im_b64 = list(image_json.values())[0]
    print(im_b64[:50])

    return jsonify(success=True)
    # header = data.headers
    # header['Access-Control-Allow-Origin'] = '*'
    # return data


if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
