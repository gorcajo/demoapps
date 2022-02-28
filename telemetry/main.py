import json
import logging

from flask import Flask, Response, request
from werkzeug.exceptions import NotFound, MethodNotAllowed

import redis_client


logging.basicConfig(
    format  = "%(asctime)-5s.%(msecs)03d | %(levelname)-7s | %(threadName)10s | %(module)s:L%(lineno)d | %(message)s",
    level   = logging.DEBUG,
    datefmt = "%Y-%m-%d %H:%M:%S")

logging.getLogger('werkzeug').setLevel(logging.ERROR)


app = Flask(__name__)


@app.before_request
def before_request() -> Response:
    logging.info(f'Request "{request.method.upper()} {request.path.lower()}" from "{request.remote_addr}"')


@app.after_request
def after_request(response: Response) -> Response:
    logging.info(f'Returning HTTP {response.status_code}')
    return response


@app.errorhandler(Exception)
def handle_exceptions(e) -> Response:
    if isinstance(e, NotFound):
        logging.error('Returning HTTP 404')
        return Response(status=404, response=json.dumps({'error': 'HTTP 404 Not Found'}), content_type='application/json')
    elif isinstance(e, MethodNotAllowed):
        logging.error('Returning HTTP 405')
        return Response(status=405, response=json.dumps({'error': 'HTTP 405 Method Not Allowed'}), content_type='application/json')
    else:
        logging.error('Exception!', e)
        return Response(status=500, response=json.dumps({'error': 'HTTP 500 Internal Server Error'}), content_type='application/json')


@app.route('/devices/<device_id>/temperature', methods=['PUT'])
def put_temperature(device_id: str) -> Response:
    redis_client.instance().set(device_id, float(request.json['temperature']))
    return Response(status=204, response='', content_type='application/json')


@app.route('/devices/<device_id>/temperature', methods=['GET'])
def get_temperature(device_id: str) -> Response:
    temperature = redis_client.instance().get(device_id)

    if temperature is None:
        return Response(status=404, response=json.dumps({'error': f'Device ID {device_id} not found'}), content_type='application/json')

    return Response(status=200, response=json.dumps({'temperature': float(temperature)}), content_type='application/json')


@app.route('/devices', methods=['GET'])
def list_device_ids() -> Response:
    device_ids = [key.decode('utf8') for key in redis_client.instance().keys('*')]
    return Response(status=200, response=json.dumps(device_ids), content_type='application/json')
