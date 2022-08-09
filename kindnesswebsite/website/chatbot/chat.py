from msilib.schema import tables
import random
import json
import torch
from model  import NeuralNet
from preprocessing import bag_of_words, tokenize


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('website/chatbot/intents.json', 'r') as f:
     intents = json.load(f)
     
     
FILE = 'website/chatbot/data.pth'

data = torch.load(FILE)


input_size = data['input_size']
hidden_size = data['hidden_size']
output_size = data['output_size']     

all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size=input_size, hidden_size=hidden_size, output_size=output_size)
model.load_state_dict(model_state)
model.eval()

bot_name = "Davi"

print("let's chat! type 'quit' to exit")

while True:
    sentence = input("You: ")
    
    if sentence == "quit":
        break
    
    tokenized_sentence = tokenize(sentence)
    x = bag_of_words(tokenized_sentence, all_words)
    x = x.reshape(1, x.shape[0]) # need to understand
    x = torch.from_numpy(x).to(device)
    
    output = model(x)
    
    _, predicted = torch.max(output, dim=1)
    
    tag = tags[predicted.item()]
    
    ## check prob
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                print(f'{bot_name}: {random.choice(intent["responses"])}')   
    else:
        print(f'{bot_name}: Sorry, I don\'t understand')   