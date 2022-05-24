import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle
import json
from urllib.parse import urlsplit, parse_qs, urlparse
import numpy as np

from data.preprocess import preprocess_sentence
from models.predict_model import predict

class S(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        content_len = int(self.headers['content-length'])
        post_body = self.rfile.read(content_len)
        labels = predict(str(post_body))

        response = {
            "tags" : labels
        }
        json_str=json.dumps(response)
        self._set_response()
        self.wfile.write(json_str.encode('utf-8'))

        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')

def serve(port=8080):
    run(port=port)