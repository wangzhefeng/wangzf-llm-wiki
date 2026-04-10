---
source_type: web
title: "How Much Forecasting Performance Do You Lose During Model Selection?"
author:
  - 
  - "[[Vitor Cerqueira]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://towardsdatascience.com/how-much-forecasting-performance-do-you-lose-during-model-selection-923889e2f2dc/"
published: 2023-01-06
created: 2026-04-06
description: "How often does cross-validation pick the best forecasting model? What happens when it doesn't?"
tags:
  - 
  - "clippings"
---

![[04Fw68lkKHlKIGW-Y-scaled.jpg|Photo by Héctor J. Rivas on Unsplash]]

Photo by Héctor J. Rivas on Unsplash

Suppose you have a forecasting problem. You need to select a model to solve it. [You may want to test a few alternatives with cross-validation](https://towardsdatascience.com/4-things-to-do-when-applying-cross-validation-with-time-series-c6a5674ebf3a).

Have you ever wondered what’s the chance that cross-validation selects the best possible model? And, if not, how poorer is the model that is picked?

Let’s find out.

---

## Introduction

Cross-validation, for time series or otherwise, solves two problems:

- **Performance estimation.** How well is the model going to perform in new data? You can use these estimations to assess whether the model can be deployed;
- **Model Selection.** Use the above estimates to rank a pool of available models. For example, different configurations of a learning algorithm for hyper-parameter tuning. In this case, you select the model with the best performance estimates.

Wait! Aren’t these two problems the same?

Not really. A given method (say, [TimeSeriesSplits](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.TimeSeriesSplit.html)) may provide good performance estimates, on average. But it can be poor for ranking the available models, thereby poor for model selection.

### Example

Let me give an example. Suppose you want to compare four models: *M1*, *M2*, *M3*, and *M4*. These are shown in the x-axis of Figure 1 below.

The true test loss of these models is displayed in blue bars. Their ranking is *M1* > *M2* > *M3* > *M4*. So, *M1* is the best model because it shows the lowest error (say, the mean absolute error).

Then, two cross-validation methods (*CV1* and *CV2*) are used to estimate the error of each model.

![[12KNipUyOjgbfd2X2D-0VmQ.png|Figure 1: The goal of cross-validation is to approximate the true error (blue bars). CV1 (light green blue) provides, on average, better estimations than CV2 (dark green). But CV2 ranks the models perfectly, unlike CV1.]]

Figure 1: The goal of cross-validation is to approximate the true error (blue bars). CV1 (light green blue) provides, on average, better estimations than CV2 (dark green). But CV2 ranks the models perfectly, unlike CV1.

*CV1* produces the best estimations (nearest to the true error), on average. But, the estimated ranking (*M2* > *M1* > *M4* > *M3*) is different than the actual one. It is also worse than the ranking produced by *CV2*.

Despite providing worse performance estimates, *CV2* outputs a perfect ranking of the models.

This example shows that one CV technique can be better for performance estimation (*CV1*), but another for model selection (*CV2*).

---

## Performance Loss During Model Selection

Suppose you’re doing model selection for forecasting. Two questions may come to your mind:

1. What’s the chance that cross-validation selects the best model? The one that will have the best performance in the test set.
2. What happens when it doesn’t? How poorer is the performance of the selected model?

### Testing Different Cross-Validation Approaches

We can answer these questions by simulating a realistic scenario. First, apply cross-validation to select a model using the training data. Then, check how this model does in a test set.

Let’s do this step-by-step.

I prepared 50 different forecasting models. These include different configurations of linear models, and decision trees, among others. [The models are trained with a supervised learning approach called auto-regression.](https://towardsdatascience.com/machine-learning-for-forecasting-transformations-and-feature-extraction-bbbea9de0ac2) Without going into details, the recent past values are used as explanatory variables. The target variables are future observations.

Then, I applied several cross-validation techniques to select the best model. These include [TimeSeriesSplits](https://towardsdatascience.com/4-things-to-do-when-applying-cross-validation-with-time-series-c6a5674ebf3a) (a.k.a. Time Series Cross-Validation), [MonteCarloCV](https://medium.com/towards-data-science/monte-carlo-cross-validation-for-time-series-ed01c41e2995), or [K-fold Cross-validation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html). You can check a description for each method [in a previous article](https://medium.com/@vcerq/9-techniques-for-cross-validating-time-series-data-7828fc3f781d).

I repeated this process for almost 3000 different time series.

Here are the results.

### Cross-validation Selection Accuracy

The selection accuracy is the percentage of times a cross-validation approach picks the best model.

![[1YR-Wxkxjl5rVzi2E4b04-Q.png|Figure 2: Accuracy of different cross-validation methods for selecting the best forecasting model. The description of each method is available in a previous article. Image by Author.]]

Figure 2: Accuracy of different cross-validation methods for selecting the best forecasting model. The description of each method is available in a previous article. Image by Author.

The scores range from 7% to 10%.

Sounds low, right? Still, if you were to select a model at random you’d expect a 2% accuracy (1 over 50 possible models). So, 7% to 10% is way better than that.

Yet, all methods will probably fail to select the best model. Then, comes the second question.

### How good is the selected model?

To answer this question, we compare the selected model with the model that should have been selected.

We can measure the percentage difference in error between these two. The difference is 0 when the best model is selected by cross-validation.

![[1Us1IeBn91ZaQ0zSPIkE09A.png|Figure 3: Average percentage difference in error (and respective standard deviation) between the selected model and the best possible model. Image by Author.]]

Figure 3: Average percentage difference in error (and respective standard deviation) between the selected model and the best possible model. Image by Author.

Most estimators select a model that performs about 0.3% worse than the best possible model, on average. There are some differences here and there. But, by and large, different cross-validation methods show similar performance for model selection.

The exception is *Holdout*, which represents [a single split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html). This corroborates the recommendation I put forth in [a previous article](https://medium.com/towards-data-science/4-things-to-do-when-applying-cross-validation-with-time-series-c6a5674ebf3a). Unless the time series is large, carry out many splits if you can.

You can check the full experiments in the [article](https://arxiv.org/pdf/2104.00584.pdf) in reference \[1\]. These can be reproduced using the code available in [my Github](https://github.com/vcerqueira/model_selection_forecasting).

---

## Take Aways

- Model selection is the process of using cross-validation for selecting a model from a pool of alternatives;
- With 50 alternative models, cross-validation has a 7%-10% chance of picking the best one;
- When the best model is not picked, the selected model will perform about 0.3–0.35% worse, on average;
- Several cross-validation splits are important for better model selection.