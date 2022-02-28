import json
import logging
import os

from flask import Flask, Response, request
from werkzeug.exceptions import NotFound, MethodNotAllowed


logging.basicConfig(
    format  = "%(asctime)-5s.%(msecs)03d | %(levelname)-7s | %(threadName)10s | %(module)s:L%(lineno)d | %(message)s",
    level   = logging.DEBUG,
    datefmt = "%Y-%m-%d %H:%M:%S")

logging.getLogger('werkzeug').setLevel(logging.ERROR)


VISITS_FILE = '/tmp/visits.txt'

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


@app.route('/count', methods=['GET'])
def get_random_number() -> Response:
    count = get_visit_count()
    count += 1
    store_visit_count(count)
    return Response(status=200, response=json.dumps({'visit-count': count}), content_type='application/json')


def get_visit_count() -> int:
    if not os.path.isfile(VISITS_FILE):
        with open(VISITS_FILE, 'w') as visits_file:
            visits_file.write('0')

    with open(VISITS_FILE, 'r') as visits_file:
        return int(visits_file.read())


def store_visit_count(new_visit_count: int) -> int:
    with open(VISITS_FILE, 'w') as visits_file:
        visits_file.write(str(new_visit_count))
