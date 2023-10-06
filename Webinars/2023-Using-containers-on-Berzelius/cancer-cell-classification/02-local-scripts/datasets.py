import os

import pandas as pd
from torch.utils.data import Dataset
from torchvision.io import read_image


class OralCancerImageDataset(Dataset):
    def __init__(self, img_dir, labels_file=None, transform=None,
                 target_transform=None, indices=None):
        self.img_dir = img_dir
        self.labels = pd.read_csv(labels_file) if labels_file else None
        self.transform = transform
        self.target_transform = target_transform
        self.indices = indices

    def __len__(self):
        if self.indices is not None:
            return len(self.indices)

        if self.labels is not None:
            return len(self.labels)

        return len([name for name in os.listdir(self.img_dir)
                    if os.path.isfile(os.path.join(self.img_dir, name))])

    def __getitem__(self, index):
        if self.indices is not None:
            index = self.indices[index]
        if self.labels is not None:
            img_path = os.path.join(self.img_dir,
                                    f'{self.labels.iloc[index, 0]}.jpg')
            label = self.labels.iloc[index, 1]
        else:
            img_path = img_path = os.path.join(self.img_dir,
                                    f'cell_{index}.jpg')
            label = f'cell_{index}'

        image = (read_image(img_path)/255.0)

        if self.transform:
            image = self.transform(image)

        if self.target_transform:
            label = self.target_transform(label)

        sample = {'image': image, 'label': label}

        return sample
