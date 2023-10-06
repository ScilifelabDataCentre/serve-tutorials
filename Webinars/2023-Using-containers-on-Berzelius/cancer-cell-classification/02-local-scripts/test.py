import argparse
import os
from datasets import OralCancerImageDataset
from models import ConvNeuralNetwork
from transforms import DiscreteRotationTransform

import pandas as pd
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import transforms

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str, required=True)
parser.add_argument('--batch_size', type=int, default=32)
parser.add_argument('--n_cpu', type=int, default=0)

opt = parser.parse_args()

print(opt)

model_path = os.path.join(os.getcwd(), f'models/{opt.model}.pth')
data_path = os.path.join(os.getcwd(), 'data')
test_dir = os.path.join(data_path, 'test')
output_dir = f'output/{opt.model}'

if not os.path.isfile(model_path):
    raise FileNotFoundError(f'Model {opt.model} does not exist.')

train_transform = transforms.Compose([
    DiscreteRotationTransform(angles=[-90, 90, 180]),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip()
])

test_dataset = OralCancerImageDataset(img_dir=test_dir)
test_dataloader = DataLoader(test_dataset, batch_size=opt.batch_size,
                             shuffle=False, num_workers=opt.n_cpu)

model = ConvNeuralNetwork().to('cuda')
model.load_state_dict(torch.load(model_path))

model.eval()
all_y_pred = []
all_y_names = []

print('Predicting.')

for batch in test_dataloader:
    X = batch['image'].to('cuda')
    names = batch['label']

    prediction = model(X)
    y_pred = nn.Softmax(dim=1)(prediction)[:, 1]
    all_y_pred += y_pred.tolist()
    all_y_names += names

print('Done.')

prediction_output = pd.DataFrame({'Name': all_y_names,
                                  'Diagnosis': all_y_pred})

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

prediction_output.to_csv(f'{output_dir}/test_prediction.csv', index=False)
