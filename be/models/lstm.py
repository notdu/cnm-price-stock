from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Activation
import os
import numpy as np


class Lstm:
    def __init__(self, path, features=None, n_days=60, epochs=50):
        if not features:
            features = ['Close']

        self.path = path
        self.features = features
        self.n_days = n_days
        self.epochs = epochs

        if os.path.isfile(path):
            self.model = load_model(path)
        else:
            self.model = Sequential()
            self.model.add(LSTM(50, input_shape=(1, len(features)*n_days), return_sequences=True))
            self.model.add(LSTM(25))
            self.model.add(Dense(1))
            self.model.add(Activation('linear'))
            self.model.compile(loss='mean_squared_error', optimizer='adam')

    def fit(self, X: np.ndarray, Y):
        X = X.reshape((X.shape[0], 1, X.shape[1]))
        self.model.fit(X, Y, epochs=self.epochs)
        self.model.save(self.path)

    def predict(self, X: np.ndarray):
        X = X.reshape((X.shape[0], 1, X.shape[1]))
        return self.model.predict(X).reshape(-1, 1)
