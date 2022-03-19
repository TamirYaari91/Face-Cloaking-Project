from flask import Flask, request, jsonify
from flask_cors import CORS

# Set up Flask:
app = Flask(__name__)
# Set up Flask to bypass CORS:
cors = CORS(app)


# Create the receiver API POST endpoint:
@app.route("/params_receiver", methods=["POST"])
def postME():
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
        inputs_json[key] += 1
    output = [inputs_json]
    print(output)
    res = jsonify(output)
    return res




if __name__ == "__main__":
    # app.run()
    app.run(debug=True)
