from torch import nn
from collections import OrderedDict

class ConvolutionalClassification(nn.Module):
    def __init__(self, class_count):
        super(ConvolutionalClassification, self).__init__()
        self.avg_pool = nn.Sequential(
            nn.AdaptiveAvgPool3d((class_count,1,1)),
            nn.Flatten(start_dim=1)
        )
    def forward(self, x):
        x = self.avg_pool(x)
        return x

    
class ResidualBlock(nn.Module):
    def __init__(self, layer_count, channel_num, filter_size=3):
        super(ResidualBlock, self).__init__()
        
        conv_list = []
        for i in range(layer_count):
            conv_list.append((f'conv{i}', nn.Conv2d(channel_num, channel_num, filter_size, padding=1)))
            conv_list.append((f'relu{i}', nn.ReLU()))
            
        self.conv = nn.Sequential(OrderedDict(conv_list))
        self.relu = nn.ReLU()
        
    def forward(self, x):
        residual = x
        x = self.conv(x)
        x = x + residual
        out = self.relu(x)
        return out

    
class ConvNeuralNetwork(nn.Module):
    def __init__(self):
        super(ConvNeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.conv_network = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=8, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.Dropout(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU()
        )

        self.fc = nn.Linear(in_features=12800*2, out_features=2)

    def forward(self, x):
        x = self.conv_network(x)
        x = x.view(-1, 12800*2)
        x = self.fc(x)
        return x

    
class ResConvNeuralNetwork(nn.Module):
    def __init__(self):
        super(ResConvNeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.conv_network = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=8, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.Dropout(),            
            ResidualBlock(layer_count=3, channel_num=8),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=8),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=8),
            
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=16),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=16),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=16),
            
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2)),
            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=32),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=32),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=32),
            
            nn.Dropout(),
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=(3, 3),
                      stride=(1, 1), padding=(1, 1)),
            nn.ReLU(),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=64),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=64),
            nn.Dropout(),
            ResidualBlock(layer_count=3, channel_num=64),
        )
        
        self.classification = ConvolutionalClassification(2)
    def forward(self, x):
        x = self.conv_network(x)
        x = self.classification(x)
        return x
