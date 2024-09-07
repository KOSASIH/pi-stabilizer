import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

class Forecasting:
    def __init__(self, data, order, seasonal_order):
        self.data = data
        self.order = order
        self.seasonal_order = seasonal_order

    def fit_arima(self):
        self.model = ARIMA(self.data, order=self.order)
        self.model_fit = self.model.fit(disp=0)

    def fit_sarimax(self):
        self.model = SARIMAX(self.data, order=self.order, seasonal_order=self.seasonal_order)
        self.model_fit = self.model.fit(disp=0)

    def forecast(self, steps):
        forecast = self.model_fit.forecast(steps=steps)
        return forecast

    def evaluate(self, test_data):
        predictions = self.model_fit.predict(start=len(self.data) - len(test_data), end=len(self.data) - 1)
        mse = mean_squared_error(test_data, predictions)
        rmse = np.sqrt(mse)
        return rmse

    def walk_forward_validation(self, test_size=0.2):
        tscv = TimeSeriesSplit(n_splits=5)
        scores = []
        for train_index, test_index in tscv.split(self.data):
            X_train, X_test = self.data[train_index], self.data[test_index]
            self.fit_arima()
            score = self.evaluate(X_test)
            scores.append(score)
        return scores

    def hyperparameter_tuning(self):
        def objective(params):
            order = params["order"]
            seasonal_order = params["seasonal_order"]
            self.order = order
            self.seasonal_order = seasonal_order
            self.fit_sarimax()
            score = self.walk_forward_validation()
            return score

        space = {
            "order": hp.quniform("order", 1, 5, 1),
            "seasonal_order": hp.quniform("seasonal_order", 1, 5, 1)
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        return best

    def plot_forecast(self, steps):
        forecast = self.forecast(steps)
        plt.plot(forecast)
        plt.title("Forecast")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()

    def plot_residuals(self):
        residuals = self.model_fit.resid
        plt.plot(residuals)
        plt.title("Residuals")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()

    def plot_diagnostics(self):
        self.model_fit.plot_diagnostics()
        plt.show()
