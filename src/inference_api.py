import cgi
from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle
import json
from urllib.parse import urlsplit, parse_qs, urlparse
import numpy as np
import sys

from common.preprocessing import preprocess_sentence
from common.predicting import predict

# TODO use dependency injection instead of global variables

class S(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)
        self.load_models()

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def load_models(self):
        if not hasattr(self, "vectorizer"):
            self.vectorizer = pickle.load(open(f"{global_model_folder}/vectorizer.pkl", "rb"))
            self.model = pickle.load(open(f"{global_model_folder}/tfidf_model.pkl", "rb"))
            self.tags = np.loadtxt(global_tags_filename, dtype=str, delimiter="\n")
            print("[Inference] Loaded models")

    def do_GET(self):
        self._set_response()

        params = parse_qs(urlparse(self.path).query)
        print(params)
        if len(params) < 1:
            return

        self.load_models()
        sentence = " ".join(params['sentence'])
        processed_sentence = preprocess_sentence(sentence, self.vectorizer)
        labels = predict(processed_sentence, self.model, self.tags)

        response = {
            "Tags" : labels
        }
        json_str=json.dumps(response)
        self.wfile.write(json_str.encode('utf-8'))


    def do_POST(self):
        content_len = int(self.headers['content-length'])
        postvars = parse_qs(self.rfile.read(content_len), keep_blank_values=1)
        print(postvars.keys())
        if b'question' in postvars:
            self.load_models()
            sentence = str(postvars[b'question'][0].decode("utf-8"))
            processed_sentence = preprocess_sentence(sentence, self.vectorizer)
            labels = predict(processed_sentence, self.model, self.tags)

            response = {
                "tags" : labels
            }
            json_str=json.dumps(response)
            self._set_response()
            self.wfile.write(json_str.encode('utf-8'))

            #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        else:
            print(f"Received data did not have a question. content: {postvars}")

def run(model_folder, tags_filename, server_class=HTTPServer, handler_class=S, port=8080):
    global global_model_folder, global_tags_filename
    global_model_folder = model_folder
    global_tags_filename = tags_filename
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')

# TODO merge code below with run method
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/inference_api.py [model_folder] [tags_file]")
        exit(1)
    
    model_folder = sys.argv[1]
    tags_file = sys.argv[2]
    run(model_folder, tags_file)
