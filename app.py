#!/usr/bin/env python
from flask import Flask, request, send_from_directory, jsonify, Response, json, abort, send_file
from flask_cors import CORS
import datetime
import os
import signal
import simpleflock
class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)


debug = False

app = Flask(__name__,static_url_path='/static')
CORS(app)

@app.route("/")
def index():
    return Response("It works!"), 200


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/records/add/<string:file_name>', methods=['POST'])
def add_record(file_name):
    if len(file_name) == 0:
        abort(400)
    if not request.json:
        return jsonify({'status': 'error: not a valid json'}), 201
    out = request.json
    file_path = "/dev/shm/logging/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(file_path+file_name+'.json', "a") as myfile:
        out['server_time'] = str(datetime.datetime.utcnow())
        with simpleflock.SimpleFlock(file_path+file_name+'.lock', timeout = 5):
            with timeout():
                myfile.write(json.dumps(out)+'\n')
    return jsonify({'status': (out if debug else 'log added')}), 201


@app.route('/records/add', methods=['POST'])
def add_record_default():
    if not request.json:
        return jsonify({'status': 'error: not a valid json'}), 201
    out = request.json
    file_path = "/dev/shm/logging/"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_name = "db"
    if 'ex_id' in out and len(out['ex_id']) > 0:
        file_name = out['ex_id']
    with open(file_path+file_name+'.json', "a") as myfile:
        #out = request.json
        out['server_time'] = str(datetime.datetime.utcnow())
        with simpleflock.SimpleFlock(file_path+file_name+'.lock', timeout = 5):
            with timeout():
                myfile.write(json.dumps(out)+'\n')
    return jsonify({'status': (out if debug else 'log added')}), 201

@app.route('/records/delete/<string:filename>', methods=['POST'])
def delete_record(filename):
    if not request.json:
        return jsonify({'status': 'error: not a valid json'}), 201
    out = request.json
    file_path = "/dev/shm/logging/"
    if not os.path.exists(file_path):
        if 'password' in out:
            return jsonify({'status': 'error: file not found'}), 201
        else:
            abort(400)
    f = file_path+filename+'.json'
    if 'password' in out and out['password']=='ciaociao' and os.path.isfile(f):
        os.remove(f)
    return jsonify({'status': (out if debug else 'logs deleted')}), 201

#to parse the file use pandas.read_csv(,lines=True)
#a = []
#   for line in open('db.json', 'r'):
#   a.append(json.loads(line))

@app.route('/records/get/<string:filename>', methods=['GET'])
def get_record(filename):
   filen = '/dev/shm/logging/'+filename+'.json'
   if os.path.isfile(filen):
      #return Response(open(filen).read(), mimetype='text/plain')
      temp = []
      for line in open(filen,'r'):
          temp.append(json.loads(line))
      return jsonify({'logs':temp}), 201
   else:
      return jsonify({'logs': []}), 201


@app.route('/records/download/<string:filename>', methods=['GET'])
def download_record(filename):
   filen = '/dev/shm/logging/'+filename+'.json'
   if os.path.isfile(filen):
      return send_file(filen, as_attachment=True)
   else:
      abort(404)

#@app.route('/.well-known/acme-challenge/<path:path>')
#def send_static2(path):
#    return send_from_directory('static', path)


#@app.after_request
#def apply_caching(resp):
#    resp.headers['Access-Control-Allow-Origin'] = '*'
#    return resp

if __name__ == '__main__':
    app.run(debug=debug,threaded=False)
    #app.run(host='0.0.0.0',port=5000,debug=False,threaded=False)
