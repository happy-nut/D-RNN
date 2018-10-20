import os

import torch
import torch.utils.data as data
from torchvision import datasets, transforms
from gensim.models import KeyedVectors

from datasets import Imdb


class BaseData(object):
    """ Base class of the data model.
    """

    def __init__(self):
        self.cuda = torch.cuda.is_available()


class MNIST(BaseData):
    root = 'data/mnist'

    def __init__(self, batch_size):
        BaseData.__init__(self)
        self.batch_size = batch_size

    def load(self, is_eval):
        additional_options = {'num_workers': 1, 'pin_memory': True} if self.cuda else {}
        return torch.utils.data.DataLoader(
            datasets.MNIST(root=self.root,
                           train=not is_eval,
                           download=True,
                           transform=transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))
                           ])),
            batch_size=self.batch_size,
            shuffle=True,
            **additional_options)

    def eval_data(self):
        return self.load(True)

    def train_data(self):
        return self.load(False)


class ACLIMDB(BaseData):
    # root = 'data/aclImdb/'
    root = os.path.join('data', 'aclImdb')
    data = None

    def __init__(self, batch_size, word_embedding, is_eval, test_mode):
        BaseData.__init__(self)
        self.batch_size = batch_size
        self.word_embedding = word_embedding
        self.is_eval = is_eval
        self.data = Imdb(
            root=self.root,
            word_embedding=self.word_embedding,
            train=not self.is_eval,
            test_mode=test_mode)

    def load(self):
        additional_options = {'num_workers': 0, 'pin_memory': True} if self.cuda else {}
        # TODO(hyungsun): make this class adapt word embedding dynamically.
        return torch.utils.data.DataLoader(self.data, batch_size=self.batch_size, shuffle=True, **additional_options)


if __name__ == "__main__":
    # TODO(hyungsun): Remove these after debugging.
    batch_size = 3
    loader = ACLIMDB(batch_size, 'CBOW', False, True).load()

    for batch_idx, (data, target) in enumerate(loader):
        if batch_idx > 100:
            break
        print('batch index:', batch_idx)
        # data = torch.FloatTensor(data)
        print('num of words:', len(data))
        print('score:', target)
        for datum in data:
            # datum = torch.FloatTensor(datum)
            print('data(word index):', datum)
        print('-' * 20)

