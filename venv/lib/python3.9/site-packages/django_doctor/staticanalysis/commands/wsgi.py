import json
import mimetypes
import pathlib
import threading
from wsgiref.simple_server import make_server
from wsgiref.util import FileWrapper
from wsgiref.simple_server import WSGIRequestHandler

import django_doctor.wizard
from django_doctor.staticanalysis.commands import helpers
from django_doctor.staticanalysis.helpers import serializer


build_dir = pathlib.Path(django_doctor.wizard.__path__[0])


def home_handler(environ, respond, app):
    dumped_messages = json.dumps(app.messages, default=serializer)
    with open(build_dir / 'index.html', 'r') as f:
        response_body = f.read()
        response_body = response_body.replace(
            '<head>',
            f'<head><script id="context-messages" type="application/json">{dumped_messages}</script>'
        )
    response_body = response_body.encode('utf-8')
    respond('200 OK', [('Content-Type', 'text/html'), ('Content-Length', str(len(response_body)))])
    return [response_body]


def static_handler(environ, respond, app):
    content_type = mimetypes.guess_type(environ['PATH_INFO'])[0]
    path = build_dir / environ['PATH_INFO'][1:]

    if path.exists():
        respond('200 OK', [('Content-Type', content_type)])
        return FileWrapper(open(path, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'not found']


def submit_handler(environ, respond, app):
    body_size = int(environ.get('CONTENT_LENGTH', 0))
    request_body = environ['wsgi.input'].read(body_size)
    whitelist = json.loads(request_body)
    helpers.trasform_files(project_root=app.project_root, whitelist=whitelist)
    respond('200 OK', [('Content-Type', 'text/plain')])
    threading.Timer(0.5, app.server.shutdown).start()
    return [b'']


class Application(object):
    def __init__(self, messages, project_root):
        self.messages = messages
        self.project_root = project_root

    def __call__(self, environ, respond):
        if environ.get('PATH_INFO') == '/':
            if environ['REQUEST_METHOD'] == 'POST':
                handler = submit_handler
            else:
                handler = home_handler
        else:
            handler = static_handler
        return handler(environ=environ, respond=respond, app=self)


class NoLogWSGIRequestHandler(WSGIRequestHandler):
    def log_message(self, *args, **kwargs):
        return


def create(address, port, messages, project_root):
    app = Application(messages=messages, project_root=project_root)
    server = make_server(host=address, port=port, app=app, handler_class=NoLogWSGIRequestHandler)
    app.server = server
    return server
