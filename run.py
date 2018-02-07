import base64
import random # Avoid * imports as they add a lot of unkwnown namespaces to your file
import json
from flask import Flask, Response, request, render_template, jsonify, current_app
from flask_cors import cross_origin

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")


@app.route('/api/random', methods=['GET'])
@cross_origin(allow_headers=['Content-Type'])
def random_number():
    response = {'randomNumber': random.randint(1, 100)}
    return jsonify(response)


@app.route('/api/upload', methods=['GET','POST'])
@cross_origin(allow_headers=['Content-Type'])
def upload_me():
    if request.method == 'GET':
        """ Show saved image """
        if current_app.file:
            data = current_app.file
            mimetype, image_string = data.split(';base64,')
            image_bytes = image_string.encode('utf-8')
            return Response(base64.decodebytes(image_bytes), mimetype=mimetype)

    if request.method == 'POST':
        """ Receive base 64 encoded image """
        request_data = json.loads(request.get_data())
        data = request_data['data'][5:]
        current_app.file = data
        return Response(status=200)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")
