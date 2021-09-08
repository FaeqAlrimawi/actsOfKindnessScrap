import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dense, Dropout, SpatialDropout1D
from tensorflow.keras.layers import Embedding
import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

# read excel sheet
df = pd.read_excel("actsOfKindess.xlsx")

# get title and description
review_df = df[['Title', 'Description', 'Class']]
# print(review_df)

# convert class into a numerical code (e..g, 'kind' to 0)
sentiment_label = review_df.Class.factorize()

# print(sentiment_label)

# get the description
act_description = review_df.Description.values

# print(act_description)


tokenizer = Tokenizer(num_words=5000)

tokenizer.fit_on_texts(act_description)

encoded_docs = tokenizer.texts_to_sequences(act_description)

padded_sequence = pad_sequences(encoded_docs, maxlen=1000)

## model builder
embedding_vector_length = 128
vocab_size = 100
model = Sequential()
model.add(Embedding(vocab_size, embedding_vector_length, input_length=1000))
model.add(SpatialDropout1D(0.25))
model.add(LSTM(50, dropout=0.5, recurrent_dropout=0.5))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam', metrics=['accuracy'])

# print(model.summary())



## train model
history = model.fit(padded_sequence,sentiment_label[0],validation_split=0.2, epochs=8, batch_size=32)

# print(history)