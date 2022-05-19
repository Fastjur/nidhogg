from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle
import json
from urllib.parse import parse_qs, urlparse
import numpy as np

from preprocess_data import preprocess_sentence
from predict_model import predict

# TODO use dependency injection instead of global variables

class S(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)
        self.vectorizer = pickle.load(open(f"{global_model_folder}/vectorizer.pkl", "rb"))
        self.model = pickle.load(open(f"{global_model_folder}/tfidf_model.pkl", "rb"))
        self.tags = np.loadtxt(global_tags_filename, dtype=str, delimiter="\n")

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_response()

        #sentence = preprocess_sentence("What dies my JS compiler have in common with Pytorch?", vectorizer)
        # get url param
        params = parse_qs(urlparse(self.path).query)
        print(params)
        sentence = " ".join(params['sentence'])
        processed_sentence = preprocess_sentence(sentence)
        labels = predict(processed_sentence, self.vectorizer, self.model, self.tags)

        response = {
            "Tags" : labels
        }
        json_str=json.dumps(response)
        self.wfile.write(json_str.encode('utf-8'))

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

def run(model_folder, tags_filename, server_class=HTTPServer, handler_class=S, port=8080):
    global global_model_folder, global_tags_filename
    global_model_folder = model_folder
    global_tags_filename = tags_filename
    server_address = ('', port)
    HTTPServer()
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')
