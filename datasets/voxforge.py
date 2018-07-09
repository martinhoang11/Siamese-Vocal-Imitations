from torch.utils.data import dataset

from datafiles.urban_sound_8k import UrbanSound8K
from datafiles.voxforge import Voxforge
from utils.utils import zip_shuffle


class All(dataset.Dataset):
    def __init__(self, data: Voxforge, shuffle=True):
        self.labels = data.labels
        self.unique_labels = data.unique_labels
        self.audio = data.audio

        if shuffle:
            self.labels, self.audio = zip_shuffle(self.labels, self.audio)

        self.by_label = dict({(u, []) for u in self.unique_labels})
        self.training = []
        self.validation = []

        examples_per_language = 8000
        n_train = int(.7 * examples_per_language)
        n_validate = int(.3 * examples_per_language)

        for unique_label in self.unique_labels:
            for audio, label in zip(self.audio, self.labels):
                if label == unique_label:
                    self.by_label[label].append([audio, label])

        for unique_label in self.unique_labels:
            language = self.by_label[unique_label]
            self.training += language[:n_train]
            self.validation += language[n_train:n_train + n_validate]

        self.validating = False

    def validation_mode(self):
        if self.validating:
            raise RuntimeWarning("Redundant switch to validation mode")
        self.validating = True

    def training_mode(self):
        if not self.validating:
            raise RuntimeWarning("Redundant switch to training mode")
        self.validating = False

    def __getitem__(self, index):
        if self.validating:
            return self.validation[index]
        else:
            return self.training[index]

    def __len__(self):
        if self.validating:
            return len(self.validation)
        else:
            return len(self.training)
