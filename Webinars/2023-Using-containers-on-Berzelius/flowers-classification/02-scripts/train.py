import argparse
import glob
import os
import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn.metrics as skl_m
import datetime as dt

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim 
import torchvision
import torchvision.transforms as transforms
from torchvision import datasets, models, transforms

parser = argparse.ArgumentParser()
#parser.add_argument('--model', type=str, default="vgg16")
parser.add_argument('--epochs', type=int, default=2)
parser.add_argument('--lr', type=float, default=0.001)
parser.add_argument('--validate_steps', type=int, default=10)
parser.add_argument('--batch_size', type=int, default=64)
parser.add_argument('--n_cpu', type=int, default=0)

opt = parser.parse_args()

print(opt)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)

model_name = "vgg19"

model_path = os.path.join(os.getcwd(), f'models/{model_name}.pth')
#data_path = os.path.join( Path(os.getcwd()).parent.absolute(), 'data')
DATA_PATH = os.path.join( Path(os.getcwd()).parent.absolute(), 'data')

# Image transformations
train_data_transforms = transforms.Compose ([transforms.RandomRotation (30),
                                             transforms.RandomResizedCrop (224),
                                             transforms.RandomHorizontalFlip (),
                                             transforms.ToTensor (),
                                             transforms.Normalize ([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
                                            ])
valid_data_transforms = transforms.Compose ([transforms.Resize (256),
                                             transforms.CenterCrop (224),
                                             transforms.ToTensor (),
                                             transforms.Normalize ([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
                                            ])
test_data_transforms = transforms.Compose ([transforms.Resize (256),
                                             transforms.CenterCrop (224),
                                             transforms.ToTensor (),
                                             transforms.Normalize ([0.485, 0.456, 0.406],[0.229, 0.224, 0.225])
                                            ])

# Use previously downladed datasets
trainset = torchvision.datasets.Flowers102(root=DATA_PATH, split="train",
                                      download=True, transform=train_data_transforms)

valset = torchvision.datasets.Flowers102(root=DATA_PATH, split="val",
                                      download=True, transform=valid_data_transforms)

testset = torchvision.datasets.Flowers102(root=DATA_PATH, split="test",
                                      download=True, transform=test_data_transforms)

train_dataloader = torch.utils.data.DataLoader(trainset, batch_size = opt.batch_size, shuffle = True, num_workers = opt.n_cpu)
validation_dataloader = torch.utils.data.DataLoader(valset, batch_size = opt.batch_size, shuffle = True, num_workers = opt.n_cpu)
test_dataloader = torch.utils.data.DataLoader(testset, batch_size = opt.batch_size, shuffle = True, num_workers = opt.n_cpu)

print(f"Total number of images: {len(trainset)+len(valset)+len(testset)}")
print(f"Nr of images in the training set: {len(trainset)}")
print(f"Nr of images in the validation set: {len(valset)}")
print(f"Nr of images in the test set: {len(testset)}")
print("")

# The number of classes
class_num = 102

# The CNN model
# Downloading a pre-trained VGG16 model takes about 1 min
model = models.vgg19(weights="VGG19_Weights.DEFAULT")

# We need to set requires_grad = False to freeze the parameters so that the gradients are not computed in backward() on features layer
for param in model.features.parameters():
    param.requires_grad = False
    
# update the classifier layer
classifier = nn.Sequential(
          nn.Linear(in_features=25088, out_features=4096, bias=True),
          nn.ReLU(),
          nn.Dropout (p = 0.5),
          nn.Linear(in_features=4096, out_features=2048, bias=True),
          nn.ReLU(),
          nn.Dropout (p = 0.5),
          nn.Linear(in_features=2048, out_features=class_num, bias=True)
        )
model.classifier = classifier

# Begin training
# Use the available GPU or CPU device
model = torch.nn.DataParallel(model).to(device)

epochs = opt.epochs

training_losses = np.zeros(epochs)
training_metrics = np.zeros(epochs)
validation_losses = []
validation_metrics = []

best_model_state = None
best_model_metric = 100

print_every = opt.validate_steps
steps = 0
start = dt.datetime.now()

optimizer = torch.optim.AdamW(model.parameters(), lr=opt.lr)
criterion = nn.CrossEntropyLoss()

for e in range(epochs):
    print(f"On epoch {e+1}")

    running_loss = 0
    for ii, (inputs, labels) in enumerate(train_dataloader):
        steps += 1
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()

        output = model.forward(inputs)
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        if steps % print_every == 0:
            print(f"  Evaluating model on step {steps}")
            model.eval()
            v_lost = 0
            v_accuracy=0
            for ii, (inputs2,labels2) in enumerate(validation_dataloader):
                optimizer.zero_grad()
                inputs2, labels2 = inputs2.to(device) , labels2.to(device)
                model.to(device)
                with torch.no_grad():    
                    outputs = model.forward(inputs2)
                    v_lost = criterion(outputs,labels2)
                    ps = torch.exp(outputs).data
                    equality = (labels2.data == ps.max(1)[1])
                    v_accuracy += equality.type_as(torch.FloatTensor()).mean()

            v_lost = v_lost / len(validation_dataloader)
            v_accuracy = v_accuracy /len(validation_dataloader)

            if v_lost < best_model_metric:
                print("  Saving as best model")
                torch.save(model.state_dict(), model_path)
                best_model_metric = v_lost

            print("  Epoch: {}/{}... ".format(e+1, epochs),
                "Training Loss: {:.4f}".format(running_loss/print_every),
                "Validation Loss: {:.4f}".format(v_lost),
                "Validation Accuracy: {:.4f}".format(v_accuracy * 100))


            running_loss = 0

print(f"Training complete. Training duration {str(dt.datetime.now() - start)}")
print("\n")

# load best performing model
model.load_state_dict(torch.load(model_path))

if not os.path.isdir(f'output/{model_name}'):
    os.makedirs(f'output/{model_name}')

plt.figure()
plt.plot(np.linspace(1, epochs, len(training_losses)),
         training_losses,
         label='Training')
plt.plot(np.linspace(1, epochs, len(validation_losses)),
         validation_losses,
         label='Validation')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.savefig(f'output/{model_name}/model_losses.png')

plt.figure()
plt.plot(np.linspace(1, epochs, len(training_metrics)),
         training_metrics,
         label='Training')
plt.plot(np.linspace(1, epochs, len(validation_metrics)),
         validation_metrics,
         label='Validation')
plt.xlabel('Epochs')
plt.ylabel('MSE')
plt.legend()
plt.savefig(f'output/{model_name}/model_metrics.png')
