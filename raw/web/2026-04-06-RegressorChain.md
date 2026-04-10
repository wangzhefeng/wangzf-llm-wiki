---
source_type: web
title: "RegressorChain"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.RegressorChain.html#sklearn.multioutput.RegressorChain"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

## RegressorChain

*class* sklearn.multioutput.RegressorChain(*estimator=None*, *\**, *order=None*, *cv=None*, *random\_state=None*, *verbose=False*, *base\_estimator='deprecated'*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L1167) [#](#sklearn.multioutput.RegressorChain "Link to this definition")

A multi-label model that arranges regressions into a chain.

Each model makes a prediction in the order specified by the chain using all of the available features provided to the model plus the predictions of models that are earlier in the chain.

Read more in the [User Guide](https://scikit-learn.org/stable/modules/multiclass.html#regressorchain).

Added in version 0.20.

Parameters:

**estimator** estimator

The base estimator from which the regressor chain is built.

**order** array-like of shape (n\_outputs,) or ‘random’, default=None

If `None`, the order will be determined by the order of columns in the label matrix Y.:

```
order = [0, 1, 2, ..., Y.shape[1] - 1]
```

The order of the chain can be explicitly set by providing a list of integers. For example, for a chain of length 5.:

```
order = [1, 3, 2, 4, 0]
```

means that the first model in the chain will make predictions for column 1 in the Y matrix, the second model will make predictions for column 3, etc.

If order is ‘random’ a random ordering will be used.

**cv** int, cross-validation generator or an iterable, default=None

Determines whether to use cross validated predictions or true labels for the results of previous estimators in the chain. Possible inputs for cv are:

- None, to use true labels when fitting,
- integer, to specify the number of folds in a (Stratified)KFold,
- [CV splitter](https://scikit-learn.org/stable/glossary.html#term-CV-splitter),
- An iterable yielding (train, test) splits as arrays of indices.

**random\_state** int, RandomState instance or None, optional (default=None)

If `order='random'`, determines random number generation for the chain order. In addition, it controls the random seed given at each `base_estimator` at each chaining iteration. Thus, it is only used when `base_estimator` exposes a `random_state`. Pass an int for reproducible output across multiple function calls. See [Glossary](https://scikit-learn.org/stable/glossary.html#term-random_state).

**verbose** bool, default=False

If True, chain progress is output as each model is completed.

Added in version 1.2.

**base\_estimator** estimator, default=”deprecated”

Use `estimator` instead.

Deprecated since version 1.7: `base_estimator` is deprecated and will be removed in 1.9. Use `estimator` instead.

Attributes:

**estimators\_** list

A list of clones of base\_estimator.

**order\_** list

The order of labels in the classifier chain.

**n\_features\_in\_** int

Number of features seen during [fit](https://scikit-learn.org/stable/glossary.html#term-fit). Only defined if the underlying `base_estimator` exposes such an attribute when fit.

Added in version 0.24.

**feature\_names\_in\_** ndarray of shape (`n_features_in_`,)

Names of features seen during [fit](https://scikit-learn.org/stable/glossary.html#term-fit). Defined only when `X` has feature names that are all strings.

Added in version 1.0.

See also

[`ClassifierChain`](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.ClassifierChain.html#sklearn.multioutput.ClassifierChain "sklearn.multioutput.ClassifierChain")

Equivalent for classification.

[`MultiOutputRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html#sklearn.multioutput.MultiOutputRegressor "sklearn.multioutput.MultiOutputRegressor")

Learns each output independently rather than chaining.

Examples

```
>>> from sklearn.multioutput import RegressorChain
>>> from sklearn.linear_model import LogisticRegression
>>> logreg = LogisticRegression(solver='lbfgs')
>>> X, Y = [[1, 0], [0, 1], [1, 1]], [[0, 2], [1, 1], [2, 0]]
>>> chain = RegressorChain(logreg, order=[0, 1]).fit(X, Y)
>>> chain.predict(X)
array([[0., 2.],
       [1., 1.],
       [2., 0.]])
```

fit(*X*, *Y*, *\*\*fit\_params*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L1270) [#](#sklearn.multioutput.RegressorChain.fit "Link to this definition")

Fit the model to data matrix X and targets Y.

Parameters:

**X** {array-like, sparse matrix} of shape (n\_samples, n\_features)

The input data.

**Y** array-like of shape (n\_samples, n\_classes)

The target values.

**\*\*fit\_params** dict of string -> object

Parameters passed to the `fit` method at each step of the regressor chain.

Added in version 0.23.

Returns:

**self** object

Returns a fitted instance.

Get metadata routing of this object.

Please check [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing) on how the routing mechanism works.

Added in version 1.3.

Returns:

**routing** MetadataRouter

A [`MetadataRouter`](https://scikit-learn.org/stable/modules/generated/sklearn.utils.metadata_routing.MetadataRouter.html#sklearn.utils.metadata_routing.MetadataRouter "sklearn.utils.metadata_routing.MetadataRouter") encapsulating routing information.

get\_params(*deep=True*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/base.py#L240) [#](#sklearn.multioutput.RegressorChain.get_params "Link to this definition")

Get parameters for this estimator.

Parameters:

**deep** bool, default=True

If True, will return the parameters for this estimator and contained subobjects that are estimators.

Returns:

**params** dict

Parameter names mapped to their values.

predict(*X*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L856) [#](#sklearn.multioutput.RegressorChain.predict "Link to this definition")

Predict on the data matrix X using the ClassifierChain model.

Parameters:

**X** {array-like, sparse matrix} of shape (n\_samples, n\_features)

The input data.

Returns:

**Y\_pred** array-like of shape (n\_samples, n\_classes)

The predicted values.

score(*X*, *y*, *sample\_weight=None*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/base.py#L610) [#](#sklearn.multioutput.RegressorChain.score "Link to this definition")

Return [coefficient of determination](https://scikit-learn.org/stable/modules/model_evaluation.html#r2-score) on test data.

The coefficient of determination, $R^{2}$, is defined as $\left(\right. 1 - \frac{u}{v} \left.\right)$, where $u$ is the residual sum of squares `((y_true - y_pred)** 2).sum()` and $v$ is the total sum of squares `((y_true - y_true.mean()) ** 2).sum()`. The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse). A constant model that always predicts the expected value of `y`, disregarding the input features, would get a $R^{2}$ score of 0.0.

Parameters:

**X** array-like of shape (n\_samples, n\_features)

Test samples. For some estimators this may be a precomputed kernel matrix or a list of generic objects instead with shape `(n_samples, n_samples_fitted)`, where `n_samples_fitted` is the number of samples used in the fitting for the estimator.

**y** array-like of shape (n\_samples,) or (n\_samples, n\_outputs)

True values for `X`.

**sample\_weight** array-like of shape (n\_samples,), default=None

Sample weights.

Returns:

**score** float

$R^{2}$ of `self.predict(X)` w.r.t. `y`.

Notes

The $R^{2}$ score used when calling `score` on a regressor uses `multioutput='uniform_average'` from version 0.23 to keep consistent with default value of [`r2_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score "sklearn.metrics.r2_score"). This influences the `score` method of all the multioutput regressors (except for [`MultiOutputRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html#sklearn.multioutput.MultiOutputRegressor "sklearn.multioutput.MultiOutputRegressor")).

set\_params(*\*\*params*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/base.py#L338) [#](#sklearn.multioutput.RegressorChain.set_params "Link to this definition")

Set the parameters of this estimator.

The method works on simple estimators as well as on nested objects (such as [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline "sklearn.pipeline.Pipeline")). The latter have parameters of the form `<component>__<parameter>` so that it’s possible to update each component of a nested object.

Parameters:

**\*\*params** dict

Estimator parameters.

Returns:

**self** estimator instance

Estimator instance.

set\_score\_request(*\**, *sample\_weight: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") = '$UNCHANGED$'*) → [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/utils/_metadata_requests.py#L1315) [#](#sklearn.multioutput.RegressorChain.set_score_request "Link to this definition")

Configure whether metadata should be requested to be passed to the `score` method.

Note that this method is only relevant when this estimator is used as a sub-estimator within a [meta-estimator](https://scikit-learn.org/stable/glossary.html#term-meta-estimator) and metadata routing is enabled with `enable_metadata_routing=True` (see [`sklearn.set_config`](https://scikit-learn.org/stable/modules/generated/sklearn.set_config.html#sklearn.set_config "sklearn.set_config")). Please check the [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing) on how the routing mechanism works.

The options for each parameter are:

- `True`: metadata is requested, and passed to `score` if provided. The request is ignored if metadata is not provided.
- `False`: metadata is not requested and the meta-estimator will not pass it to `score`.
- `None`: metadata is not requested, and the meta-estimator will raise an error if the user provides it.
- `str`: metadata should be passed to the meta-estimator with this given alias instead of the original name.

The default (`sklearn.utils.metadata_routing.UNCHANGED`) retains the existing request. This allows you to change the request for some parameters and not others.

Added in version 1.3.

Parameters:

**sample\_weight** str, True, False, or None, default=sklearn.utils.metadata\_routing.UNCHANGED

Metadata routing for `sample_weight` parameter in `score`.

Returns:

**self** object

The updated object.