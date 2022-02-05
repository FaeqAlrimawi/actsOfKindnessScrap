import os
import pickle

import PySimpleGUI as sg

# ----- Full layout -----
import numpy as np

layout = [

    [
        sg.Text("Enter act:"),
        sg.InputText(size=(30, 1), enable_events=True, key="-ACT-"),
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

sg.theme("DarkBlue3")
# sg.set_options(font=("Courier New", 13))

window = sg.Window("Acts of Kindness Predictor", layout, finalize=True)
window['-ACT-'].bind("<Return>", "_Enter")

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:

        break

    elif event == "-CHECK-" or event == "-ACT-" + "_Enter":
        X = [values["-ACT-"]]
        converted_data = loaded_vec.fit_transform(X)
        transformer = TfidfTransformer()
        X = transformer.fit_transform(converted_data).toarray()
        y_pred = model.predict_proba(X)
        # result = "".join(y_pred).upper()
        yes_result = y_pred[0][1]
        lower_threshold = 0.4
        upper_threshold = 0.6

        if yes_result < lower_threshold:
            window["-RESULT-"].update("Is an AoK? Not Really! (Yes% " + str(y_pred[0][1]*100)+ "%)")
        elif yes_result >= lower_threshold and yes_result <= upper_threshold:
            window["-RESULT-"].update("Is an AoK? Hmmm maybe?! (Yes% " + str(y_pred[0][1] * 100) + "%)")
        else:
            window["-RESULT-"].update("Is an AoK? Yep! (Yes% " + str(y_pred[0][1]*100)+ "%)")


window.close()