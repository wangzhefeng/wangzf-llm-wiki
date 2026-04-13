---
source_type: web
title: "Embrace Randomness in Machine Learning"
author:
  - 
  - "[[Jason Brownlee]]"
created_at: 2026-04-06
status: inbox
created: 2026-04-06
description: "Why Do You Get Different Results On Different Runs Of An Algorithm With The Same Data? Applied machine learning is a tapestry of breakthroughs and mindset shifts. Understanding the role of randomness in machine learning algorithms is one of those breakthroughs. Once you get it, you will see things differently. In a whole new light. Things like […]"
tags:
  - 
  - "clippings"
source_url: "https://machinelearningmastery.com/randomness-in-machine-learning/"
published_at: 2016-09-28
related_concepts: []
topics:
  - machine-learning-theory
  - 机器学习理论
---

### Why Do You Get Different Results On Different Runs Of An Algorithm With The Same Data?

Applied machine learning is a tapestry of breakthroughs and mindset shifts.

Understanding the role of randomness in machine learning algorithms is one of those breakthroughs.

Once you get it, you will see things differently. In a whole new light. Things like choosing between one algorithm and another, hyperparameter tuning and reporting results.

You will also start to see the abuses everywhere. The criminally unsupported performance claims.

In this post, I want to gently open your eyes to the role of [random numbers in machine learning](https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/). I want to give you the tools to embrace this uncertainty. To give you a breakthrough.

