import pandas
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
# Libraries for text preprocessing
import re
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
# nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.feature_extraction.text import TfidfTransformer
from openpyxl import load_workbook


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""

    # use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        # keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    # create a tuples of feature,score
    # results = zip(feature_vals,score_vals)
    results = {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]] = score_vals[idx]

    return results


# column text name
excel_file_name = 'actsOfKindness.xlsx'
# excel_file_name = input("What is the file path to the excelsheet?")

column_description = 'Description'
# column_description = input("What is the column's title that has the text?")
# column_count = 'count_word'

# load the dataset
dataset = pandas.read_excel(excel_file_name, sheet_name='AoKs_Stories')
# print(dataset.head())

# Fetch wordcount for each abstract
# dataset[column_count] = dataset[column_description].apply(lambda x: len(str(x).split(" ")))

# print(dataset[['Description','word_count']].head())

##Descriptive statistics of word counts
# print(dataset.word_count.describe())

# Identify common words
common = pandas.Series(' '.join(dataset[column_description]).split()).value_counts()[:20]
# print(common)

# Identify uncommon words
uncommon = pandas.Series(' '.join(dataset
                                  [column_description]).split()).value_counts()[-20:]
# print(uncommon)

lem = WordNetLemmatizer()
stem = PorterStemmer()

##Creating a list of stop words and adding custom stopwords
stop_words = set(stopwords.words("english"))

##Creating a list of custom stopwords
new_words = ["kind", "kindly", "randomactsofkindness", "act"]
stop_words = stop_words.union(new_words)

corpus = []
for i in range(0, len(dataset[column_description])):
    # Remove punctuations
    text = re.sub('[^a-zA-Z]', ' ', dataset[column_description][i])

    # Convert to lowercase
    text = text.lower()

    # remove tags
    text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)

    # remove special characters and digits
    text = re.sub("(\\d|\\W)+", " ", text)

    ##Convert to list from string
    text = text.split()

    ## Stemming
    ps = PorterStemmer()
    # Lemmatisation
    lem = WordNetLemmatizer()
    text = [lem.lemmatize(word) for word in text if not word in
                                                        stop_words]
    text = " ".join(text)
    corpus.append(text)

cv = CountVectorizer(max_df=0.8, stop_words=stop_words, max_features=10000, ngram_range=(1, 1))
X = cv.fit_transform(corpus)

tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
tfidf_transformer.fit(X)  # get feature names
feature_names = cv.get_feature_names()

# book = load_workbook('acts_keywords.xlsx')
# writer = pandas.ExcelWriter('acts_keywords.xlsx', engine='openpyxl')
# writer.book = book
# writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

## ExcelWriter for some reason uses writer.sheets to access the sheet.
## If you leave it empty it will not know that sheet Main is already there
## and will create a new sheet.


# df = pandas.DataFrame()
# df = pandas.DataFrame({'Description':['tst']})
fileName = "acts_keywords.txt"
f = open(fileName, 'w')
f.write("Description$Keywords" + '\n')
f.close()
f = open(fileName, 'a')

for i in range(0, len(corpus)):
    # fetch document for which keywords needs to be extracted
    doc = corpus[i]

    # generate tf-idf for the given document
    tf_idf_vector = tfidf_transformer.transform(cv.transform([doc]))

    # sort the tf-idf vectors by descending order of scores
    sorted_items = sort_coo(tf_idf_vector.tocoo())

    # extract only the top n; n here is 5
    keywords = extract_topn_from_vector(feature_names, sorted_items, 5)

    # now print the results
    print("\nAbstract:")
    print(doc)
    print("\nKeywords:")
    for k in keywords:
        print(k, keywords[k])

    f.write(doc + "$" + ', '.join(keywords.keys()) + '\n')

    # df1 = pandas.DataFrame({'Description':[', '.join(keywords.keys())]})
    # print(df1)
    # print("before")
    # print(df)
    # df.add(df1)
    # print('after')
    # print(df)
    # = pandas.DataFrame([[', '.join(keywords.keys())]], columns=['Description'])
    # df1.to_excel(writer)
    # writer.save()

f.close()
# print(keywords.keys())
# print(df)
# df.to_excel(writer)
# writer.save()


# df.to_excel(writer, sheet_name='new2')
#
# writer.save()
# writer.save()
