import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from hyperopt import hp, fmin, tpe, Trials
import matplotlib.pyplot as plt

class LSTMModel:
    def __init__(self, data, n_features, n_steps, n_epochs, batch_size, optimizer):
        self.data = data
        self.n_features = n_features
        self.n_steps = n_steps
        self.n_epochs = n_epochs
        self.batch_size = batch_size
        self.optimizer = optimizer
        self.model = None
        self.model_fit = None
        self.params = None

    def fit(self):
        self.model = Sequential()
        self.model.add(LSTM(50, input_shape=(self.n_steps, self.n_features)))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer=self.optimizer)
        self.model_fit = self.model.fit(self.data, epochs=self.n_epochs, batch_size=self.batch_size, verbose=0)

    def _auto_n_features(self):
        def objective(params):
            n_features = params["n_features"]
            model = LSTMModel(self.data[:, :n_features], n_features, self.n_steps, self.n_epochs, self.batch_size, self.optimizer)
            model.fit()
            return model.model_fit.history['loss'][-1]

        space = {
            "n_features": hp.quniform("n_features", 1, self.data.shape[1], 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return int(best["n_features"])

    def _auto_n_steps(self):
        def objective(params):
            n_steps = params["n_steps"]
            model = LSTMModel(self.data[:, :, :self.n_features], self.n_features, n_steps, self.n_epochs, self.batch_size, self.optimizer)
            model.fit()
            return model.model_fit.history['loss'][-1]

        space = {
            "n_steps": hp.quniform("n_steps", 1, self.data.shape[1], 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return int(best["n_steps"])

    def _auto_n_epochs(self):
        def objective(params):
            n_epochs = params["n_epochs"]
            model = LSTMModel(self.data[:, :, :self.n_features], self.n_features, self.n_steps, n_epochs, self.batch_size, self.optimizer)
            model.fit()
            return model.model_fit.history['loss'][-1]

        space = {
            "n_epochs": hp.quniform("n_epochs", 1, 100, 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return int(best["n_epochs"])

    def _auto_batch_size(self):
        def objective(params):
            batch_size = params["batch_size"]
            model = LSTMModel(self.data[:, :, :self.n_features], self.n_features, self.n_steps, self.n_epochs, batch_size, self.optimizer)
            model.fit()
            return model.model_fit.history['loss'][-1]

        space = {
            "batch_size": hp.quniform("batch_size", 1, 128, 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return int(best["batch_size"])

    def _auto_optimizer(self):
        def objective(params):
            optimizer = params["optimizer"]
            model = LSTMModel(self.data[:, :, :self.n_features], self.n_features, self.n_steps, self.n_epochs, self.batch_size, optimizer)
            model.fit()
            return model.model_fit.history['loss'][-1]

        space = {
            "optimizer": hp.choice("optimizer", ['adam', 'rmsprop', 'sgd'])
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return best["optimizer"]

    def forecast(self, steps):
        forecast = self.model.predict(steps)
        return forecast

    def evaluate(self, test_data):
        predictions = self.model.predict(test_data)
        mse = mean_squared_error(test_data, predictions)
        rmse = np.sqrt(mse)
        return rmse

    def plot_forecast(self, steps):
        forecast = self.forecast(steps)
        plt.plot(forecast)
        plt.title("Forecast")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()

    def walk_forward_validation(self, test_size=0.2):
        tscv = TimeSeriesSplit(n_splits=5)
        scores = []
        for train_index, test_index in tscv.split(self.data):
            X_train, X_test = self.data[train_index], self.data[test_index]
            self.fit()
            score = self.evaluate(X_test)
            scores.append(score)
        return scores

    def hyperparameter_tuning(self):
        def objective(params):
            self.n_features = params["n_features"]
            self.n_steps = params["n_steps"]
            self.n_epochs = params["n_epochs"]
            self.batch_size = params["batch_size"]
            self.optimizer = params["optimizer"]
            self.fit()
            score = self.walk_forward_validation()
            return score

        space = {
            "n_features": hp.quniform("n_features", 1, self.data.shape[1], 1),
            "n_steps": hp.quniform("n_steps", 1, self.data.shape[1], 1),
            "n_epochs": hp.quniform("n_epochs", 1, 100, 1),
            "batch_size": hp.quniform("batch_size", 1, 128, 1),
            "optimizer": hp.choice("optimizer", ['adam', 'rmsprop', 'sgd'])
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        return best
