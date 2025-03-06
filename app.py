from flask import Flask, jsonify, request
from dotenv import load_dotenv
import threading
import time
import os

load_dotenv()

api_key = os.environ.get("API_KEY")

app = Flask(__name__)
generator = [{
    'state': 'stopped',
    'voltage_main': 230,
    'voltage_aux': 12,
    'temperature': 22
}]


class startGenerator(threading.Thread):
    def run(self, *args, **kwargs):
        for i in range(0,10):
            time.sleep(1)
            print(i)
        generator[0]['state'] = 'started'

class stopGenerator(threading.Thread):
    def run(self, *args, **kwargs):
        for i in range(0,10):
            time.sleep(1)
            print(i)
        generator[0]['state'] = 'stopped'

def authenticate_api_key(x):
    return x == api_key

@app.before_request
def before_request():
    y = request.headers.get('API-Key')
    if not api_key or not authenticate_api_key(y):
        return jsonify({'error': 'Unauthorized'}), 401

@app.route('/generator', methods=['GET'])
def get_generator():
    return jsonify({'data': generator})

@app.route('/generator/start', methods=['GET'])
async def start_generator_route():
    t = startGenerator()
    t.start()
    generator[0]['state'] = 'starting'
    return jsonify({'data': generator})

@app.route('/generator/stop', methods=['GET'])
def stop_generator_route():
    t = stopGenerator()
    t.start()
    generator[0]['state'] = 'stopping'
    return jsonify({'data': generator})

if __name__ == '__main__':
    app.run(debug=True)