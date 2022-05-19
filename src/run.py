import sys

import train_model
import predict_model
import preprocess_data
import inference_api

raw_data_folder = "./data"
processed_data_folder = "./outputs/processed_data"
model_folder = "./outputs/models"

if __name__ == "__main__":
    if (sys.argv[1] == "--preprocess"):
        preprocess_data.preprocess_data(raw_data_folder, processed_data_folder, model_folder)
    elif (sys.argv[1] == "--train"):
        train_model.start_training(processed_data_folder, model_folder)
    elif (sys.argv[1] == "--eval"):
        predict_model.evaluate() # TODO fix evaluate
    elif (sys.argv[1] == "--serve"):
        inference_api.run(model_folder, f"{processed_data_folder}/tags.txt")
    else:
        print("Please specify command from: [--preprocess, --train, --eval, --serve]")
