import os
import sys
import json
import time
import pickle
import mimetypes

import importlib

from wsgiref.handlers import read_environ
from wsgiref.simple_server import make_server

import lab

print('loading small data...', end='', flush=True)
with open('./resources/small.pickle', 'rb') as f:
    small_data = lab.transform_data(pickle.load(f))
print('done!')

print('loading large data...', end='', flush=True)
with open('./resources/large.pickle', 'rb') as f:
    large_data = lab.transform_data(pickle.load(f))
print('done!')

print()

cur_dir = os.path.realpath(os.path.dirname(__file__))
app_root = os.path.join(cur_dir, 'ui')

def parse_post(environ):
    try:
        body_size = int(environ.get('CONTENT_LENGTH', 0))
    except:
        body_size = 0

    if not body_size:
        return {}

    body = environ['wsgi.input'].read(body_size)
    return json.loads(body)

def ls(params):
    path = os.path.join(cur_dir, params.get('path'))
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def cat(params):
    path = os.path.join(cur_dir, params.get('path'))
    with open(path, 'r') as f:
        return f.read()

def load_pickle(params):
    path = os.path.join(cur_dir, params.get('path'))
    with open(path, 'rb') as f:
        return pickle.load(f)

special_routes = {
    '/ls': ls,
    '/cat': cat,
    '/load_pickle': load_pickle,
    '/better_together': lambda d: lab.acted_together(small_data, d['actor_1'], d['actor_2']),
    '/bacon_number': lambda d: list(lab.actors_with_bacon_number(small_data, d['n'])),
    '/bacon_path': lambda d: lab.bacon_path(small_data, d['actor_name']),
    '/restart': lambda d: (importlib.reload(lab) and {'ok': True})
}

def application(environ, start_response):
    path = environ.get('PATH_INFO', '/') or '/'
    params = parse_post(environ)

    print(f'requested {path}, params: {params}')

    if path in special_routes:
        type_ = 'application/json'
        status = '200 OK'
        body = json.dumps(special_routes[path](params)).encode('utf-8')
    else:
        if path == '/':
            # main page
            static_file = 'index.html'
        else:
            if path.startswith('/ui/'):
                static_file = path[4:]
            else:
                static_file = path[1:]

        test_fname = os.path.join(app_root, static_file)
        if os.path.isfile(test_fname):
            with open(test_fname, 'rb') as f:
                body = f.read()
            status = '200 OK'
            type_ = mimetypes.guess_type(test_fname)[0] or 'text/plain'
        else:
            body = b'File not found: %r' % test_fname
            status = '404 FILE NOT FOUND'
            type_ = 'text/plain'
    len_ = str(len(body))
    headers = [('Content-type', type_), ('Content-length', len_)]
    start_response(status, headers)
    return [body]


if __name__ == '__main__':
    PORT = 6101
    print(f'starting server.  navigate to http://localhost:{PORT}/')
    with make_server('', PORT, application) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
