import json
import logging
import random

from flask import Flask, Response, request
from werkzeug.exceptions import NotFound, MethodNotAllowed


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


@app.route('/number', methods=['GET'])
def get_random_number() -> Response:
    number = random.randint(1, 1000)
    return Response(status=200, response=json.dumps({'number': number}), content_type='application/json')
