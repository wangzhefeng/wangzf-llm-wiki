---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
source_type: web
status: inbox
tags:
- null
- clippings
title: 'User guide: contents — Version 0.14.1'
source_url: https://imbalanced-learn.org/stable/user_guide.html
published_at: null
related_concepts: []
topics:
  - machine-learning
  - 机器学习理论
---

## User Guide

- [1\. Introduction](https://imbalanced-learn.org/stable/introduction.html)
- [2\. Over-sampling](https://imbalanced-learn.org/stable/over_sampling.html)
	- [2.1. A practical guide](https://imbalanced-learn.org/stable/over_sampling.html#a-practical-guide)
		- [2.2. Mathematical formulation](https://imbalanced-learn.org/stable/over_sampling.html#mathematical-formulation)
- [3\. Under-sampling](https://imbalanced-learn.org/stable/under_sampling.html)
	- [3.1. Prototype generation](https://imbalanced-learn.org/stable/under_sampling.html#prototype-generation)
		- [3.2. Prototype selection](https://imbalanced-learn.org/stable/under_sampling.html#prototype-selection)
		- [3.2.1. Controlled under-sampling techniques](https://imbalanced-learn.org/stable/under_sampling.html#controlled-under-sampling-techniques)
			- [3.2.1.1. Random under-sampling](https://imbalanced-learn.org/stable/under_sampling.html#random-under-sampling)
						- [3.2.1.2. Mathematical formulation](https://imbalanced-learn.org/stable/under_sampling.html#mathematical-formulation)
				- [3.2.2. Cleaning under-sampling techniques](https://imbalanced-learn.org/stable/under_sampling.html#cleaning-under-sampling-techniques)
			- [3.2.2.1. Tomek’s links](https://imbalanced-learn.org/stable/under_sampling.html#tomek-s-links)
						- [3.2.2.2. Editing data using nearest neighbours](https://imbalanced-learn.org/stable/under_sampling.html#editing-data-using-nearest-neighbours)
				- [3.2.2.2.1. Edited nearest neighbours](https://imbalanced-learn.org/stable/under_sampling.html#edited-nearest-neighbours)
								- [3.2.2.2.2. Repeated Edited Nearest Neighbours](https://imbalanced-learn.org/stable/under_sampling.html#repeated-edited-nearest-neighbours)
								- [3.2.2.2.3. All KNN](https://imbalanced-learn.org/stable/under_sampling.html#all-knn)
						- [3.2.2.3. Condensed nearest neighbors](https://imbalanced-learn.org/stable/under_sampling.html#condensed-nearest-neighbors)
				- [3.2.2.3.1. One Sided Selection](https://imbalanced-learn.org/stable/under_sampling.html#one-sided-selection)
				- [3.2.3. Additional undersampling techniques](https://imbalanced-learn.org/stable/under_sampling.html#additional-undersampling-techniques)
			- [3.2.3.1. Instance hardness threshold](https://imbalanced-learn.org/stable/under_sampling.html#id11)
- [4\. Combination of over- and under-sampling](https://imbalanced-learn.org/stable/combine.html)
- [5\. Ensemble of samplers](https://imbalanced-learn.org/stable/ensemble.html)
	- [5.1. Classifier including inner balancing samplers](https://imbalanced-learn.org/stable/ensemble.html#classifier-including-inner-balancing-samplers)
		- [5.1.1. Bagging classifier](https://imbalanced-learn.org/stable/ensemble.html#bagging-classifier)
				- [5.1.2. Forest of randomized trees](https://imbalanced-learn.org/stable/ensemble.html#forest-of-randomized-trees)
				- [5.1.3. Boosting](https://imbalanced-learn.org/stable/ensemble.html#boosting)
- [6\. Miscellaneous samplers](https://imbalanced-learn.org/stable/miscellaneous.html)
	- [6.1. Custom samplers](https://imbalanced-learn.org/stable/miscellaneous.html#custom-samplers)
		- [6.2. Custom generators](https://imbalanced-learn.org/stable/miscellaneous.html#custom-generators)
		- [6.2.1. TensorFlow generator](https://imbalanced-learn.org/stable/miscellaneous.html#tensorflow-generator)
				- [6.2.2. Keras generator](https://imbalanced-learn.org/stable/miscellaneous.html#keras-generator)
- [7\. Metrics](https://imbalanced-learn.org/stable/metrics.html)
	- [7.1. Classification metrics](https://imbalanced-learn.org/stable/metrics.html#classification-metrics)
		- [7.1.1. Sensitivity and specificity metrics](https://imbalanced-learn.org/stable/metrics.html#sensitivity-and-specificity-metrics)
				- [7.1.2. Additional metrics specific to imbalanced datasets](https://imbalanced-learn.org/stable/metrics.html#additional-metrics-specific-to-imbalanced-datasets)
				- [7.1.3. Macro-Averaged Mean Absolute Error (MA-MAE)](https://imbalanced-learn.org/stable/metrics.html#macro-averaged-mean-absolute-error-ma-mae)
				- [7.1.4. Summary of important metrics](https://imbalanced-learn.org/stable/metrics.html#summary-of-important-metrics)
		- [7.2. Pairwise metrics](https://imbalanced-learn.org/stable/metrics.html#pairwise-metrics)
		- [7.2.1. Value Difference Metric](https://imbalanced-learn.org/stable/metrics.html#value-difference-metric)
- [8\. Cross validation](https://imbalanced-learn.org/stable/model_selection.html)
	- [8.1. Instance hardness and average precision](https://imbalanced-learn.org/stable/model_selection.html#instance-hardness-and-average-precision)
		- [8.2. Create imbalanced dataset with samples with large instance hardness](https://imbalanced-learn.org/stable/model_selection.html#create-imbalanced-dataset-with-samples-with-large-instance-hardness)
		- [8.3. Assess cross validation performance variance using `InstanceHardnessCV` splitter](https://imbalanced-learn.org/stable/model_selection.html#assess-cross-validation-performance-variance-using-instancehardnesscv-splitter)
- [9\. Common pitfalls and recommended practices](https://imbalanced-learn.org/stable/common_pitfalls.html)
	- [9.1. Data leakage](https://imbalanced-learn.org/stable/common_pitfalls.html#data-leakage)
- [10\. Dataset loading utilities](https://imbalanced-learn.org/stable/datasets/index.html)
- [11\. Developer guideline](https://imbalanced-learn.org/stable/developers_utils.html)
	- [11.1. Developer utilities](https://imbalanced-learn.org/stable/developers_utils.html#developer-utilities)
		- [11.2. Making a release](https://imbalanced-learn.org/stable/developers_utils.html#making-a-release)
- [12\. References](https://imbalanced-learn.org/stable/zzz_references.html)