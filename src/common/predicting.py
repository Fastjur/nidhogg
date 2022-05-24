def predict(preprocessed_sentence, model, tags):
    prediction = model.predict(preprocessed_sentence)
    
    # TODO optimize: output = tags[prediction[0]]
    output = []
    for i, p in enumerate(prediction[0]):
        if p == 1:
            output.append(tags[i])
    return output
