import os
import pickle

import PySimpleGUI as sg

# ----- Full layout -----
import numpy as np

layout = [

    [
        sg.Text("Enter act:"),
        sg.In(size=(50, 10), enable_events=True, key="-ACT-"),
        sg.Button("Check", key="-CHECK-")
    ],
    [
        sg.Text("Is an AoK?", key="-RESULT-")
    ]
]

## load model
model = pickle.load(open('AoK_classifier_model.pkl', 'rb'))

features_file = pickle.load(open("AoK_features.pkl", "rb"))

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
loaded_vec = CountVectorizer(decode_error="replace",vocabulary=features_file)



window = sg.Window("AoK Predictor", layout)

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:

        break

    if event == "-CHECK-":
        X = [values["-ACT-"]]
        converted_data = loaded_vec.fit_transform(X)
        transformer = TfidfTransformer()
        X = transformer.fit_transform(converted_data).toarray()
        y_pred = model.predict(X)
        result = "".join(y_pred).upper()
        if result == "NO":
            window["-RESULT-"].update("Is an AoK? Not Really!")
        else:
            window["-RESULT-"].update("Is an AoK? Yep!")


window.close()