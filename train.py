import json
import numpy as np
from nltk_utils import tokenize, stem, bag_of_words
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet

# Load intents file
with open("data/intents.json", 'r') as f:
    intents = json.load(f)

all_words = []
tags = []
xy = []

# Tokenize and stem the words in patterns
for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

# Remove ignore words and stem the rest
ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))

X_train = []
Y_train = []

# Create bag of words and labels
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)
    label = tags.index(tag)
    Y_train.append(label)

X_train = np.array(X_train)
Y_train = np.array(Y_train)

# Define the dataset class
class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = Y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples

# Hyperparameters
batch_size = 8
hidden_size = 16  # Increased hidden size
output_size = len(tags)
input_size = len(X_train[0])
learning_rate = 0.001
num_epochs = 1000

# Create dataset and dataloader
dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, num_workers=0)  # Set num_workers=0 for Windows compatibility

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Training loop
for epoch in range(num_epochs):
    for words, labels in train_loader:
        words = words.to(device)
        labels = labels.to(device, dtype=torch.long)  # Ensure labels are of type LongTensor

        # Forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    if (epoch + 1) % 100 == 0:
        print(f'Epoch {epoch+1}/{num_epochs}, Loss={loss.item():.4f}')

print(f'Final Loss: Loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

FILE = "data/data.pth"
torch.save(data, FILE)

print(f'Training completed. File saved to {FILE}')
