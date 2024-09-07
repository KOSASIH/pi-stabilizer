import pandas as pd
import numpy as np
from fbprophet import Prophet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from hyperopt import hp, fmin, tpe, Trials
import matplotlib.pyplot as plt

class ProphetModel:
    def __init__(self, data, seasonality_mode='additive', growth='linear'):
        self.data = data
        self.seasonality_mode = seasonality_mode
        self.growth = growth
        self.model = None
        self.model_fit = None
        self.params = None

    def fit(self):
        self.model = Prophet(seasonality_mode=self.seasonality_mode, growth=self.growth)
        self.model.fit(self.data)

    def _auto_seasonality_mode(self):
        def objective(params):
            seasonality_mode = params["seasonality_mode"]
            model = Prophet(seasonality_mode=seasonality_mode, growth=self.growth)
            model.fit(self.data)
            return model.rsquare()

        space = {
            "seasonality_mode": hp.choice("seasonality_mode", ['additive', 'multiplicative'])
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return best["seasonality_mode"]

    def _auto_growth(self):
        def objective(params):
            growth = params["growth"]
            model = Prophet(seasonality_mode=self.seasonality_mode, growth=growth)
            model.fit(self.data)
            return model.rsquare()

        space = {
            "growth": hp.choice("growth", ['linear', 'logistic'])
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=10, trials=trials)
        return best["growth"]

    def forecast(self, steps):
        future = self.model.make_future_dataframe(periods=steps)
        forecast = self.model.predict(future)
        return forecast

    def evaluate(self, test_data):
        predictions = self.model.predict(test_data)
        mse = mean_squared_error(test_data['y'], predictions['yhat'])
        rmse = np.sqrt(mse)
        return rmse

    def plot_forecast(self, steps):
        forecast = self.forecast(steps)
        self.model.plot(forecast)
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
            self.seasonality_mode = params["seasonality_mode"]
            self.growth = params["growth"]
            self.fit()
            score = self.walk_forward_validation()
            return score

        space = {
            "seasonality_mode": hp.choice("seasonality_mode", ['additive', 'multiplicative']),
            "growth": hp.choice("growth", ['linear', 'logistic'])
        }
        trials = Trials()
        best = fmin(objective, space, algo=tpe.suggest, max_evals=50, trials=trials)
        return best
