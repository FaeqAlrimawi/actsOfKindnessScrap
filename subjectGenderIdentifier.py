import spacy
import random
from nltk.corpus import names
from nltk import NaiveBayesClassifier
import pandas as pd


def gender_features(word):
    return {'last_letter': word[-1]}


# train gender identification model
# Read the names from the files.
# Label each name with the corresponding gender.
male_names = [(name, 'male') for name in names.words('male.txt')]
female_names = [(name, 'female') for name in names.words('female.txt')]

# Combine the lists.
labeled_names = male_names + female_names

# Shuffle the list.
random.shuffle(labeled_names)

# Extract the features using the `gender_features()` function.
featuresets = [(gender_features(n), gender) for (n, gender) in labeled_names]

# Split the dataset into train and test set.
train_set, test_set = featuresets[500:], featuresets[:500]

# Train a Naive Bayes classifier
classifier = NaiveBayesClassifier.train(train_set)

### find PoS
file_name = 'actsOfKindness.xlsx'
sheet_name = 'AoKs_Stories'
description_column = 'Description'
classifier_column = 'Tech'
start_index = 0
end_index = 10

# df_train= pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column, classifier_column])[:170]
df_test = pd.read_excel(file_name, sheet_name=sheet_name, usecols=[description_column])[start_index:end_index]

# movie_data = load_files(r"D:\txt_sentoken")
X = df_test[description_column]

nlp = spacy.load("en_core_web_sm")

for sent in X:
    print("processing: ", sent)
    # sent = "I shot an elephant, and james went to school"
    doc = nlp(sent)
    sub_toks = [tok for tok in doc if (tok.dep_ == "nsubj")]

    print("subjects: ", sub_toks)

    ### do the gender identification of subjects
    for subject in sub_toks:
        neo_gender = classifier.classify(gender_features(str(subject)))
        print(subject, " is most probably a {}.".format(neo_gender))
