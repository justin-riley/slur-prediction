from pandas import read_csv
from sklearn.preprocessing import OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from copy import deepcopy

class AutoEncoder:
    '''
    Deep Neural Network class that OneHotEncodes n-grams and returns
    pandas.core.series.Series of 3-tuples.
    '''
    def __init__(self):
        '''
        Initialize Autoencoder class as a sequential tensorflow.\
        keras.models.Sequential model
        '''
        self.model=Sequential()
        self.encoder=OneHotEncoder()
        self.data=None

    def _get_neuron_counts(self,n):
        out = []
        accumulator = 3
        while accumulator < n:
            out.append(accumulator)
            accumulator **= 2
        out = out[::-1]
        sub = deepcopy(out[:-1])
        out.extend(sub[::-1])
        return out

    def _build_network(self,n):
        self.model.add(Dense(n, input_dim=n, activation='relu')
        neuron_counts = self._get_neuron_counts(n)
        for counts in neuron_counts:
            if counts == 3:
                self.model.add(Dense(counts,activation='linear',
                                        name='bottleneck'))
            else:
                self.model.add(Dense(counts,activation='relu'))
        self.model.add(Dense(n,activation='softmax'))

    def encode(self,series):
        
