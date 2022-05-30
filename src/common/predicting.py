def predict(preprocessed_sentence, model, tags):
    prediction = model.predict(preprocessed_sentence)
    return list(tags[prediction[0] == 1])
