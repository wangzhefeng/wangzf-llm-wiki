---
author:
- null
- '[[Jason Brownlee]]'
created: 2026-04-06
created_at: 2026-04-06
description: Multioutput regression are regression problems that involve predicting
  two or more numerical values given an input example. An example might be to predict
  a coordinate given an input, e.g. predicting x and y values. Another example would
  be multi-step time series forecasting that involves predicting multiple future time
  series of a given variable. Many machine […]
source_type: web
status: inbox
tags:
- null
- clippings
title: How to Develop Multi-Output Regression Models with Python
topics:
- 机器学习
source_url: https://machinelearningmastery.com/multi-output-regression-models-with-python/
published_at: 2020-03-27
related_concepts: []
---

Multioutput regression are regression problems that involve predicting two or more numerical values given an input example.

An example might be to predict a coordinate given an input, e.g. predicting x and y values. Another example would be multi-step time series forecasting that involves predicting multiple future time series of a given variable.

Many machine learning algorithms are designed for predicting a single numeric value, referred to simply as regression. Some algorithms do support multioutput regression inherently, such as linear regression and decision trees. There are also special workaround models that can be used to wrap and use those algorithms that do not natively support predicting multiple outputs.

In this tutorial, you will discover how to develop machine learning models for multioutput regression.

After completing this tutorial, you will know:

- The problem of multioutput regression in machine learning.
- How to develop machine learning models that inherently support multiple-output regression.
- How to develop wrapper models that allow algorithms that do not inherently support multiple outputs to be used for multiple-output regression.

