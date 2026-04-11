---
source_type: web
title: "How to Make Out-of-Sample Forecasts with ARIMA in Python"
author:
  - 
  - "[[Jason Brownlee]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
created: 2026-04-06
description: "Making out-of-sample forecasts can be confusing when getting started with time series data. The statsmodels Python API provides functions for performing one-step and multi-step out-of-sample forecasts. In this tutorial, you will clear up any confusion you have about making out-of-sample forecasts with time series data in Python. After completing this tutorial, you will know: How […]"
tags:
  - 
  - "clippings"
source_url: "https://machinelearningmastery.com/make-sample-forecasts-arima-python/"
published_at: 2017-03-24
related_concepts: []
---

Making out-of-sample forecasts can be confusing when getting started with time series data.

The statsmodels Python API provides functions for performing one-step and multi-step out-of-sample forecasts.

In this tutorial, you will clear up any confusion you have about making out-of-sample forecasts with time series data in Python.

After completing this tutorial, you will know:

- How to make a one-step out-of-sample forecast.
- How to make a multi-step out-of-sample forecast.
- The difference between the *forecast()* and *predict()* functions.

**Kick-start your project** with my new book [Time Series Forecasting With Python](https://machinelearningmastery.com/introduction-to-time-series-forecasting-with-python/), including *step-by-step tutorials* and the *Python source code* files for all examples.

Let’s get started.

- **Updated Apr/2019**: Updated the link to dataset.
- **Updated Aug/2019**: Updated data loading to use new API.
- **Updated Oct/2020**: Updated file loading for changes to the API.
- **Updated Dec/2020**: Updated ARIMA API to the latest version of statsmodels.
- **Updated Dec/2020**: Fixed out of sample examples due to API changes.
![[How-to-Make-Out-of-Sample-Forecasts-with-ARIMA-in-Python.jpg|How to Make Out-of-Sample Forecasts with ARIMA in Python]]

How to Make Out-of-Sample Forecasts with ARIMA in Python  
Photo by [dziambel](https://www.flickr.com/photos/141999355@N08/32706989645/), some rights reserved.

## Tutorial Overview

This tutorial is broken down into the following 5 steps:

1. Dataset Description
2. Split Dataset
3. Develop Model
4. One-Step Out-of-Sample Forecast
5. Multi-Step Out-of-Sample Forecast

### Stop learning Time Series Forecasting the slow way!

Take my free 7-day email course and discover how to get started (with sample code).

Click to sign-up and also get a free PDF Ebook version of the course.

## 1\. Minimum Daily Temperatures Dataset

This dataset describes the minimum daily temperatures over 10 years (1981-1990) in the city of Melbourne, Australia.

The units are in degrees Celsius and there are 3,650 observations. The source of the data is credited as the Australian Bureau of Meteorology.

- [Download the dataset](https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv)

Download the Minimum Daily Temperatures dataset to your current working directory with the filename “ *daily-minimum-temperatures.csv”*.

The example below loads the dataset as a Pandas Series.

| 1  2  3  4  5  6  7  8  9  10 | \# line plot of time series  from pandas import read\_csv  from matplotlib import pyplot  \# load dataset  \# display first few rows  print(series.head(20))  \# line plot of dataset  series.plot()  pyplot.show() |
| --- | --- |

Running the example prints the first 20 rows of the loaded dataset.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21 | Date  1981-01-01 20.7  1981-01-02 17.9  1981-01-03 18.8  1981-01-04 14.6  1981-01-05 15.8  1981-01-06 15.8  1981-01-07 15.8  1981-01-08 17.4  1981-01-09 21.8  1981-01-10 20.0  1981-01-11 16.2  1981-01-12 13.3  1981-01-13 16.7  1981-01-14 21.5  1981-01-15 25.0  1981-01-16 20.7  1981-01-17 20.6  1981-01-18 24.8  1981-01-19 17.7  1981-01-20 15.5 |
| --- | --- |

A line plot of the time series is also created.

![[Minimum-Daily-Temperatures-Dataset-Line-Plot.png|Minimum Daily Temperatures Dataset Line Plot]]

Minimum Daily Temperatures Dataset Line Plot

## 2\. Split Dataset

We can split the dataset into two parts.

The first part is the training dataset that we will use to prepare an ARIMA model. The second part is the test dataset that we will pretend is not available. It is these time steps that we will treat as out of sample.

The dataset contains data from January 1st 1981 to December 31st 1990.

We will hold back the last 7 days of the dataset from December 1990 as the test dataset and treat those time steps as out of sample.

Specifically 1990-12-25 to 1990-12-31:

| 1  2  3  4  5  6  7 | 1990-12-25,12.9  1990-12-26,14.6  1990-12-27,14.0  1990-12-28,13.6  1990-12-29,13.5  1990-12-30,15.7  1990-12-31,13.0 |
| --- | --- |

The code below will load the dataset, split it into the training and validation datasets, and save them to files *dataset.csv* and *validation.csv* respectively.

| 1  2  3  4  5  6  7  8 | \# split the dataset  from pandas import read\_csv  split\_point = len(series) - 7  dataset, validation = series\[0:split\_point\], series\[split\_point:\]  print('Dataset %d, Validation %d' % (len(dataset), len(validation)))  dataset.to\_csv('dataset.csv', index=False)  validation.to\_csv('validation.csv', index=False) |
| --- | --- |

Run the example and you should now have two files to work with.

The last observation in the dataset.csv is Christmas Eve 1990:

| 1 | 1990-12-24,10.0 |
| --- | --- |

That means Christmas Day 1990 and onwards are out-of-sample time steps for a model trained on *dataset.csv*.

## 3\. Develop Model

In this section, we are going to make the data stationary and develop a simple ARIMA model.

The data has a strong seasonal component. We can neutralize this and make the data stationary by taking the seasonal difference. That is, we can take the observation for a day and subtract the observation from the same day one year ago.

This will result in a stationary dataset from which we can fit a model.

| 1  2  3  4  5  6  7 | \# create a differenced series  def difference(dataset, interval=1):  diff = list()  for i in range(interval, len(dataset)):  value = dataset\[i\] - dataset\[i - interval\]  diff.append(value)  return numpy.array(diff) |
| --- | --- |

We can invert this operation by adding the value of the observation one year ago. We will need to do this to any forecasts made by a model trained on the seasonally adjusted data.

| 1  2  3 | \# invert differenced value  def inverse\_difference(history, yhat, interval=1):  return yhat + history\[-interval\] |
| --- | --- |

We can fit an ARIMA model.

Fitting a strong ARIMA model to the data is not the focus of this post, so rather than going through the analysis of the problem or [grid searching parameters](https://machinelearningmastery.com/grid-search-arima-hyperparameters-with-python/), I will choose a simple ARIMA(7,0,7) configuration.

We can put all of this together as follows:

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23 | from pandas import read\_csv  from statsmodels.tsa.arima.model import ARIMA  import numpy  \# create a differenced series  def difference(dataset, interval=1):  diff = list()  for i in range(interval, len(dataset)):  value = dataset\[i\] - dataset\[i - interval\]  diff.append(value)  return numpy.array(diff)  \# load dataset  \# seasonal difference  X = series.values  days\_in\_year = 365  differenced = difference(X, days\_in\_year)  \# fit model  model = ARIMA(differenced, order=(7,0,1))  model\_fit = model.fit()  \# print summary of fit model  print(model\_fit.summary()) |
| --- | --- |

Running the example loads the dataset, takes the seasonal difference, then fits an ARIMA(7,0,7) model and prints the summary of the fit model.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28 | SARIMAX Results  \==============================================================================  Dep. Variable: y No. Observations: 3278  Model: ARIMA(7, 0, 1) Log Likelihood -8673.748  Date: Mon, 28 Dec 2020 AIC 17367.497  Time: 08:12:26 BIC 17428.447  Sample: 0 HQIC 17389.322  \- 3278  Covariance Type: opg  \==============================================================================  coef std err z P>\|z\| \[0.025 0.975\]  \------------------------------------------------------------------------------  const 0.0127 0.133 0.096 0.924 -0.247 0.273  ar.L1 1.1428 0.316 3.620 0.000 0.524 1.762  ar.L2 -0.4348 0.169 -2.577 0.010 -0.766 -0.104  ar.L3 0.0961 0.044 2.172 0.030 0.009 0.183  ar.L4 0.0125 0.029 0.425 0.671 -0.045 0.070  ar.L5 -0.0101 0.029 -0.352 0.725 -0.066 0.046  ar.L6 0.0119 0.026 0.464 0.643 -0.038 0.062  ar.L7 0.0088 0.025 0.356 0.722 -0.040 0.057  ma.L1 -0.6161 0.315 -1.955 0.051 -1.234 0.002  sigma2 11.6360 0.282 41.296 0.000 11.084 12.188  \===================================================================================  Ljung-Box (L1) (Q): 0.00 Jarque-Bera (JB): 1.40  Prob(Q): 1.00 Prob(JB): 0.50  Heteroskedasticity (H): 0.84 Skew: -0.02  Prob(H) (two-sided): 0.00 Kurtosis: 3.10  \=================================================================================== |
| --- | --- | --- | --- |

We are now ready to explore making out-of-sample forecasts with the model.

## 4\. One-Step Out-of-Sample Forecast

ARIMA models are great for one-step forecasts.

A one-step forecast is a forecast of the very next time step in the sequence from the available data used to fit the model.

In this case, we are interested in a one-step forecast of Christmas Day 1990:

| 1 | 1990-12-25 |
| --- | --- |

### Forecast Function

The statsmodel ARIMAResults object provides a *forecast()* function for making predictions.

By default, this function makes a single step out-of-sample forecast. As such, we can call it directly and make our forecast. The result of the *forecast()* function is an array containing the forecast value, the standard error of the forecast, and the confidence interval information. Now, we are only interested in the first element of this forecast, as follows.

| 1  2 | \# one-step out-of sample forecast  forecast = model\_fit.forecast()\[0\] |
| --- | --- |

Once made, we can invert the seasonal difference and convert the value back into the original scale.

| 1  2 | \# invert the differenced forecast to something usable  forecast = inverse\_difference(X, forecast, days\_in\_year) |
| --- | --- |

The complete example is listed below:

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30 | from pandas import read\_csv  from statsmodels.tsa.arima.model import ARIMA  import numpy  \# create a differenced series  def difference(dataset, interval=1):  diff = list()  for i in range(interval, len(dataset)):  value = dataset\[i\] - dataset\[i - interval\]  diff.append(value)  return numpy.array(diff)  \# invert differenced value  def inverse\_difference(history, yhat, interval=1):  return yhat + history\[-interval\]  \# load dataset  \# seasonal difference  X = series.values  days\_in\_year = 365  differenced = difference(X, days\_in\_year)  \# fit model  model = ARIMA(differenced, order=(7,0,1))  model\_fit = model.fit()  \# one-step out-of sample forecast  forecast = model\_fit.forecast()\[0\]  \# invert the differenced forecast to something usable  forecast = inverse\_difference(X, forecast, days\_in\_year)  print('Forecast: %f' % forecast) |
| --- | --- |

Running the example prints 14.8 degrees, which is close to the expected 12.9 degrees in the *validation.csv* file.

| 1 | Forecast: 14.861669 |
| --- | --- |

### Predict Function

The statsmodel ARIMAResults object also provides a *predict()* function for making forecasts.

The predict function can be used to predict arbitrary in-sample and out-of-sample time steps, including the next out-of-sample forecast time step.

The predict function requires a start and an end to be specified, these can be the indexes of the time steps relative to the beginning of the training data used to fit the model, for example:

| 1  2  3  4 | \# one-step out of sample forecast  start\_index = len(differenced)  end\_index = len(differenced)  forecast = model\_fit.predict(start=start\_index, end=end\_index) |
| --- | --- |

The start and end can also be a datetime string or a “datetime” type; for example:

| 1  2  3 | start\_index = '1990-12-25'  end\_index = '1990-12-25'  forecast = model\_fit.predict(start=start\_index, end=end\_index) |
| --- | --- |

and

| 1  2  3  4 | from pandas import datetime  start\_index = datetime(1990, 12, 25)  end\_index = datetime(1990, 12, 26)  forecast = model\_fit.predict(start=start\_index, end=end\_index) |
| --- | --- |

Using anything other than the time step indexes results in an error on my system, as follows:

| 1 | AttributeError: 'NoneType' object has no attribute 'get\_loc' |
| --- | --- |

Perhaps you will have more luck; for now, I am sticking with the time step indexes.

The complete example is listed below:

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33 | from pandas import read\_csv  from statsmodels.tsa.arima.model import ARIMA  import numpy  from pandas import datetime  \# create a differenced series  def difference(dataset, interval=1):  diff = list()  for i in range(interval, len(dataset)):  value = dataset\[i\] - dataset\[i - interval\]  diff.append(value)  return numpy.array(diff)  \# invert differenced value  def inverse\_difference(history, yhat, interval=1):  return yhat + history\[-interval\]  \# load dataset  \# seasonal difference  X = series.values  days\_in\_year = 365  differenced = difference(X, days\_in\_year)  \# fit model  model = ARIMA(differenced, order=(7,0,1))  model\_fit = model.fit()  \# one-step out of sample forecast  start\_index = len(differenced)  end\_index = len(differenced)  forecast = model\_fit.predict(start=start\_index, end=end\_index)  \# invert the differenced forecast to something usable  forecast = inverse\_difference(X, forecast, days\_in\_year)  print('Forecast: %f' % forecast) |
| --- | --- |

Running the example prints the same forecast as above when using the *forecast()* function.

| 1 | Forecast: 14.861669 |
| --- | --- |

You can see that the predict function is more flexible. You can specify any point or contiguous forecast interval in or out of sample.

Now that we know how to make a one-step forecast, we can now make some multi-step forecasts.

## 5\. Multi-Step Out-of-Sample Forecast

We can also make multi-step forecasts using the *forecast()* and *predict()* functions.

It is common with weather data to make one week (7-day) forecasts, so in this section we will look at predicting the minimum daily temperature for the next 7 out-of-sample time steps.

### Forecast Function

The *forecast()* function has an argument called *steps* that allows you to specify the number of time steps to forecast.

By default, this argument is set to 1 for a one-step out-of-sample forecast. We can set it to 7 to get a forecast for the next 7 days.

| 1  2 | \# multi-step out-of-sample forecast  forecast = model\_fit.forecast(steps=7)\[0\] |
| --- | --- |

We can then invert each forecasted time step, one at a time and print the values. Note that to invert the forecast value for t+2, we need the inverted forecast value for t+1. Here, we add them to the end of a list called history for use when calling *inverse\_difference()*.

| 1  2  3  4  5  6  7  8 | \# invert the differenced forecast to something usable  history = \[x for x in X\]  day = 1  for yhat in forecast:  inverted = inverse\_difference(history, yhat, days\_in\_year)  print('Day %d: %f' % (day, inverted))  history.append(inverted)  day += 1 |
| --- | --- |

The complete example is listed below:

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35 | from pandas import read\_csv  from statsmodels.tsa.arima.model import ARIMA  import numpy  \# create a differenced series  def difference(dataset, interval=1):  diff = list()  for i in range(interval, len(dataset)):  value = dataset\[i\] - dataset\[i - interval\]  diff.append(value)  return numpy.array(diff)  \# invert differenced value  def inverse\_difference(history, yhat, interval=1):  return yhat + history\[-interval\]  \# load dataset  \# seasonal difference  X = series.values  days\_in\_year = 365  differenced = difference(X, days\_in\_year)  \# fit model  model = ARIMA(differenced, order=(7,0,1))  model\_fit = model.fit()  \# multi-step out-of-sample forecast  forecast = model\_fit.forecast(steps=7)  \# invert the differenced forecast to something usable  history = \[x for x in X\]  day = 1  for yhat in forecast:  inverted = inverse\_difference(history, yhat, days\_in\_year)  print('Day %d: %f' % (day, inverted))  history.append(inverted)  day += 1 |
| --- | --- |

Running the example prints the forecast for the next 7 days.

| 1  2  3  4  5  6  7 | Day 1: 14.861669  Day 2: 15.628784  Day 3: 13.331349  Day 4: 11.722413  Day 5: 10.421523  Day 6: 14.415549  Day 7: 12.674711 |
| --- | --- |

### Predict Function

The *predict()* function can also forecast the next 7 out-of-sample time steps.

Using time step indexes, we can specify the end index as 6 more time steps in the future; for example:

| 1  2  3  4 | \# multi-step out-of-sample forecast  start\_index = len(differenced)  end\_index = start\_index + 6  forecast = model\_fit.predict(start=start\_index, end=end\_index) |
| --- | --- |

The complete example is listed below.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31  32  33  34  35  36  37 | from pandas import read\_csv  from statsmodels.tsa.arima.model import ARIMA  import numpy  \# create a differenced series  def difference(dataset, interval=1):  diff = list()  for i in range(interval, len(dataset)):  value = dataset\[i\] - dataset\[i - interval\]  diff.append(value)  return numpy.array(diff)  \# invert differenced value  def inverse\_difference(history, yhat, interval=1):  return yhat + history\[-interval\]  \# load dataset  \# seasonal difference  X = series.values  days\_in\_year = 365  differenced = difference(X, days\_in\_year)  \# fit model  model = ARIMA(differenced, order=(7,0,1))  model\_fit = model.fit()  \# multi-step out-of-sample forecast  start\_index = len(differenced)  end\_index = start\_index + 6  forecast = model\_fit.predict(start=start\_index, end=end\_index)  \# invert the differenced forecast to something usable  history = \[x for x in X\]  day = 1  for yhat in forecast:  inverted = inverse\_difference(history, yhat, days\_in\_year)  print('Day %d: %f' % (day, inverted))  history.append(inverted)  day += 1 |
| --- | --- |

Running the example produces the same results as calling the *forecast()* function in the previous section, as you would expect.

| 1  2  3  4  5  6  7 | Day 1: 14.861669  Day 2: 15.628784  Day 3: 13.331349  Day 4: 11.722413  Day 5: 10.421523  Day 6: 14.415549  Day 7: 12.674711 |
| --- | --- |

## Summary

In this tutorial, you discovered how to make out-of-sample forecasts in Python using statsmodels.

Specifically, you learned:

- How to make a one-step out-of-sample forecast.
- How to make a 7-day multi-step out-of-sample forecast.
- How to use both the *forecast()* and *predict()* functions when forecasting.

Do you have any questions about out-of-sample forecasts, or about this post? Ask your questions in the comments and I will do my best to answer.

## Want to Develop Time Series Forecasts with Python?

[![[Introduction-to-Time-Series-Forecasting-With-Python-220 1.png|Introduction to Time Series Forecasting With Python]]](https://machinelearningmastery.com/wp-content/uploads/2022/11/TSFP-220.png)

#### Develop Your Own Forecasts in Minutes

...with just a few lines of python code

Discover how in my new Ebook:  
[Introduction to Time Series Forecasting With Python](https://machinelearningmastery.com/introduction-to-time-series-forecasting-with-python/)

It covers **self-study tutorials** and **end-to-end projects** on topics like: *Loading data, visualization, modeling, algorithm tuning,* and much more...

#### Finally Bring Time Series Forecasting to Your Own Projects

Skip the Academics. Just Results.

[See What's Inside](https://machinelearningmastery.com/introduction-to-time-series-forecasting-with-python/)