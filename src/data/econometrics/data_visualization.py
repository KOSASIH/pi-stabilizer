import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

class DataVisualization:
    def __init__(self, data):
        self.data = data

    def plot_time_series(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data)
        plt.title("Time Series Plot")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.show()

    def plot_autocorrelation(self):
        plot_acf(self.data)
        plt.title("Autocorrelation Plot")
        plt.show()

    def plot_partial_autocorrelation(self):
        plot_pacf(self.data)
        plt.title("Partial Autocorrelation Plot")
        plt.show()

    def plot_seasonal_decomposition(self):
        decomposition = seasonal_decompose(self.data, model='additive')
        trend = decomposition.trend
        seasonal = decomposition.seasonal
        residual = decomposition.resid
        plt.figure(figsize=(12, 6))
        plt.subplot(411)
        plt.plot(self.data, label='Original')
        plt.legend(loc='best')
        plt.subplot(412)
        plt.plot(trend, label='Trend')
        plt.legend(loc='best')
        plt.subplot(413)
        plt.plot(seasonal, label='Seasonality')
        plt.legend(loc='best')
        plt.subplot(414)
        plt.plot(residual, label='Residuals')
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

    def plot_distribution(self):
        sns.distplot(self.data)
        plt.title("Distribution Plot")
        plt.show()

    def test_stationarity(self):
        result = adfuller(self.data)
        print("ADF Statistic: %f" % result[0])
        print("p-value: %f" % result[1])
        if result[1] < 0.05:
            print("Reject null hypothesis: The time series is likely stationary")
        else:
            print("Fail to reject null hypothesis: The time series is likely non-stationary")

    def visualize(self):
        self.plot_time_series()
        self.plot_autocorrelation()
        self.plot_partial_autocorrelation()
        self.plot_seasonal_decomposition()
        self.plot_distribution()
        self.test_stationarity()
