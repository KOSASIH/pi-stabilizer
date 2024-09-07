import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from hyperopt import hp, fmin, tpe, Trials
import matplotlib.pyplot as plt

class ARIMAModel:
    def __init__(self, data, order=None, seasonal_order=None):
        self.data = data
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.model_fit = None
        self.params = None

    def fit(self):
        if self.order is None:
            self.order = self._auto_arima()
        if self.seasonal_order is None:
            self.seasonal_order = self._auto_seasonal_arima()
        self.model = SARIMAX(self.data, order=self.order, seasonal_order=self.seasonal_order)
        self.model_fit = self.model.fit()

    def _auto_arima(self):
        def objective(params):
            order = params["order"]
            model = ARIMA(self.data, order=order)
            model_fit = model.fit()
            return model_fit.aic

        space = {
            "order": hp.quniform("order", 0, 5, 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        return tuple(best["order"])

    def _auto_seasonal_arima(self):
        def objective(params):
            seasonal_order = params["seasonal_order"]
            model = SARIMAX(self.data, order=self.order, seasonal_order=seasonal_order)
            model_fit = model.fit()
            return model_fit.aic

        space = {
            "seasonal_order": hp.quniform("seasonal_order", 0, 2, 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        return tuple(best["seasonal_order"])

    def forecast(self, steps):
        return self.model_fit.forecast(steps=steps)

    def evaluate(self, test_data):
        predictions = self.model_fit.predict(start=len(self.data), end=len(self.data)+len(test_data)-1)
        mse = mean_squared_error(test_data, predictions)
        rmse = np.sqrt(mse)
        return rmse

    def plot_residuals(self):
        residuals = self.model_fit.resid
        residuals.plot()
        plt.title("Residuals")
        plt.xlabel("Time")
        plt.ylabel("Residual")
        plt.show()

    def plot_forecast(self, steps):
        forecast = self.forecast(steps)
        plt.plot(self.data)
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
            self.order = params["order"]
            self.seasonal_order = params["seasonal_order"]
            self.fit()
            score = self.walk_forward_validation()
            return score

        space = {
            "order": hp.quniform("order", 0, 5, 1),
            "seasonal_order": hp.quniform("seasonal_order", 0, 2, 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        return best