**Kick-start your project** with my new book [Master Machine Learning Algorithms](https://machinelearningmastery.com/master-machine-learning-algorithms/), including *step-by-step tutorials* and the *Excel Spreadsheet* files for all examples.

Let’s dive in.

(*special thanks to Xu Zhang and Nil Fero who promoted this post*)

![[Embrace-Randomness-in-Applied-Machine-Learning.jpg|Embrace Randomness in Applied Machine Learning]]

Embrace Randomness in Applied Machine Learning  
Photo by [Peter Pham](https://www.flickr.com/photos/136807076@N07/24137339992), some rights reserved.

## Why Are Results Different With The Same Data?

A lot of people ask this question or variants of this question.

**You are not alone!**

I get an email along these lines once per week.

Here are some similar questions posted to Q&A sites:

- [Why do I get different results each time I run my algorithm?](http://stats.stackexchange.com/questions/56362/why-do-i-get-different-results-each-time-i-run-my-algorithm)
- [Cross-Validation gives different result on the same data](http://stats.stackexchange.com/questions/144387/cross-validation-gives-different-result-on-the-same-data)
- [Randomness in Artificial Intelligence & Machine Learning](http://stackoverflow.com/questions/5891727/randomness-in-artificial-intelligence-machine-learning)
- [Why are the weights different in each running after convergence?](https://www.researchgate.net/post/Why_are_the_weights_different_in_each_running_after_convergence)
- [Does the same neural network with the same learning data and same test data in two computers give different results?](https://www.quora.com/Does-the-same-neural-network-with-the-same-learning-data-and-same-test-data-in-two-computers-give-different-results)

## Machine Learning Algorithms Use Random Numbers

Machine learning algorithms make use of randomness.

### 1\. Randomness in Data Collection

Trained with different data, machine learning algorithms will construct different models. It depends on the algorithm. How different a model is with different data is called the model variance (as in the [bias-variance trade off](https://machinelearningmastery.com/gentle-introduction-to-the-bias-variance-trade-off-in-machine-learning/)).

So, the data itself is a source of randomness. Randomness in the collection of the data.

### 2\. Randomness in Observation Order

The order that the observations are exposed to the model affects internal decisions.

Some algorithms are especially susceptible to this, like neural networks.

It is good practice to randomly shuffle the training data before each training iteration. Even if your algorithm is not susceptible. It’s a best practice.

### 3\. Randomness in the Algorithm

Algorithms harness randomness.

An algorithm may be initialized to a random state. Such as the initial weights in an artificial neural network.

Votes that end in a draw (and other internal decisions) during training in a deterministic method may rely on randomness to resolve.

### 4\. Randomness in Sampling

We may have too much data to reasonably work with.

In which case, we may work with a random subsample to train the model.

### 5\. Randomness in Resampling

We sample when we evaluate an algorithm.

We use techniques like splitting the data into a random training and test set or use k-fold cross validation that makes k random splits of the data.

The result is an estimate of the performance of the model (and process used to create it) on unseen data.

### No Doubt

There’s no doubt, randomness plays a big part in applied machine learning.

**The randomness that we can control, should be controlled.**

## Get your FREE Algorithms Mind Map

![[Machine-Learning-Algorithms-Mindmap-Sample.png|Machine Learning Algorithms Mind Map]]

Sample of the handy machine learning algorithms mind map.

I've created a handy mind map of 60+ algorithms organized by type.

Download it, print it and use it.

  
Also get exclusive access to the machine learning algorithms email mini-course.

## Random Seeds and Reproducible Results

Run an algorithm on a dataset and get a model.

Can you get the same model again given the same data?

You should be able to. It should be a requirement that is high on the list for your modeling project.

We achieve reproducibility in applied machine learning by using the exact same **code**, **data** and **sequence of random numbers**.

[Random numbers are generated](https://machinelearningmastery.com/how-to-generate-random-numbers-in-python/) in software using a pretend random number generator. It’s a simple math function that generates a sequence of numbers that are random enough for most applications.

This math function is deterministic. If it uses the same starting point called a seed number, it will give the same sequence of random numbers.

**Problem solved.**  
**Mostly.**

We can get reproducible results by fixing the random number generator’s seed before each model we construct.

In fact, this is a best practice.

We should be doing this if not already.

In fact, we should be giving the same sequence of random numbers to each algorithm we compare and each technique we try.

It should be a default part of each experiment we run.

## Machine Learning Algorithms are Stochastic

If a machine learning algorithm gives a different model with a different sequence of random numbers, then which model do we pick?

Ouch. There’s the rub.

I get asked this question from time to time and I love it.

It’s a sign that someone really gets to the meat of all this applied machine learning stuff – or is about to.

- Different runs of an algorithm with…
- Different random numbers give…
- Different models with…
- Different performance characteristics…

But the differences are within a range.

A fancy name for this difference or random behavior within a range is stochastic.

Machine learning algorithms are stochastic in practice.

- Expect them to be stochastic.
- Expect there to be a range of models to choose from and not a single model.
- Expect the performance to be a range and not a single value.

**These are very real expectations that you MUST address in practice.**

What tactics can you think of to address these expectations?

![[Machine-Learning-Algorithms-Use-Random-Numbers.jpg|Machine Learning Algorithms Use Random Numbers]]

Machine Learning Algorithms Use Random Numbers  
Photo by [Pete](https://www.flickr.com/photos/comedynose/3786642240/), some rights reserved.

## Tactics To Address The Uncertainty of Stochastic Algorithms

Thankfully, academics have been struggling with this challenge for a long time.

There are 2 simple strategies that you can use:

1. Reduce the Uncertainty.
2. Report the Uncertainty.

### Tactics to Reduce the Uncertainty

If we get different models essentially every time we run an algorithm, what can we do?

How about we try running the algorithm many times and gather a population of performance measures.

We already do this if we use *k* -fold cross validation. We build *k* different models.

We can increase *k* and build even more models, as long as the data within each fold remains representative of the problem.

We can also repeat our evaluation process *n* times to get even more numbers in our population of performance measures.

**This tactic is called random repeats or random restarts.**

It is more prevalent with stochastic optimization and neural networks, but is just as relevant generally. Try it.

### Tactics to Report the Uncertainty

Never report the performance of your machine learning algorithm with a single number.

If you do, you’ve most likely made an error.

You have gathered a population of performance measures. Use statistics on this population.

**This tactic is called report summary statistics.**

The distribution of results is most likely a Gaussian, so a great start would be to report the mean and standard deviation of performance. Include the highest and lowest performance observed.

In fact, this is a best practice.

You can then compare populations of result measures when you’re performing model selection. Such as:

- Choosing between algorithms.
- Choosing between configurations for one algorithm.

You can see that this has important implications on the processes you follow. Such as: to select which algorithm to use on your problem and for tuning and choosing algorithm hyperparameters.

Lean on statistical significance tests. Statistical tests can determine if the difference between one population of result measures is significantly different from a second population of results.

Report the significance as well.

This too is a best practice, that sadly does not have enough adoption.

## Wait, What About Final Model Selection

The final model is the one prepared on the entire training dataset, once we have chosen an algorithm and configuration.

It’s the model we intend to use to make predictions or deploy into operations.

We also get a different final model with different sequences of random numbers.

I’ve had some students ask:

> Should I create many final models and select the one with the best accuracy on a hold out validation dataset.

“ *No* ” I replied.

This would be a fragile process, highly dependent on the quality of the held out validation dataset. You are selecting random numbers that optimize for a small sample of data.

**Sounds like a recipe for overfitting.**

In general, I would rely on the confidence gained from the above tactics on reducing and reporting uncertainty. Often I just take the first model, it’s just as good as any other.

Sometimes your application domain makes you care more.

In this situation, I would tell you to build an ensemble of models, each trained with a different random number seed.

Use a simple voting ensemble. Each model makes a prediction and the mean of all predictions is reported as the final prediction.

Make the ensemble as big as you need to. I think 10, 30 or 100 are nice round numbers.

Maybe keep adding new models until the predictions become stable. For example, continue until the variance of the predictions tightens up on some holdout set.

## Summary

In this post, you discovered why random numbers are integral to applied machine learning. You can’t really escape them.

You learned about tactics that you can use to ensure that your results are reproducible.

You learned about techniques that you can use to embrace the stochastic nature of machine learning algorithms when selecting models and reporting results.

For more information on the importance of reproducible results in machine learning and techniques that you can use, see the post:

- [Reproducible Machine Learning Results By Default](https://machinelearningmastery.com/reproducible-machine-learning-results-by-default/)

Do you have any questions about random numbers in machine learning or about this post?

Ask your question in the comments and I will do my best to answer.

## Discover How Machine Learning Algorithms Work!

[![[MMLA-220.png|Mater Machine Learning Algorithms]]](https://machinelearningmastery.com/master-machine-learning-algorithms/)

#### See How Algorithms Work in Minutes

...with just arithmetic and simple examples

Discover how in my new Ebook:  
[Master Machine Learning Algorithms](https://machinelearningmastery.com/master-machine-learning-algorithms/)

It covers **explanations** and **examples** of **10 top algorithms**, like:  
*Linear Regression*, *k-Nearest Neighbors*, *Support Vector Machines* and much more...

#### Finally, Pull Back the Curtain on Machine Learning Algorithms

Skip the Academics. Just Results.

[See What's Inside](https://machinelearningmastery.com/master-machine-learning-algorithms/)