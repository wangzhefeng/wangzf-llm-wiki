---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: 'Gallery examples: Comparing random forests and the multi-output meta
  estimator'
source_type: web
status: inbox
tags:
- null
- clippings
title: MultiOutputRegressor
topics:
- 机器学习
source_url: https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputRegressor.html
published_at: null
related_concepts: []
---

## MultiOutputRegressor

*class* sklearn.multioutput.MultiOutputRegressor(*estimator*, *\**, *n\_jobs=None*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L342) [#](#sklearn.multioutput.MultiOutputRegressor "Link to this definition")

Multi target regression.

This strategy consists of fitting one regressor per target. This is a simple strategy for extending regressors that do not natively support multi-target regression.

Added in version 0.18.

Parameters:

**estimator** estimator object

An estimator object implementing [fit](https://scikit-learn.org/stable/glossary.html#term-fit) and [predict](https://scikit-learn.org/stable/glossary.html#term-predict).

**n\_jobs** int or None, optional (default=None)

The number of jobs to run in parallel., and (if supported by the passed estimator) will be parallelized for each target.

When individual estimators are fast to train or predict, using `n_jobs > 1` can result in slower performance due to the parallelism overhead.

`None` means `1` unless in a [`joblib.parallel_backend`](https://joblib.readthedocs.io/en/latest/generated/joblib.parallel_backend.html#joblib.parallel_backend "(in joblib v1.6.dev0)") context. `-1` means using all available processes / threads. See [Glossary](https://scikit-learn.org/stable/glossary.html#term-n_jobs) for more details.

Changed in version 0.20: `n_jobs` default changed from `1` to `None`.

Attributes:

**estimators\_** list of `n_output` estimators

Estimators used for predictions.

**n\_features\_in\_** int

Number of features seen during [fit](https://scikit-learn.org/stable/glossary.html#term-fit). Only defined if the underlying `estimator` exposes such an attribute when fit.

Added in version 0.24.

**feature\_names\_in\_** ndarray of shape (`n_features_in_`,)

Names of features seen during [fit](https://scikit-learn.org/stable/glossary.html#term-fit). Only defined if the underlying estimators expose such an attribute when fit.

Added in version 1.0.

See also

[`RegressorChain`](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.RegressorChain.html#sklearn.multioutput.RegressorChain "sklearn.multioutput.RegressorChain")

A multi-label model that arranges regressions into a chain.

[`MultiOutputClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.multioutput.MultiOutputClassifier.html#sklearn.multioutput.MultiOutputClassifier "sklearn.multioutput.MultiOutputClassifier")

Classifies each output independently rather than chaining.

Examples

```
>>> import numpy as np
>>> from sklearn.datasets import load_linnerud
>>> from sklearn.multioutput import MultiOutputRegressor
>>> from sklearn.linear_model import Ridge
>>> X, y = load_linnerud(return_X_y=True)
>>> regr = MultiOutputRegressor(Ridge(random_state=123)).fit(X, y)
>>> regr.predict(X[[0]])
array([[176, 35.1, 57.1]])
```

fit(*X*, *y*, *sample\_weight=None*, *\*\*fit\_params*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L208) [#](#sklearn.multioutput.MultiOutputRegressor.fit "Link to this definition")

Fit the model to data, separately for each output variable.

Parameters:

**X** {array-like, sparse matrix} of shape (n\_samples, n\_features)

The input data.

**y** {array-like, sparse matrix} of shape (n\_samples, n\_outputs)

Multi-output targets. An indicator matrix turns on multilabel estimation.

**sample\_weight** array-like of shape (n\_samples,), default=None

Sample weights. If `None`, then samples are equally weighted. Only supported if the underlying regressor supports sample weights.

**\*\*fit\_params** dict of string -> object

Parameters passed to the `estimator.fit` method of each step.

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

get\_params(*deep=True*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/base.py#L240) [#](#sklearn.multioutput.MultiOutputRegressor.get_params "Link to this definition")

Get parameters for this estimator.

Parameters:

**deep** bool, default=True

If True, will return the parameters for this estimator and contained subobjects that are estimators.

Returns:

**params** dict

Parameter names mapped to their values.

partial\_fit(*X*, *y*, *sample\_weight=None*, *\*\*partial\_fit\_params*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L411) [#](#sklearn.multioutput.MultiOutputRegressor.partial_fit "Link to this definition")

Incrementally fit the model to data, for each output variable.

Parameters:

**X** {array-like, sparse matrix} of shape (n\_samples, n\_features)

The input data.

**y** {array-like, sparse matrix} of shape (n\_samples, n\_outputs)

Multi-output targets.

**sample\_weight** array-like of shape (n\_samples,), default=None

Sample weights. If `None`, then samples are equally weighted. Only supported if the underlying regressor supports sample weights.

**\*\*partial\_fit\_params** dict of str -> object

Parameters passed to the `estimator.partial_fit` method of each sub-estimator.

Only available if `enable_metadata_routing=True`. See the [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing).

Added in version 1.3.

Returns:

**self** object

Returns a fitted instance.

predict(*X*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/multioutput.py#L288) [#](#sklearn.multioutput.MultiOutputRegressor.predict "Link to this definition")

Predict multi-output variable using model for each target variable.

Parameters:

**X** {array-like, sparse matrix} of shape (n\_samples, n\_features)

The input data.

Returns:

**y** {array-like, sparse matrix} of shape (n\_samples, n\_outputs)

Multi-output targets predicted across multiple predictors. Note: Separate models are generated for each predictor.

score(*X*, *y*, *sample\_weight=None*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/base.py#L610) [#](#sklearn.multioutput.MultiOutputRegressor.score "Link to this definition")

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

The $R^{2}$ score used when calling `score` on a regressor uses `multioutput='uniform_average'` from version 0.23 to keep consistent with default value of [`r2_score`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.r2_score.html#sklearn.metrics.r2_score "sklearn.metrics.r2_score"). This influences the `score` method of all the multioutput regressors (except for ).

set\_fit\_request(*\**, *sample\_weight: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") = '$UNCHANGED$'*) → [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/utils/_metadata_requests.py#L1315) [#](#sklearn.multioutput.MultiOutputRegressor.set_fit_request "Link to this definition")

Configure whether metadata should be requested to be passed to the `fit` method.

Note that this method is only relevant when this estimator is used as a sub-estimator within a [meta-estimator](https://scikit-learn.org/stable/glossary.html#term-meta-estimator) and metadata routing is enabled with `enable_metadata_routing=True` (see [`sklearn.set_config`](https://scikit-learn.org/stable/modules/generated/sklearn.set_config.html#sklearn.set_config "sklearn.set_config")). Please check the [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing) on how the routing mechanism works.

The options for each parameter are:

- `True`: metadata is requested, and passed to `fit` if provided. The request is ignored if metadata is not provided.
- `False`: metadata is not requested and the meta-estimator will not pass it to `fit`.
- `None`: metadata is not requested, and the meta-estimator will raise an error if the user provides it.
- `str`: metadata should be passed to the meta-estimator with this given alias instead of the original name.

The default (`sklearn.utils.metadata_routing.UNCHANGED`) retains the existing request. This allows you to change the request for some parameters and not others.

Added in version 1.3.

Parameters:

**sample\_weight** str, True, False, or None, default=sklearn.utils.metadata\_routing.UNCHANGED

Metadata routing for `sample_weight` parameter in `fit`.

Returns:

**self** object

The updated object.

set\_params(*\*\*params*) [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/base.py#L338) [#](#sklearn.multioutput.MultiOutputRegressor.set_params "Link to this definition")

Set the parameters of this estimator.

The method works on simple estimators as well as on nested objects (such as [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline "sklearn.pipeline.Pipeline")). The latter have parameters of the form `<component>__<parameter>` so that it’s possible to update each component of a nested object.

Parameters:

**\*\*params** dict

Estimator parameters.

Returns:

**self** estimator instance

Estimator instance.

set\_partial\_fit\_request(*\**, *sample\_weight: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") = '$UNCHANGED$'*) → [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/utils/_metadata_requests.py#L1315) [#](#sklearn.multioutput.MultiOutputRegressor.set_partial_fit_request "Link to this definition")

Configure whether metadata should be requested to be passed to the `partial_fit` method.

Note that this method is only relevant when this estimator is used as a sub-estimator within a [meta-estimator](https://scikit-learn.org/stable/glossary.html#term-meta-estimator) and metadata routing is enabled with `enable_metadata_routing=True` (see [`sklearn.set_config`](https://scikit-learn.org/stable/modules/generated/sklearn.set_config.html#sklearn.set_config "sklearn.set_config")). Please check the [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing) on how the routing mechanism works.

The options for each parameter are:

- `True`: metadata is requested, and passed to `partial_fit` if provided. The request is ignored if metadata is not provided.
- `False`: metadata is not requested and the meta-estimator will not pass it to `partial_fit`.
- `None`: metadata is not requested, and the meta-estimator will raise an error if the user provides it.
- `str`: metadata should be passed to the meta-estimator with this given alias instead of the original name.

The default (`sklearn.utils.metadata_routing.UNCHANGED`) retains the existing request. This allows you to change the request for some parameters and not others.

Added in version 1.3.

Parameters:

**sample\_weight** str, True, False, or None, default=sklearn.utils.metadata\_routing.UNCHANGED

Metadata routing for `sample_weight` parameter in `partial_fit`.

Returns:

**self** object

The updated object.

set\_score\_request(*\**, *sample\_weight: [bool](https://docs.python.org/3/library/functions.html#bool "(in Python v3.14)") | [None](https://docs.python.org/3/library/constants.html#None "(in Python v3.14)") | [str](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") = '$UNCHANGED$'*) → [\[source\]](https://github.com/scikit-learn/scikit-learn/blob/fe2edb3cd/sklearn/utils/_metadata_requests.py#L1315) [#](#sklearn.multioutput.MultiOutputRegressor.set_score_request "Link to this definition")

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

## Gallery examples

![[raw/assets/attachments/machinelearning/sphx_glr_plot_random_forest_regression_multioutput_thumb.png]]

[Comparing random forests and the multi-output meta estimator](https://scikit-learn.org/stable/auto_examples/ensemble/plot_random_forest_regression_multioutput.html)

Comparing random forests and the multi-output meta estimator