**Kick-start your project** with my new book [Ensemble Learning Algorithms With Python](https://machinelearningmastery.com/ensemble-learning-algorithms-with-python/), including *step-by-step tutorials* and the *Python source code* files for all examples.

Let’s get started.

- **Updated Aug/2020**: Elaborated examples of wrapper models.
![[How-to-Develop-Multioutput-Regression-Models-in-Python.jpg|How to Develop Multioutput Regression Models in Python]]

How to Develop Multioutput Regression Models in Python  
Photo by [a\_terracini](https://flickr.com/photos/arterracini/32096684665/), some rights reserved.

## Tutorial Overview

This tutorial is divided into five parts; they are:

1. Problem of Multioutput Regression
	1. Check Scikit-Learn Version
		2. Multioutput Regression Test Problem
2. Inherently Multioutput Regression Algorithms
	1. Linear Regression for Multioutput Regression
		2. k-Nearest Neighbors for Multioutput Regression
		3. Evaluate Multioutput Regression With Cross-Validation
3. Wrapper Multioutput Regression Algorithms
4. Direct Multioutput Regression
5. Chained Multioutput Regression

## Problem of Multioutput Regression

Regression refers to a predictive modeling problem that involves predicting a numerical value.

For example, predicting a size, weight, amount, number of sales, and number of clicks are regression problems. Typically, a single numeric value is predicted given input variables.

Some regression problems require the prediction of two or more numeric values. For example, predicting an x and y coordinate.

These problems are referred to as multiple-output regression, or multioutput regression.

- **Regression**: Predict a single numeric output given an input.
- **Multioutput Regression**: Predict two or more numeric outputs given an input.

In multioutput regression, typically the outputs are dependent upon the input and upon each other. This means that often the outputs are not independent of each other and may require a model that predicts both outputs together or each output contingent upon the other outputs.

Multi-step time series forecasting may be considered a type of multiple-output regression where a sequence of future values are predicted and each predicted value is dependent upon the prior values in the sequence.

There are a number of strategies for handling multioutput regression and we will explore some of them in this tutorial.

### Want to Get Started With Ensemble Learning?

Take my free 7-day email crash course now (with sample code).

Click to sign-up and also get a free PDF Ebook version of the course.

### Check Scikit-Learn Version

First, confirm that you have a modern version of the scikit-learn library installed.

This is important because some of the models we will explore in this tutorial require a modern version of the library.

You can check the version of the library with the following code example:

| 1  2  3 | \# check scikit-learn version  import sklearn  print(sklearn.\_\_version\_\_) |
| --- | --- |

Running the example will print the version of the library.

At the time of writing, this is about version 0.22. You need to be using this version of scikit-learn or higher.

| 1 | 0.22.1 |
| --- | --- |

### Multioutput Regression Test Problem

We can define a test problem that we can use to demonstrate the different modeling strategies.

We will use the [make\_regression() function](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html) to create a test dataset for multiple-output regression. We will generate 1,000 examples with 10 input features, five of which will be redundant and five that will be informative. The problem will require the prediction of two numeric values.

- **Problem Input**: 10 numeric variables.
- **Problem Output**: 2 numeric variables.

The example below generates the dataset and summarizes the shape.

| 1  2  3  4  5  6 | \# example of multioutput regression test problem  from sklearn.datasets import make\_regression  \# create datasets  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# summarize dataset  print(X.shape, y.shape) |
| --- | --- |

Running the example creates the dataset and summarizes the shape of the input and output elements of the dataset for modeling, confirming the chosen configuration.

| 1 | (1000, 10) (1000, 2) |
| --- | --- |

Next, let’s look at modeling this problem directly.

## Inherently Multioutput Regression Algorithms

Some regression machine learning algorithms support multiple outputs directly.

This includes most of the popular machine learning algorithms implemented in the scikit-learn library, such as:

- LinearRegression (and related)
- KNeighborsRegressor
- DecisionTreeRegressor
- RandomForestRegressor (and related)

Let’s look at a few examples to make this concrete.

### Linear Regression for Multioutput Regression

The example below fits a linear regression model on the multioutput regression dataset, then makes a single prediction with the fit model.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14 | \# linear regression for multioutput regression  from sklearn.datasets import make\_regression  from sklearn.linear\_model import LinearRegression  \# create datasets  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define model  model = LinearRegression()  \# fit model  model.fit(X, y)  \# make a prediction  row = \[0.21947749, 0.32948997, 0.81560036, 0.440956, -0.0606303, -0.29257894, -0.2820059, -0.00290545, 0.96402263, 0.04992249\]  yhat = model.predict(\[row\])  \# summarize prediction  print(yhat\[0\]) |
| --- | --- |

Running the example fits the model and then makes a prediction for one input, confirming that the model predicted two required values.

| 1 | \[-11.73511093 52.78406297\] |
| --- | --- |

### k-Nearest Neighbors for Multioutput Regression

The example below fits a k-nearest neighbors model on the multioutput regression dataset, then makes a single prediction with the fit model.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14 | \# k-nearest neighbors for multioutput regression  from sklearn.datasets import make\_regression  from sklearn.neighbors import KNeighborsRegressor  \# create datasets  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define model  model = KNeighborsRegressor()  \# fit model  model.fit(X, y)  \# make a prediction  row = \[0.21947749, 0.32948997, 0.81560036, 0.440956, -0.0606303, -0.29257894, -0.2820059, -0.00290545, 0.96402263, 0.04992249\]  yhat = model.predict(\[row\])  \# summarize prediction  print(yhat\[0\]) |
| --- | --- |

Running the example fits the model and then makes a prediction for one input, confirming that the model predicted two required values.

| 1 | \[-11.73511093 52.78406297\] |
| --- | --- |

### Decision Tree for Multioutput Regression

The example below fits a decision tree model on the multioutput regression dataset, then makes a single prediction with the fit model.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14 | \# decision tree for multioutput regression  from sklearn.datasets import make\_regression  from sklearn.tree import DecisionTreeRegressor  \# create datasets  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define model  model = DecisionTreeRegressor()  \# fit model  model.fit(X, y)  \# make a prediction  row = \[0.21947749, 0.32948997, 0.81560036, 0.440956, -0.0606303, -0.29257894, -0.2820059, -0.00290545, 0.96402263, 0.04992249\]  yhat = model.predict(\[row\])  \# summarize prediction  print(yhat\[0\]) |
| --- | --- |

Running the example fits the model and then makes a prediction for one input, confirming that the model predicted two required values.

| 1 | \[49.93137149 64.08484989\] |
| --- | --- |

### Evaluate Multioutput Regression With Cross-Validation

We may want to evaluate a multioutput regression using [k-fold cross-validation](https://machinelearningmastery.com/k-fold-cross-validation/).

This can be achieved in the same way as evaluating any other machine learning model.

We will fit and evaluate a *DecisionTreeRegressor* model on the test problem using 10-fold cross-validation with three repeats. We will use the mean absolute error (MAE) performance metric as the score.

The complete example is listed below.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20 | \# evaluate multioutput regression model with k-fold cross-validation  from numpy import absolute  from numpy import mean  from numpy import std  from sklearn.datasets import make\_regression  from sklearn.tree import DecisionTreeRegressor  from sklearn.model\_selection import cross\_val\_score  from sklearn.model\_selection import RepeatedKFold  \# create datasets  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define model  model = DecisionTreeRegressor()  \# define the evaluation procedure  cv = RepeatedKFold(n\_splits=10, n\_repeats=3, random\_state=1)  \# evaluate the model and collect the scores  n\_scores = cross\_val\_score(model, X, y, scoring='neg\_mean\_absolute\_error', cv=cv, n\_jobs=-1)  \# force the scores to be positive  n\_scores = absolute(n\_scores)  \# summarize performance  print('MAE: %.3f (%.3f)' % (mean(n\_scores), std(n\_scores))) |
| --- | --- |

Running the example evaluates the performance of the decision tree model for multioutput regression on the test problem. The mean and standard deviation of the MAE is reported calculated across all folds and all repeats.

**Note**: Your [results may vary](https://machinelearningmastery.com/different-results-each-time-in-machine-learning/) given the stochastic nature of the algorithm or evaluation procedure, or differences in numerical precision. Consider running the example a few times and compare the average outcome.

Importantly, error is reported across both output variables, rather than separate error scores for each output variable.

| 1 | MAE: 51.817 (2.863) |
| --- | --- |

## Wrapper Multioutput Regression Algorithms

Not all regression algorithms support multioutput regression.

One example is the [support vector machine](https://machinelearningmastery.com/support-vector-machines-for-machine-learning/), although for regression, it is referred to as support vector regression, or [SVR](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html).

This algorithm does not support multiple outputs for a regression problem and will raise an error. We can demonstrate this with an example, listed below.

| 1  2  3  4  5  6  7  8  9  10 | \# failure of support vector regression for multioutput regression (causes an error)  from sklearn.datasets import make\_regression  from sklearn.svm import LinearSVR  \# create datasets  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1)  \# define model  model = LinearSVR()  \# fit model  \# (THIS WILL CAUSE AN ERROR!)  model.fit(X, y) |
| --- | --- |

Running the example reports an error message indicating that the model does not support multioutput regression.

| 1 | ValueError: bad input shape (1000, 2) |
| --- | --- |

A workaround for using regression models designed for predicting one value for multioutput regression is to divide the multioutput regression problem into multiple sub-problems.

The most obvious way to do this is to split a multioutput regression problem into multiple single-output regression problems.

For example, if a multioutput regression problem required the prediction of three values *y1*, *y2* and *y3* given an input *X*, then this could be partitioned into three single-output regression problems:

- **Problem 1**: Given *X*, predict *y1*.
- **Problem 2**: Given *X*, predict *y2*.
- **Problem 3**: Given *X*, predict *y3*.

There are two main approaches to implementing this technique.

The first approach involves developing a separate regression model for each output value to be predicted. We can think of this as a direct approach, as each target value is modeled directly.

The second approach is an extension of the first method except the models are organized into a chain. The prediction from the first model is taken as part of the input to the second model, and the process of output-to-input dependency repeats along the chain of models.

- **Direct Multioutput**: Develop an independent model for each numerical value to be predicted.
- **Chained Multioutput**: Develop a sequence of dependent models to match the number of numerical values to be predicted.

Let’s take a closer look at each of these techniques in turn.

## Direct Multioutput Regression

The direct approach to multioutput regression involves dividing the regression problem into a separate problem for each target variable to be predicted.

This assumes that the outputs are independent of each other, which might not be a correct assumption. Nevertheless, this approach can provide surprisingly effective predictions on a range of problems and may be worth trying, at least as a performance baseline.

For example, the outputs for your problem may, in fact, be mostly independent, if not completely independent, and this strategy can help you find out.

This approach is supported by the [MultiOutputRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html) class that takes a regression model as an argument. It will then create one instance of the provided model for each output in the problem.

The example below demonstrates how we can first create a single-output regression model then use the *MultiOutputRegressor* class to wrap the regression model and add support for multioutput regression.

| 1  2  3  4  5 | ...  \# define base model  model = LinearSVR()  \# define the direct multioutput wrapper model  wrapper = MultiOutputRegressor(model) |
| --- | --- |

We can demonstrate this strategy with a worked example on our synthetic multioutput regression problem.

The example below demonstrates evaluating the *MultiOutputRegressor* class with linear SVR using [repeated k-fold cross-validation](https://machinelearningmastery.com/repeated-k-fold-cross-validation-with-python/) and reporting the average mean absolute error (MAE) across all folds and repeats.

The complete example is listed below.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23 | \# example of evaluating direct multioutput regression with an SVM model  from numpy import mean  from numpy import std  from numpy import absolute  from sklearn.datasets import make\_regression  from sklearn.model\_selection import cross\_val\_score  from sklearn.model\_selection import RepeatedKFold  from sklearn.multioutput import MultiOutputRegressor  from sklearn.svm import LinearSVR  \# define dataset  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define base model  model = LinearSVR()  \# define the direct multioutput wrapper model  wrapper = MultiOutputRegressor(model)  \# define the evaluation procedure  cv = RepeatedKFold(n\_splits=10, n\_repeats=3, random\_state=1)  \# evaluate the model and collect the scores  n\_scores = cross\_val\_score(wrapper, X, y, scoring='neg\_mean\_absolute\_error', cv=cv, n\_jobs=-1)  \# force the scores to be positive  n\_scores = absolute(n\_scores)  \# summarize performance  print('MAE: %.3f (%.3f)' % (mean(n\_scores), std(n\_scores))) |
| --- | --- |

Running the example reports the mean and standard deviation MAE of the direct wrapper model.

**Note**: Your [results may vary](https://machinelearningmastery.com/different-results-each-time-in-machine-learning/) given the stochastic nature of the algorithm or evaluation procedure, or differences in numerical precision. Consider running the example a few times and compare the average outcome.

In this case, we can see that the Linear SVR model wrapped by the direct multioutput regression strategy achieved a MAE of about 0.419.

| 1 | MAE: 0.419 (0.024) |
| --- | --- |

We can also use the direct multioutput regression wrapper as a final model and make predictions on new data.

First, the model is fit on all available data, then the *predict()* function can be called to make predictions on new data.

The example below demonstrates this on our synthetic multioutput regression dataset.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17 | \# example of making a prediction with the direct multioutput regression model  from sklearn.datasets import make\_regression  from sklearn.multioutput import MultiOutputRegressor  from sklearn.svm import LinearSVR  \# define dataset  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define base model  model = LinearSVR()  \# define the direct multioutput wrapper model  wrapper = MultiOutputRegressor(model)  \# fit the model on the whole dataset  wrapper.fit(X, y)  \# make a single prediction  row = \[0.21947749, 0.32948997, 0.81560036, 0.440956, -0.0606303, -0.29257894, -0.2820059, -0.00290545, 0.96402263, 0.04992249\]  yhat = wrapper.predict(\[row\])  \# summarize the prediction  print('Predicted: %s' % yhat\[0\]) |
| --- | --- |

Running the example fits the direct wrapper model on the entire dataset and is then used to make a prediction on a new row of data, as we might when using the model in an application.

| 1 | Predicted: \[50.01932887 64.49432991\] |
| --- | --- |

Now that we are familiar with using the direct multioutput regression wrapper, let’s look at the chained method.

## Chained Multioutput Regression

Another approach to using single-output regression models for multioutput regression is to create a linear sequence of models.

The first model in the sequence uses the input and predicts one output; the second model uses the input and the output from the first model to make a prediction; the third model uses the input and output from the first two models to make a prediction, and so on.

For example, if a multioutput regression problem required the prediction of three values *y1*, *y2* and *y3* given an input *X*, then this could be partitioned into three dependent single-output regression problems as follows:

- **Problem 1**: Given *X*, predict *y1*.
- **Problem 2**: Given *X* and *yhat1*, predict *y2*.
- **Problem 3**: Given *X, yhat1, and yhat2*, predict *y3*.

This can be achieved using the [RegressorChain](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.RegressorChain.html) class in the scikit-learn library.

The order of the models may be based on the order of the outputs in the dataset (the default) or specified via the “ *order* ” argument. For example, *order=\[0,1\]* would first predict the oth output, then the 1st output, whereas an *order=\[1,0\]* would first predict the last output variable and then the first output variable in our test problem.

The example below demonstrates how we can first create a single-output regression model then use the *RegressorChain* class to wrap the regression model and add support for multioutput regression.

| 1  2  3  4  5 | ...  \# define base model  model = LinearSVR()  \# define the chained multioutput wrapper model  wrapper = RegressorChain(model, order=\[0,1\]) |
| --- | --- |

We can demonstrate this strategy with a worked example on our synthetic multioutput regression problem.

The example below demonstrates evaluating the *RegressorChain* class with linear SVR using [repeated k-fold cross-validation](https://machinelearningmastery.com/repeated-k-fold-cross-validation-with-python/) and reporting the average mean absolute error (MAE) across all folds and repeats.

The complete example is listed below.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17  18  19  20  21  22  23 | \# example of evaluating chained multioutput regression with an SVM model  from numpy import mean  from numpy import std  from numpy import absolute  from sklearn.datasets import make\_regression  from sklearn.model\_selection import cross\_val\_score  from sklearn.model\_selection import RepeatedKFold  from sklearn.multioutput import RegressorChain  from sklearn.svm import LinearSVR  \# define dataset  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define base model  model = LinearSVR()  \# define the chained multioutput wrapper model  wrapper = RegressorChain(model)  \# define the evaluation procedure  cv = RepeatedKFold(n\_splits=10, n\_repeats=3, random\_state=1)  \# evaluate the model and collect the scores  n\_scores = cross\_val\_score(wrapper, X, y, scoring='neg\_mean\_absolute\_error', cv=cv, n\_jobs=-1)  \# force the scores to be positive  n\_scores = absolute(n\_scores)  \# summarize performance  print('MAE: %.3f (%.3f)' % (mean(n\_scores), std(n\_scores))) |
| --- | --- |

Running the example reports the mean and standard deviation MAE of the chained wrapper model.  
Note that you may see a *ConvergenceWarning* when running the example, which can be safely ignored.

**Note**: Your [results may vary](https://machinelearningmastery.com/different-results-each-time-in-machine-learning/) given the stochastic nature of the algorithm or evaluation procedure, or differences in numerical precision. Consider running the example a few times and compare the average outcome.

In this case, we can see that the Linear SVR model wrapped by the chained multioutput regression strategy achieved a MAE of about 0.643.

| 1 | MAE: 0.643 (0.313) |
| --- | --- |

We can also use the chained multioutput regression wrapper as a final model and make predictions on new data.

First, the model is fit on all available data, then the *predict()* function can be called to make predictions on new data.

The example below demonstrates this on our synthetic multioutput regression dataset.

| 1  2  3  4  5  6  7  8  9  10  11  12  13  14  15  16  17 | \# example of making a prediction with the chained multioutput regression model  from sklearn.datasets import make\_regression  from sklearn.multioutput import RegressorChain  from sklearn.svm import LinearSVR  \# define dataset  X, y = make\_regression(n\_samples=1000, n\_features=10, n\_informative=5, n\_targets=2, random\_state=1, noise=0.5)  \# define base model  model = LinearSVR()  \# define the chained multioutput wrapper model  wrapper = RegressorChain(model)  \# fit the model on the whole dataset  wrapper.fit(X, y)  \# make a single prediction  row = \[0.21947749, 0.32948997, 0.81560036, 0.440956, -0.0606303, -0.29257894, -0.2820059, -0.00290545, 0.96402263, 0.04992249\]  yhat = wrapper.predict(\[row\])  \# summarize the prediction  print('Predicted: %s' % yhat\[0\]) |
| --- | --- |

Running the example fits the chained wrapper model on the entire dataset and is then used to make a prediction on a new row of data, as we might when using the model in an application.

| 1 | Predicted: \[50.03206 64.73673318\] |
| --- | --- |

## Further Reading

This section provides more resources on the topic if you are looking to go deeper.

### APIs

- [Multiclass and multilabel algorithms, API](https://scikit-learn.org/stable/modules/multiclass.html).
- [sklearn.datasets.make\_regression API](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.make_regression.html).
- [sklearn.multioutput.MultiOutputRegressor API](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html).
- [sklearn.multioutput.RegressorChain API](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.RegressorChain.html).

## Summary

In this tutorial, you discovered how to develop machine learning models for multioutput regression.

Specifically, you learned:

- The problem of multioutput regression in machine learning.
- How to develop machine learning models that inherently support multiple-output regression.
- How to develop wrapper models that allow algorithms that do not inherently support multiple outputs to be used for multiple-output regression.

**Do you have any questions?**  
Ask your questions in the comments below and I will do my best to answer.

## Get a Handle on Modern Ensemble Learning!

[![[ELA4ML-220.png|Ensemble Learning Algorithms With Python]]](https://machinelearningmastery.com/ensemble-learning-algorithms-with-python/)

#### Improve Your Predictions in Minutes

...with just a few lines of python code

Discover how in my new Ebook:  
[Ensemble Learning Algorithms With Python](https://machinelearningmastery.com/ensemble-learning-algorithms-with-python/)

It provides **self-study tutorials** with **full working code** on:  
*Stacking*, *Voting*, *Boosting*, *Bagging*, *Blending*, *Super Learner*, and much more...

#### Bring Modern Ensemble Learning Techniques to Your Machine Learning Projects

  

[See What's Inside](https://machinelearningmastery.com/ensemble-learning-algorithms-with-python/)