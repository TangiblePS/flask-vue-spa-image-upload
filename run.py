import os
import base64
import random # Avoid * imports as they add a lot of unkwnown namespaces to your file
import json
from flask import Flask, Response, request, render_template, jsonify
from flask_cors import cross_origin
from time import perf_counter
import numpy as np # added 3/7
import pets # from local dir
import subprocess
import re

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
        if os.path.exists('webdata/file.img'):
            with open('webdata/file.img', 'r') as rf:
                data = rf.read()
                mimetype, image_string = data.split(';base64,')
                image_bytes = image_string.encode('utf-8')
                return Response(base64.decodebytes(image_bytes), mimetype=mimetype)

    if request.method == 'POST':
        """ Receive base 64 encoded image """
        start = perf_counter()
        print('Request received')
        request_data = json.loads(request.get_data().decode('utf-8'))
        data = request_data['data'][5:]

        with open('webdata/file.img', 'w') as wf:
            wf.write(data)

        mimetype, image_string = data.split(';base64,')
        image_bytes = image_string.encode('utf-8')

        with open('webdata/dir/file.jpg', 'wb') as wf:
            wf.write(base64.b64decode(image_bytes))
            
        print('Saved in file.')
        print('Time elapsed: {}'.format(perf_counter() - start))
        return Response(status=200)

    return render_template('index.html')

@app.route('/api/name', methods=['GET','POST'])
@cross_origin(allow_headers=['Content-Type'])
def find_and_show_a_name():
    if request.method == 'GET':
        """ Show name of a saved image """
        if os.path.exists('webdata/dir/file.jpg'):
            python2_command = "python pets-direct.py"
            process = subprocess.Popen(python2_command.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            if output.decode('ascii').startswith('I don'):
                return jsonify({'error': output.decode('ascii').strip()})
            # ok now I need to get what's between the '' in a REGEXP
            petName = re.search('(?<=\\n)\w+',output.decode('ascii')).group(0)
#            petName = output.decode('ascii')
            response = {'petName': petName}
            return jsonify(response)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template('index.html')
