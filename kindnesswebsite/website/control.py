import pickle


## load model

model = pickle.load(open('./website/static/AoK_classifier_model.pkl', 'rb'))

features_file = pickle.load(open("./website/static/AoK_features.pkl", "rb"))

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
loaded_vec = CountVectorizer(decode_error="replace",vocabulary=features_file)


def checkIfAoK(act):
    
    converted_data = loaded_vec.fit_transform([act])
    transformer = TfidfTransformer()
    text = transformer.fit_transform(converted_data).toarray()
    y_pred = model.predict_proba(text)
        
    prob = y_pred[0][1]*100
    
    print("#### act:", act, " prob:", prob)
    
    return prob