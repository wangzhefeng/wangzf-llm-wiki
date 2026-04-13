---
source_type: web
title: "Time Series Forecasting as Supervised Learning"
author:
  - 
  - "[[Jason Brownlee]]"
created_at: 2026-04-06
status: inbox
created: 2026-04-06
description: "Time series forecasting can be framed as a supervised learning problem. This re-framing of your time series data allows you access to the suite of standard linear and nonlinear machine learning algorithms on your problem. In this post, you will discover how you can re-frame your time series problem as a supervised learning problem for […]"
tags:
  - 
  - "clippings"
source_url: "https://machinelearningmastery.com/time-series-forecasting-supervised-learning/"
published_at: 2016-12-05
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

Time series forecasting can be framed as a supervised learning problem.

This re-framing of your time series data allows you access to the suite of standard linear and nonlinear machine learning algorithms on your problem.

In this post, you will discover how you can re-frame your time series problem as a supervised learning problem for machine learning. After reading this post, you will know:

- What supervised learning is and how it is the foundation for all [predictive modeling](https://machinelearningmastery.com/gentle-introduction-to-predictive-modeling/) machine learning algorithms.
- The sliding window method for framing a time series dataset and how to use it.
- How to use the sliding window for multivariate data and multi-step forecasting.

**Kick-start your project** with my new book [Time Series Forecasting With Python](https://machinelearningmastery.com/introduction-to-time-series-forecasting-with-python/), including *step-by-step tutorials* and the *Python source code* files for all examples.

Let’s get started.

![[Time-Series-Forecasting-as-Supervised-Learning.jpg|Time Series Forecasting as Supervised Learning]]

Time Series Forecasting as Supervised Learning  
Photo by [Jeroen Looyé](https://www.flickr.com/photos/looye/6780166094/), some rights reserved.

## Supervised Machine Learning

The majority of practical machine learning uses supervised learning.

Supervised learning is where you have input variables (**X**) and an output variable (**y**) and you use an algorithm to learn the mapping function from the input to the output.

| 1 | Y = f(X) |
| --- | --- |

The goal is to approximate the real underlying mapping so well that when you have new input data (**X**), you can predict the output variables (**y**) for that data.

Below is a contrived example of a supervised learning dataset where each row is an observation comprised of one input variable (**X**) and one output variable to be predicted (**y**).

| 1  2  3  4  5  6 | X, y  5, 0.9  4, 0.8  5, 1.0  3, 0.7  4, 0.9 |
| --- | --- |

It is called supervised learning because the process of an algorithm learning from the training dataset can be thought of as a teacher supervising the learning process.

We know the correct answers; the algorithm iteratively makes predictions on the training data and is corrected by making updates. Learning stops when the algorithm achieves an acceptable level of performance.

Supervised learning problems can be further grouped into regression and classification problems.

- **Classification**: A classification problem is when the output variable is a category, such as “ *red* ” and “ *blue* ” or “ *disease* ” and “ *no disease*.”
- **Regression**: A regression problem is when the output variable is a real value, such as “ *dollars* ” or “ *weight*.” The contrived example above is a regression problem.

### Stop learning Time Series Forecasting the slow way!

Take my free 7-day email course and discover how to get started (with sample code).

Click to sign-up and also get a free PDF Ebook version of the course.

## Sliding Window For Time Series Data

Time series data can be phrased as supervised learning.

Given a sequence of numbers for a time series dataset, we can restructure the data to look like a supervised learning problem. We can do this by using previous time steps as input variables and use the next time step as the output variable.

Let’s make this concrete with an example. Imagine we have a time series as follows:

| 1  2  3  4  5  6 | time, measure  1, 100  2, 110  3, 108  4, 115  5, 120 |
| --- | --- |

We can restructure this time series dataset as a supervised learning problem by using the value at the previous time step to predict the value at the next time-step. Re-organizing the time series dataset this way, the data would look as follows:

| 1  2  3  4  5  6  7 | X, y  ?, 100  100, 110  110, 108  108, 115  115, 120  120,? |
| --- | --- |

Take a look at the above transformed dataset and compare it to the original time series. Here are some observations:

- We can see that the previous time step is the input (**X**) and the next time step is the output (**y**) in our supervised learning problem.
- We can see that the order between the observations is preserved, and must continue to be preserved when using this dataset to train a supervised model.
- We can see that we have no previous value that we can use to predict the first value in the sequence. We will delete this row as we cannot use it.
- We can also see that we do not have a known next value to predict for the last value in the sequence. We may want to delete this value while training our supervised model also.

The use of prior time steps to predict the next time step is called the sliding window method. For short, it may be called the window method in some literature. In statistics and time series analysis, this is called a lag or lag method.

The number of previous time steps is called the window width or size of the lag.

This sliding window is the basis for how we can turn any time series dataset into a supervised learning problem. From this simple example, we can notice a few things:

- We can see how this can work to turn a time series into either a regression or a classification supervised learning problem for real-valued or labeled time series values.
- We can see how once a time series dataset is prepared this way that any of the standard linear and nonlinear machine learning algorithms may be applied, as long as the order of the rows is preserved.
- We can see how the width sliding window can be increased to include more previous time steps.
- We can see how the sliding window approach can be used on a time series that has more than one value, or so-called multivariate time series.

We will explore some of these uses of the sliding window, starting next with using it to handle time series with more than one observation at each time step, called multivariate time series.

## Sliding Window With Multivariate Time Series Data

The number of observations recorded for a given time in a time series dataset matters.

Traditionally, different names are used:

- **Univariate Time Series**: These are datasets where only a single variable is observed at each time, such as temperature each hour. The example in the previous section is a univariate time series dataset.
- **Multivariate Time Series**: These are datasets where two or more variables are observed at each time.

Most time series analysis methods, and even books on the topic, focus on univariate data. This is because it is the simplest to understand and work with. Multivariate data is often more difficult to work with. It is harder to model and often many of the classical methods do not perform well.

> Multivariate time series analysis considers simultaneously multiple time series. … It is, in general, much more complicated than univariate time series analysis

— Page 1, [Multivariate Time Series Analysis: With R and Financial Applications](https://amzn.to/31Q2N4V).

The sweet spot for using machine learning for time series is where classical methods fall down. This may be with complex univariate time series, and is more likely with multivariate time series given the additional complexity.

Below is another worked example to make the sliding window method concrete for multivariate time series.

Assume we have the contrived multivariate time series dataset below with two observations at each time step. Let’s also assume that we are only concerned with predicting **measure2**.

| 1  2  3  4  5  6 | time, measure1, measure2  1, 0.2, 88  2, 0.5, 89  3, 0.7, 87  4, 0.4, 88  5, 1.0, 90 |
| --- | --- |

We can re-frame this time series dataset as a supervised learning problem with a window width of one.

This means that we will use the previous time step values of **measure1** and **measure2**. We will also have available the next time step value for **measure1**. We will then predict the next time step value of **measure2**.

This will give us 3 input features and one output value to predict for each training pattern.

| 1  2  3  4  5  6  7 | X1, X2, X3, y  ?,?, 0.2, 88  0.2, 88, 0.5, 89  0.5, 89, 0.7, 87  0.7, 87, 0.4, 88  0.4, 88, 1.0, 90  1.0, 90,?,? |
| --- | --- |

We can see that as in the univariate time series example above, we may need to remove the first and last rows in order to train our supervised learning model.

This example raises the question of what if we wanted to predict both **measure1** and **measure2** for the next time step?

The sliding window approach can also be used in this case.

Using the same time series dataset above, we can phrase it as a supervised learning problem where we predict both **measure1** and **measure2** with the same window width of one, as follows.

| 1  2  3  4  5  6  7 | X1, X2, y1, y2  ?,?, 0.2, 88  0.2, 88, 0.5, 89  0.5, 89, 0.7, 87  0.7, 87, 0.4, 88  0.4, 88, 1.0, 90  1.0, 90,?,? |
| --- | --- |

Not many supervised learning methods can handle the prediction of multiple output values without modification, but some methods, like artificial neural networks, have little trouble.

We can think of predicting more than one value as predicting a sequence. In this case, we were predicting two different output variables, but we may want to predict multiple time-steps ahead of one output variable.

This is called multi-step forecasting and is covered in the next section.

## Sliding Window With Multi-Step Forecasting

The number of time steps ahead to be forecasted is important.

Again, it is traditional to use different names for the problem depending on the number of time-steps to forecast:

- **One-Step Forecast**: This is where the next time step (t+1) is predicted.
- **Multi-Step Forecast**: This is where two or more future time steps are to be predicted.

All of the examples we have looked at so far have been one-step forecasts.

There are are a number of ways to model multi-step forecasting as a supervised learning problem. We will cover some of these alternate ways in a future post.

For now, we are focusing on framing multi-step forecast using the sliding window method.

Consider the same univariate time series dataset from the first sliding window example above:

| 1  2  3  4  5  6 | time, measure  1, 100  2, 110  3, 108  4, 115  5, 120 |
| --- | --- |

We can frame this time series as a two-step forecasting dataset for supervised learning with a window width of one, as follows:

| 1  2  3  4  5  6  7 | X1, y1, y2  ? 100, 110  100, 110, 108  110, 108, 115  108, 115, 120  115, 120,?  120,?,? |
| --- | --- |

We can see that the first row and the last two rows cannot be used to train a supervised model.

It is also a good example to show the burden on the input variables. Specifically, that a supervised model only has **X1** to work with in order to predict both **y1** and **y2**.

Careful thought and experimentation are needed on your problem to find a window width that results in acceptable model performance.

## Further Reading

If you are looking for more resources on how to work with time series data as a machine learning problem, see the following two papers:

- [Machine Learning for Sequential Data: A Review](http://web.engr.oregonstate.edu/~tgd/publications/mlsd-ssspr.pdf) (2002) \[PDF\]
- [Machine Learning Strategies for Time Series Forecasting](http://link.springer.com/chapter/10.1007%2F978-3-642-36318-4_3) (2013) ([also slides](http://www.ulb.ac.be/di/map/gbonte/ftp/time_ser.pdf) PDF)

For Python code for how to do this, see the post:

- [How to Convert a Time Series to a Supervised Learning Problem in Python](https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/)

## Summary

In this post, you discovered how you can re-frame your time series prediction problem as a supervised learning problem for use with machine learning methods.

Specifically, you learned:

- Supervised learning is the most popular way of framing problems for machine learning as a collection of observations with inputs and outputs.
- Sliding window is the way to restructure a time series dataset as a supervised learning problem.
- Multivariate and multi-step forecasting time series can also be framed as supervised learning using the sliding window method.

Do you have any questions about the sliding window method or about this post?  
Ask your questions in the comments below and I will do my best to answer.

## Want to Develop Time Series Forecasts with Python?

[![[Introduction-to-Time-Series-Forecasting-With-Python-220 2.png|Introduction to Time Series Forecasting With Python]]](https://machinelearningmastery.com/wp-content/uploads/2022/11/TSFP-220.png)

#### Develop Your Own Forecasts in Minutes

...with just a few lines of python code

Discover how in my new Ebook:  
[Introduction to Time Series Forecasting With Python](https://machinelearningmastery.com/introduction-to-time-series-forecasting-with-python/)

It covers **self-study tutorials** and **end-to-end projects** on topics like: *Loading data, visualization, modeling, algorithm tuning,* and much more...

#### Finally Bring Time Series Forecasting to Your Own Projects

Skip the Academics. Just Results.

[See What's Inside](https://machinelearningmastery.com/introduction-to-time-series-forecasting-with-python/)