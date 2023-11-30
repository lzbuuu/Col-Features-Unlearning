import numpy as np
import scipy.sparse as sp
import pickle as pkl
from sklearn.preprocessing import normalize

import torch.utils.data as data
import torch
from sklearn.preprocessing import StandardScaler

D = 2 ** 13  # number of weights use for learning
BATCH_SIZE = 500  # Criteo batch_size
MAX_TRAINSET_SIZE = 20000


class Adult(data.Dataset):
    def __init__(self, dataset, feature_ids, train=True, batch_size=BATCH_SIZE):
        x = dataset.iloc[:, :-1].iloc[:, feature_ids]
        y = dataset.iloc[:, -1]
        self.total_features = dataset.columns[:-1]
        self.client_features = feature_ids
        self.batch_size = batch_size
        sc = StandardScaler()
        x = sc.fit_transform(x)
        x = np.array(x)
        self.data = x
        self.targets = y
        self.train = train

    def __len__(self):
        if len(self.targets) % self.batch_size == 0:
            return int(len(self.targets) / self.batch_size)
        else:
            return int(len(self.targets) / self.batch_size) + 1

    def __getitem__(self, index):
        assert -len(self) < index < len(self), 'list index out of range'
        if index < 0:
            index = len(self) - index
        start = index * self.batch_size
        stop = (index + 1) * self.batch_size
        length = len(self.targets)
        if stop <= length:
            data, label = self.data[start:stop], self.targets[start:stop]
        else:
            stop = -1
            data, label = self.data[start:stop], self.targets[start:stop]
        data = torch.tensor(data, dtype=torch.float32)
        label = torch.tensor(list(label), dtype=torch.long)
        assert -len(self) < index < len(self), 'list index out of range'
        return data, label