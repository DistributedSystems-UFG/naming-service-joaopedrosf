from flask import Flask, request, jsonify
from const import *
import requests

app = Flask(__name__)
service_registry = {}

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    service_name = data.get('serviceName')
    url = data.get('url')

    if service_name and url:
        service_registry[service_name] = url
        return jsonify(), 201
    else:
        return jsonify({'error': 'Invalid request payload'}), 400

@app.route('/lookup', methods=['GET'])
def lookup():
    service_name = request.args.get('serviceName')

    if service_name in service_registry:
        return jsonify({'url': service_registry[service_name]})
    else:
        return jsonify({'error': f'Service {service_name} not found'}), 404

@app.route('/unregister', methods=['DELETE'])
def unregister():
    service_name = request.args.get('serviceName')

    if service_name in service_registry:
        del service_registry[service_name]
        return jsonify(), 204
    else:
        return jsonify({'error': f'Service {service_name} not found'}), 404
    
def get_ip():
    response = requests.get('https://httpbin.org/get')
    return response.json()['origin']

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)