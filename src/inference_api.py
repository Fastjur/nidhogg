from http.server import BaseHTTPRequestHandler, HTTPServer
import pickle
import json
from urllib.parse import parse_qs, urlparse
import numpy as np
import sys

from common.preprocessing import get_stopwords, preprocess_sentence
from common.predicting import predict

# TODO use dependency injection instead of global variables
global nltk_corpora_folder, model_folder

class S(BaseHTTPRequestHandler):
    def __init__(self, *args):
        BaseHTTPRequestHandler.__init__(self, *args)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def load_models(self):
        # TODO models are still loaded on every request
        if not hasattr(self, "vectorizer"):
            self.stopwords = get_stopwords(nltk_corpora_folder)
            self.vectorizer = pickle.load(open(f"{model_folder}/vectorizer.pkl", "rb"))
            self.model = pickle.load(open(f"{model_folder}/tfidf_model.pkl", "rb"))
            self.tags = np.loadtxt(f"{model_folder}/tags.txt", dtype=str, delimiter="\n")
            print("[Inference] Loaded models")

    def do_GET(self):
        self._set_response()

        params = parse_qs(urlparse(self.path).query)
        print(params)
        if len(params) < 1:
            return

        self.load_models()
        sentence = " ".join(params['sentence'])
        processed_sentence = preprocess_sentence(sentence, self.vectorizer, self.stopwords)
        labels = predict(processed_sentence, self.model, self.tags)

        response = {
            "Tags" : labels
        }
        json_str=json.dumps(response)
        self.wfile.write(json_str.encode('utf-8'))

    def do_POST(self):
        content_len = int(self.headers['content-length'])
        post_body = self.rfile.read(content_len) # TODO potential security risk (Heartbleed)?
        labels = predict(str(post_body))

        response = {
            "tags" : labels
        }
        json_str=json.dumps(response)
        self._set_response()
        self.wfile.write(json_str.encode('utf-8'))

        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python src/inference_api.py [nltk_corpora_folder] [model_folder]")
        exit(1)
    [_, nltk_corpora_folder, model_folder] = sys.argv

    server_address = ('', 8080)
    httpd = HTTPServer(server_address, S)
    print('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print('Stopping httpd...\n')
